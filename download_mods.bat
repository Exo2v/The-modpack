@echo off
setlocal enabledelayedexpansion
title Ashenfall Modpack - Direct Mod Downloader

echo =================================================================
echo   ASHENFALL MODPACK -- Direct Mod Downloader
echo   Minecraft 1.21.1 NeoForge
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

echo Using Python command: !PYTHON_CMD!
echo Starting mod download...
echo.

%PYTHON_CMD% "%~dp0download_mods.py" --phase M0 %*

echo.
pause
