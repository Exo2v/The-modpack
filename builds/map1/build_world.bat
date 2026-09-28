@echo off
setlocal enabledelayedexpansion
title Ashenfall 1-Click World Installer
cls
echo =======================================================================
echo         ⚔ ASHENFALL - 1-Click World & Worldgen Installer ⚔
echo =======================================================================
echo.

:: 1. Check if Python is available and working
python -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Running with Python...
    python "%~dp0build_world.py" %*
    goto :end
)

py -c "import sys; sys.exit(0)" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Running with py launcher...
    py "%~dp0build_world.py" %*
    goto :end
)

:: 2. Python is NOT installed -> Run Native PowerShell Installer (Zero Python Needed!)
echo [*] Python not detected. Running native Windows PowerShell installer...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "$zipUrl = 'https://raw.githubusercontent.com/Exo2v/The-modpack/arena/01a0e180-the-modpack/downloads/ashenfall-map1-native-release.zip'; " ^
    "$tmpZip = \"$env:TEMP\ashenfall_setup.zip\"; " ^
    "$extractDir = \"$env:TEMP\ashenfall_extracted\"; " ^
    "$candidates = @( " ^
    "    \"$env:APPDATA\.tlauncher\legacy\Minecraft\game\home\NeoForge 1.21.1\", " ^
    "    \"$env:APPDATA\.tlauncher\legacy\Minecraft\game\", " ^
    "    \"$env:APPDATA\.tlauncher\legacy\Minecraft\", " ^
    "    \"$env:APPDATA\.minecraft\" " ^
    "); " ^
    "$mcDir = $null; " ^
    "foreach ($c in $candidates) { if (Test-Path \"$c\saves\") { $mcDir = $c; break } }; " ^
    "if (-not $mcDir) { $mcDir = \"$env:APPDATA\.minecraft\"; New-Item -ItemType Directory -Path \"$mcDir\saves\" -Force | Out-Null }; " ^
    "$worldDir = \"$mcDir\saves\Ashenfall\"; " ^
    "Write-Host 'Target Minecraft Directory: ' -NoNewline -ForegroundColor Gray; Write-Host $mcDir -ForegroundColor Cyan; " ^
    "Write-Host 'Target World Save Folder:   ' -NoNewline -ForegroundColor Gray; Write-Host $worldDir -ForegroundColor Cyan; " ^
    "Write-Host 'Downloading Ashenfall master bundle...' -NoNewline -ForegroundColor Yellow; " ^
    "(New-Object System.Net.WebClient).DownloadFile($zipUrl, $tmpZip); " ^
    "Write-Host ' Done.' -ForegroundColor Green; " ^
    "if (Test-Path \"$worldDir\region\") { Remove-Item -Recurse -Force \"$worldDir\region\" -ErrorAction SilentlyContinue }; " ^
    "if (Test-Path $extractDir) { Remove-Item -Recurse -Force $extractDir -ErrorAction SilentlyContinue }; " ^
    "Expand-Archive -Path $tmpZip -DestinationPath $extractDir -Force; " ^
    "New-Item -ItemType Directory -Path $worldDir -Force | Out-Null; " ^
    "Copy-Item -Path \"$extractDir\saves\Ashenfall\*\" -Destination $worldDir -Recurse -Force; " ^
    "Write-Host '[✓] World save and data2 worldgen installed successfully!' -ForegroundColor Green; " ^
    "$kubejsDir = \"$mcDir\kubejs\server_scripts\"; " ^
    "New-Item -ItemType Directory -Path $kubejsDir -Force | Out-Null; " ^
    "if (Test-Path \"$extractDir\kubejs\server_scripts\wayfinder_compass.js\") { " ^
    "    Copy-Item -Path \"$extractDir\kubejs\server_scripts\wayfinder_compass.js\" -Destination $kubejsDir -Force; " ^
    "    Write-Host '[✓] Wayfinder Compass script installed!' -ForegroundColor Green; " ^
    "}; " ^
    "Remove-Item -Force $tmpZip -ErrorAction SilentlyContinue; " ^
    "Remove-Item -Recurse -Force $extractDir -ErrorAction SilentlyContinue; " ^
    "Write-Host '`n[✓] SETUP COMPLETE — READY TO PLAY!' -ForegroundColor Green"

if %ERRORLEVEL% equ 0 goto :end

echo.
echo [!] An error occurred during setup.
pause
exit /b 1

:end
echo.
pause
