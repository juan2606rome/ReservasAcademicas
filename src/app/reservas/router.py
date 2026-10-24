from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from typing import Optional, List
from src.app.autorizacion.dependencies import get_current_user
from src.app.reservas import service
from src.app.reservas.schemas import SolicitudReservaCreate, ReservaResponse, FranjaDisponibilidad, ReservaDetalladaResponse


router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post("/solicitudes", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_solicitud(request: Request, solicitud: SolicitudReservaCreate, usuario=Depends(get_current_user)):
    try:
        # Ignorar usuario en cuerpo si viene
        resultado = service.crear_solicitud_reserva(
            usuario_id=usuario["id"],
            espacio_id=solicitud.espacio_id,
            inicio_str=solicitud.inicio,
            fin_str=solicitud.fin,
            motivo=solicitud.motivo
        )
        return resultado
    except service.SolicitudReservaError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/disponibilidad", response_model=List[FranjaDisponibilidad])
def consultar_disponibilidad(espacio_id: int = Query(...), fecha: str = Query(...), usuario=Depends(get_current_user)):
    try:
        resultado = service.consultar_disponibilidad(espacio_id, fecha)
        return resultado
    except service.SolicitudReservaError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=List[ReservaDetalladaResponse])
def listar_reservas(
    estado: Optional[str] = Query(None),
    espacio_id: Optional[str] = Query(None),
    usuario=Depends(get_current_user)
):
    try:
        # Validar espacio_id si viene
        espacio_id_int = None
        if espacio_id is not None:
            # Verificar si es numérico
            try:
                # Intentar convertir
                espacio_id_int = int(espacio_id)
            except Exception:
                raise HTTPException(status_code=422, detail="espacio_id inválido")
        resultado = service.listar_reservas_usuario(usuario, estado=estado, espacio_id=espacio_id_int)
        return resultado
    except service.SolicitudReservaError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{reserva_id}", response_model=ReservaDetalladaResponse)
def obtener_reserva(reserva_id: int, usuario=Depends(get_current_user)):
    try:
        resultado = service.obtener_reserva(usuario, reserva_id)
        return resultado
    except service.SolicitudReservaError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
