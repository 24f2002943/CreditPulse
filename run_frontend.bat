@echo off
set "PATH=C:\Users\VRUNDA\tools\nodejs;%PATH%"
cd /d "%~dp0frontend"

echo =======================================================
echo   Starting CreditPulse Frontend (Next.js 14 Dashboard)
echo   Web App URL: http://localhost:3000
echo =======================================================

npm run dev
pause
