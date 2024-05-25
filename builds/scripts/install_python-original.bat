@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe
    start /wait python-installer.exe
    del python-installer.exe
) else (
    echo Python is already installed.
)

echo Installation complete.
endlocal
pause
