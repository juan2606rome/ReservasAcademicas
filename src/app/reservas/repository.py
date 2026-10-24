import sqlite3
from datetime import datetime, date, timezone
from typing import Optional, List
from src.app.nucleo.conexion import get_connection


def buscar_reservas_solapadas(espacio_id: int, inicio_iso: str, fin_iso: str, conn=None) -> List[dict]:
    """Busca reservas que se solapan con el intervalo [inicio_iso, fin_iso) en el MISMO espacio
    Solo considera reservas PENDIENTE o APROBADA"""
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        # Intervalos semiabiertos: a1 < b2 AND b1 < a2
        cur = conn.execute(
            """
            SELECT * FROM reservas 
            WHERE espacio_id = ? 
            AND estado IN ('PENDIENTE', 'APROBADA')
            AND inicio < ? 
            AND ? < fin
            """,
            (espacio_id, fin_iso, inicio_iso),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        if debe_cerrar:
            conn.close()


def crear_reserva(espacio_id: int, usuario_id: int, inicio_iso: str, fin_iso: str, motivo: str, estado: str = 'PENDIENTE', conn=None) -> dict:
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        creada_en = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        cur = conn.execute(
            """
            INSERT INTO reservas (espacio_id, usuario_id, inicio, fin, motivo, estado, creada_en)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (espacio_id, usuario_id, inicio_iso, fin_iso, motivo, estado, creada_en),
        )
        conn.commit()
        reserva_id = cur.lastrowid
        cur = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        row = cur.fetchone()
        return dict(row) if row else {"id": reserva_id}
    finally:
        if debe_cerrar:
            conn.close()


def obtener_reservas_por_fecha_espacio(espacio_id: int, fecha: date, conn=None) -> List[dict]:
    """Obtiene reservas PENDIENTE o APROBADA de un espacio en una fecha dada (evaluada en hora Bogotá)"""
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        # Convertir fecha de Bogotá (UTC-5) a rango UTC para buscar
        from datetime import timedelta
        from zoneinfo import ZoneInfo
        tz_bogota = ZoneInfo("America/Bogota")
        # Inicio del día en Bogotá
        inicio_bogota = datetime.combine(fecha, datetime.min.time(), tzinfo=tz_bogota)
        fin_bogota = inicio_bogota + timedelta(days=1)
        # Convertir a UTC
        inicio_utc = inicio_bogota.astimezone(timezone.utc)
        fin_utc = fin_bogota.astimezone(timezone.utc)
        inicio_utc_str = inicio_utc.isoformat().replace('+00:00', 'Z')
        fin_utc_str = fin_utc.isoformat().replace('+00:00', 'Z')
        # Buscar reservas que intersequen con el día
        cur = conn.execute(
            """
            SELECT * FROM reservas 
            WHERE espacio_id = ? 
            AND estado IN ('PENDIENTE', 'APROBADA')
            AND inicio < ? 
            AND fin > ?
            ORDER BY inicio
            """,
            (espacio_id, fin_utc_str, inicio_utc_str),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        if debe_cerrar:
            conn.close()


def listar_reservas(usuario_id: Optional[int] = None, es_admin: bool = False, estado: Optional[str] = None, espacio_id: Optional[int] = None, conn=None) -> List[dict]:
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        query = "SELECT * FROM reservas WHERE 1=1"
        params = []
        if not es_admin:
            query += " AND usuario_id = ?"
            params.append(usuario_id)
        if estado:
            query += " AND estado = ?"
            params.append(estado)
        if espacio_id is not None:
            query += " AND espacio_id = ?"
            params.append(espacio_id)
        query += " ORDER BY creada_en DESC, id DESC"
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        if debe_cerrar:
            conn.close()


def obtener_reserva_por_id(reserva_id: int, conn=None) -> Optional[dict]:
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        cur = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        if debe_cerrar:
            conn.close()
