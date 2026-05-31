@echo off
REM Hardware III orchestrator launcher.
REM
REM Run this from the repo root or pass --cwd to point at it.
REM Adjust env vars below if your Serial port or vision laptop differ.

REM ==== EDIT THESE IF NEEDED ====
set HW3_SERIAL_PORT=COM4
set HW3_SERIAL_BAUD=115200
set HW3_VISION_OSC_PORT=7000
set HW3_TD_OSC_HOST=127.0.0.1
set HW3_TD_OSC_PORT=7001
set HW3_LOG_LEVEL=INFO
set HW3_RFID_PRIORITY=1
REM ===============================

cd /d %~dp0..

REM Activate a venv if one exists at .venv/, otherwise rely on system Python
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

python -m orchestrator.main
