@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM sync_to_cloud.bat — Sync the-exile-king assets to Google Drive + GitHub
REM ============================================================
REM 1. Robocopy generated images  -> Google Drive (ArtOutput)
REM 2. Robocopy design docs       -> Google Drive (Projects/Games/Exile King/docs)
REM 3. Git commit + push          -> GitHub
REM
REM Tip: Schedule this via Task Scheduler for periodic auto-sync.
REM ============================================================

set "WORKSPACE=D:\the-exile-king"
set "COMFYUI_OUTPUT=D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile"
set "GDRIVE_ARTOUTPUT=G:\My Drive\ArtOutput\annointed-exile"
set "GDRIVE_DOCS=G:\My Drive\Projects\Games\Exile King\docs"
set "LOG=%WORKSPACE%\sync_to_cloud.log"

echo [%date% %time%] === Starting cloud sync === >> "%LOG%"

REM --- 1. Sync generated images to Google Drive ---
echo [%date% %time%] Syncing images to Google Drive (ArtOutput) >> "%LOG%"
robocopy "%COMFYUI_OUTPUT%" "%GDRIVE_ARTOUTPUT%" /MIR /FFT /R:2 /W:5 ^
  /XD "__pycache__" "node_modules" "to_review" "to_trash" "to_duplicates" "_archive_regeneration_round2" ^
  /NJH /NJS /NP /LOG+:"%LOG%"
echo [%date% %time%] Image sync done >> "%LOG%"

REM --- 2. Sync design docs to Google Drive ---
echo [%date% %time%] Syncing docs to Google Drive (Projects/Games/Exile King/docs) >> "%LOG%"

REM 2a. Root-level .md files (exclude non-doc dirs)
robocopy "%WORKSPACE%" "%GDRIVE_DOCS%" *.md /S ^
  /XD ".kilo" "command_cards" "Assets" "Packages" "ProjectSettings" "__pycache__" ".vs" "Library" "Temp" "Obj" "Build" "Builds" ^
  /NJH /NJS /NP /LOG+:"%LOG%"

REM 2b. Command cards
robocopy "%WORKSPACE%\command_cards" "%GDRIVE_DOCS%\command_cards" /S ^
  /XD "__pycache__" ^
  /NJH /NJS /NP /LOG+:"%LOG%"

REM 2c. .kilo plans + handoff glossary + config
robocopy "%WORKSPACE%\.kilo\plans" "%GDRIVE_DOCS%\.kilo\plans" /S /NJH /NJS /NP /LOG+:"%LOG%"
robocopy "%WORKSPACE%\.kilo" "%GDRIVE_DOCS%\.kilo" handoff_glossary.md kilo.jsonc /NJH /NJS /NP /LOG+:"%LOG%"

echo [%date% %time%] Doc sync done >> "%LOG%"

REM --- 3. Commit and push to GitHub ---
echo [%date% %time%] Committing to GitHub >> "%LOG%"
cd /d "%WORKSPACE%"
git add -A
git commit -m "Auto-sync: updated docs and assets" --allow-empty >> "%LOG%" 2>&1
git push >> "%LOG%" 2>&1
echo [%date% %time%] GitHub push done >> "%LOG%"

echo [%date% %time%] === Cloud sync COMPLETE ===
