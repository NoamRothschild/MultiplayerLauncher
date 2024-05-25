@echo off
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
    exit /b 1
) else (
    echo Python is installed.
    exit /b 0
)