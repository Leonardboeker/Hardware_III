# vision/

Camera input, ArUco marker detection, distance/area calculations. Either runs standalone in Python and pipes to TouchDesigner, OR lives inside a TD Script CHOP — TBD by the vision owner.

## Scope

- Overhead camera capture
- ArUco marker detection (OpenCV `cv2.aruco`)
- Distance + area math: 10 footprint pucks → polygon → square meters
- Optional: YOLO for the 3D-printed method models (if RFID approach is dropped)
- Send results to TouchDesigner (OSC suggested)

## Suggested layout

```
vision/
├── pyproject.toml or requirements.txt
├── src/
│   ├── capture.py
│   ├── aruco_detect.py
│   ├── footprint.py        # polygon + area calc
│   └── osc_send.py
├── calibration/
│   └── camera_intrinsics.yml   # do the calibration once, commit the result
└── tests/
```

## Conventions

- Pin OpenCV + numpy versions. Vision code breaks subtly across versions.
- Camera intrinsics live in `calibration/` — anyone running the system needs them.
- Don't commit raw camera footage. Sample frames for debugging are fine.
