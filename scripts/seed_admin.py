#!/usr/bin/env python3
"""Crea el primer administrador a partir de variables de entorno.
Uso: definir ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD y ejecutar este script."""
import os
import sys

# Agregar la raiz del proyecto al path para poder importar "src"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from src.app.nucleo import conexion, seguridad
from src.app.usuarios import repository
from src.app.usuarios.repository import UsuarioDuplicadoError


def main():
    nombre = os.environ.get("ADMIN_NOMBRE")
    correo = os.environ.get("ADMIN_CORREO")
    password = os.environ.get("ADMIN_PASSWORD")

    if not nombre or not correo or not password:
        print("Error: se requieren las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD")
        sys.exit(1)

    try:
        conexion.init_db()
        if repository.existe_correo(correo):
            print("El usuario ya existe")
            return
        hash_pwd = seguridad.hash_contraseña(password)
        usuario = repository.crear_usuario(
            nombre=nombre.strip(),
            correo=correo.strip().lower(),
            hash_contraseña=hash_pwd,
            rol="ADMINISTRADOR",
            activo=True,
        )
        print(f"Usuario administrador creado: {usuario['correo']}")
    except UsuarioDuplicadoError:
        print("El usuario ya existe")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
