@echo off
setlocal enabledelayedexpansion
title Ashenfall 1-Click World Installer
cls
echo =======================================================================
echo         ASHENFALL - 1-Click World and Worldgen Installer
echo =======================================================================
echo.

:: 1. Check if Python is available and working
python -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Running with Python...
    python "%~dp0build_world.py" %*
    goto :end
)

py -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Running with py launcher...
    py "%~dp0build_world.py" %*
    goto :end
)

:: 2. Python is not installed -> Run Native PowerShell Installer
echo [*] Python not detected. Running native Windows PowerShell installer...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/Exo2v/The-modpack/arena/01a0e180-the-modpack/setup.ps1', '%TEMP%\setup.ps1'); & '%TEMP%\setup.ps1'"

if %ERRORLEVEL% equ 0 goto :end

echo.
echo [!] An error occurred during setup.
pause
exit /b 1

:end
echo.
pause
