# =============================================================================
# ASHENFALL - Native Windows PowerShell 1-Click Installer (Zero Python Needed)
# =============================================================================
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$zipUrl = 'https://raw.githubusercontent.com/Exo2v/The-modpack/arena/01a0e180-the-modpack/downloads/ashenfall-map1-native-release.zip'
$tmpZip = Join-Path $env:TEMP 'ashenfall_setup.zip'
$extractDir = Join-Path $env:TEMP 'ashenfall_extracted'

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host '   ASHENFALL - Native 1-Click Installer (Zero Python Needed)' -ForegroundColor Yellow
Write-Host '======================================================================' -ForegroundColor Cyan

# 1. Detect Minecraft Directory (TLauncher isolated profiles + standard vanilla)
$candidates = @(
    "$env:APPDATA\.tlauncher\legacy\Minecraft\game\home\NeoForge 1.21.1",
    "$env:APPDATA\.tlauncher\legacy\Minecraft\game",
    "$env:APPDATA\.tlauncher\legacy\Minecraft",
    "$env:APPDATA\.minecraft"
)

$mcDir = $null
foreach ($c in $candidates) {
    if (Test-Path "$c\saves") {
        $mcDir = $c
        break
    }
}

if (-not $mcDir) {
    $mcDir = "$env:APPDATA\.minecraft"
    New-Item -ItemType Directory -Path "$mcDir\saves" -Force | Out-Null
}

$worldDir = Join-Path $mcDir 'saves\Ashenfall'

Write-Host 'Target Minecraft Directory: ' -NoNewline -ForegroundColor Gray
Write-Host $mcDir -ForegroundColor Cyan
Write-Host 'Target World Save Folder:   ' -NoNewline -ForegroundColor Gray
Write-Host $worldDir -ForegroundColor Cyan

# 2. Download Master Bundle
Write-Host 'Downloading Ashenfall master bundle...' -NoNewline -ForegroundColor Yellow
$wc = New-Object System.Net.WebClient
$wc.DownloadFile($zipUrl, $tmpZip)
Write-Host ' Done.' -ForegroundColor Green

# 3. Clean any old synthetic chunks
$regionDir = Join-Path $worldDir 'region'
if (Test-Path $regionDir) {
    Write-Host 'Purging stale synthetic chunks...' -ForegroundColor Yellow
    Remove-Item -Recurse -Force $regionDir -ErrorAction SilentlyContinue
}

# 4. Extract
if (Test-Path $extractDir) {
    Remove-Item -Recurse -Force $extractDir -ErrorAction SilentlyContinue
}
Expand-Archive -Path $tmpZip -DestinationPath $extractDir -Force

# 5. Install World Save
New-Item -ItemType Directory -Path $worldDir -Force | Out-Null
$srcSave = Join-Path $extractDir 'saves\Ashenfall\*'
Copy-Item -Path $srcSave -Destination $worldDir -Recurse -Force
Write-Host '[OK] Installed clean Ashenfall world save and data2 worldgen!' -ForegroundColor Green

# 6. Install KubeJS Wayfinder Script
$kubejsDir = Join-Path $mcDir 'kubejs\server_scripts'
New-Item -ItemType Directory -Path $kubejsDir -Force | Out-Null
$srcScript = Join-Path $extractDir 'kubejs\server_scripts\wayfinder_compass.js'
if (Test-Path $srcScript) {
    Copy-Item -Path $srcScript -Destination $kubejsDir -Force
    Write-Host '[OK] Installed Wayfinder Compass script into KubeJS!' -ForegroundColor Green
}

# 7. Cleanup
Remove-Item -Force $tmpZip -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $extractDir -ErrorAction SilentlyContinue

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host ' [OK] SETUP COMPLETE - 100% READY TO PLAY!' -ForegroundColor Green
Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host ' HOW TO PLAY:'
Write-Host '  1. Launch Minecraft 1.21.1 NeoForge.'
Write-Host '  2. Select Ashenfall - The Broken Realm in Singleplayer.'
Write-Host '  3. Right-click your Wayfinder Compass to teleport to the 5 nations:'
Write-Host '     [1] The Forgotten Coast   (0, 68, 2500)      [Spawn Bluffs]'
Write-Host '     [2] The Cogwork March     (-2000, 85, 0)     [River Canyons and Badlands]'
Write-Host '     [3] The Ashen Caldera     (0, 80, 0)         [Volcanic Crater and Basalt]'
Write-Host '     [4] The Glacial Spine     (0, 160, -2500)    [Alpine Peaks, Y=160+]'
Write-Host '     [5] The Gilded Dunes      (2500, 75, 0)      [Amber Desert Sand Sea]'
Write-Host '======================================================================'
