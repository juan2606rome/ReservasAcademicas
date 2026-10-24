import re
from src.app.usuarios import repository
from src.app.nucleo.seguridad import hash_contraseña, verificar_contraseña, generar_token


class DatosInvalidosError(Exception):
    pass


class UsuarioDuplicadoError(Exception):
    pass


class CredencialesInvalidasError(Exception):
    pass


class CuentaInactivaError(Exception):
    pass


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_correo(correo: str) -> bool:
    if not correo or not isinstance(correo, str):
        return False
    return bool(EMAIL_REGEX.match(correo.strip()))


def validar_contraseña(contraseña: str) -> bool:
    if not contraseña or not isinstance(contraseña, str):
        return False
    if len(contraseña) < 8 or len(contraseña) > 72:
        return False
    return True


def validar_nombre(nombre: str) -> bool:
    if not nombre or not isinstance(nombre, str):
        return False
    if nombre.strip() == "":
        return False
    return True


def registrar_usuario(nombre: str, correo: str, contraseña: str, rol=None):
    if not validar_nombre(nombre):
        raise DatosInvalidosError()
    if not validar_correo(correo):
        raise DatosInvalidosError()
    if not validar_contraseña(contraseña):
        raise DatosInvalidosError()

    correo_normalizado = correo.strip().lower()
    hash_pwd = hash_contraseña(contraseña)
    # rol siempre SOLICITANTE, activo=true, ignora rol enviado
    try:
        usuario = repository.crear_usuario(
            nombre=nombre.strip(),
            correo=correo_normalizado,
            hash_contraseña=hash_pwd,
            rol="SOLICITANTE",
            activo=True,
        )
    except repository.UsuarioDuplicadoError:
        raise UsuarioDuplicadoError()

    # Respuesta sin contraseña ni hash
    return {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "rol": usuario["rol"],
        "activo": bool(usuario["activo"]),
    }


def iniciar_sesion(correo: str, contraseña: str):
    if not correo or not contraseña:
        raise DatosInvalidosError()
    if not validar_correo(correo):
        raise DatosInvalidosError()

    usuario = repository.buscar_usuario_por_correo(correo)
    if not usuario:
        raise CredencialesInvalidasError()

    # Verificar contraseña
    if not verificar_contraseña(contraseña, usuario["hash_contraseña"]):
        raise CredencialesInvalidasError()

    if not usuario["activo"]:
        raise CuentaInactivaError()

    token = generar_token(usuario["id"], usuario["rol"])
    return {"access_token": token, "token_type": "bearer"}
