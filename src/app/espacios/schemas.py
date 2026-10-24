from pydantic import BaseModel, Field
from typing import Optional, Literal


class EspacioCreateRequest(BaseModel):
    nombre: str = Field(...)
    tipo: Literal["LABORATORIO", "AUDITORIO", "SALA_COMPUTO"]
    capacidad: int


class EspacioUpdateRequest(BaseModel):
    nombre: str = Field(...)
    tipo: Literal["LABORATORIO", "AUDITORIO", "SALA_COMPUTO"]
    capacidad: int


class EspacioResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    capacidad: int
    activo: bool
