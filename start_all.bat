@echo off
echo ========================================================
echo   Launching CreditPulse Full-Stack Platform...
echo ========================================================
echo   - Backend (FastAPI + XGBoost) -> http://localhost:8000
echo   - Frontend (Next.js Dashboard) -> http://localhost:3000
echo ========================================================

start "CreditPulse Backend (FastAPI)" cmd /c "%~dp0run_backend.bat"
timeout /t 2 /nobreak >nul
start "CreditPulse Frontend (Next.js)" cmd /c "%~dp0run_frontend.bat"

echo.
echo Both services are launching in separate windows!
echo Open your browser at http://localhost:3000 to use CreditPulse.
