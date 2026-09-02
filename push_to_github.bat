@echo off
set "PATH=C:\Users\VRUNDA\tools\git\cmd;C:\Users\VRUNDA\tools\nodejs;C:\Users\VRUNDA\tools\uv;%PATH%"

echo =========================================
echo   Pushing CreditPulse to GitHub (main)
echo =========================================

git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================================
    echo SUCCESS! Your repository is now updated:
    echo https://github.com/24f2002943/CreditPulse
    echo ============================================================================
) else (
    echo.
    echo Push encountered an error. Please review the output above.
)
pause
