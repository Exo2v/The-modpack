@echo off
setlocal enabledelayedexpansion
title Ashenfall Modpack - Combined Phase M3 & M3b Installer

echo =================================================================
echo   ASHENFALL MODPACK -- Combined Phase M3 & M3b Installer
echo   World Generation, Landmarks, Ecology, Storage & Fullness
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

echo Starting combined Phase M3 & M3b installation...
echo Preserving existing Phase M0, M1 & M2 mods,
echo and installing Terralith, Explorify, Dungeons & Taverns, Towns & Towers,
echo Sophisticated Backpacks, FallingTree, Guard Villagers, Farmer's Delight,
echo Supplementaries, Comforts, and Tool Belt.
echo.

%PYTHON_CMD% "%~dp0download_mods.py" --phase M3+M3b %*

echo.
pause
