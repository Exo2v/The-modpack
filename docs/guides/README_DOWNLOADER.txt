=================================================================
 ASHENFALL — DIRECT MOD DOWNLOADER (Phase M0)
 Target: Minecraft 1.21.1 · NeoForge 21.1.x
=================================================================

QUICK START (Windows):
1. Make sure Python 3 is installed (https://www.python.org/downloads/)
   and "Add Python to PATH" was checked during install.
2. Double-click "download_mods.bat".
3. The script will:
   - Automatically detect your TLauncher / Minecraft mods folder:
     C:\Users\<YourUser>\AppData\Roaming\.tlauncher\legacy\Minecraft\game\home\NeoForge 1.21.1\mods
   - Clean any corrupted or non-JAR files (preventing "zip END header not found").
   - Download the verified 1.21.1 NeoForge mod JARs directly from Modrinth.
   - Verify every file's ZIP integrity before saving.
4. Launch Minecraft 1.21.1 NeoForge and enjoy!

MANUAL / COMMAND LINE:
Run in Command Prompt or PowerShell:
  python download_mods.py --phase M0

Custom destination folder:
  python download_mods.py --phase M0 --dest "C:\path\to\your\mods"
