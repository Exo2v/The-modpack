@echo off
setlocal enabledelayedexpansion
title Ashenfall - WorldPainter API Automation Runner
chcp 65001 >nul

echo ===============================================================================
echo        ASHENFALL - WorldPainter JSR223 API Headless Runner
echo ===============================================================================
echo.

set SCRIPT_PATH=%~dp0..\worldpainter\ashenfall_worldpainter_setup.js
if not exist "%SCRIPT_PATH%" (
    set SCRIPT_PATH=%~dp0ashenfall_worldpainter_setup.js
)

:: 1. Search for wpscript.exe in PATH
set WPSCRIPT_BIN=
where wpscript.exe >nul 2>nul
if %ERRORLEVEL% equ 0 (
    for /f "delims=" %%I in ('where wpscript.exe') do (
        set WPSCRIPT_BIN=%%I
        goto :FOUND
    )
)

:: 2. Check Standard Installation Paths
if exist "C:\Program Files\WorldPainter\wpscript.exe" (
    set WPSCRIPT_BIN=C:\Program Files\WorldPainter\wpscript.exe
    goto :FOUND
)
if exist "%LOCALAPPDATA%\Programs\WorldPainter\wpscript.exe" (
    set WPSCRIPT_BIN=%LOCALAPPDATA%\Programs\WorldPainter\wpscript.exe
    goto :FOUND
)
if exist "C:\Program Files (x86)\WorldPainter\wpscript.exe" (
    set WPSCRIPT_BIN=C:\Program Files (x86)\WorldPainter\wpscript.exe
    goto :FOUND
)

:NOT_FOUND
echo [!] Could not locate wpscript.exe in standard directories.
echo.
echo WorldPainter is either not installed or installed in a custom location.
echo.
echo To run this automation:
echo   1. If WorldPainter is installed, open WorldPainter GUI.
echo   2. Click: Tools -^> Run script...
echo   3. Select: worldpainter\ashenfall_worldpainter_setup.js
echo.
echo Or add WorldPainter's installation directory to your Windows PATH:
echo   set PATH=%%PATH%%;C:\Program Files\WorldPainter
echo.
pause
exit /b 1

:FOUND
echo [✓] Found WorldPainter Scripting Engine:
echo     "%WPSCRIPT_BIN%"
echo.
echo [✓] Target Script:
echo     "%SCRIPT_PATH%"
echo.
echo Running headless world synthesis... Please wait...
echo -------------------------------------------------------------------------------

"%WPSCRIPT_BIN%" "%SCRIPT_PATH%"

echo -------------------------------------------------------------------------------
echo [✓] Execution complete! Check your Downloads folder for Ashenfall_Continent.world.
echo.
pause
