from fastapi import FastAPI
from src.app.usuarios import router as usuarios_router

app = FastAPI(title="Sistema de Reservas Académicas")

app.include_router(usuarios_router.router)

@app.get("/")
def root():
    return {"message": "Sistema de Reservas Académicas"}
