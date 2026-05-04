# Tolerance Specification

**Status:** PLACEHOLDER — fill in after running Plan 02-05 calibration rig

---

## How to measure jitter

1. Fix one ArUco puck on the table without moving it.
2. Run the Python pipeline for 300 frames:
   ```bash
   python -m vision.src.run_vertical_slice --dry-run --puck-id 0 --target-x 0 --target-y 0
   ```
   (target coords don't matter here — we're measuring detection scatter)
3. Log the `projector_xy` values from each frame. Compute standard deviation in X and Y.
4. `JITTER_STD_PX` = max(std_x, std_y)
5. Set `TOLERANCE_PX` = 3 × JITTER_STD_PX (3-sigma rule)

---

## Measured Values (fill in after calibration)

```
JITTER_STD_PX: TBD      # measured std deviation of static puck position
TOLERANCE_PX:  TBD      # = 3 × JITTER_STD_PX, used in osc_send.py
CAMERA_DEVICE: TBD      # e.g. Logitech C920
PROJECTOR_RES: TBD      # e.g. 1280x720
MOUNT_HEIGHT_CM: TBD    # camera height above table
MEASUREMENT_DATE: TBD
MEASURED_BY: TBD
```

---

## Tolerance loader (used by osc_send.py)

`vision/calibration/tolerance_loader.py` must export `get_tolerance() -> float`.
Until real values are available, it returns the fallback below.

---

## Fallback value

**`TOLERANCE_FALLBACK_PX = 30`**

This is a conservative estimate for a 1280×720 projector at ~1.5m table width.
A puck is roughly 5–8cm across; at typical setups that's ~30–50 projector pixels.
Using 30px as the fallback keeps false-positives low until real jitter is measured.

---

## Notes

- Tolerance is in **projector pixels**, not camera pixels.
- If detection is too strict (user can't trigger VALID): increase TOLERANCE_PX.
- If false-positives appear (VALID fires when puck is wrong): decrease TOLERANCE_PX.
- Re-measure whenever the camera mount or projector position changes.
