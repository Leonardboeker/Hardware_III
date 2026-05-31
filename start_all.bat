@echo off
REM Hardware III - all-in-one launcher.
REM
REM Starts:
REM   1. Vision script (vision2/main.py) in its own window
REM   2. Orchestrator in the current window (foreground - so you see its logs)
REM
REM Both talk to TouchDesigner via local OSC.
REM
REM Stop both with: Ctrl+C in this window (orchestrator) + close the Vision window
REM Or: close BOTH windows.

REM ==== EDIT THESE IF NEEDED ====
set HW3_SERIAL_PORT=COM4
set HW3_SERIAL_BAUD=115200
set HW3_VISION_OSC_PORT=7000
set HW3_TD_OSC_HOST=127.0.0.1
set HW3_TD_OSC_PORT=7001
set HW3_LOG_LEVEL=INFO
set HW3_RFID_PRIORITY=1

set VISION_DIR=C:\Users\leona\Downloads\vision2
set VISION_CAM_INDEX=0
REM ===============================

REM ----- Sanity check vision folder + venv -----
if not exist "%VISION_DIR%\main.py" (
    echo [ERROR] Vision folder not found: %VISION_DIR%
    pause
    exit /b 1
)
if not exist "%VISION_DIR%\.venv\Scripts\python.exe" (
    echo [ERROR] Vision venv not found. Run:  cd %VISION_DIR% ^&^& python -m venv .venv ^&^& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

REM ----- Spawn vision in its OWN window so you can see its logs -----
echo [start_all] launching vision (cam index %VISION_CAM_INDEX%) in new window...
start "HW3 Vision" cmd /k "cd /d %VISION_DIR% && .\.venv\Scripts\python.exe main.py --cam-index %VISION_CAM_INDEX% --td-host 127.0.0.1"

REM ----- Brief pause so vision starts first (so heartbeat shows up before orchestrator boots) -----
timeout /t 2 /nobreak >nul

REM ----- Orchestrator in THIS window (foreground) -----
echo [start_all] launching orchestrator (foreground)...
cd /d %~dp0
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

python -m orchestrator.main

REM ----- When orchestrator exits, kill vision too -----
echo [start_all] orchestrator exited. Closing vision window...
taskkill /FI "WINDOWTITLE eq HW3 Vision*" /F /T >nul 2>&1
