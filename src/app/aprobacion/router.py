from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Optional
from pydantic import BaseModel
from src.app.autorizacion.dependencies import require_admin
from src.app.aprobacion import service


router = APIRouter(prefix="/reservas", tags=["aprobacion"])


class MotivoRequest(BaseModel):
    motivo: Optional[str] = None


@router.post("/{reserva_id}/aprobar", status_code=status.HTTP_200_OK)
def aprobar_reserva(reserva_id: int, body: Optional[MotivoRequest] = None, usuario=Depends(require_admin)):
    try:
        motivo = None
        if body is not None:
            motivo = body.motivo
        resultado = service.aprobar_reserva(usuario, reserva_id, motivo=motivo)
        return resultado
    except service.AprobacionError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{reserva_id}/rechazar", status_code=status.HTTP_200_OK)
def rechazar_reserva(reserva_id: int, body: MotivoRequest, usuario=Depends(require_admin)):
    try:
        motivo = body.motivo if body is not None else None
        resultado = service.rechazar_reserva(usuario, reserva_id, motivo=motivo)
        return resultado
    except service.AprobacionError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
