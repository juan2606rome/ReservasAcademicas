@echo off
REM Abre la interfaz visual. Antes debe estar corriendo la API (iniciar.bat).
cd /d "%~dp0"
if exist .venv\Scripts\activate call .venv\Scripts\activate
start "" http://127.0.0.1:5500
python demo\servidor.py
pause
