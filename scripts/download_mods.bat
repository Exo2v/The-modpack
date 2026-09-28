@echo off
setlocal enabledelayedexpansion
title Ashenfall Modpack - Complete Direct Mod Downloader

echo =================================================================
echo   ASHENFALL MODPACK -- Complete Direct Mod Downloader
echo   Minecraft 1.21.1 NeoForge (Vanilla PvP Mechanics)
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
    echo   [1] Complete Full Modpack -- All Phases (Recommended) [DEFAULT]
    echo   [2] Remaining Phases Only (M3c through M7: Magic, Dungeons, Bosses, RPG)
    echo   [3] Phase M3 + M3b (Worldgen, Structures, Fullness)
    echo   [4] Phase M1 + M2 (Movement, Vanilla PvP, Simply Swords, Soulslike)
    echo   [0] Phase M0 Only (Skeleton & Performance Engine -- 24 mods)
    echo.
    set /p CHOICE="Enter choice [1/2/3/4/0] (Press Enter for Full Modpack): "
    if "!CHOICE!"=="2" (
        set PHASE=remaining
    ) else if "!CHOICE!"=="3" (
        set PHASE=M3+M3b
    ) else if "!CHOICE!"=="4" (
        set PHASE=M1+M2
    ) else if "!CHOICE!"=="0" (
        set PHASE=M0
    ) else (
        set PHASE=all
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
