from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegistroUsuarioRequest(BaseModel):
    nombre: str = Field(..., min_length=1)
    correo: EmailStr
    contraseña: str = Field(..., min_length=8, max_length=72)
    rol: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool


class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
