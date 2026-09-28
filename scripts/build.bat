@echo off
rem ASHENFALL build runner wrapper for Windows
setlocal

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -3 "%~dp0tools\build.py" %*
    exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%~dp0tools\build.py" %*
    exit /b %ERRORLEVEL%
)

echo Error: Python 3.11+ is required to build Ashenfall.
exit /b 1
