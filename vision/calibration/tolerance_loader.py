"""Load tolerance value from TOLERANCE.md or return fallback.

Used by vision/src/osc_send.py. Replace TOLERANCE_PX with the measured value
from TOLERANCE.md once calibration is complete.
"""
import os

TOLERANCE_FALLBACK_PX = 30.0


def get_tolerance() -> float:
    env_val = os.environ.get("ARUCO_TOLERANCE_PX")
    if env_val:
        return float(env_val)
    return TOLERANCE_FALLBACK_PX
