from datetime import datetime, timezone
from typing import Optional
from src.app.nucleo.conexion import get_connection
from src.app.aprobacion import repository as aprobacion_repo
from src.app.reservas import repository as reservas_repo


class AprobacionError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def _parsear_fecha(fecha_str: str):
    try:
        # Intentar parsear ISO
        fecha_str_limpia = fecha_str.replace('Z', '+00:00')
        return datetime.fromisoformat(fecha_str_limpia)
    except Exception:
        raise ValueError("Fecha inválida")


def aprobar_reserva(usuario: dict, reserva_id: int, motivo: Optional[str] = None) -> dict:
    conn = get_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        # El orden de validaciones debe seguir: 401, 403, 404, 422, 409
        # 401 ya lo maneja auth, pero lo mantenemos según orden
        # 403: validar rol ADMINISTRADOR
        if not usuario:
            conn.rollback()
            raise AprobacionError(401, "No autorizado")
        rol = usuario.get("rol")
        # Primero verificamos existencia? El orden dice 404 va después de 403
        # Según los casos de prueba: solicitante que aprueba reserva inexistente recibe 403
        # Administrador que rechaza reserva inexistente sin motivo recibe 404
        # Así que debemos chequear rol (403) antes que existencia (404) cuando hay rol vs no existe? 
        # "Solicitante intenta aprobar una reserva inexistente" - devuelve 403
        if rol != "ADMINISTRADOR":
            conn.rollback()
            raise AprobacionError(403, "Permisos insuficientes")
        # 404: validar existencia
        reserva = aprobacion_repo.obtener_reserva_por_id(reserva_id, conn=conn)
        if not reserva:
            conn.rollback()
            raise AprobacionError(404, "Reserva no encontrada")
        # 422: para aprobar, motivo es opcional (puede ser nulo) - no aplicamos validación 422
        # 409: validar estado PENDIENTE
        estado = reserva.get("estado")
        if estado != "PENDIENTE":
            conn.rollback()
            raise AprobacionError(409, "Transición de estado inválida")
        # Validar que no se apruebe si el inicio ya pasó
        try:
            inicio = _parsear_fecha(reserva.get("inicio"))
            ahora = datetime.now(timezone.utc)
            # Comparar en UTC
            if inicio.tzinfo is None:
                inicio = inicio.replace(tzinfo=timezone.utc)
            if ahora.tzinfo is None:
                ahora = ahora.replace(tzinfo=timezone.utc)
            if inicio < ahora:
                conn.rollback()
                raise AprobacionError(409, "No se puede aprobar una reserva cuyo inicio ya pasó")
        except AprobacionError:
            raise
        except Exception:
            pass  # Si no podemos parsear, continuar con otras validaciones
        # Revalidar disponibilidad al aprobar, excluyendo la propia reserva
        solapadas = aprobacion_repo.buscar_reservas_solapadas_aprobacion(
            reserva.get("espacio_id"),
            reserva.get("inicio"),
            reserva.get("fin"),
            reserva_id,
            conn=conn
        )
        if solapadas:
            conn.rollback()
            raise AprobacionError(409, "Solapamiento de reserva")
        # Registrar trazabilidad
        motivo_decision = motivo
        if motivo_decision is not None and isinstance(motivo_decision, str):
            motivo_decision = motivo_decision.strip() if motivo_decision.strip() == motivo_decision else motivo_decision
            # Para aprobar, si viene vacío lo tratamos como None? No dice, dice opcional puede ser nulo
            if motivo_decision == "":
                motivo_decision = None
        resultado = aprobacion_repo.aprobar_reserva(reserva_id, usuario.get("id"), motivo_decision, conn=conn)
        conn.commit()
        return resultado
    except AprobacionError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise AprobacionError(422, str(e))
    finally:
        conn.close()


def rechazar_reserva(usuario: dict, reserva_id: int, motivo: Optional[str] = None) -> dict:
    conn = get_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        if not usuario:
            conn.rollback()
            raise AprobacionError(401, "No autorizado")
        rol = usuario.get("rol")
        # 403 primero si no es admin
        if rol != "ADMINISTRADOR":
            conn.rollback()
            raise AprobacionError(403, "Permisos insuficientes")
        # 404 después de 403
        reserva = aprobacion_repo.obtener_reserva_por_id(reserva_id, conn=conn)
        if not reserva:
            conn.rollback()
            raise AprobacionError(404, "Reserva no encontrada")
        # 422: motivo obligatorio al rechazar
        if motivo is None:
            conn.rollback()
            raise AprobacionError(422, "Motivo requerido")
        if isinstance(motivo, str):
            motivo_limpio = motivo.strip()
            if motivo_limpio == "":
                conn.rollback()
                raise AprobacionError(422, "Motivo requerido")
            if len(motivo) > 500:  # revisar longitud del motivo original o limpio?
                conn.rollback()
                raise AprobacionError(422, "Motivo inválido")
            motivo_a_guardar = motivo  # guardar tal como viene o limpio? revisar - dice "proporcionado" en trazabilidad
        else:
            conn.rollback()
            raise AprobacionError(422, "Motivo requerido")
        # 409: validar estado PENDIENTE
        estado = reserva.get("estado")
        if estado != "PENDIENTE":
            conn.rollback()
            raise AprobacionError(409, "Transición de estado inválida")
        resultado = aprobacion_repo.rechazar_reserva(reserva_id, usuario.get("id"), motivo, conn=conn)
        conn.commit()
        return resultado
    except AprobacionError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise AprobacionError(422, str(e))
    finally:
        conn.close()
