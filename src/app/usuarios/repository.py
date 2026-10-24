import sqlite3
from src.app.nucleo.conexion import get_connection


class UsuarioDuplicadoError(Exception):
    pass


def crear_usuario(nombre: str, correo: str, hash_contraseña: str, rol: str, activo: bool):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, hash_contraseña, rol, activo) VALUES (?, ?, ?, ?, ?)",
            (nombre, correo, hash_contraseña, rol, 1 if activo else 0),
        )
        conn.commit()
        usuario_id = cursor.lastrowid
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        raise UsuarioDuplicadoError()
    finally:
        conn.close()


def buscar_usuario_por_correo(correo: str):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE LOWER(correo) = LOWER(?)", (correo,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def existe_correo(correo: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE LOWER(correo) = LOWER(?)", (correo,))
        row = cursor.fetchone()
        return row is not None
    finally:
        conn.close()
