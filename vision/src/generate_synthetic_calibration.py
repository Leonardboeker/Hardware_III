"""Generate synthetic calibration YAMLs for hardware-blocked fallback.

Run ONLY if Plan 02-05 physical calibration is blocked (see contingency in Plan 02-07).
Files are labeled SYNTHETIC — DO NOT USE IN FINAL DEMO.

Usage:
    python -m vision.src.generate_synthetic_calibration

Outputs:
    vision/calibration/synthetic_intrinsics.yml
    vision/calibration/synthetic_homography.yml
    vision/calibration/SYNTHETIC-FALLBACK.md
"""
from __future__ import annotations

import datetime
from pathlib import Path

import numpy as np
import yaml

CALIBRATION_DIR = Path("vision/calibration")

# Typical Logitech C920 @ 1920×1080
SYNTHETIC_INTRINSICS = {
    "calibrated_by": "SYNTHETIC",
    "mounting_notes": "SYNTHETIC FALLBACK — DO NOT SHIP DEMO WITH THIS FILE",
    "camera_model": "Logitech C920 (estimated)",
    "resolution": [1920, 1080],
    "camera_matrix": [
        [1450.0, 0.0, 960.0],
        [0.0, 1450.0, 540.0],
        [0.0, 0.0, 1.0],
    ],
    "dist_coeffs": [-0.1, 0.05, 0.0, 0.0, 0.0],
}

# Typical 1280×720 projector, camera centered above table
# Identity-ish homography with scale to map camera FOV to projector FOV
SYNTHETIC_HOMOGRAPHY = {
    "calibrated_by": "SYNTHETIC",
    "mounting_notes": "SYNTHETIC FALLBACK — DO NOT SHIP DEMO WITH THIS FILE",
    "projector_resolution": [1280, 720],
    "camera_resolution": [1920, 1080],
    "homography": [
        [0.667, 0.0, 0.0],
        [0.0, 0.667, 0.0],
        [0.0, 0.0, 1.0],
    ],
}

FALLBACK_NOTE = f"""# SYNTHETIC CALIBRATION FALLBACK

Generated: {datetime.date.today().isoformat()}

These files are PLACEHOLDER calibration data for software development only.
They use estimated parameters for a Logitech C920 camera and a 1280x720 projector.

## DO NOT use these files for any actual demo or test with physical hardware.

## When to delete:
Phase 2.5 catch-up: re-run Plan 02-05 with real hardware, regenerate real YAMLs,
then delete `synthetic_intrinsics.yml`, `synthetic_homography.yml`, and this file.
Phase 3 is BLOCKED until real calibration files replace these.

## Files:
- `synthetic_intrinsics.yml` — fake camera intrinsics
- `synthetic_homography.yml` — fake camera→projector homography
"""


def main():
    CALIBRATION_DIR.mkdir(parents=True, exist_ok=True)

    intrinsics_path = CALIBRATION_DIR / "synthetic_intrinsics.yml"
    homography_path = CALIBRATION_DIR / "synthetic_homography.yml"
    note_path = CALIBRATION_DIR / "SYNTHETIC-FALLBACK.md"

    with open(intrinsics_path, "w") as f:
        yaml.dump(SYNTHETIC_INTRINSICS, f, default_flow_style=False)

    with open(homography_path, "w") as f:
        yaml.dump(SYNTHETIC_HOMOGRAPHY, f, default_flow_style=False)

    note_path.write_text(FALLBACK_NOTE)

    print(f"[OK] {intrinsics_path}")
    print(f"[OK] {homography_path}")
    print(f"[OK] {note_path}")
    print("\n[WARN] These are SYNTHETIC — re-run Plan 02-05 with real hardware before Phase 3.")


if __name__ == "__main__":
    main()
