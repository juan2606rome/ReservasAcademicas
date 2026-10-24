import bcrypt
import jwt
from datetime import datetime, timedelta
from src.app.nucleo.configuracion import get_jwt_secret


def hash_contraseña(contraseña: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(contraseña.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verificar_contraseña(contraseña: str, hash_contraseña: str) -> bool:
    try:
        return bcrypt.checkpw(contraseña.encode("utf-8"), hash_contraseña.encode("utf-8"))
    except Exception:
        return False


def generar_token(usuario_id: int, rol: str) -> str:
    secret = get_jwt_secret()
    payload = {
        "id": usuario_id,
        "rol": rol,
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
