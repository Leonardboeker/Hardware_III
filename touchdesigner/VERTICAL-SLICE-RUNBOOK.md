# Vertical Slice Runbook — Phase 2

One-puck closed-loop CV demo. Run this before Phase 3 to prove the pipeline works end-to-end.

---

## Prerequisites

```
pip install opencv-contrib-python python-osc pyyaml numpy
```

TouchDesigner build: **2025.32050** (pin this — do not upgrade mid-project)

---

## Hardware Setup

1. Mount webcam overhead, pointing straight down at the table.
2. Connect projector, set resolution to **1280×720** (or match your actual unit).
3. Print or 3D-print one ArUco puck using **DICT_4X4_50, ID=0**.
4. Have real calibration files ready in `vision/calibration/`:
   - `camera_intrinsics.yml` — from Plan 02-05 (checkerboard calibration)
   - `homography.yml` — from Plan 02-05 (camera-to-projector mapping)
   - If not ready yet: use `--dry-run` flag (synthetic YAMLs, not for demo).

---

## Step 1: Determine target zone

Open TD, run `vertical-slice.toe`, and note the projector-pixel coordinates of the target zone you want the puck to land in. Example: `640 400` (center of a 1280×720 projector).

---

## Step 2: Start the Python vision pipeline

From the project root:

```bash
python -m vision.src.run_vertical_slice \
    --camera 0 \
    --intrinsics vision/calibration/camera_intrinsics.yml \
    --homography vision/calibration/homography.yml \
    --td-host 127.0.0.1 \
    --td-port 7000 \
    --puck-id 0 \
    --target-x 640 --target-y 400
```

With synthetic calibration (no hardware yet):
```bash
python -m vision.src.run_vertical_slice --dry-run --puck-id 0 --target-x 640 --target-y 400
```

A preview window opens showing the camera feed with detected puck positions overlaid.

---

## Step 3: Build the TouchDesigner node graph

Open TouchDesigner and build `touchdesigner/vertical-slice.toe` with this network:

```
[OSC In CHOP]  port=7000, UDP
     │
     ▼
[DAT Execute]  ← script: touchdesigner/scripts/osc_handler.py
               fires onReceiveOSC() for each incoming message
               stores puck data into parent() storage

[Script CHOP]  ← script: touchdesigner/scripts/fsm_vertical_slice.py
               cook() runs every frame
               outputs: fsm_state (int), visual_state (int)
     │
     ▼
[Select CHOP]  channel: visual_state
     │
     ▼
[Switch TOP]   input 0=DISCONNECTED, 1=PENDING, 2=INVALID, 3=VALID
               (each input is a TOP branch per ERROR-FEEDBACK-SPEC.md)
     │
     ▼
[Window COMP]  fullscreen on projector output
```

**Storage node:** Use a `Base COMP` named `storage` at the root. All `parent().store/fetch` calls target this.

---

## Step 4: Set output channels on the Script CHOP

In the Script CHOP's `setupParameters` callback (or the `info` DAT), declare these channels:
```python
scriptOp.appendChan('fsm_state')
scriptOp.appendChan('visual_state')
```

---

## Step 5: Test the four visual states

| Test | How | Expected |
|------|-----|----------|
| DISCONNECTED | Kill the Python script | Dotted outline, pulsing |
| PENDING | Put puck on table, away from target zone | Solid white outline at target |
| INVALID | Move puck close to but outside target | Red halo on puck + cyan ghost at target |
| VALID | Place puck inside target zone | Green expanding ring |
| CONFIRMED | Hold puck in zone for ≥5 frames | `fsm_state` flips to 1, stays green |

---

## Step 6: Record the demo video

Use OBS or any screen recorder. Required deliverable: `deliverables/vertical-slice-demo.mp4`
- Duration: 30 seconds minimum
- Show: puck outside zone → INVALID → move to zone → VALID → CONFIRMED
- Record the camera preview window AND the projector output side-by-side if possible

---

## Latency measurement

The Python pipeline prints avg/max latency at exit. To measure end-to-end (including TD render):
- Film with a high-speed phone camera (240fps)
- Move puck rapidly and count frames between physical puck entering zone and projection changing color
- Target: < 150 ms (= < 36 frames at 240fps)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No OSC data in TD | Check port 7000 is not blocked by firewall; confirm `--td-port` matches OSC In CHOP port |
| Puck not detected | Check ARUCO_DICT_NAME matches `cad/PUCK-SPEC.md`; increase camera exposure |
| High false-positive rate | Reduce ambient light; cover projector hotspots; tighten `minMarkerPerimeterRate` |
| Ghost at wrong position | Re-run calibration (Plan 02-05); verify homography.yml was generated for current camera mount |
| `in_target` always 0 | Check `--target-x/y` match actual projector-pixel target zone; recalibrate tolerance in `TOLERANCE.md` |

---

## Files

| File | Purpose |
|------|---------|
| `vision/src/aruco_detect.py` | CV core — detect pucks, map to projector coords |
| `vision/src/osc_send.py` | OSC sender |
| `vision/src/run_vertical_slice.py` | CLI entry point |
| `vision/calibration/camera_intrinsics.yml` | Camera intrinsics (from Plan 02-05) |
| `vision/calibration/homography.yml` | Camera→projector homography (from Plan 02-05) |
| `vision/calibration/TOLERANCE.md` | Tolerance value + jitter measurements |
| `touchdesigner/scripts/osc_handler.py` | TD Script DAT — parses OSC, writes storage |
| `touchdesigner/scripts/fsm_vertical_slice.py` | TD Script CHOP — 2-state FSM |
| `touchdesigner/ERROR-FEEDBACK-SPEC.md` | Visual state spec |
| `touchdesigner/vertical-slice.toe` | TD project (binary — build from this runbook) |
