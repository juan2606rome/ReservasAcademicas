from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from src.app.autorizacion import dependencies as auth_dep
from src.app.cancelacion import service as cancel_service
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class CancelarBody(BaseModel):
    comentario: Optional[str] = None
    motivo: Optional[str] = None


@router.post("/reservas/{reserva_id}/cancelar")
async def cancelar(reserva_id: int, request: Request, usuario=Depends(auth_dep.obtener_usuario_actual), body: CancelarBody = None):
    try:
        comentario = None
        if body:
            comentario = body.comentario if body.comentario is not None else body.motivo
        # Si no hay body con Pydantic, intentar parsear manualmente
        if comentario is None:
            try:
                raw = await request.json()
                if isinstance(raw, dict):
                    comentario = raw.get('comentario') or raw.get('motivo')
            except Exception:
                pass
        result = cancel_service.cancelar_reserva(usuario, reserva_id, comentario)
        return JSONResponse(status_code=200, content=result)
    except cancel_service.CancelacionError as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
