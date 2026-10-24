from src.app.espacios import repository


TIPOS_VALIDOS = {"LABORATORIO", "AUDITORIO", "SALA_COMPUTO"}


class DatosInvalidosError(Exception):
    pass


class EspacioDuplicadoError(Exception):
    pass


class EspacioNoEncontradoError(Exception):
    pass


def _normalizar_nombre(nombre: str) -> str:
    if nombre is None:
        return ""
    return str(nombre).strip()


def _validar_nombre(nombre: str):
    nombre_norm = _normalizar_nombre(nombre)
    if nombre_norm == "":
        raise DatosInvalidosError()
    return nombre_norm


def _validar_tipo(tipo: str):
    if tipo not in TIPOS_VALIDOS:
        raise DatosInvalidosError()
    return tipo


def _validar_capacidad(capacidad):
    # Debe ser entero mayor que 0
    if isinstance(capacidad, bool):
        raise DatosInvalidosError()
    # Verificar que sea entero (no float con decimales)
    if isinstance(capacidad, float):
        # Si es float, solo aceptar si es entero
        if not capacidad.is_integer():
            raise DatosInvalidosError()
        capacidad_int = int(capacidad)
    elif isinstance(capacidad, int):
        capacidad_int = capacidad
    else:
        # Intentar convertir si viene como string numérico
        try:
            # Verificar si es entero
            if isinstance(capacidad, str) and "." in capacidad:
                raise DatosInvalidosError()
            capacidad_int = int(capacidad)
        except Exception:
            raise DatosInvalidosError()
    if capacidad_int <= 0:
        raise DatosInvalidosError()
    return capacidad_int


def crear_espacio(nombre: str, tipo: str, capacidad, usuario: dict = None) -> dict:
    nombre_validado = _validar_nombre(nombre)
    tipo_validado = _validar_tipo(tipo)
    capacidad_validada = _validar_capacidad(capacidad)
    try:
        espacio = repository.crear_espacio(nombre_validado, tipo_validado, capacidad_validada)
    except repository.EspacioDuplicadoError:
        raise EspacioDuplicadoError()
    # Convertir activo a bool si viene como int
    if isinstance(espacio.get("activo"), int):
        espacio["activo"] = bool(espacio["activo"])
    return espacio


def listar_espacios(usuario: dict = None, incluir_inactivos: bool = False) -> list:
    # Solo administrador puede incluir inactivos
    if incluir_inactivos:
        rol = usuario.get("rol") if usuario else None
        if rol != "ADMINISTRADOR":
            incluir_inactivos = False
    espacios = repository.listar_espacios(incluir_inactivos=incluir_inactivos)
    resultado = []
    for e in espacios:
        if isinstance(e.get("activo"), int):
            e = dict(e)
            e["activo"] = bool(e["activo"])
        resultado.append(e)
    return resultado


def obtener_espacio_por_id(espacio_id: int, usuario: dict = None) -> dict:
    espacio = repository.obtener_espacio_por_id(espacio_id)
    if espacio is None:
        raise EspacioNoEncontradoError()
    if isinstance(espacio.get("activo"), int):
        espacio = dict(espacio)
        espacio["activo"] = bool(espacio["activo"])
    # Si está inactivo, solo administrador puede verlo (recibe 200), solicitante recibe 404
    if not espacio.get("activo"):
        rol = usuario.get("rol") if usuario else None
        if rol != "ADMINISTRADOR":
            raise EspacioNoEncontradoError()
    return espacio


def actualizar_espacio(espacio_id: int, nombre: str, tipo: str, capacidad, usuario: dict = None) -> dict:
    nombre_validado = _validar_nombre(nombre)
    tipo_validado = _validar_tipo(tipo)
    capacidad_validada = _validar_capacidad(capacidad)
    # Verificar existencia
    existente = repository.obtener_espacio_por_id(espacio_id)
    if existente is None:
        raise EspacioNoEncontradoError()
    try:
        espacio = repository.actualizar_espacio(espacio_id, nombre_validado, tipo_validado, capacidad_validada)
    except repository.EspacioDuplicadoError:
        raise EspacioDuplicadoError()
    if espacio is None:
        raise EspacioNoEncontradoError()
    if isinstance(espacio.get("activo"), int):
        espacio["activo"] = bool(espacio["activo"])
    return espacio


def desactivar_espacio(espacio_id: int, usuario: dict = None) -> dict:
    existente = repository.obtener_espacio_por_id(espacio_id)
    if existente is None:
        raise EspacioNoEncontradoError()
    try:
        espacio = repository.desactivar_espacio(espacio_id)
    except Exception:
        raise
    if espacio is None:
        raise EspacioNoEncontradoError()
    if isinstance(espacio.get("activo"), int):
        espacio["activo"] = bool(espacio["activo"])
    return espacio


def activar_espacio(espacio_id: int, usuario: dict = None) -> dict:
    existente = repository.obtener_espacio_por_id(espacio_id)
    if existente is None:
        raise EspacioNoEncontradoError()
    try:
        espacio = repository.activar_espacio(espacio_id)
    except Exception:
        raise
    if espacio is None:
        raise EspacioNoEncontradoError()
    if isinstance(espacio.get("activo"), int):
        espacio["activo"] = bool(espacio["activo"])
    return espacio
