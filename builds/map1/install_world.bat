@echo off
setlocal enabledelayedexpansion
title Ashenfall World Installer
cls
echo =======================================================================
echo         ASHENFALL - Handcrafted World Save Installer
echo =======================================================================
echo.

:: Test Python availability
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python "%~dp0install_world.py" %*
    goto :end
)

py --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py "%~dp0install_world.py" %*
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
