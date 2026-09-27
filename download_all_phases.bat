@echo off
setlocal enabledelayedexpansion
title Ashenfall Modpack - 1-Click Complete Modpack Installer

echo =================================================================
echo   ASHENFALL MODPACK -- Complete 1-Click Installer
echo   Minecraft 1.21.1 NeoForge (Pure Vanilla PvP Mechanics)
echo =================================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python 3 was not found in your system PATH!
        echo.
        echo Please install Python 3 from https://www.python.org/downloads/
        echo IMPORTANT: Check the box "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo Starting complete Ashenfall installation (All Phases)...
echo Existing mods will be checked and verified as up-to-date.
echo Pure Vanilla PvP mechanics are preserved (no Better Combat).
echo.

%PYTHON_CMD% "%~dp0download_mods.py" --phase all %*

echo.
pause
