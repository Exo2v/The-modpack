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

if "%~1"=="" (
    echo Select phase to install:
    echo   [1] Combined Phase M1 + M2 (Movement, Vanilla PvP, Simply Swords & Soulslike) [DEFAULT]
    echo   [0] Phase M0 Only (Skeleton & Performance Engine -- 24 mods)
    echo   [A] All Phases
    echo.
    set /p CHOICE="Enter choice [1/0/A] (Press Enter for Combined M1+M2): "
    if "!CHOICE!"=="0" (
        set PHASE=M0
    ) else if "!CHOICE!"=="a" (
        set PHASE=all
    ) else if "!CHOICE!"=="A" (
        set PHASE=all
    ) else (
        set PHASE=M1+M2
    )
) else (
    goto run_custom
)

echo.
echo Running installer for Phase !PHASE!...
echo.
%PYTHON_CMD% "%~dp0download_mods.py" --phase !PHASE!
goto finish

:run_custom
%PYTHON_CMD% "%~dp0download_mods.py" %*

:finish
echo.
pause
