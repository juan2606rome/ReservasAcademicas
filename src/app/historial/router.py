from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from src.app.autorizacion import dependencies as auth_dep
from src.app.historial import service as hist_service

router = APIRouter()


@router.get("/historial")
async def obtener_historial(request: Request, usuario=Depends(auth_dep.obtener_usuario_actual)):
    try:
        params = request.query_params
        reserva_id = params.get('reserva_id')
        espacio_id = params.get('espacio_id')
        estado = params.get('estado')
        desde = params.get('desde')
        hasta = params.get('hasta')
        result = hist_service.consultar_historial(usuario, reserva_id=reserva_id, espacio_id=espacio_id,
                                                  estado=estado, desde=desde, hasta=hasta)
        return JSONResponse(status_code=200, content=result)
    except hist_service.HistorialError as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
