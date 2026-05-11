# Hardware III — ArUco + MediaPipe Building Sketch
### Session Export · 2026-05-04 (updated)

---

## Project Context

**Course:** Hardware III — IAAC (MRAC+MAAI 2025/2026)
**Concept:** Interactive table installation. Overhead USB-C camera + projector guides physical model assembly.
**Deadline:** May 22, 2026
**Team:** 6 people

The system uses 4 ArUco markers as physical table corners to define a virtual working plane via homography. A user traces a building footprint with hand gestures detected by MediaPipe, confirms with a three-finger hold, and the footprint is extruded into a live 3D AR visualisation projected back onto the table via `cv2.solvePnP` + `cv2.projectPoints`.

---

## File Structure

```
aruco detecction/
├── main.py                   # Application entry point
├── working_plane.py          # ArUco detection + homography + corner pixel export
├── gestures.py               # MediaPipe Tasks API hand gesture detector
├── sketch.py                 # 2D footprint state (points, walls, windows)
├── extrusion.py              # 3D pose estimation, wall rendering, ModularFBX class
├── calibrate.py              # One-time camera calibration script (checkerboard)
├── detect_aruco_test.py      # Utility: test which ArUco dict matches your markers
├── generate_board_markers.py # Utility: generate marker images (unused for corners)
├── requirements.txt          # Python dependencies
├── run.bat                   # One-click launcher (Windows)
├── calibration.npz           # Saved after running calibrate.py
├── hand_landmarker.task      # Downloaded on first run (~8 MB, auto)
└── .venv/                    # Virtual environment (auto-created by run.bat)
```

---

## ArUco Marker Layout (DICT_4X4_50)

Markers are from `PRINT_A3.pdf`, printed at 100% on A3.

```
ID 0 (Top-Left)  ──────────────  ID 1 (Top-Right)
      │                                 │
      │         working plane           │
      │         900 px × 600 px         │
      │                                 │
ID 3 (Bot-Left)  ──────────────  ID 2 (Bot-Right)
```

**Building-type selector markers** (place anywhere on the table):

| ID | Type     |
|----|----------|
| 20 | Masonry  |
| 21 | 3D Print |
| 22 | Prefab   |

---

## Gesture Reference

| Gesture | Hand shape | Action | Trigger condition |
|---------|------------|--------|-------------------|
| Index only | Index up, rest folded | `place_point` | Hold ≥ 3 s inside plane; fires once per raise |
| Peace (V) | Index + middle up | `add_window` | Hold ≥ 3 s; fires once per raise |
| Three fingers | Index + middle + ring up, pinky folded | `extrude` | Hold ≥ 4 s; fires once per raise |
| Fist | All fingers folded | `undo` | Release at 4–5 s total hold |
| Fist | All fingers folded | `reset` | Release at > 5 s total hold |

**Important:** `place_point` only registers if the finger tip is inside the working plane boundary. Terminal prints `[!] Finger outside working plane` otherwise. Status bar reads `WORKING PLANE NOT DETECTED` when ArUco markers 0–3 are not visible.

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `P` | Toggle top-down working-plane debug window |
| `E` | Toggle 3D extrusion on/off manually |

---

## How Point Registration Works (full chain)

```
MediaPipe detects hand
        ↓
index_tip_cam = pixel position of landmark 8 (index tip)
        ↓
cam_to_plane(tip_cam, H)  →  tip_plane (x, y) in virtual plane coords
        ↓
is_inside_plane(tip_plane)  →  tip_valid  [0..900, 0..600]
        ↓
dwell timer reaches 3 s  →  actions.append('place_point')
        ↓
if tip_valid:
    sketch.add_point(tip_plane)   ← point actually stored here
else:
    print("[!] Finger outside working plane")
```

**Most common failure:** markers 0–3 not visible → `H` is `None` → `tip_valid` always `False`.

---

## 3D AR Extrusion Pipeline

### Physical coordinate system (world space, mm)
```
Origin  = ID-0 marker centre (Top-Left)
X-axis  = rightward toward ID-1 (Top-Right)
Y-axis  = downward toward ID-3 (Bot-Left)
Z-axis  = upward from table surface (toward camera)
```

### Full rendering chain per frame
```
detect_working_plane(frame)
    → corner_pixels (4×2 float array, TL TR BR BL pixel positions)
        ↓
estimate_pose(corner_pixels, K, dist)
    → rvec, tvec  (camera pose via cv2.solvePnP SQPNP)
        ↓
draw_walls(frame, sketch, rvec, tvec, K, dist)
    → for each wall segment A→B:
          convert plane coords → world mm  (_to_world)
          build 4-corner wall quad in 3D   [A_base, B_base, B_top, A_top]
          project to image pixels           cv2.projectPoints
          depth-sort (far→near)
          fillPoly wall + window opening
          addWeighted 65/35 blend for transparency
          polylines + top edge on top of blend
```

### Configuration (extrusion.py top of file)
```python
PHYSICAL_W_MM  = 594.0   # measure: ID0 → ID1 centre-to-centre in mm
PHYSICAL_H_MM  = 420.0   # measure: ID0 → ID3 centre-to-centre in mm
WALL_HEIGHT_MM = 80.0    # virtual wall height — tune to taste
```
**Must measure your printout and set these before the 3D mode looks correct.**

### Metric scale
The virtual plane (900 × 600 px) maps linearly to the physical marker rectangle. With the defaults above, 1 virtual px ≈ 0.66 mm (width) / 0.70 mm (height). All footprint coordinates and `WALL_HEIGHT_MM` are in mm, so the AR scale is physically grounded. Print a grid on the A3 sheet for visual user reference — the machine uses only the 4 marker corners.

---

## Camera Calibration (`calibrate.py`)

Required once before accurate 3D projection. Without it, `extrusion.py` falls back to an approximated `K` (may drift at frame edges).

### Steps
1. Print a **9×6 inner-corner checkerboard** at 100% (search "opencv checkerboard 9x6 pdf").
2. Measure one square side in mm → set `SQUARE_MM` at top of `calibrate.py`.
3. Run: `python calibrate.py`
4. Press `SPACE` to capture 15–20 frames from varied angles, distances, and rotations.
5. Press `C` to calibrate → saves `calibration.npz`.

### Quality targets
| RMS reprojection error | Assessment |
|------------------------|------------|
| < 0.5 px | Excellent |
| 0.5–1.0 px | Acceptable |
| > 1.0 px | Recapture with more varied angles |

### Output
`calibration.npz` contains arrays `K` (3×3 intrinsic matrix) and `dist` (distortion coefficients). Loaded automatically by `main.py` at startup via `load_calibration()`.

---

## Modular FBX Support (`ModularFBX` class in `extrusion.py`)

Requires `pip install trimesh` (already in `requirements.txt`).

### FBX coordinate convention expected
```
+X  = along wall length  (scaled and rotated to fit each segment)
+Z  = wall height
+Y  = wall depth / outward face
Origin at bottom-left corner of the module face
```

### Usage in main.py
```python
from extrusion import ModularFBX

mfbx = ModularFBX('wall_panel.fbx', window_fbx='wall_window.fbx')

# In draw loop (when is_extruded):
mfbx.draw(frame, sketch, rvec, tvec, K, dist)
# Replace the draw_walls() call above with this line
```

### How it works
For each wall segment A→B:
1. Compute wall length and direction angle in world mm.
2. Build a 4×4 transform: scale FBX X-axis to wall length, rotate to wall direction, translate to segment start.
3. Apply transform to all mesh vertices → world coordinates.
4. `cv2.projectPoints` → image pixels.
5. Depth-sort faces far→near, `fillConvexPoly` each face, `addWeighted` blend.

Window segments use `window_fbx` instead of `wall_fbx` if provided.

---

## PyPRT — What It Is and How It Relates

**PyPRT** (Python Procedural Runtime) is Esri's Python binding for the engine behind **CityEngine**.

| Concept | Detail |
|---------|--------|
| Input | 2D polygon (your footprint) + a CGA rule file |
| CGA | Computer Generated Architecture — a grammar language for buildings |
| Output | Full 3D mesh: walls, floors, windows, roofs, balconies |
| FBX in CGA | `insert("my_panel.fbx")` places your model at any generated face |
| SDK size | ~200 MB separate Esri PRT SDK install |

### Relevance to this project
- **Guided assembly target model** — feed the sketch footprint into PyPRT + a rule, generate a detailed 3D guide model showing what the physical model should look like, then project it onto the table.
- **Replaces `ModularFBX`** — CGA handles wall splitting, tiling, window insertion, and floor repetition automatically without manual tiling logic.
- **Not recommended for May 22 deadline** — CGA has a learning curve and PRT SDK setup takes time. Use `extrusion.py` + `ModularFBX` for the demo; revisit PyPRT for a polished version.

---

## Dependencies

```
opencv-contrib-python >= 4.7.0
mediapipe >= 0.10.0
numpy >= 1.24.0
trimesh >= 4.0.0
```

Confirmed working: `cv2 4.13.0 | mediapipe 0.10.35 | numpy 2.4.4`

---

## Key Technical Decisions

### MediaPipe 0.10.35 — Tasks API
`mp.solutions` and `mediapipe.python` were both removed/inaccessible in 0.10.35. The Tasks API is used throughout:

```python
import mediapipe as mp

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=_MODEL_PATH),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
)
landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
result   = landmarker.detect_for_video(mp_image, int(time.time() * 1000))
lm       = result.hand_landmarks[0]   # list of 21 NormalizedLandmark objects
```

Model `hand_landmarker.task` (~8 MB) auto-downloaded on first run.

### Finger-up detection
```python
_TIPS = [8, 12, 16, 20]   # index middle ring pinky tips
_PIPS = [6, 10, 14, 18]   # PIP joints

up = [lm[_TIPS[i]].y < lm[_PIPS[i]].y for i in range(4)]
# tip.y < pip.y  →  finger extended (y increases downward in normalised image space)
```

### Gesture classification
```python
idx, mid, ring, pinky = up
if idx and not mid and not ring and not pinky:  → 'index_only'
if idx and mid and not ring and not pinky:      → 'peace'
if idx and mid and ring and not pinky:          → 'three_fingers'
if not any(up):                                 → 'fist'
```

### Fist fires on release, not on hold
Held duration is measured from when fist began. Release at 4–5 s → `undo`; release > 5 s → `reset`. Prevents accidental triggers during extended holds.

### Dwell one-shot pattern
Each gesture has a `_fired` flag reset only when the gesture changes. This means each raise→hold cycle fires at most once. User must lower and re-raise the hand to trigger again.

### Homography persists between frames
If markers are briefly occluded, the last known H and rvec/tvec are reused. Both are updated only when a fresh detection succeeds.

### Camera pose (solvePnP)
```python
# Object points: physical marker positions in world mm (z=0, flat on table)
_CORNERS_3D = [[0,W,0], [W,0,0], [W,H,0], [0,H,0]]   # TL TR BR BL

ok, rvec, tvec = cv2.solvePnP(
    _CORNERS_3D, corner_pixels_2d, K, dist,
    flags=cv2.SOLVEPNP_SQPNP
)
```

`corner_pixels` is now returned by `detect_working_plane()` (updated in `working_plane.py`) alongside the existing H and H_inv.

### Plane-to-world coordinate conversion
```python
# working_plane px  →  world mm
x_mm = pt_plane[0] * (PHYSICAL_W_MM / PLANE_W)
y_mm = pt_plane[1] * (PHYSICAL_H_MM / PLANE_H)
```

### Wall face depth sorting
Wall quads are sorted far-to-near before rendering (using projected centroid Z-depth in camera space) to handle building corners correctly without a full depth buffer.

---

## Errors Encountered & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AttributeError: module 'mediapipe' has no attribute 'solutions'` | mediapipe 0.10.35 removed `mp.solutions` | Switched to Tasks API |
| `ModuleNotFoundError: No module named 'mediapipe.python'` | Not a directly importable package | Same — Tasks API |
| `NameError: name '_mp_hands' is not defined` | Old alias left in class body after import rewrite | Updated to `Hands(...)` / `draw_landmarks(...)` |
| Points show but don't register | ArUco markers 0–3 not visible → H is None → tip_valid always False | Ensure all 4 corner markers visible |

---

## Setup Checklist (first run)

- [ ] Print `PRINT_A3.pdf` at 100% on A3
- [ ] Tape ID 0/1/2/3 at table corners
- [ ] Measure marker centre distances → set `PHYSICAL_W_MM` / `PHYSICAL_H_MM` in `extrusion.py`
- [ ] Print a 9×6 checkerboard, measure square size → set `SQUARE_MM` in `calibrate.py`
- [ ] Run `calibrate.py`, capture 15–20 frames, press C → `calibration.npz` saved
- [ ] Run `run.bat` → installs deps, downloads hand model, launches app

## run.bat Sequence

1. Check Python ≥ 3.8 on PATH
2. Create `.venv` if absent
3. `pip install -r requirements.txt` (includes trimesh)
4. Verify imports: cv2, mediapipe, numpy
5. Launch `main.py` — which loads `calibration.npz`, auto-downloads `hand_landmarker.task` if missing, opens camera

---

## Recommended Next Steps (post-calibration)

1. Tune `WALL_HEIGHT_MM` in `extrusion.py` until the AR walls look right at your table scale.
2. Prepare `wall_panel.fbx` and `wall_window.fbx` in the FBX convention above.
3. Swap `draw_walls()` for `ModularFBX(...).draw()` in `main.py`.
4. Consider PyPRT for generating the target reference model for guided assembly.
