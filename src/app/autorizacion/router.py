from fastapi import APIRouter, Depends, HTTPException, status
from src.app.autorizacion import dependencies
from src.app.usuarios import repository


router = APIRouter(tags=["usuarios-admin"])


@router.get("/usuarios/yo")
def obtener_mi_usuario(usuario=Depends(dependencies.get_current_user)):
    return {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "rol": usuario["rol"],
    }


@router.get("/usuarios")
def listar_usuarios(usuario=Depends(dependencies.require_admin)):
    usuarios = repository.obtener_todos_usuarios()
    result = []
    for u in usuarios:
        result.append({
            "id": u["id"],
            "nombre": u["nombre"],
            "correo": u["correo"],
            "rol": u["rol"],
            "activo": bool(u["activo"]) if "activo" in u else u.get("activo"),
        })
    return result


@router.get("/usuarios/{id}")
def obtener_usuario(id: int, usuario=Depends(dependencies.require_admin)):
    usuario_res = repository.obtener_usuario_por_id(id)
    if not usuario_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "id": usuario_res["id"],
        "nombre": usuario_res["nombre"],
        "correo": usuario_res["correo"],
        "rol": usuario_res["rol"],
        "activo": bool(usuario_res["activo"]) if "activo" in usuario_res else usuario_res.get("activo"),
    }


@router.patch("/usuarios/{id}/desactivar")
def desactivar_usuario(id: int, usuario_admin=Depends(dependencies.require_admin)):
    # No puede desactivarse a sí mismo
    if usuario_admin["id"] == id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No puede desactivarse a sí mismo")
    usuario_res = repository.desactivar_usuario(id)
    if usuario_res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "id": usuario_res["id"],
        "nombre": usuario_res["nombre"],
        "correo": usuario_res["correo"],
        "rol": usuario_res["rol"],
        "activo": bool(usuario_res["activo"]) if "activo" in usuario_res else usuario_res.get("activo"),
    }


@router.patch("/usuarios/{id}/activar")
def activar_usuario(id: int, usuario_admin=Depends(dependencies.require_admin)):
    usuario_res = repository.activar_usuario(id)
    if usuario_res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "id": usuario_res["id"],
        "nombre": usuario_res["nombre"],
        "correo": usuario_res["correo"],
        "rol": usuario_res["rol"],
        "activo": bool(usuario_res["activo"]) if "activo" in usuario_res else usuario_res.get("activo"),
    }
