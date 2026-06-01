# vision/

> **⚠️ Note:** The production vision pipeline now lives **outside this repo** at
> `C:\Users\leona\Downloads\vision2\` (Onur's branch, cloned locally for the
> single-laptop demo setup). This folder contains the earlier vertical-slice
> work from Phase 2, kept for reference.

## Where the current vision actually runs

`C:\Users\leona\Downloads\vision2\main.py` — runs on Leo's laptop, the SAME
machine as the orchestrator + TouchDesigner. Single-laptop setup eliminates
cross-machine OSC issues.

Started via `start_all.bat` in the repo root:

```powershell
.\.venv\Scripts\python.exe main.py --cam-index 0 --td-host 127.0.0.1
```

OSC target: `127.0.0.1:7000` (the orchestrator's `VisionListener`).

## What this folder contains

The Phase 2 vertical-slice Python module (`src/`), camera calibration files
(`calibration/`), and a pyproject. Functional but **superseded by the vision2
external folder** which Onur maintains separately.

```
vision/
├── src/                        — Phase 2 ArUco + OSC vertical slice
│   ├── capture.py
│   ├── aruco_detect.py
│   ├── footprint.py            — polygon + area calc
│   └── osc_send.py
├── calibration/                — synthetic + real intrinsics + homography YAMLs
└── tests/
```

## OSC addresses the orchestrator listens for

| Address | Type | Notes |
|---------|------|-------|
| `/vision/heartbeat` | int | **Required** at ≥ 1 Hz. Drives `hb_alive`. |
| `/puck/<idx>` | int float float | frame, projector-x, projector-y (per ArUco / sketch point) |
| `/puck/detected` | int … | List of currently visible puck IDs |
| `/puck/lost` | int | Single puck ID that left frame |
| `/method/selected` | int | 1=MASONRY 2=3D PRINTED 3=PREFAB 4=RECLAIMED. RFID has priority. |
| `/sketch/points` `/walls` `/windows` `/is_extruded` | int | Sketch state counts |
| `/sketch/area_m2` `/sketch/perim_m` | float | Sketch geometry (orchestrator uses these directly when `hb_alive=1`) |
| `/fsm/state` | int | Vision-side FSM state ID |
| `/fsm/state_name` | string | Human-readable state name |
| `/gesture/id` `/dwell` `/action` | int float int | Hand-gesture passthrough |

The orchestrator's `vision_listener.py` parses all of these into a thread-safe
State dataclass, then `ui_state.py` builds the TD payload from it.

## Conventions

- Pin OpenCV + numpy versions. Vision code breaks subtly across versions.
- Camera intrinsics live in `calibration/`. Recalibrate when the camera mount
  changes.
- The Logitech BRIO is the current camera. Disable Logitech Options "Show
  Mode" zoom *OR* set `CAMERA_ZOOM` in `vision2/main.py` — pick one source.
- Don't commit raw camera footage. Sample frames for debugging are fine.
