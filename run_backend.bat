@echo off
set "PATH=C:\Users\VRUNDA\tools\uv;%PATH%"
cd /d "%~dp0backend"

echo =======================================================
echo   Starting CreditPulse Backend (FastAPI + ML Engine)
echo   Interactive API Docs: http://localhost:8000/docs
echo   Base API URL:         http://localhost:8000/api
echo =======================================================

.venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
pause
