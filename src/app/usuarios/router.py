from fastapi import APIRouter, HTTPException, status
from src.app.usuarios import schemas, service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/registro", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(usuario: schemas.RegistroUsuarioRequest):
    try:
        return service.registrar_usuario(
            nombre=usuario.nombre,
            correo=str(usuario.correo),
            contraseña=usuario.contraseña,
            rol=usuario.rol,
        )
    except service.DatosInvalidosError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")
    except service.UsuarioDuplicadoError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Correo ya registrado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")


@router.post("/login", response_model=schemas.TokenResponse)
def login(credenciales: schemas.LoginRequest):
    try:
        return service.iniciar_sesion(correo=str(credenciales.correo), contraseña=credenciales.contraseña)
    except service.DatosInvalidosError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")
    except service.CredencialesInvalidasError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    except service.CuentaInactivaError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta inactiva")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
