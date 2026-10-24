from src.app.nucleo.conexion import get_connection
from src.app.cancelacion import repository as cancel_repo
from src.app.historial import repository as hist_repo
from src.app.reservas import politicas
from datetime import datetime, timezone


class CancelacionError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def cancelar_reserva(usuario: dict, reserva_id: int, comentario: str = None):
    # Validaciones en orden: 401 ya debe estar manejado por auth, pero lo verificamos
    if not usuario:
        raise CancelacionError(401, "No autorizado")
    
    conn = get_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        # 404 - existencia
        reserva = cancel_repo.obtener_reserva_por_id(reserva_id, conn=conn)
        if not reserva:
            raise CancelacionError(404, "Reserva no encontrada")
        # 403 - propiedad o rol
        es_admin = usuario.get("rol") == "ADMINISTRADOR"
        usuario_id = usuario.get("id")
        if not es_admin and reserva.get("usuario_id") != usuario_id:
            raise CancelacionError(403, "No autorizado")
        # 409 - estado cancelable
        estado = reserva.get("estado")
        if estado in ('RECHAZADA', 'CANCELADA'):
            raise CancelacionError(409, "No se puede cancelar la reserva")
        if estado not in ('PENDIENTE', 'APROBADA'):
            raise CancelacionError(409, "No se puede cancelar la reserva")
        # Validar comentario
        if comentario is not None and len(str(comentario)) > 500:
            raise CancelacionError(422, "Comentario demasiado largo")
        # Preparar comentario para historial
        if comentario is None or str(comentario).strip() == "":
            comentario_hist = "Cancelada"
        else:
            comentario_hist = str(comentario)
        # Cancelar y registrar en misma transacción
        estado_anterior = estado
        cancel_repo.actualizar_estado_reserva(reserva_id, 'CANCELADA', conn=conn)
        try:
            hist_repo.registrar_historial(reserva_id, estado_anterior, 'CANCELADA', usuario_id, comentario_hist, conn=conn)
        except Exception:
            conn.rollback()
            raise
        conn.commit()
        return {"mensaje": "Reserva cancelada", "reserva_id": reserva_id, "estado": "CANCELADA"}
    except CancelacionError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise CancelacionError(500, str(e))
    finally:
        conn.close()
