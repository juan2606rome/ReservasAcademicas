from fastapi import FastAPI
from src.app.usuarios import router as usuarios_router
from src.app.autorizacion import router as autorizacion_router

app = FastAPI(title="Sistema de Reservas Acad\u00e9micas")

app.include_router(usuarios_router.router)
app.include_router(autorizacion_router.router)

@app.get("/")
def root():
    return {"message": "Sistema de Reservas Acad\u00e9micas"}
