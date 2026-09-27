@echo off
setlocal enabledelayedexpansion
title Ashenfall Modpack - Combined Phase M1 & M2 Installer

echo =================================================================
echo   ASHENFALL MODPACK -- Combined Phase M1 & M2 Installer
echo   Movement, Vanilla PvP Combat & Soulslike Difficulty
echo   Target: Minecraft 1.21.1 NeoForge
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

echo Starting combined Phase M1 & M2 installation...
echo Preserving Phase M0, ensuring pure Vanilla PvP mechanics,
echo and installing Combat Roll, ParCool, Simply Swords, and Power Scale.
echo.

%PYTHON_CMD% "%~dp0download_mods.py" --phase M1+M2 %*

echo.
pause
