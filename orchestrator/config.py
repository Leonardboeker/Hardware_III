"""Configuration constants. Override via environment variables for portability."""
from __future__ import annotations

import os
from pathlib import Path


# ----- Repo paths -----
REPO_ROOT = Path(__file__).resolve().parent.parent
METHODS_DB_PATH = REPO_ROOT / "data" / "methods_db.json"


# ----- Serial (ESP32) -----
SERIAL_PORT = os.environ.get("HW3_SERIAL_PORT", "COM4")
SERIAL_BAUD = int(os.environ.get("HW3_SERIAL_BAUD", "115200"))
SERIAL_RECONNECT_S = float(os.environ.get("HW3_SERIAL_RECONNECT_S", "2.0"))


# ----- Vision OSC (incoming from Elias's main.py) -----
VISION_OSC_HOST = os.environ.get("HW3_VISION_OSC_HOST", "0.0.0.0")
VISION_OSC_PORT = int(os.environ.get("HW3_VISION_OSC_PORT", "7000"))


# ----- TouchDesigner OSC (outgoing — TD listens here) -----
TD_OSC_HOST = os.environ.get("HW3_TD_OSC_HOST", "127.0.0.1")
TD_OSC_PORT = int(os.environ.get("HW3_TD_OSC_PORT", "7001"))


# ----- Orchestrator tick rate -----
TICK_HZ = float(os.environ.get("HW3_TICK_HZ", "30"))
TICK_DT = 1.0 / TICK_HZ


# ----- Slider B Manual-Override settings (matches firmware/TD defaults) -----
PHASE_OVERRIDE_S = float(os.environ.get("HW3_PHASE_OVERRIDE_S", "10.0"))
PHASE_OVERRIDE_THRESHOLD = float(os.environ.get("HW3_PHASE_OVERRIDE_THRESHOLD", "0.05"))
PHASE_HYST_EPSILON = float(os.environ.get("HW3_PHASE_HYST_EPSILON", "0.02"))


# ----- Heartbeat staleness -----
HB_TIMEOUT_S = float(os.environ.get("HW3_HB_TIMEOUT_S", "3.0"))
SLIDER_TIMEOUT_S = float(os.environ.get("HW3_SLIDER_TIMEOUT_S", "2.0"))


# ----- Logging -----
LOG_LEVEL = os.environ.get("HW3_LOG_LEVEL", "INFO")
