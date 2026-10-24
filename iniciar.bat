@echo off
REM ============================================================
REM  Inicia el Sistema de Reservas (ejecutar desde la carpeta raiz
REM  del proyecto, la que tiene requirements.txt y la carpeta src)
REM ============================================================
cd /d "%~dp0"

if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv
)
call .venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

REM ---- Variables de entorno (cambia la clave si quieres) ----
set JWT_SECRET=una-clave-larga-de-prueba-1234567890
set ADMIN_NOMBRE=Administrador
set ADMIN_CORREO=admin@ejemplo.com
set ADMIN_PASSWORD=ClaveSegura123
set PYTHONPATH=%CD%

echo Creando tablas de la base de datos (reservas.db)...
python -c "from src.app.nucleo import conexion; conexion.init_db()"

echo Creando el primer administrador (si no existe)...
python scripts\seed_admin.py

echo.
echo ============================================================
echo  Aplicacion lista. Abre en el navegador:
echo     http://127.0.0.1:8000/docs
echo  Usuario admin: admin@ejemplo.com   Clave: ClaveSegura123
echo  (para detener: Ctrl + C)
echo ============================================================
start "" http://127.0.0.1:8000/docs
python -m uvicorn src.app.main:app --reload
pause
