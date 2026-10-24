from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Tuple, Optional


TZ_BOGOTA = ZoneInfo("America/Bogota")


def parse_datetime_con_zona_horaria(fecha_str: str) -> datetime:
    """Parsea datetime ISO 8601 con zona horaria. Si no trae zona horaria, lanza error."""
    try:
        dt = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
    except Exception:
        raise ValueError("Formato de fecha inválido")
    # Verificar que tenga zona horaria
    if dt.tzinfo is None:
        raise ValueError("Fecha debe tener zona horaria")
    return dt


def validar_solicitud_reserva(inicio_str: str, fin_str: str, motivo: str) -> Tuple[datetime, datetime]:
    """Valida solicitud de reserva según reglas. Retorna (inicio_utc, fin_utc)."""
    # Verificar campos obligatorios
    if inicio_str is None or fin_str is None or motivo is None:
        raise ValueError("Campos obligatorios faltantes")
    
    # Validar motivo
    if not isinstance(motivo, str) or motivo.strip() == "":
        raise ValueError("Motivo inválido")
    if len(motivo) > 500:
        raise ValueError("Motivo inválido")
    
    # Parsear con zona horaria
    try:
        inicio_dt = parse_datetime_con_zona_horaria(inicio_str)
        fin_dt = parse_datetime_con_zona_horaria(fin_str)
    except ValueError as e:
        if "zona horaria" in str(e).lower():
            raise
        raise ValueError("Fecha inválida")
    
    # Convertir a hora de Bogotá para validaciones
    inicio_bogota = inicio_dt.astimezone(TZ_BOGOTA)
    fin_bogota = fin_dt.astimezone(TZ_BOGOTA)
    
    # fin > inicio
    if fin_dt <= inicio_dt:
        raise ValueError("fin debe ser mayor a inicio")
    
    # mismo día en hora de Bogotá
    if inicio_bogota.date() != fin_bogota.date():
        raise ValueError("Reserva debe ser en el mismo día")
    
    # inicio no en el pasado en hora de Bogotá
    ahora_bogota = datetime.now(TZ_BOGOTA)
    # Comparar con inicio en Bogotá
    if inicio_bogota < ahora_bogota:
        raise ValueError("Inicio no puede estar en el pasado")
    
    # Convertir a UTC para guardar
    inicio_utc = inicio_dt.astimezone(timezone.utc)
    fin_utc = fin_dt.astimezone(timezone.utc)
    
    return inicio_utc, fin_utc


def hay_solapamiento(inicio1: datetime, fin1: datetime, inicio2: datetime, fin2: datetime) -> bool:
    """Verifica solapamiento con intervalos semiabiertos [inicio, fin)"""
    # a1 < b2 AND b1 < a2
    return inicio1 < fin2 and inicio2 < fin1


def formatear_utc_iso8601(dt: datetime) -> str:
    """Formatea datetime a ISO 8601 con zona horaria UTC"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace('+00:00', 'Z')


def parsear_fecha_bogota(fecha_str: str) -> date:
    """Parsea fecha YYYY-MM-DD"""
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Fecha inválida")
