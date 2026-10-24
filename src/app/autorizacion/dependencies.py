from fastapi import Header, HTTPException, Depends, status
from typing import Optional, List
import jwt
from src.app.nucleo import seguridad
from src.app.usuarios import repository as usuarios_repo


class TokenInvalidoError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")


class TokenFaltaError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")


class UsuarioNoEncontradoError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")


class UsuarioInactivoError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta inactiva")


class PermisosInsuficientesError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes")


def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise TokenFaltaError()
    partes = authorization.split()
    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise TokenInvalidoError()
    token = partes[1]
    if not token:
        raise TokenInvalidoError()
    return token


def get_current_user(token: str = Depends(get_token_from_header)):
    try:
        payload = seguridad.decodificar_token(token)
    except jwt.ExpiredSignatureError:
        raise TokenInvalidoError()
    except Exception:
        raise TokenInvalidoError()

    usuario_id = payload.get("id") or payload.get("usuario_id") or payload.get("sub")
    if usuario_id is None:
        raise TokenInvalidoError()
    usuario = usuarios_repo.buscar_usuario_por_id(usuario_id)
    if not usuario:
        raise UsuarioNoEncontradoError()
    activo = usuario.get("activo")
    if activo == 0 or activo is False:
        raise UsuarioInactivoError()
    return usuario


def require_roles(*roles_permitidos: str):
    def _role_checker(usuario=Depends(get_current_user)):
        rol_usuario = usuario.get("rol")
        if rol_usuario not in roles_permitidos:
            raise PermisosInsuficientesError()
        return usuario
    return _role_checker


require_admin = require_roles("ADMINISTRADOR")


# Alias for compatibility
obtener_usuario_actual = get_current_user

