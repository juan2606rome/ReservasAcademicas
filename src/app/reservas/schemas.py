from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolicitudReservaCreate(BaseModel):
    espacio_id: int
    inicio: str
    fin: str
    motivo: str


class ReservaResponse(BaseModel):
    id: int
    espacio_id: int
    usuario_id: int
    inicio: str
    fin: str
    motivo: str
    estado: str


class FranjaDisponibilidad(BaseModel):
    inicio: str
    fin: str
    estado: str


class ReservaDetalladaResponse(BaseModel):
    id: int
    espacio_id: int
    usuario_id: int
    inicio: str
    fin: str
    motivo: str
    estado: str
    creada_en: Optional[str] = None
