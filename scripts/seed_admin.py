#!/usr/bin/env python3
import os
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from src.app.usuarios import repository
from src.app.usuarios.repository import UsuarioDuplicadoError
from src.app.nucleo import seguridad


def main():
    nombre = os.environ.get('ADMIN_NOMBRE')
    correo = os.environ.get('ADMIN_CORREO')
    password = os.environ.get('ADMIN_PASSWORD')
    
    if not nombre or not correo or not password:
        print('Error: Se requieren las variables de entorno ADMIN_NOMBRE, ADMIN_CORREO y ADMIN_PASSWORD')
        sys.exit(1)
    
    try:
        # Verificar si el correo ya existe
        if repository.existe_correo(correo):
            print('El usuario ya existe')
            return
        hash_pwd = seguridad.hash_contrase\u00f1a(password)
        usuario = repository.crear_usuario(
            nombre=nombre.strip(),
            correo=correo.strip().lower(),
            hash_contrase\u00f1a=hash_pwd,
            rol='ADMINISTRADOR',
            activo=True,
        )
        print(f'Usuario administrador creado: {usuario[\"correo\"]}')
    except UsuarioDuplicadoError:
        print('El usuario ya existe')
        return
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
