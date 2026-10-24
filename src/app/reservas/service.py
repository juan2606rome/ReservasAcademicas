from datetime import datetime, timezone
from typing import Optional, List
from src.app.nucleo.conexion import get_connection
from src.app.espacios import repository as espacios_repo
from src.app.reservas import repository as reservas_repo
from src.app.reservas import politicas


class SolicitudReservaError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def crear_solicitud_reserva(usuario_id: int, espacio_id: int, inicio_str: str, fin_str: str, motivo: str) -> dict:
    conn = get_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        # Validar espacio
        espacio = espacios_repo.obtener_espacio_por_id(espacio_id)
        if not espacio:
            raise SolicitudReservaError(404, "Espacio no encontrado")
        # Validar espacio activo
        activo = espacio.get("activo")
        if activo == 0 or activo is False:
            raise SolicitudReservaError(409, "Espacio no disponible")
        # Validar políticas
        try:
            inicio_utc, fin_utc = politicas.validar_solicitud_reserva(inicio_str, fin_str, motivo)
        except ValueError as e:
            msg = str(e)
            if "zona horaria" in msg.lower() or "fecha" in msg.lower() or "fin" in msg.lower() or "día" in msg.lower() or "pasado" in msg.lower() or "motivo" in msg.lower() or "campos" in msg.lower():
                raise SolicitudReservaError(422, msg)
            raise SolicitudReservaError(422, msg)
        # Verificar solapamientos
        solapadas = reservas_repo.buscar_reservas_solapadas(espacio_id, inicio_utc.isoformat().replace('+00:00', 'Z'), fin_utc.isoformat().replace('+00:00', 'Z'), conn=conn)
        if solapadas:
            raise SolicitudReservaError(409, "Solapamiento de reserva")
        # Crear reserva
        inicio_utc_str = politicas.formatear_utc_iso8601(inicio_utc)
        fin_utc_str = politicas.formatear_utc_iso8601(fin_utc)
        reserva = reservas_repo.crear_reserva(espacio_id, usuario_id, inicio_utc_str, fin_utc_str, motivo, estado='PENDIENTE', conn=conn)
        conn.commit()
        # Formatear respuesta
        return {
            "id": reserva["id"],
            "espacio_id": reserva["espacio_id"],
            "usuario_id": reserva["usuario_id"],
            "inicio": reserva["inicio"] if reserva.get("inicio") and reserva["inicio"].endswith(('Z', '+00:00')) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(reserva["inicio"]).replace('Z', '+00:00')) if reserva.get("inicio") else inicio_utc),
            "fin": reserva["fin"] if reserva.get("fin") and (str(reserva["fin"]).endswith('Z') or '+' in str(reserva["fin"])) else politicas.formatear_utc_iso8601(fin_utc),
            "motivo": reserva["motivo"],
            "estado": reserva["estado"]
        }
    except SolicitudReservaError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise SolicitudReservaError(422, str(e))
    finally:
        conn.close()


def consultar_disponibilidad(espacio_id: int, fecha_str: str) -> List[dict]:
    # Validar espacio
    espacio = espacios_repo.obtener_espacio_por_id(espacio_id)
    if not espacio:
        raise SolicitudReservaError(404, "Espacio no encontrado")
    # Validar fecha
    try:
        fecha = politicas.parsear_fecha_bogota(fecha_str)
    except Exception:
        raise SolicitudReservaError(422, "Fecha inválida")
    # Obtener reservas
    reservas = reservas_repo.obtener_reservas_por_fecha_espacio(espacio_id, fecha)
    result = []
    for r in reservas:
        result.append({
            "inicio": r["inicio"] if r.get("inicio") and (str(r["inicio"]).endswith('Z') or '+' in str(r["inicio"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(r["inicio"]).replace('Z', '+00:00'))),
            "fin": r["fin"] if r.get("fin") and (str(r["fin"]).endswith('Z') or '+' in str(r["fin"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(r["fin"]).replace('Z', '+00:00'))),
            "estado": r["estado"]
        })
    # Ordenar por inicio
    result.sort(key=lambda x: x["inicio"])
    return result


def listar_reservas_usuario(usuario: dict, estado: Optional[str] = None, espacio_id: Optional[int] = None) -> List[dict]:
    es_admin = usuario.get("rol") == "ADMINISTRADOR"
    usuario_id = usuario.get("id")
    # Validar filtros
    if estado and estado not in ['PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA']:
        raise SolicitudReservaError(422, "Estado inválido")
    if espacio_id is not None:
        try:
            int(espacio_id)
        except Exception:
            raise SolicitudReservaError(422, "espacio_id inválido")
    reservas = reservas_repo.listar_reservas(usuario_id=usuario_id, es_admin=es_admin, estado=estado, espacio_id=int(espacio_id) if espacio_id is not None else None)
    result = []
    for r in reservas:
        result.append({
            "id": r["id"],
            "espacio_id": r["espacio_id"],
            "usuario_id": r["usuario_id"],
            "inicio": r["inicio"] if r.get("inicio") and (str(r["inicio"]).endswith('Z') or '+' in str(r["inicio"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(r["inicio"]).replace('Z', '+00:00'))),
            "fin": r["fin"] if r.get("fin") and (str(r["fin"]).endswith('Z') or '+' in str(r["fin"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(r["fin"]).replace('Z', '+00:00'))),
            "motivo": r["motivo"],
            "estado": r["estado"],
            "creada_en": r.get("creada_en")
        })
    return result


def obtener_reserva(usuario: dict, reserva_id: int) -> dict:
    reserva = reservas_repo.obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise SolicitudReservaError(404, "Reserva no encontrada")
    es_admin = usuario.get("rol") == "ADMINISTRADOR"
    usuario_id = usuario.get("id")
    if not es_admin and reserva.get("usuario_id") != usuario_id:
        raise SolicitudReservaError(403, "No autorizado")
    return {
        "id": reserva["id"],
        "espacio_id": reserva["espacio_id"],
        "usuario_id": reserva["usuario_id"],
        "inicio": reserva["inicio"] if reserva.get("inicio") and (str(reserva["inicio"]).endswith('Z') or '+' in str(reserva["inicio"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(reserva["inicio"]).replace('Z', '+00:00'))),
        "fin": reserva["fin"] if reserva.get("fin") and (str(reserva["fin"]).endswith('Z') or '+' in str(reserva["fin"])) else politicas.formatear_utc_iso8601(datetime.fromisoformat(str(reserva["fin"]).replace('Z', '+00:00'))),
        "motivo": reserva["motivo"],
        "estado": reserva["estado"],
        "creada_en": reserva.get("creada_en")
    }
