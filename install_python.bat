@echo off
title Velpro Hospital - Python Installer

echo ============================================
echo   Velpro Hospital Automated Python Setup
echo ============================================
echo.

:: Check if Python is already installed
python --version >nul 2>nul
if %errorlevel%==0 (
    echo Python is already installed.
    echo Exiting...
    pause
    exit /b 0
)

echo Python not found. Proceeding with installation...
echo.

:: Create temp directory
mkdir temp 2>nul

echo Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/njohnjoel/velpro_hospital/releases/download/binaries/python-3.13.12-amd64.exe' -OutFile 'temp\python.exe'"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Download failed.
    rmdir temp 2>nul
    pause
    exit /b 1
)

echo.
echo Installing Python silently...
start /wait "" temp\python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed.
    del temp\python.exe
    rmdir temp
    pause
    exit /b 1
)

echo.
echo Installation completed successfully.
echo Cleaning up...

del temp\python.exe
rmdir temp

echo.
echo Setup finished.
pause