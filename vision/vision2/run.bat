@echo off
setlocal EnableDelayedExpansion
title Building Sketch — ArUco + MediaPipe

set "ROOT=%~dp0"
set "VENV=%ROOT%.venv"
set "PY=%VENV%\Scripts\python.exe"
set "PIP=%VENV%\Scripts\pip.exe"

:: MX Brio is always index 1 on this machine (index 0 = built-in, index 2 = virtual)
if not defined CAM_INDEX set "CAM_INDEX=1"

echo.
echo  ============================================================
echo   Building Sketch  ^|  ArUco Working Plane + Hand Gestures
echo  ============================================================
echo.

:: ── 1. Check Python is on PATH ──────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found on PATH.
    echo          Download from https://www.python.org/downloads/
    echo          Make sure to tick "Add Python to PATH" during install.
    goto :fail
)

:: Check version is 3.8 – 3.12 (mediapipe requirement)
for /f "tokens=2 delims= " %%V in ('python --version 2^>^&1') do set "PYVER=%%V"
for /f "tokens=1,2 delims=." %%A in ("!PYVER!") do (
    set "PYMAJ=%%A"
    set "PYMIN=%%B"
)
if !PYMAJ! LSS 3 (
    echo  [ERROR] Python 3.8 or newer required ^(found !PYVER!^).
    goto :fail
)
if !PYMAJ! EQU 3 if !PYMIN! LSS 8 (
    echo  [ERROR] Python 3.8 or newer required ^(found !PYVER!^).
    goto :fail
)
echo  [OK] Python !PYVER! detected.

:: ── 2. Create virtual environment (first run only) ──────────────────────────
if not exist "%VENV%\Scripts\activate.bat" (
    echo  [SETUP] Creating virtual environment...
    python -m venv "%VENV%"
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment.
        goto :fail
    )
    echo  [OK] Virtual environment created.
) else (
    echo  [OK] Virtual environment found.
)

:: ── 3. Install / sync dependencies ──────────────────────────────────────────
echo.
echo  [SETUP] Checking dependencies...

"%PIP%" install --upgrade pip --quiet --no-warn-script-location

:: Track whether anything was actually installed
"%PIP%" install -r "%ROOT%requirements.txt" --quiet --no-warn-script-location
if errorlevel 1 (
    echo.
    echo  [ERROR] Dependency installation failed.
    echo          Try running this manually for details:
    echo            "%PIP%" install -r "%ROOT%requirements.txt"
    goto :fail
)
echo  [OK] All dependencies ready.
echo.

:: ── 4. Verify key imports before launching ──────────────────────────────────
"%PY%" -c "import cv2, mediapipe, numpy; print(' [OK] cv2', cv2.__version__, '| mediapipe', mediapipe.__version__, '| numpy', numpy.__version__)"
if errorlevel 1 (
    echo  [ERROR] Import check failed — see message above.
    goto :fail
)

:: ── 5. Launch ────────────────────────────────────────────────────────────────
echo.
echo  NOTE: First run downloads a ~8 MB hand-landmark model (one-time).
echo.
echo  Controls:
echo    Index finger  ^(hold 3s^)  — place footprint point
echo    Peace sign    ^(hold 3s^)  — add window to nearest wall
echo    Fist          ^(~4s^)      — undo last action
echo    Fist          ^(~5s^)      — reset working plane
echo    P             — toggle top-down plane view
echo    Q             — quit
echo.
echo  ─────────────────────────────────────────────────────────────
echo   Starting...  ^(close the OpenCV windows or press Q to exit^)
echo  ─────────────────────────────────────────────────────────────
echo.

"%PY%" "%ROOT%main.py"

echo.
echo  [DONE] Session ended.
goto :end

:fail
echo.
echo  Press any key to close...
pause >nul
exit /b 1

:end
echo  Press any key to close...
pause >nul
exit /b 0
