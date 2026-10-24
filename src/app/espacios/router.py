from fastapi import APIRouter, HTTPException, status, Depends, Query
from src.app.espacios import schemas, service
from src.app.autorizacion import dependencies

router = APIRouter(prefix="/espacios", tags=["espacios"])


@router.post("", response_model=schemas.EspacioResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=schemas.EspacioResponse, status_code=status.HTTP_201_CREATED)
def crear_espacio(
    espacio: schemas.EspacioCreateRequest,
    usuario=Depends(dependencies.require_admin),
):
    try:
        return service.crear_espacio(
            nombre=espacio.nombre,
            tipo=espacio.tipo,
            capacidad=espacio.capacidad,
            usuario=usuario,
        )
    except service.DatosInvalidosError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")
    except service.EspacioDuplicadoError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Espacio duplicado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")


@router.get("", response_model=list[schemas.EspacioResponse])
@router.get("/", response_model=list[schemas.EspacioResponse])
def listar_espacios(
    incluir_inactivos: bool = Query(False),
    usuario=Depends(dependencies.get_current_user),
):
    try:
        return service.listar_espacios(usuario=usuario, incluir_inactivos=incluir_inactivos)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK)


@router.get("/{espacio_id}", response_model=schemas.EspacioResponse)
def obtener_espacio(
    espacio_id: int,
    usuario=Depends(dependencies.get_current_user),
):
    try:
        return service.obtener_espacio_por_id(espacio_id, usuario=usuario)
    except service.EspacioNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")


@router.put("/{espacio_id}", response_model=schemas.EspacioResponse)
def actualizar_espacio(
    espacio_id: int,
    espacio: schemas.EspacioUpdateRequest,
    usuario=Depends(dependencies.require_admin),
):
    try:
        return service.actualizar_espacio(
            espacio_id=espacio_id,
            nombre=espacio.nombre,
            tipo=espacio.tipo,
            capacidad=espacio.capacidad,
            usuario=usuario,
        )
    except service.DatosInvalidosError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")
    except service.EspacioDuplicadoError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Espacio duplicado")
    except service.EspacioNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Datos inválidos")


@router.patch("/{espacio_id}/desactivar", response_model=schemas.EspacioResponse)
def desactivar_espacio(
    espacio_id: int,
    usuario=Depends(dependencies.require_admin),
):
    try:
        return service.desactivar_espacio(espacio_id, usuario=usuario)
    except service.EspacioNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")


@router.patch("/{espacio_id}/activar", response_model=schemas.EspacioResponse)
def activar_espacio(
    espacio_id: int,
    usuario=Depends(dependencies.require_admin),
):
    try:
        return service.activar_espacio(espacio_id, usuario=usuario)
    except service.EspacioNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
