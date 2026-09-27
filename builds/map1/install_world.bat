@echo off
setlocal enabledelayedexpansion
title Ashenfall World Installer
cls
echo =======================================================================
echo         ASHENFALL - Handcrafted World Save Installer
echo =======================================================================
echo.

set SCRIPT_NAME=build_world.py
if not exist "%~dp0build_world.py" (
    if exist "%~dp0install_world.py" (
        set SCRIPT_NAME=install_world.py
    )
)

:: Test Python availability
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python "%~dp0!SCRIPT_NAME!" %*
    goto :end
)

py --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py "%~dp0!SCRIPT_NAME!" %*
    goto :end
)

echo [!] ERROR: Python 3 was not detected on your system.
echo Please install Python 3 from https://www.python.org/ or the Microsoft Store.
echo Make sure to check the box: "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:end
echo.
pause
