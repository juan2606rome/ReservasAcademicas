import sqlite3
from datetime import datetime, timezone
from typing import Optional, List
from src.app.nucleo.conexion import get_connection


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


def buscar_reservas_solapadas_aprobacion(espacio_id: int, inicio_iso: str, fin_iso: str, excluir_reserva_id: int, conn=None) -> List[dict]:
    """Busca reservas solapadas con el intervalo, excluyendo la propia reserva.
    Considera reservas PENDIENTE o APROBADA"""
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        cur = conn.execute(
            """
            SELECT * FROM reservas 
            WHERE espacio_id = ? 
            AND estado IN ('PENDIENTE', 'APROBADA')
            AND id != ?
            AND inicio < ? 
            AND ? < fin
            """,
            (espacio_id, excluir_reserva_id, fin_iso, inicio_iso),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        if debe_cerrar:
            conn.close()


def aprobar_reserva(reserva_id: int, decidido_por: int, motivo_decision: Optional[str], conn=None) -> dict:
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        decidido_en = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        cur = conn.execute(
            """
            UPDATE reservas 
            SET estado = 'APROBADA', decidido_por = ?, decidido_en = ?, motivo_decision = ?
            WHERE id = ?
            """,
            (decidido_por, decidido_en, motivo_decision, reserva_id),
        )
        if conn.in_transaction is False and debe_cerrar:
            conn.commit()
        cur = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        row = cur.fetchone()
        return dict(row) if row else {"id": reserva_id}
    finally:
        if debe_cerrar:
            conn.close()


def rechazar_reserva(reserva_id: int, decidido_por: int, motivo_decision: str, conn=None) -> dict:
    debe_cerrar = False
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    try:
        decidido_en = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        cur = conn.execute(
            """
            UPDATE reservas 
            SET estado = 'RECHAZADA', decidido_por = ?, decidido_en = ?, motivo_decision = ?
            WHERE id = ?
            """,
            (decidido_por, decidido_en, motivo_decision, reserva_id),
        )
        if conn.in_transaction is False and debe_cerrar:
            conn.commit()
        cur = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        row = cur.fetchone()
        return dict(row) if row else {"id": reserva_id}
    finally:
        if debe_cerrar:
            conn.close()
