from src.app.nucleo.conexion import get_connection
from typing import Optional


def obtener_reserva_por_id(reserva_id: int, conn=None):
    c = conn or get_connection()
    should_close = conn is None
    try:
        cur = c.cursor()
        cur.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        if should_close:
            c.close()


def actualizar_estado_reserva(reserva_id: int, estado: str, conn=None):
    c = conn or get_connection()
    should_close = conn is None
    try:
        cur = c.cursor()
        cur.execute("UPDATE reservas SET estado = ? WHERE id = ?", (estado, reserva_id))
        c.commit() if should_close else None
        return cur.rowcount
    finally:
        if should_close:
            c.close()
