---
phase: 2
plan: 05
title: Camera-projector calibration rig + RECALIBRATE.md runbook
owner: _TBD_
wave: 1
depends_on: []
files_modified:
  - vision/calibration/checkerboard_9x6_25mm.pdf
  - vision/calibration/aruco_board_5x7_DICT_4X4_50.pdf
  - vision/calibration/RECALIBRATE.md
  - vision/calibration/camera_intrinsics.yml
  - vision/calibration/projector_camera_homography.yml
  - vision/src/calibrate_camera.py
  - vision/src/calibrate_projector_homography.py
  - vision/pyproject.toml
  - vision/README.md
autonomous: false
requirements:
  - INP-01
  - INP-03
estimated_effort_hours: 8
---

<objective>
Build the camera-projector calibration rig that Plan 07 (one-puck closed-loop CV vertical slice) depends on. The rig produces TWO outputs: (a) `camera_intrinsics.yml` — the OpenCV camera matrix + distortion coefficients from a checkerboard calibration; (b) `projector_camera_homography.yml` — a 3×3 homography matrix that maps detected ArUco pixel coordinates in the camera frame to projector-output pixel coordinates, so the projector can paint accurately on top of any ArUco-detected puck. Both outputs are version-controlled YAML so the team can re-calibrate without re-deriving from scratch. The plan ALSO produces `RECALIBRATE.md`, a runbook any team member can follow in <30 min to re-run the calibration after a camera/projector nudge — a non-negotiable Phase 2 success criterion (ROADMAP item 3). Per locked decision #1 (closed-loop CV from day one) and lit-review strand 03's explicit warning ("calibration drift is the demo-day failure mode of this whole literature"), this plan is the single highest-leverage engineering task in Phase 2. It addresses INP-01 (sensor/webcam streaming into runtime — here, into TouchDesigner via the published intrinsics) and INP-03 (input triggers correct FSM transitions in real time — here by establishing the coordinate-system bridge that makes "puck position → projected target zone comparison" tractable in Plan 07). Per the realignment note: INP-01 was originally framed as "via Firefly" — the SPIRIT (sensor pipeline streaming to runtime) is preserved using the new TouchDesigner stack via OpenCV/OSC.

**Cross-plan ordering note (BLOCKER fix from checker iter 1):** This plan was originally Wave 1 with `depends_on: []`, but Task 5.2 originally generated BOTH the checkerboard PDF (dictionary-agnostic) AND the ArUco-board PDF (which hard-codes the ArUco dictionary). Plan 02-03's Task 3.1 — the checkpoint:decision that locks the ArUco dictionary — also runs in Wave 1, creating a race condition: if the team picks a non-default dictionary in Plan 03, the calibration board PDF would have the wrong dictionary and would be incompatible with the puck markers used in Plan 07. **Fix applied (Option C):** Task 5.2 has been split. Task 5.2a (checkerboard PDF — dictionary-agnostic) runs immediately. Task 5.2b (ArUco-board PDF — dictionary-dependent) has an explicit sentinel pre-check that REFUSES to run until `cad/PUCK-SPEC.md` exists with a locked Dictionary value (i.e. until Plan 02-03 Task 3.1+3.2 have shipped). This keeps the rest of Plan 05 (intrinsics calibration, runbook scaffolding) unblocked in Wave 1 while preventing the race.
</objective>

<must_haves>
- `vision/pyproject.toml` (or `requirements.txt`) pins the OpenCV + numpy versions used. Anyone running calibration uses the same versions.
- A printed checkerboard PDF exists in `vision/calibration/checkerboard_9x6_25mm.pdf` ready to be physically printed at A4 / Letter at 100% scale (no "fit to page"). **Dictionary-agnostic — produced in Wave 1 immediately by Task 5.2a.**
- A printed ArUco-board PDF exists in `vision/calibration/aruco_board_5x7_DICT_4X4_50.pdf` (or the dict chosen in Plan 03) for projector-camera homography calibration. **Dictionary-dependent — produced by Task 5.2b ONLY AFTER Plan 02-03's `cad/PUCK-SPEC.md` is committed and lists a locked Dictionary value.**
- `vision/src/calibrate_camera.py` runs and produces `vision/calibration/camera_intrinsics.yml` (camera matrix + distortion coefficients) given ≥ 10 captured frames of the checkerboard. **Dictionary-agnostic — fully unblocked in Wave 1.**
- `vision/src/calibrate_projector_homography.py` runs and produces `vision/calibration/projector_camera_homography.yml` given a captured frame where the projector displays a known ArUco-board pattern that the camera sees. **Dictionary-dependent — script can be authored in Wave 1 with the dictionary value read from PUCK-SPEC.md at run time, but actual physical homography calibration in Task 5.6 still requires the printed ArUco board from 5.2b.**
- `vision/calibration/RECALIBRATE.md` runbook exists. A team member who has never run calibration can follow it end-to-end in < 30 minutes (verified by Task 5.6 checkpoint).
- The calibration outputs are non-empty YAML files with the exact keys `camera_matrix`, `dist_coeffs` (intrinsics) and `homography`, `image_size_camera`, `image_size_projector` (homography file).
- Both YAML files include a metadata header: `calibrated_at: <ISO date>`, `calibrated_by: <NAME>`, `camera_model: <e.g. Logitech C920>`, `projector_model: <e.g. Epson EH-TW650>`, `mounting_notes: <e.g. "camera 95 cm above table, projector 110 cm above offset 15 cm to the left">` so a future re-calibration knows what physical setup the YAML was produced from.
- `vision/README.md` is updated to document where the calibration files live and that any vision pipeline reads them.
</must_haves>

<tasks>

<task type="auto">
  <name>Task 5.1: Write vision/pyproject.toml + install dependencies</name>
  <action>Create `vision/pyproject.toml` with these pinned versions (chosen for stability — these are the versions every team member installs):

  ```toml
  [project]
  name = "vision"
  version = "0.1.0"
  description = "Camera input, ArUco detection, calibration for the IAAC tabletop installation"
  requires-python = ">=3.11"
  dependencies = [
      "opencv-contrib-python==4.10.0.84",
      "numpy==1.26.4",
      "python-osc==1.8.3",
      "pyyaml==6.0.2",
      "reportlab==4.2.5",
  ]

  [project.optional-dependencies]
  dev = [
      "pytest==8.3.3",
  ]

  [build-system]
  requires = ["setuptools>=68"]
  build-backend = "setuptools.build_meta"

  [tool.setuptools]
  packages = ["src"]
  ```

  IMPORTANT: use `opencv-contrib-python` (NOT `opencv-python`) because `cv2.aruco` lives in the contrib package only.

  After writing the file, install in a virtualenv (the script-run owner does this — it's not a Claude action per se, but document the steps in `vision/README.md` Task 5.7):

  ```
  cd vision
  python -m venv .venv
  # Windows: .venv\Scripts\activate
  # macOS/Linux: source .venv/bin/activate
  pip install -e ".[dev]"
  python -c "import cv2; print(cv2.__version__); import cv2.aruco; print('aruco ok')"
  ```

  The last line MUST print `4.10.0` and `aruco ok` — that's the smoke test that opencv-contrib is installed correctly.</action>
  <read_first>
    - vision/README.md (current contents — for the suggested layout convention)
    - .planning/phases/02-data-research-physical-model-design/02-CONTEXT.md "Claude's Discretion: Vision pipeline location"
  </read_first>
  <acceptance_criteria>
    - `vision/pyproject.toml` exists.
    - File pins `opencv-contrib-python==4.10.0.84` (NOT `opencv-python`).
    - File pins `numpy`, `python-osc`, `pyyaml`, `reportlab` with version specifiers.
    - File specifies `requires-python = ">=3.11"`.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 5.2a: Generate the checkerboard PDF for camera intrinsics (DICTIONARY-AGNOSTIC — runs in Wave 1)</name>
  <action>Create `vision/src/generate_calibration_targets.py`. In THIS task, implement ONLY the checkerboard generator. The ArUco-board generator is added in Task 5.2b after Plan 02-03 ships PUCK-SPEC.md with the locked dictionary.

  Generator: `vision/calibration/checkerboard_9x6_25mm.pdf` — standard OpenCV calibration checkerboard, 9 inner corners horizontal × 6 inner corners vertical (so 10 × 7 squares total), 25 mm square size. Print at 100% scale on A4 or Letter — fits with margins. Add a footer "Print at 100% — do NOT fit-to-page. Square size = 25 mm. Verify by measuring after printing." After printing, the user measures one square with a ruler; if it's not 25 mm exactly, the calibration accuracy will be off by that ratio — document in RECALIBRATE.md.

  Use this skeleton (Wave 1 — checkerboard only; the ArUco board function will be appended in Task 5.2b):

  ```python
  """Generate printable calibration targets per RECALIBRATE.md.

  Wave 1 (Task 5.2a): checkerboard only — dictionary-agnostic.
  Wave 2 (Task 5.2b): ArUco board + projector pattern PNG appended once
                      cad/PUCK-SPEC.md exists with the locked dictionary value.
  """
  from reportlab.lib.pagesizes import A4
  from reportlab.pdfgen import canvas
  from reportlab.lib.units import mm

  # ----- Checkerboard (DICTIONARY-AGNOSTIC) -----
  COLS, ROWS = 10, 7  # squares (so inner corners = 9, 6)
  SQUARE_MM = 25.0

  def render_checkerboard_pdf(path):
      c = canvas.Canvas(path, pagesize=A4)
      origin_x = (A4[0] - COLS * SQUARE_MM * mm) / 2
      origin_y = (A4[1] - ROWS * SQUARE_MM * mm) / 2
      for r in range(ROWS):
          for col in range(COLS):
              if (r + col) % 2 == 0:
                  c.setFillColorRGB(0, 0, 0)
              else:
                  c.setFillColorRGB(1, 1, 1)
              c.rect(origin_x + col * SQUARE_MM * mm,
                     origin_y + r * SQUARE_MM * mm,
                     SQUARE_MM * mm,
                     SQUARE_MM * mm,
                     stroke=0, fill=1)
      c.setFillColorRGB(0, 0, 0)
      c.setFont("Helvetica", 10)
      c.drawString(20 * mm, 15 * mm,
                   "Print at 100% scale (NOT fit-to-page). Each square = 25 mm. Measure to verify.")
      c.save()

  if __name__ == "__main__":
      render_checkerboard_pdf("vision/calibration/checkerboard_9x6_25mm.pdf")
      print("checkerboard PDF written")
      print("NOTE: ArUco board PDF + projector pattern PNG are produced by Task 5.2b once cad/PUCK-SPEC.md exists.")
  ```

  Run the script. Confirm the PDF exists and visually preview it (open in any PDF viewer). The checkerboard should be black/white squares.</action>
  <read_first>
    - vision/pyproject.toml (Task 5.1)
  </read_first>
  <acceptance_criteria>
    - `vision/src/generate_calibration_targets.py` exists with `render_checkerboard_pdf` function.
    - Script runs without error in the pinned environment.
    - `vision/calibration/checkerboard_9x6_25mm.pdf` exists, file size > 5 KB (real PDF, not empty).
    - Visual verification: open PDF — checkerboard shows ~10×7 squares.
    - Script does NOT yet import `cv2.aruco` or generate any ArUco-dependent artifacts (those land in Task 5.2b).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 5.2b: Generate ArUco-board PDF + projector pattern PNG (DICTIONARY-DEPENDENT — gated by sentinel check on cad/PUCK-SPEC.md)</name>
  <sentinel_pre_check>
    **DO NOT START this task until ALL of the following are TRUE:**
    1. `cad/PUCK-SPEC.md` exists in the working tree (Plan 02-03 Task 3.2 output).
    2. `cad/PUCK-SPEC.md` contains an "## ArUco marker" section with a literal Dictionary value spelled out as `DICT_4X4_50` OR `DICT_5X5_100` OR `DICT_6X6_250` (Plan 02-03 Task 3.1 decision locked).
    3. The Dictionary value is NOT a placeholder like `<DICT_4X4_50 / DICT_5X5_100 / DICT_6X6_250>` — it must be one literal value.

    **Runtime sentinel check (executor MUST run this before any other action in this task):**

    ```bash
    # Verify PUCK-SPEC.md exists and has a locked dictionary
    test -f cad/PUCK-SPEC.md || { echo "BLOCKED: cad/PUCK-SPEC.md does not exist — Plan 02-03 Task 3.2 must ship first"; exit 1; }
    DICT=$(grep -E "^\| Dictionary \| (DICT_[0-9]+X[0-9]+_[0-9]+)" cad/PUCK-SPEC.md | head -1 | awk -F'| ' '{print $3}' | awk '{print $1}')
    if [ -z "$DICT" ] || echo "$DICT" | grep -q "/"; then
      echo "BLOCKED: cad/PUCK-SPEC.md does not contain a single locked Dictionary value (found: '$DICT')"
      echo "Plan 02-03 Task 3.1 (checkpoint:decision) must be resolved first."
      exit 1
    fi
    echo "OK: locked dictionary is $DICT"
    ```

    If the sentinel check FAILS, STOP. Notify the executor that Plan 02-03 must complete Task 3.1 + Task 3.2 first. Do NOT proceed with hardcoded fallbacks.
  </sentinel_pre_check>
  <action>After the sentinel passes, read the locked dictionary from `cad/PUCK-SPEC.md` and APPEND two new functions to `vision/src/generate_calibration_targets.py`:

  1. `render_aruco_board_pdf(path, dict_name)`: ArUco grid board, 5 markers wide × 7 markers tall, marker side = 30 mm, marker separation = 10 mm. Use OpenCV's `cv2.aruco.GridBoard` — uses IDs 15..49 from the dictionary (offset to avoid colliding with puck IDs 0–14 reserved in `cad/PUCK-SPEC.md`). Render to PDF.

  2. `render_projector_pattern_png(path, dict_name)`: 1280×720 PNG with 4 ArUco markers (IDs 45, 46, 47, 48) at corners (200,200), (1080,200), (1080,520), (200,520) for the projector-camera homography step.

  Append (do NOT replace the Wave-1 checkerboard function):

  ```python
  # ----- ArUco board + projector pattern (DICTIONARY-DEPENDENT) -----
  # Added in Task 5.2b after sentinel check on cad/PUCK-SPEC.md.
  import os
  import re
  import cv2
  import numpy as np

  BOARD_COLS, BOARD_ROWS = 5, 7
  MARKER_MM = 30.0
  SEPARATION_MM = 10.0
  ID_OFFSET = 15  # IDs 0–14 reserved for pucks per PUCK-SPEC.md

  PROJECTOR_RESOLUTION = (1280, 720)
  CORNER_OFFSETS = [(200, 200), (1080, 200), (1080, 520), (200, 520)]
  CORNER_IDS = [45, 46, 47, 48]
  CORNER_MARKER_PX = 120

  def read_locked_dictionary(puck_spec_path="cad/PUCK-SPEC.md"):
      """Parse the Dictionary value from cad/PUCK-SPEC.md. Refuses placeholders."""
      with open(puck_spec_path) as f:
          text = f.read()
      m = re.search(r"^\|\s*Dictionary\s*\|\s*(DICT_\d+X\d+_\d+)\b", text, re.MULTILINE)
      if not m:
          raise RuntimeError(
              f"{puck_spec_path} does not contain a single locked Dictionary value. "
              "Plan 02-03 Task 3.1 (checkpoint:decision) must resolve first."
          )
      return m.group(1)

  def render_aruco_board_pdf(path, dict_name):
      d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dict_name))
      board = cv2.aruco.GridBoard(
          (BOARD_COLS, BOARD_ROWS),
          MARKER_MM / 1000.0,
          SEPARATION_MM / 1000.0,
          d,
          ids=np.arange(ID_OFFSET, ID_OFFSET + BOARD_COLS * BOARD_ROWS, dtype=np.int32),
      )
      width_px = int((BOARD_COLS * MARKER_MM + (BOARD_COLS - 1) * SEPARATION_MM) * 10)
      height_px = int((BOARD_ROWS * MARKER_MM + (BOARD_ROWS - 1) * SEPARATION_MM) * 10)
      img = board.generateImage((width_px, height_px), marginSize=20)
      png_path = path.replace(".pdf", ".png")
      cv2.imwrite(png_path, img)
      c = canvas.Canvas(path, pagesize=A4)
      width_mm_v = BOARD_COLS * MARKER_MM + (BOARD_COLS - 1) * SEPARATION_MM
      height_mm_v = BOARD_ROWS * MARKER_MM + (BOARD_ROWS - 1) * SEPARATION_MM
      origin_x = (A4[0] - width_mm_v * mm) / 2
      origin_y = (A4[1] - height_mm_v * mm) / 2
      c.drawImage(png_path, origin_x, origin_y, width=width_mm_v * mm, height=height_mm_v * mm)
      c.setFont("Helvetica", 10)
      c.drawString(20 * mm, 15 * mm,
                   f"Print at 100%. Marker side = {MARKER_MM} mm. Separation = {SEPARATION_MM} mm. Dict={dict_name}.")
      c.save()

  def render_projector_pattern_png(path, dict_name):
      d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dict_name))
      img = np.ones((PROJECTOR_RESOLUTION[1], PROJECTOR_RESOLUTION[0]), dtype=np.uint8) * 255
      for (x, y), mid in zip(CORNER_OFFSETS, CORNER_IDS):
          marker = cv2.aruco.generateImageMarker(d, mid, CORNER_MARKER_PX)
          half = CORNER_MARKER_PX // 2
          img[y - half:y + half, x - half:x + half] = marker
      cv2.imwrite(path, img)

  if __name__ == "__main__" and os.environ.get("RUN_ARUCO", "0") == "1":
      DICT = read_locked_dictionary()
      pdf_path = f"vision/calibration/aruco_board_5x7_{DICT}.pdf"
      png_path = "vision/calibration/projector_pattern_4markers.png"
      render_aruco_board_pdf(pdf_path, DICT)
      render_projector_pattern_png(png_path, DICT)
      print(f"wrote {pdf_path} and {png_path} (dict={DICT})")
  ```

  Run with `RUN_ARUCO=1 python vision/src/generate_calibration_targets.py`. The script will:
  1. Re-emit the checkerboard PDF (idempotent — no harm).
  2. Read `cad/PUCK-SPEC.md` for the locked dictionary.
  3. Generate `vision/calibration/aruco_board_5x7_<DICT>.pdf` (filename embeds the actual dictionary).
  4. Generate `vision/calibration/projector_pattern_4markers.png` at 1280×720.

  After running, update the `files_modified` frontmatter: replace `aruco_board_5x7_DICT_4X4_50.pdf` with the actual filename produced (e.g. `aruco_board_5x7_DICT_5X5_100.pdf` if Plan 03 chose that dict). Also update `RECALIBRATE.md` (Task 5.5) to reference the actual filename.</action>
  <read_first>
    - vision/src/generate_calibration_targets.py (Task 5.2a output)
    - cad/PUCK-SPEC.md (Plan 03 Task 3.2 output — REQUIRED, sentinel-checked)
    - vision/pyproject.toml (Task 5.1)
  </read_first>
  <acceptance_criteria>
    - Sentinel check passed (output `OK: locked dictionary is DICT_*`).
    - `vision/src/generate_calibration_targets.py` now contains `render_aruco_board_pdf` and `render_projector_pattern_png` functions.
    - `vision/calibration/aruco_board_5x7_<LOCKED_DICT>.pdf` exists, file size > 10 KB. The filename literally contains the dictionary string read from PUCK-SPEC.md (NOT a hardcoded `DICT_4X4_50`).
    - `vision/calibration/projector_pattern_4markers.png` exists at 1280×720 (file > 5 KB).
    - The Wave-1 checkerboard PDF still exists (was not deleted by the rerun).
    - The Dictionary value parsed by `read_locked_dictionary()` matches the value in `cad/PUCK-SPEC.md` (sanity check: `python -c "import sys; sys.path.insert(0,'vision/src'); from generate_calibration_targets import read_locked_dictionary; print(read_locked_dictionary())"` prints exactly the same string as the spec).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 5.3: Write vision/src/calibrate_camera.py (intrinsics from checkerboard) — DICTIONARY-AGNOSTIC, runs in Wave 1</name>
  <action>Create `vision/src/calibrate_camera.py`. The script:

  1. Captures or loads ≥ 10 frames of the checkerboard at different positions/angles within the camera's view.
  2. For each frame, runs `cv2.findChessboardCorners(frame, (9, 6), ...)` (note: 9, 6 are INNER corners — 10×7 squares give 9×6 inner corners).
  3. Refines corners with `cv2.cornerSubPix`.
  4. Calls `cv2.calibrateCamera(...)` to recover `mtx` (camera matrix) and `dist` (distortion coeffs).
  5. Writes results to `vision/calibration/camera_intrinsics.yml` with the metadata header.

  This script is dictionary-agnostic: it operates on the checkerboard ONLY and has no dependency on Plan 02-03's dictionary decision. It can therefore be authored AND run in Wave 1 against the Task 5.2a checkerboard PDF.

  The script supports two input modes:
  - `python calibrate_camera.py --capture --device 0 --num-frames 15` : opens webcam, asks user to position checkerboard, captures N frames on spacebar, runs calibration.
  - `python calibrate_camera.py --frames-dir captured/` : loads all `*.jpg|*.png` from the directory and runs calibration.

  Use this skeleton:

  ```python
  """Camera intrinsics calibration via checkerboard. See RECALIBRATE.md."""
  import argparse
  import datetime
  import getpass
  import os
  import sys
  import yaml
  import cv2
  import numpy as np

  CHECKERBOARD = (9, 6)  # inner corners
  SQUARE_SIZE_MM = 25.0
  CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  def world_points():
      objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
      objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
      objp *= SQUARE_SIZE_MM
      return objp

  def detect_in_frame(frame_bgr):
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      ok, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
      if not ok:
          return None, gray.shape[::-1]
      corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
      return corners, gray.shape[::-1]

  def capture_frames(device, num_frames):
      cap = cv2.VideoCapture(device)
      if not cap.isOpened():
          raise RuntimeError(f"camera {device} did not open")
      collected = []
      print(f"position checkerboard, press SPACE to capture (need {num_frames}), q to quit")
      while len(collected) < num_frames:
          ok, frame = cap.read()
          if not ok:
              continue
          preview = frame.copy()
          corners, _ = detect_in_frame(frame)
          if corners is not None:
              cv2.drawChessboardCorners(preview, CHECKERBOARD, corners, True)
          cv2.putText(preview, f"{len(collected)}/{num_frames} captured",
                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
          cv2.imshow("calibrate_camera", preview)
          k = cv2.waitKey(1) & 0xFF
          if k == ord(" ") and corners is not None:
              collected.append(frame)
              print(f"captured {len(collected)}")
          elif k == ord("q"):
              break
      cap.release()
      cv2.destroyAllWindows()
      return collected

  def load_frames(frames_dir):
      out = []
      for name in sorted(os.listdir(frames_dir)):
          if name.lower().endswith((".jpg", ".jpeg", ".png")):
              img = cv2.imread(os.path.join(frames_dir, name))
              if img is not None:
                  out.append(img)
      return out

  def calibrate(frames):
      objp = world_points()
      object_points = []
      image_points = []
      image_size = None
      for f in frames:
          corners, size = detect_in_frame(f)
          if corners is None:
              continue
          object_points.append(objp)
          image_points.append(corners)
          image_size = size
      if len(object_points) < 5:
          raise RuntimeError(f"only {len(object_points)} usable frames; need at least 5")
      ret, mtx, dist, _, _ = cv2.calibrateCamera(object_points, image_points, image_size, None, None)
      return ret, mtx, dist, image_size, len(object_points)

  def write_yaml(out_path, ret, mtx, dist, image_size, n_frames, camera_model, projector_model, mounting_notes):
      data = {
          "calibrated_at": datetime.datetime.now().isoformat(timespec="seconds"),
          "calibrated_by": getpass.getuser(),
          "camera_model": camera_model,
          "projector_model": projector_model,
          "mounting_notes": mounting_notes,
          "n_frames_used": n_frames,
          "reprojection_error_px": float(ret),
          "image_size_camera": list(image_size),
          "checkerboard_inner_corners": list(CHECKERBOARD),
          "checkerboard_square_size_mm": SQUARE_SIZE_MM,
          "camera_matrix": mtx.tolist(),
          "dist_coeffs": dist.flatten().tolist(),
      }
      os.makedirs(os.path.dirname(out_path), exist_ok=True)
      with open(out_path, "w") as f:
          yaml.safe_dump(data, f, sort_keys=False)
      print(f"wrote {out_path} (reproj err {ret:.3f} px over {n_frames} frames)")

  if __name__ == "__main__":
      ap = argparse.ArgumentParser()
      ap.add_argument("--capture", action="store_true")
      ap.add_argument("--device", type=int, default=0)
      ap.add_argument("--num-frames", type=int, default=15)
      ap.add_argument("--frames-dir", default=None)
      ap.add_argument("--out", default="vision/calibration/camera_intrinsics.yml")
      ap.add_argument("--camera-model", default="UNKNOWN")
      ap.add_argument("--projector-model", default="UNKNOWN")
      ap.add_argument("--mounting-notes", default="UNKNOWN")
      args = ap.parse_args()
      if args.capture:
          frames = capture_frames(args.device, args.num_frames)
      elif args.frames_dir:
          frames = load_frames(args.frames_dir)
      else:
          print("specify --capture or --frames-dir", file=sys.stderr)
          sys.exit(2)
      ret, mtx, dist, size, n = calibrate(frames)
      write_yaml(args.out, ret, mtx, dist, size, n,
                 args.camera_model, args.projector_model, args.mounting_notes)
  ```

  Test the script with synthetic frames if no camera is plugged in: generate ~10 fake checkerboard images using `cv2` (search "opencv generate checkerboard frames synthetic" patterns) — OR mark this as a CHECKPOINT for the rig owner to run with the actual camera in Task 5.6.

  IMPORTANT: the script does NOT auto-run during planning execution because it requires a physical camera. The acceptance criterion below is "script syntax is valid + imports work" — actual calibration data lives in Task 5.6.</action>
  <read_first>
    - vision/pyproject.toml (Task 5.1)
    - vision/calibration/checkerboard_9x6_25mm.pdf (Task 5.2a)
    - docs/research/lit-review/03-projection-guided-construction.md "Camera-projector calibration: practical guidance" section
  </read_first>
  <acceptance_criteria>
    - `vision/src/calibrate_camera.py` exists.
    - `python -m py_compile vision/src/calibrate_camera.py` exits 0 (valid syntax).
    - `python -c "import sys; sys.path.insert(0, 'vision/src'); import calibrate_camera"` runs without ImportError (all imports resolve in the pinned env).
    - The script's `--help` output mentions both `--capture` and `--frames-dir` (verify by `python vision/src/calibrate_camera.py --help`).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 5.4: Write vision/src/calibrate_projector_homography.py — script may be authored in Wave 1; the locked-dict default it embeds is updated in Wave 2 alongside Task 5.2b</name>
  <action>Create `vision/src/calibrate_projector_homography.py`. The script computes the 3×3 homography matrix that maps camera-pixel coordinates to projector-output-pixel coordinates.

  **Sequencing note:** This script is authored in Wave 1 with `ARUCO_DICT_NAME` initialized as a module-level constant that the script READS FROM `cad/PUCK-SPEC.md` at runtime via a small loader (rather than hardcoding it). If `cad/PUCK-SPEC.md` does not yet exist (Plan 02-03 not yet done), the script falls back to printing a clear error message and exiting non-zero. This keeps the script committable in Wave 1; actual hardware execution lands in Task 5.6 after Plan 02-03 + Task 5.2b have completed.

  Procedure (documented in RECALIBRATE.md too):
  1. Lay the printed `aruco_board_5x7_<LOCKED_DICT>.pdf` (from Task 5.2b) flat on the table inside the camera's field of view AND inside the projector's projection area.
  2. The projector projects a known pattern at known coordinates (e.g. 4 large solid-colour squares at the corners of the projector output, OR — preferred — projects ArUco markers at known projector-pixel coordinates).
  3. The camera detects BOTH the printed ArUco board markers (gives camera-pixel ↔ table-mm mapping) AND the projected markers (gives camera-pixel ↔ projector-pixel mapping for the projected ones).
  4. Compute H such that for the projected markers: `projector_pixel = H @ camera_pixel` (homogeneous coords).
  5. Save H as YAML.

  Simpler v1 alternative (recommended for the 24-h Phase 2 budget): just compute H from 4 projected corner-marker centroids vs their detected camera-pixel centroids. `cv2.findHomography` with 4 point pairs is sufficient and well-documented.

  Use this skeleton (note the dictionary-loader pattern):

  ```python
  """Projector-camera homography calibration. See RECALIBRATE.md.

  Procedure (4-point version):
  1. Project 4 distinct ArUco markers (e.g. IDs 45, 46, 47, 48 from the chosen dict) at 4 known
     projector-output pixel locations, e.g. the corners of a 1280x720 projector output offset
     200 px inside each edge: (200, 200), (1080, 200), (200, 520), (1080, 520).
  2. Camera captures a frame.
  3. Script detects the 4 markers in the camera frame, gets their centroid pixel coordinates.
  4. cv2.findHomography(camera_pts, projector_pts) returns the 3x3 H.
  """
  import argparse
  import datetime
  import getpass
  import os
  import re
  import sys
  import yaml
  import cv2
  import numpy as np

  EXPECTED_IDS = [45, 46, 47, 48]      # the 4 markers projected at known corners
  DEFAULT_PROJECTOR_POINTS = [
      [200, 200],
      [1080, 200],
      [1080, 520],
      [200, 520],
  ]
  PROJECTOR_RESOLUTION = (1280, 720)

  def load_aruco_dict_from_puck_spec(puck_spec_path="cad/PUCK-SPEC.md"):
      """Read the locked ArUco dictionary from cad/PUCK-SPEC.md.

      Refuses to fall back to a hardcoded default — Plan 05 must run AFTER Plan 03.
      """
      if not os.path.exists(puck_spec_path):
          raise RuntimeError(
              f"{puck_spec_path} does not exist. Plan 02-03 must ship Task 3.2 first "
              "(decide + write PUCK-SPEC.md) before projector homography calibration can run."
          )
      with open(puck_spec_path) as f:
          text = f.read()
      m = re.search(r"^\|\s*Dictionary\s*\|\s*(DICT_\d+X\d+_\d+)\b", text, re.MULTILINE)
      if not m:
          raise RuntimeError(
              f"{puck_spec_path} does not contain a single locked Dictionary value. "
              "Plan 02-03 Task 3.1 (checkpoint:decision) must resolve first."
          )
      return m.group(1)

  def detect_markers(frame_bgr, dict_name):
      d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dict_name))
      detector = cv2.aruco.ArucoDetector(d, cv2.aruco.DetectorParameters())
      corners, ids, _ = detector.detectMarkers(frame_bgr)
      if ids is None:
          return {}
      out = {}
      for i, marker_id in enumerate(ids.flatten()):
          out[int(marker_id)] = corners[i].reshape(4, 2).mean(axis=0)
      return out

  def capture_frame(device, dict_name):
      cap = cv2.VideoCapture(device)
      if not cap.isOpened():
          raise RuntimeError(f"camera {device} did not open")
      print("press SPACE to capture, q to abort")
      while True:
          ok, frame = cap.read()
          if not ok:
              continue
          markers = detect_markers(frame, dict_name)
          preview = frame.copy()
          for mid, c in markers.items():
              cv2.circle(preview, tuple(c.astype(int)), 8, (0, 255, 0), 2)
              cv2.putText(preview, str(mid), tuple(c.astype(int) + 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
          have = sorted(markers.keys())
          missing = sorted(set(EXPECTED_IDS) - set(have))
          cv2.putText(preview, f"have {have}, need {EXPECTED_IDS}, missing {missing}",
                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
          cv2.imshow("calibrate_projector_homography", preview)
          k = cv2.waitKey(1) & 0xFF
          if k == ord(" "):
              if all(mid in markers for mid in EXPECTED_IDS):
                  cap.release()
                  cv2.destroyAllWindows()
                  return frame, markers
              else:
                  print(f"not all 4 markers visible — still missing {missing}")
          elif k == ord("q"):
              cap.release()
              cv2.destroyAllWindows()
              raise RuntimeError("user aborted")

  def compute_homography(camera_markers, projector_points):
      cam_pts = np.array([camera_markers[mid] for mid in EXPECTED_IDS], dtype=np.float32)
      proj_pts = np.array(projector_points, dtype=np.float32)
      H, _ = cv2.findHomography(cam_pts, proj_pts)
      if H is None:
          raise RuntimeError("homography computation failed")
      return H

  def write_yaml(out_path, H, image_size_camera, projector_resolution, dict_name,
                 camera_model, projector_model, mounting_notes):
      data = {
          "calibrated_at": datetime.datetime.now().isoformat(timespec="seconds"),
          "calibrated_by": getpass.getuser(),
          "camera_model": camera_model,
          "projector_model": projector_model,
          "mounting_notes": mounting_notes,
          "aruco_dict": dict_name,
          "image_size_camera": list(image_size_camera),
          "image_size_projector": list(projector_resolution),
          "projected_marker_ids": EXPECTED_IDS,
          "homography": H.tolist(),
      }
      os.makedirs(os.path.dirname(out_path), exist_ok=True)
      with open(out_path, "w") as f:
          yaml.safe_dump(data, f, sort_keys=False)
      print(f"wrote {out_path}")

  if __name__ == "__main__":
      ap = argparse.ArgumentParser()
      ap.add_argument("--device", type=int, default=0)
      ap.add_argument("--out", default="vision/calibration/projector_camera_homography.yml")
      ap.add_argument("--camera-model", default="UNKNOWN")
      ap.add_argument("--projector-model", default="UNKNOWN")
      ap.add_argument("--projector-resolution", default="1280x720",
                      help="WxH, e.g. 1920x1080")
      ap.add_argument("--mounting-notes", default="UNKNOWN")
      args = ap.parse_args()
      dict_name = load_aruco_dict_from_puck_spec()
      pw, ph = (int(x) for x in args.projector_resolution.split("x"))
      proj_pts = DEFAULT_PROJECTOR_POINTS  # MUST match what TouchDesigner is projecting
      frame, markers = capture_frame(args.device, dict_name)
      H = compute_homography(markers, proj_pts)
      write_yaml(args.out, H, frame.shape[1::-1], (pw, ph), dict_name,
                 args.camera_model, args.projector_model, args.mounting_notes)
  ```

  IMPORTANT CALLER NOTE: this script EXPECTS the projector to be displaying ArUco markers IDs 45–48 at the four DEFAULT_PROJECTOR_POINTS coordinates. RECALIBRATE.md (Task 5.5) explains how to make TouchDesigner project these — the simplest approach is a fixed PNG with 4 ArUco markers placed at the known coordinates, displayed full-screen via TD's Window COMP at the projector resolution. The pre-rendered PNG (`vision/calibration/projector_pattern_4markers.png`) lives next to the YAML so it can be re-used. **That PNG is produced by Task 5.2b — do NOT attempt to run this script before Task 5.2b has shipped.**</action>
  <read_first>
    - vision/pyproject.toml (Task 5.1)
    - vision/src/calibrate_camera.py (Task 5.3 — for shared idiom: argparse + capture + write_yaml)
    - cad/PUCK-SPEC.md (Plan 03 — for ArUco dictionary alignment; loaded at runtime not import-time so script is committable in Wave 1)
  </read_first>
  <acceptance_criteria>
    - `vision/src/calibrate_projector_homography.py` exists.
    - `python -m py_compile vision/src/calibrate_projector_homography.py` exits 0.
    - `python vision/src/calibrate_projector_homography.py --help` lists `--device`, `--out`, `--projector-resolution`, `--camera-model`, `--projector-model`, `--mounting-notes`.
    - The script's `load_aruco_dict_from_puck_spec()` function reads from `cad/PUCK-SPEC.md` at runtime — does NOT hardcode `DICT_4X4_50` as a module-level default.
    - When `cad/PUCK-SPEC.md` is absent, running the script exits with a clear "Plan 02-03 must ship first" error (not a silent fallback).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 5.5: Write vision/calibration/RECALIBRATE.md runbook</name>
  <action>Create `vision/calibration/RECALIBRATE.md`. The runbook MUST be followable end-to-end by a team member who has never run calibration, in < 30 minutes. Use this exact structure (fill in concrete commands; do not paraphrase). NOTE: the ArUco-board PDF filename embeds the actual dictionary chosen in Plan 02-03 — substitute the real name (e.g. `aruco_board_5x7_DICT_5X5_100.pdf` if Plan 03 picked DICT_5X5_100).

  ```markdown
  # RECALIBRATE — camera + projector calibration runbook

  Run this when:
  - Camera or projector has been physically moved (even slightly).
  - You see drift in the closed-loop CV demo (projected target zone no longer lines up with the puck).
  - Switching to a new camera or projector model.

  Time budget: < 30 minutes if everything is at hand. Plan for 1 hour the first time.

  ## Pre-flight (once — never re-do unless camera/projector changes)

  1. **Mount everything rigidly.** Camera + projector + table must not move during AND after calibration. Use clamps, tripods, or a fixed rig. If you nudge anything after step 4, restart from step 4.
  2. **Print the targets.** From this folder:
     - `checkerboard_9x6_25mm.pdf` — print at 100% scale on A4 (NOT fit-to-page). Measure one square with a ruler — must be 25 mm exactly.
     - `aruco_board_5x7_<LOCKED_DICT>.pdf` (where `<LOCKED_DICT>` matches the value in `cad/PUCK-SPEC.md`) — same instructions. Measure one marker side — must be 30 mm.
     - If your printer can't hold 100% scale, document the actual scale in `mounting_notes` so the YAML reflects reality.
  3. **Install the Python env (once per machine):**
     ```
     cd vision
     python -m venv .venv
     source .venv/bin/activate    # Windows: .venv\Scripts\activate
     pip install -e ".[dev]"
     python -c "import cv2; print(cv2.__version__)"
     ```
     If the version is not 4.10.0, you have the wrong opencv installed — uninstall both `opencv-python` and `opencv-contrib-python` and reinstall from `pyproject.toml`.

  ## Step 1: Camera intrinsics calibration (~10 min)

  1. Plug in the camera. Note its OS device index (usually 0; on macOS check System Information; on Windows check Device Manager).
  2. Run:
     ```
     python vision/src/calibrate_camera.py \
       --capture --device 0 --num-frames 15 \
       --out vision/calibration/camera_intrinsics.yml \
       --camera-model "Logitech C920" \
       --projector-model "Epson EH-TW650" \
       --mounting-notes "camera 95 cm above table, projector 110 cm above offset 15 cm left, 2026-05-XX"
     ```
     (Replace model names + mounting notes with what you actually have.)
  3. A live camera window opens. Hold the printed checkerboard inside the camera's view. When green corners appear overlaid on the checkerboard, hit SPACE to capture.
  4. Capture 15 frames at varied positions: corners of the field of view, tilted left/right/up/down, near and far. The script prompts you when each is captured.
  5. After 15 captures, the script computes intrinsics and writes the YAML. Look at `reprojection_error_px` printed at the end:
     - < 0.5 px: excellent.
     - 0.5–1.0 px: fine.
     - > 1.0 px: re-do with more varied checkerboard angles. (Common cause: all frames captured at the same distance/angle.)
  6. Verify the YAML exists at `vision/calibration/camera_intrinsics.yml` with non-empty `camera_matrix` and `dist_coeffs`.

  ## Step 2: Projector-camera homography calibration (~10 min)

  1. In TouchDesigner, open the calibration patch (or any patch that can display a fullscreen PNG):
     - Load `vision/calibration/projector_pattern_4markers.png` into a Movie File In TOP.
     - Route to a Window COMP set to your projector display, fullscreen, native resolution (e.g. 1280×720 or 1920×1080).
     - Verify on the table: 4 ArUco markers (IDs 45, 46, 47, 48) appear at the 4 corners of the projection area.
     - If you use a different projector resolution, regenerate the PNG: edit `PROJECTOR_RESOLUTION` in `vision/src/generate_calibration_targets.py` and rerun with `RUN_ARUCO=1`.
  2. Run:
     ```
     python vision/src/calibrate_projector_homography.py \
       --device 0 \
       --out vision/calibration/projector_camera_homography.yml \
       --camera-model "Logitech C920" \
       --projector-model "Epson EH-TW650" \
       --projector-resolution 1280x720 \
       --mounting-notes "<same as Step 1>"
     ```
     The script automatically reads the locked ArUco dictionary from `cad/PUCK-SPEC.md` — no need to pass it on the CLI.
  3. Live camera window opens. The script overlays the IDs of the projected markers it sees. When all 4 (45, 46, 47, 48) are visible, hit SPACE.
  4. The script computes the 3×3 homography and writes it to YAML.
  5. Verify the YAML exists with non-empty `homography` (3×3 list of floats).

  ## Step 3: Sanity-check (~5 min)

  Run this 5-line Python snippet to verify the homography maps a known camera pixel back to roughly the projector pixel where the corresponding marker was:

  ```python
  import yaml, numpy as np, cv2
  with open("vision/calibration/projector_camera_homography.yml") as f:
      h = yaml.safe_load(f)
  H = np.array(h["homography"])
  # Use one of the marker centroid camera pixels you saw during capture
  cam_pt = np.array([320.0, 240.0, 1.0])  # CHANGE to the actual centroid
  proj_pt = H @ cam_pt
  proj_pt = proj_pt[:2] / proj_pt[2]
  print(f"camera ({cam_pt[:2]}) -> projector ({proj_pt})")
  ```
  Expected: the printed projector point is roughly within ±5 px of the projector-output coordinate where you placed that marker (one of `(200, 200), (1080, 200), (1080, 520), (200, 520)`).

  ## Troubleshooting

  - **"camera 0 did not open"** — check device index; try 1 or 2. On macOS, grant terminal camera permission. On Windows, close any other app using the camera.
  - **Checkerboard never detects** — print quality, lighting, or distance issue. Try slightly more even ambient light, hold the checkerboard flat (no curl), at ~30–60 cm from the camera.
  - **Reprojection error > 2 px** — frames are too similar. Capture at more varied positions and angles.
  - **Homography looks wildly wrong** — verify the projected marker coordinates in `DEFAULT_PROJECTOR_POINTS` match what you actually projected. If you regenerated the PNG with different coordinates, update both the PNG and the script's defaults.
  - **"cad/PUCK-SPEC.md does not exist" on Step 2** — Plan 02-03 has not yet shipped; calibration cannot proceed until the puck dictionary is locked.

  ## When in doubt

  Re-read `docs/research/lit-review/03-projection-guided-construction.md` "Camera-projector calibration: practical guidance" — the three operational rules from Bimber & Raskar (2005) and Moreno & Taubin (2012) apply: mount rigidly, calibrate once, never move it.
  ```

  Replace placeholder values (`Logitech C920`, `1280x720`, etc.) with whatever the team actually has on the table; if unknown, leave the placeholders so the user can search-and-replace.</action>
  <read_first>
    - vision/src/calibrate_camera.py (Task 5.3)
    - vision/src/calibrate_projector_homography.py (Task 5.4)
    - vision/calibration/checkerboard_9x6_25mm.pdf (Task 5.2a)
    - docs/research/lit-review/03-projection-guided-construction.md "Camera-projector calibration" section
  </read_first>
  <acceptance_criteria>
    - `vision/calibration/RECALIBRATE.md` exists.
    - File contains exactly these section headers (verifiable by grep): `## Pre-flight`, `## Step 1: Camera intrinsics calibration`, `## Step 2: Projector-camera homography calibration`, `## Step 3: Sanity-check`, `## Troubleshooting`.
    - Each Step section starts with a "(~N min)" time estimate.
    - Total estimated time across Steps 1+2+3 = ≤ 25 minutes (10 + 10 + 5), within the 30-minute budget.
    - File contains the exact command-line invocation for both `calibrate_camera.py` and `calibrate_projector_homography.py` with all required arguments.
  </acceptance_criteria>
</task>

<task type="checkpoint:human-verify">
  <name>Task 5.6: Run the actual calibration end-to-end (HUMAN — physical hardware required)</name>
  <what-built>Both Python scripts (`calibrate_camera.py`, `calibrate_projector_homography.py`) are syntactically valid and runnable. The PDFs are generated (checkerboard from 5.2a, ArUco-board from 5.2b). RECALIBRATE.md walks through the full procedure. What's NOT built: the actual YAML outputs — these need physical hardware (camera, projector, printed targets) and only humans can run them.</what-built>
  <pre_check>Task 5.2b MUST have shipped (i.e. Plan 02-03 Task 3.1+3.2 are done AND `vision/calibration/aruco_board_5x7_<LOCKED_DICT>.pdf` + `vision/calibration/projector_pattern_4markers.png` exist). If not, Step 2 of the runbook will fail at the `load_aruco_dict_from_puck_spec()` check.</pre_check>
  <how-to-verify>
    1. Print the 2 PDFs from `vision/calibration/` (checkerboard + ArUco board) at 100% scale. Measure with a ruler — checkerboard square must be 25 mm; ArUco marker side must be 30 mm.
    2. Mount your overhead camera and projector rigidly above the table. Note approximate heights and offsets — these go in `--mounting-notes` for both YAML files.
    3. Follow `vision/calibration/RECALIBRATE.md` Step 1 — produce `vision/calibration/camera_intrinsics.yml`. Reprojection error < 1 px.
    4. Set up TouchDesigner to display `vision/calibration/projector_pattern_4markers.png` fullscreen on the projector at the resolution noted in `--projector-resolution`.
    5. Follow Step 2 — produce `vision/calibration/projector_camera_homography.yml`.
    6. Run the Step 3 sanity-check — verify the homography maps a known camera pixel back within ±5 px of its projector source.
    7. Commit both YAMLs to the repo (these are NOT secrets — they're per-rig config and are how Plan 07 finds the calibration).
    8. Time the procedure: it must complete in < 30 minutes. If it took longer, update `RECALIBRATE.md` Troubleshooting with whatever blocked you so the next person doesn't hit the same.
  </how-to-verify>
  <resume-signal>Type "calibrated" with the reprojection_error_px value AND the wall-clock time the procedure took, OR "blocked: <reason>" if something needs fixing in the scripts/runbook. If blocked: Plan 07 vertical slice cannot proceed and the team needs to debug calibration before that plan starts.</resume-signal>
</task>

<task type="auto">
  <name>Task 5.7: Update vision/README.md to point at the calibration outputs</name>
  <action>Edit `vision/README.md`. Add a new section titled "## Calibration" after the "## Conventions" section, with this exact content:

  ```markdown
  ## Calibration

  Camera intrinsics + projector-camera homography are produced once per physical rig setup.
  Outputs live in `vision/calibration/`:

  - `camera_intrinsics.yml` — OpenCV camera matrix + distortion coefficients.
  - `projector_camera_homography.yml` — 3×3 homography mapping camera-pixel → projector-pixel.

  Both are version-controlled (per-rig config, not secrets).

  To re-calibrate, follow `vision/calibration/RECALIBRATE.md`. Budget < 30 min for someone who's done it before, < 1 hr the first time.

  Per locked decision in `CONTRIBUTING.md` and the lit-review (`docs/research/lit-review/03-projection-guided-construction.md`), calibration drift is the demo-day failure mode of this whole project. Re-calibrate after ANY camera or projector nudge, and again under final exhibition lighting in Phase 5.
  ```

  Also update the "## Suggested layout" tree to add `RECALIBRATE.md` and the YAML files explicitly (preserves existing content but extends it):

  ```
  vision/
  ├── pyproject.toml
  ├── src/
  │   ├── capture.py
  │   ├── aruco_detect.py
  │   ├── footprint.py
  │   ├── osc_send.py
  │   ├── generate_markers.py
  │   ├── generate_calibration_targets.py
  │   ├── calibrate_camera.py
  │   └── calibrate_projector_homography.py
  ├── calibration/
  │   ├── RECALIBRATE.md
  │   ├── checkerboard_9x6_25mm.pdf
  │   ├── aruco_board_5x7_<LOCKED_DICT>.pdf
  │   ├── projector_pattern_4markers.png
  │   ├── camera_intrinsics.yml
  │   └── projector_camera_homography.yml
  └── tests/
  ```</action>
  <read_first>
    - vision/README.md (current contents)
    - vision/calibration/RECALIBRATE.md (Task 5.5 output)
  </read_first>
  <acceptance_criteria>
    - `vision/README.md` contains a `## Calibration` section.
    - The section names both YAML output files and links back to `RECALIBRATE.md`.
    - The "Suggested layout" tree lists `RECALIBRATE.md`, `camera_intrinsics.yml`, `projector_camera_homography.yml`.
    - Original "## Scope", "## Conventions" sections remain present (not deleted).
  </acceptance_criteria>
</task>

</tasks>

<verification>
- All script files exist and pass `python -m py_compile`.
- `vision/calibration/checkerboard_9x6_25mm.pdf` exists (from Task 5.2a, Wave 1).
- `vision/calibration/aruco_board_5x7_<LOCKED_DICT>.pdf` exists (from Task 5.2b, AFTER Plan 02-03 ships PUCK-SPEC.md).
- `vision/calibration/projector_pattern_4markers.png` exists at 1280×720 (or chosen resolution) (from Task 5.2b).
- `vision/calibration/RECALIBRATE.md` contains all 5 required sections.
- `vision/calibration/camera_intrinsics.yml` exists with `camera_matrix`, `dist_coeffs`, `reprojection_error_px`, `calibrated_at`, `calibrated_by`, `mounting_notes` keys.
- `vision/calibration/projector_camera_homography.yml` exists with `homography` (3×3), `image_size_camera`, `image_size_projector`, `aruco_dict`, `calibrated_at` keys.
- `vision/README.md` documents the calibration outputs.
- `calibrate_projector_homography.py` reads the dictionary from `cad/PUCK-SPEC.md` at runtime (no hardcoded fallback).
- `generate_calibration_targets.py` Task 5.2b function reads dictionary from `cad/PUCK-SPEC.md` (no hardcoded fallback).
- Team-member acceptance: a person who didn't write `RECALIBRATE.md` can re-run calibration in < 30 min following the runbook (checked at Task 5.6 checkpoint OR formally in Phase 5 when re-calibrating under exhibition lighting).
</verification>
