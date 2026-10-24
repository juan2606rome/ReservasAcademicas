from src.app.historial import repository as hist_repo
from src.app.nucleo.conexion import get_connection


class HistorialError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def consultar_historial(usuario: dict, reserva_id=None, espacio_id=None, estado=None, desde=None, hasta=None):
    if not usuario:
        raise HistorialError(401, "No autorizado")
    # Validar valores inválidos en filtros
    try:
        if reserva_id is not None:
            int(reserva_id)
        if espacio_id is not None:
            int(espacio_id)
    except Exception:
        raise HistorialError(422, "Valor inválido en filtros")
    if estado is not None and estado not in ('PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA'):
        raise HistorialError(422, "Estado inválido")
    if desde is not None:
        # Validar formato AAAA-MM-DD
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(desde)):
            raise HistorialError(422, "Fecha inválida")
    if hasta is not None:
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(hasta)):
            raise HistorialError(422, "Fecha inválida")
    try:
        result = hist_repo.obtener_historial_con_filtros(
            usuario=usuario,
            reserva_id=int(reserva_id) if reserva_id is not None else None,
            espacio_id=int(espacio_id) if espacio_id is not None else None,
            estado=estado,
            desde=str(desde) if desde is not None else None,
            hasta=str(hasta) if hasta is not None else None,
        )
        return result
    except ValueError:
        raise HistorialError(422, "Fecha inválida")
    except Exception as e:
        raise HistorialError(422, str(e))
