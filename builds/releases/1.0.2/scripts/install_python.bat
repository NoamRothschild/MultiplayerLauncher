@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    start ms-windows-store://pdp/?productid=9PJPW5LDXLZ5
) else (
    echo Python is already installed.
)

echo Installation complete.
endlocal
pause
