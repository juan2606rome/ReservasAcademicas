import sqlite3
from src.app.nucleo.conexion import get_connection


class EspacioDuplicadoError(Exception):
    pass


def _normalizar_nombre(nombre: str) -> str:
    if nombre is None:
        return ""
    return str(nombre).strip().lower()


def crear_espacio(nombre: str, tipo: str, capacidad: int) -> dict:
    conn = get_connection()
    try:
        nombre_norm = _normalizar_nombre(nombre)
        # Verificar duplicado
        cur = conn.execute("SELECT id FROM espacios WHERE LOWER(TRIM(nombre)) = ?", (nombre_norm,))
        if cur.fetchone():
            raise EspacioDuplicadoError()
        cur = conn.execute(
            "INSERT INTO espacios (nombre, tipo, capacidad, activo) VALUES (?, ?, ?, 1)",
            (nombre.strip() if isinstance(nombre, str) else nombre, tipo, capacidad),
        )
        conn.commit()
        espacio_id = cur.lastrowid
        cur = conn.execute("SELECT * FROM espacios WHERE id = ?", (espacio_id,))
        row = cur.fetchone()
        if row is None:
            return {"id": espacio_id, "nombre": nombre, "tipo": tipo, "capacidad": capacidad, "activo": True}
        return dict(row)
    except EspacioDuplicadoError:
        raise
    except sqlite3.IntegrityError:
        raise EspacioDuplicadoError()
    finally:
        conn.close()


def listar_espacios(incluir_inactivos: bool = False) -> list:
    conn = get_connection()
    try:
        if incluir_inactivos:
            cur = conn.execute("SELECT * FROM espacios")
        else:
            cur = conn.execute("SELECT * FROM espacios WHERE activo = 1")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def obtener_espacio_por_id(espacio_id: int) -> dict | None:
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM espacios WHERE id = ?", (espacio_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


def actualizar_espacio(espacio_id: int, nombre: str, tipo: str, capacidad: int) -> dict | None:
    conn = get_connection()
    try:
        nombre_norm = _normalizar_nombre(nombre)
        # Verificar duplicado con otro espacio
        cur = conn.execute("SELECT id FROM espacios WHERE LOWER(TRIM(nombre)) = ? AND id != ?", (nombre_norm, espacio_id))
        if cur.fetchone():
            raise EspacioDuplicadoError()
        cur = conn.execute(
            "UPDATE espacios SET nombre = ?, tipo = ?, capacidad = ? WHERE id = ?",
            (nombre.strip() if isinstance(nombre, str) else nombre, tipo, capacidad, espacio_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
        cur = conn.execute("SELECT * FROM espacios WHERE id = ?", (espacio_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    except EspacioDuplicadoError:
        raise
    except sqlite3.IntegrityError:
        raise EspacioDuplicadoError()
    finally:
        conn.close()


def desactivar_espacio(espacio_id: int) -> dict | None:
    conn = get_connection()
    try:
        cur = conn.execute("UPDATE espacios SET activo = 0 WHERE id = ?", (espacio_id,))
        conn.commit()
        if cur.rowcount == 0:
            return None
        cur = conn.execute("SELECT * FROM espacios WHERE id = ?", (espacio_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


def activar_espacio(espacio_id: int) -> dict | None:
    conn = get_connection()
    try:
        cur = conn.execute("UPDATE espacios SET activo = 1 WHERE id = ?", (espacio_id,))
        conn.commit()
        if cur.rowcount == 0:
            return None
        cur = conn.execute("SELECT * FROM espacios WHERE id = ?", (espacio_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()
