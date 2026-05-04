---
phase: 2
plan: 07
title: One-puck closed-loop CV vertical slice (the gating Phase 2 deliverable)
owner: _TBD_
wave: 2
depends_on: [3, 5, 6]
files_modified:
  - vision/src/aruco_detect.py
  - vision/src/osc_send.py
  - vision/src/run_vertical_slice.py
  - vision/calibration/TOLERANCE.md
  - touchdesigner/vertical-slice.toe
  - touchdesigner/VERTICAL-SLICE-RUNBOOK.md
  - deliverables/vertical-slice-demo.mp4
autonomous: false
requirements:
  - INP-01
  - INP-02
  - INP-03
estimated_effort_hours: 10
---

<objective>
Ship the **one-puck closed-loop CV vertical slice** that ROADMAP Phase 2 Success Criterion #4 names "THIS IS THE GATING DELIVERABLE — Phase 3 cannot start until this works." The slice runs end-to-end: webcam captures frame → Python (OpenCV + ArUco) detects ArUco puck position → camera-pixel coordinates transformed to projector-pixel coordinates via the homography from Plan 05 → position compared against a projected target zone (rendered by TouchDesigner) → if within tolerance, projector shows VALID green halo (per Plan 06's locked visual language) AND TouchDesigner FSM advances to next state; if outside tolerance, projector shows INVALID-WITH-GHOST (puck-where-it-is + ghost-of-where-it-should-be); if no marker, projector shows DISCONNECTED dotted outline. Total detection-to-projection-update latency < 150 ms (matches HITL-02). This plan delivers the proof that closed-loop CV is achievable for this team on this hardware before Phase 3 invests in scaling to 10 pucks. It addresses INP-01 (sensor/webcam streaming into runtime — here, OpenCV → OSC → TouchDesigner), INP-02 (input mapped to fabrication parameter — here, the puck position is mapped to "is this a valid placement of footprint corner #1"), and INP-03 (input triggers correct FSM state transitions in real time — the central proof). Per the realignment note: INP-01 originally read "via Firefly" and INP-03 originally implied an Anemone FSM — both are honoured in SPIRIT (sensor pipeline streams to runtime; runtime FSM advances on detected input) using the locked TouchDesigner stack.
</objective>

<must_haves>
- The full pipeline RUNS end-to-end without crashing for at least 5 minutes of continuous use.
- Latency from puck-physical-move to projection-state-change is < 150 ms (measured by Task 7.6 — hand-clap-and-stopwatch is acceptable; high-speed phone video is better).
- The 4 visual states from `touchdesigner/ERROR-FEEDBACK-SPEC.md` (VALID, PENDING, INVALID-WITH-GHOST, DISCONNECTED) all render correctly on the projector.
- When the puck is in the projected target zone (within tolerance T from `vision/calibration/TOLERANCE.md`), the TD state advances from `WAITING_FOR_PUCK` to `PUCK_CONFIRMED` exactly once per placement (no flapping).
- When the puck is OUTSIDE tolerance, a ghost outline appears at the correct projected location AND the FSM stays in `WAITING_FOR_PUCK`.
- When no marker is detected for ≥ 1 s, the projection shows the DISCONNECTED state.
- A 30-second video demo exists at `deliverables/vertical-slice-demo.mp4` showing the puck being moved into and out of the target zone with the projection responding correctly. (Per ACTIONS.md Week 1 exit criterion: "demo a 30-second video of one puck moving on a table, projection responding in real time with valid/invalid states.")
- `touchdesigner/VERTICAL-SLICE-RUNBOOK.md` tells anyone how to launch the demo: which scripts to run, in which order, with which arguments, on which hardware.
- `vision/calibration/TOLERANCE.md` records the chosen numeric tolerance value AND the measured ArUco-detection jitter that informed it.
- The slice uses the LOCKED ArUco dictionary from `cad/PUCK-SPEC.md` (Plan 03), the LOCKED calibration files from `vision/calibration/` (Plan 05), and the LOCKED visual language from `touchdesigner/ERROR-FEEDBACK-SPEC.md` (Plan 06). Any deviation requires updating the upstream spec, not the slice.
</must_haves>

<contingency>
## Hardware-blocked contingency (added per checker iter 1, WARNING #3)

The physical-calibration checkpoint (Plan 02-05 Task 5.6) is on the critical path to this plan with zero slack against the 2026-05-04 deadline. If hardware setup or calibration takes longer than expected, the vertical slice cannot complete on time without a fallback.

**Fallback rule:** If Plan 02-05 Task 5.6 (physical calibration run) is BLOCKED beyond 4h past plan estimate, the executor of Plan 02-07 may use synthetic calibration YAMLs to unblock the software-only tasks:

- `vision/calibration/synthetic_intrinsics.yml` — generated from typical Logitech C920 parameters (1920×1080, fx≈fy≈1450 px, cx≈960, cy≈540, modest barrel distortion `k1≈-0.1, k2≈0.05, p1=p2=0, k3≈0`).
- `vision/calibration/synthetic_homography.yml` — generated from typical 1080p projector parameters and an assumed camera-to-projector transform (identity-ish 3×3 with reasonable scale + offset for a 1280×720 projector cropped from a 1920×1080 camera frame centred on table).

These synthetic YAMLs MUST be clearly labelled inside the file metadata as `calibrated_by: SYNTHETIC` and `mounting_notes: SYNTHETIC FALLBACK — DO NOT SHIP DEMO WITH THIS FILE`.

**Tasks unblocked by synthetic YAMLs:**
- Task 7.1 (`aruco_detect.py`) — runs against synthetic homography; unit tests pass.
- Task 7.2 (`osc_send.py`) — pure software, no calibration dependency.
- Task 7.3 (`run_vertical_slice.py`) — CLI parsing + module wiring verified in dry-run mode.
- Task 7.5 (`VERTICAL-SLICE-RUNBOOK.md`) — pure documentation.

**Tasks STILL requiring real hardware (these slip to Phase 2.5 catch-up if Task 5.6 remains blocked):**
- Task 7.4 (TouchDesigner integration in `vertical-slice.toe`) — needs real projector + camera to verify the visual loop renders correctly under the team's actual lighting.
- Task 7.6 (end-to-end run + latency measurement + 30-second video demo) — needs the entire physical rig.

**How to generate synthetic YAMLs (one-off helper):** add `vision/src/generate_synthetic_calibration.py` that writes both YAMLs with the parameters above. Run only if Task 5.6 is declared blocked. Commit the synthetic YAMLs alongside a `vision/calibration/SYNTHETIC-FALLBACK.md` note explaining that they are placeholders and the real ones MUST be regenerated by Phase 2.5 before any public demo.

**Phase 2.5 catch-up:** if synthetic YAMLs are used, a Phase 2.5 catch-up sub-phase MUST run before Phase 3 starts. It re-runs Plan 05 Task 5.6 with real hardware, then re-runs Plan 07 Tasks 7.4 + 7.6 with the real YAMLs, then deletes the synthetic files. Phase 3 is BLOCKED until this catch-up completes — no exceptions.
</contingency>

<tasks>

<task type="auto">
  <name>Task 7.1: Write vision/src/aruco_detect.py (puck detection + camera→projector mapping)</name>
  <action>Create `vision/src/aruco_detect.py`. This module is the core CV: capture a webcam frame, detect ArUco markers, look up calibration files, transform detected camera-pixel centroids to projector-pixel coordinates via the homography. Exposes a single function `detect_pucks_in_projector_coords(frame, intrinsics_path, homography_path) -> list[dict]` that returns:

  ```
  [{"id": int, "camera_xy": (cx, cy), "projector_xy": (px, py), "corners_camera": ndarray(4,2)}]
  ```

  Use this skeleton (adjust the dictionary import to match Plan 03 / Plan 05):

  ```python
  """ArUco puck detection + camera-pixel to projector-pixel mapping.

  This is the per-frame CV core for the Phase 2 vertical slice.
  Reads calibration files from vision/calibration/ produced by Plan 05.
  """
  from __future__ import annotations
  import functools
  import yaml
  import cv2
  import numpy as np

  ARUCO_DICT_NAME = "DICT_4X4_50"  # MUST MATCH cad/PUCK-SPEC.md

  @functools.lru_cache(maxsize=4)
  def _load_intrinsics(path: str):
      with open(path) as f:
          data = yaml.safe_load(f)
      return (
          np.array(data["camera_matrix"], dtype=np.float64),
          np.array(data["dist_coeffs"], dtype=np.float64),
      )

  @functools.lru_cache(maxsize=4)
  def _load_homography(path: str):
      with open(path) as f:
          data = yaml.safe_load(f)
      return np.array(data["homography"], dtype=np.float64)

  @functools.lru_cache(maxsize=1)
  def _detector():
      d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, ARUCO_DICT_NAME))
      return cv2.aruco.ArucoDetector(d, cv2.aruco.DetectorParameters())

  def _camera_to_projector(camera_xy: np.ndarray, H: np.ndarray) -> tuple[float, float]:
      """camera_xy: shape (2,). Returns (px, py)."""
      v = np.array([camera_xy[0], camera_xy[1], 1.0], dtype=np.float64)
      out = H @ v
      return float(out[0] / out[2]), float(out[1] / out[2])

  def detect_pucks_in_projector_coords(
      frame_bgr: np.ndarray,
      intrinsics_path: str = "vision/calibration/camera_intrinsics.yml",
      homography_path: str = "vision/calibration/projector_camera_homography.yml",
      undistort: bool = True,
      puck_id_range: tuple[int, int] = (0, 14),
  ) -> list[dict]:
      """Detect ArUco markers, return puck centroids in projector pixel coords.

      Filters to puck IDs (default 0–14 reserved per cad/PUCK-SPEC.md), excluding
      the calibration-board IDs (15+).
      """
      camera_matrix, dist_coeffs = _load_intrinsics(intrinsics_path)
      H = _load_homography(homography_path)
      if undistort:
          frame_bgr = cv2.undistort(frame_bgr, camera_matrix, dist_coeffs)
      corners, ids, _ = _detector().detectMarkers(frame_bgr)
      if ids is None:
          return []
      out = []
      lo, hi = puck_id_range
      for i, marker_id in enumerate(ids.flatten()):
          mid = int(marker_id)
          if not (lo <= mid <= hi):
              continue
          c = corners[i].reshape(4, 2)
          centroid = c.mean(axis=0)
          proj_xy = _camera_to_projector(centroid, H)
          out.append({
              "id": mid,
              "camera_xy": (float(centroid[0]), float(centroid[1])),
              "projector_xy": proj_xy,
              "corners_camera": c,
          })
      return out
  ```

  IMPORTANT: replace `ARUCO_DICT_NAME = "DICT_4X4_50"` with whatever Plan 03 chose (read the actual value from `cad/PUCK-SPEC.md`).

  Also write `vision/tests/test_aruco_detect.py` with at least one test: synthesise a frame with one known ArUco marker drawn at a known location using `cv2.aruco.generateImageMarker`, run detection, assert the returned id matches and the projector_xy is within tolerance of the expected (using an identity homography for the test). This catches regressions in the dictionary / detector parameters.</action>
  <read_first>
    - cad/PUCK-SPEC.md (Plan 03 — for ArUco dictionary)
    - vision/calibration/camera_intrinsics.yml (Plan 05 — for the YAML schema this code reads; OR synthetic_intrinsics.yml if contingency is in effect)
    - vision/calibration/projector_camera_homography.yml (Plan 05 — OR synthetic_homography.yml if contingency is in effect)
    - vision/src/calibrate_camera.py (Plan 05 — for shared idiom)
  </read_first>
  <acceptance_criteria>
    - `vision/src/aruco_detect.py` exists.
    - `python -m py_compile vision/src/aruco_detect.py` exits 0.
    - `python -c "import sys; sys.path.insert(0, 'vision/src'); import aruco_detect; help(aruco_detect.detect_pucks_in_projector_coords)"` runs without ImportError.
    - `vision/tests/test_aruco_detect.py` exists.
    - `cd vision && pytest tests/test_aruco_detect.py -x` exits 0 (synthetic-frame test passes).
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 7.2: Write vision/src/osc_send.py (OSC bridge to TouchDesigner)</name>
  <action>Create `vision/src/osc_send.py`. The Python side sends two OSC messages per frame to the TouchDesigner OSC In CHOP listening on a fixed port (default 7000):

  - `/puck/state` with args `(int marker_id, float projector_x, float projector_y, float camera_x, float camera_y)` — sent once per detected puck per frame.
  - `/puck/none` with no args — sent if NO puck detected in this frame (so TD knows to switch to DISCONNECTED state after a debounce).

  TD reads these via OSC In CHOP and routes to the FSM. Use `python-osc` from pinned deps:

  ```python
  """Send puck-detection results to TouchDesigner over OSC."""
  from __future__ import annotations
  from pythonosc.udp_client import SimpleUDPClient

  class TDClient:
      def __init__(self, host: str = "127.0.0.1", port: int = 7000):
          self.client = SimpleUDPClient(host, port)

      def send_pucks(self, pucks: list[dict]) -> None:
          if not pucks:
              self.client.send_message("/puck/none", [])
              return
          for p in pucks:
              self.client.send_message(
                  "/puck/state",
                  [
                      int(p["id"]),
                      float(p["projector_xy"][0]),
                      float(p["projector_xy"][1]),
                      float(p["camera_xy"][0]),
                      float(p["camera_xy"][1]),
                  ],
              )
  ```

  Add `vision/tests/test_osc_send.py` with one test: spin up a `pythonosc.dispatcher.Dispatcher` + `BlockingOSCUDPServer` on port 7001 in a thread, send one puck, assert the dispatcher received the right message. (Use port 7001 for the test so production port 7000 is free.)</action>
  <read_first>
    - vision/pyproject.toml (Task 5.1 — confirms python-osc is pinned)
    - vision/README.md (OSC convention)
  </read_first>
  <acceptance_criteria>
    - `vision/src/osc_send.py` exists.
    - `python -m py_compile vision/src/osc_send.py` exits 0.
    - `vision/tests/test_osc_send.py` exists.
    - `cd vision && pytest tests/test_osc_send.py -x` exits 0.
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 7.3: Write vision/src/run_vertical_slice.py (the runner script)</name>
  <action>Create `vision/src/run_vertical_slice.py`. This is the main loop: open camera → for each frame → detect → send OSC → repeat. CLI arguments to specify camera device, intrinsics path, homography path, OSC host/port, target FPS. Also writes per-frame timing to a small log so latency can be measured.

  ```python
  """Vertical-slice runner: webcam → ArUco → OSC → TouchDesigner.

  See touchdesigner/VERTICAL-SLICE-RUNBOOK.md for end-to-end launch instructions.
  """
  import argparse
  import time
  import cv2
  import sys
  import os

  sys.path.insert(0, os.path.dirname(__file__))
  from aruco_detect import detect_pucks_in_projector_coords  # noqa: E402
  from osc_send import TDClient  # noqa: E402

  def main() -> int:
      ap = argparse.ArgumentParser()
      ap.add_argument("--device", type=int, default=0)
      ap.add_argument("--intrinsics", default="vision/calibration/camera_intrinsics.yml")
      ap.add_argument("--homography", default="vision/calibration/projector_camera_homography.yml")
      ap.add_argument("--osc-host", default="127.0.0.1")
      ap.add_argument("--osc-port", type=int, default=7000)
      ap.add_argument("--target-fps", type=int, default=30)
      ap.add_argument("--show-preview", action="store_true",
                      help="show camera preview window with detection overlay")
      ap.add_argument("--log-timing", default=None,
                      help="write per-frame timing to this CSV path")
      args = ap.parse_args()

      cap = cv2.VideoCapture(args.device)
      if not cap.isOpened():
          print(f"camera {args.device} did not open", file=sys.stderr)
          return 2
      td = TDClient(args.osc_host, args.osc_port)
      frame_period = 1.0 / args.target_fps
      log_f = open(args.log_timing, "w") if args.log_timing else None
      if log_f:
          log_f.write("frame_idx,capture_ms,detect_ms,osc_ms,total_ms,n_pucks\n")
      try:
          frame_idx = 0
          while True:
              t0 = time.perf_counter()
              ok, frame = cap.read()
              t1 = time.perf_counter()
              if not ok:
                  continue
              pucks = detect_pucks_in_projector_coords(
                  frame, args.intrinsics, args.homography)
              t2 = time.perf_counter()
              td.send_pucks(pucks)
              t3 = time.perf_counter()
              if log_f:
                  log_f.write(
                      f"{frame_idx},{(t1-t0)*1000:.2f},{(t2-t1)*1000:.2f},"
                      f"{(t3-t2)*1000:.2f},{(t3-t0)*1000:.2f},{len(pucks)}\n"
                  )
                  log_f.flush()
              frame_idx += 1
              if args.show_preview:
                  for p in pucks:
                      c = p["corners_camera"].astype(int)
                      cv2.polylines(frame, [c], True, (0, 255, 0), 2)
                      ctr = tuple(map(int, p["camera_xy"]))
                      cv2.circle(frame, ctr, 6, (0, 255, 0), 2)
                      cv2.putText(frame, f"id={p['id']} proj={p['projector_xy']}",
                                  (ctr[0]+10, ctr[1]),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                  cv2.imshow("vertical_slice", frame)
                  if (cv2.waitKey(1) & 0xFF) == ord("q"):
                      break
              elapsed = time.perf_counter() - t0
              if elapsed < frame_period:
                  time.sleep(frame_period - elapsed)
      finally:
          cap.release()
          cv2.destroyAllWindows()
          if log_f:
              log_f.close()
      return 0

  if __name__ == "__main__":
      raise SystemExit(main())
  ```

  Test the script's CLI parsing: `python vision/src/run_vertical_slice.py --help` should list all args. The script does NOT auto-run during planning — it requires camera + projector + a running TouchDesigner patch. Task 7.6 runs it for real.</action>
  <read_first>
    - vision/src/aruco_detect.py (Task 7.1)
    - vision/src/osc_send.py (Task 7.2)
    - vision/calibration/RECALIBRATE.md (Plan 05 — for the calibration paths the script defaults to)
  </read_first>
  <acceptance_criteria>
    - `vision/src/run_vertical_slice.py` exists.
    - `python -m py_compile vision/src/run_vertical_slice.py` exits 0.
    - `python vision/src/run_vertical_slice.py --help` lists `--device`, `--intrinsics`, `--homography`, `--osc-host`, `--osc-port`, `--target-fps`, `--show-preview`, `--log-timing`.
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action">
  <name>Task 7.4: Build touchdesigner/vertical-slice.toe (HUMAN — TouchDesigner work, .toe is binary)</name>
  <what-built>The Python side (capture, detect, OSC out) is complete. The TouchDesigner side is binary (.toe) and Claude cannot author it. Use the spec below as the build brief.</what-built>
  <hardware_requirement>This task REQUIRES real projector + real camera to verify the visual loop. If Plan 02-05 Task 5.6 has used the synthetic-fallback contingency, this task slips to the Phase 2.5 catch-up sub-phase (per the <contingency> block above) — do NOT attempt to build vertical-slice.toe against synthetic homography YAMLs because the projection-mapping geometry will be visually wrong.</hardware_requirement>
  <how-to-verify>
    Open TouchDesigner. Create `touchdesigner/vertical-slice.toe`. Build the following minimal patch:

    1. **OSC In CHOP** listening on port 7000, expecting messages `/puck/state` and `/puck/none`.
    2. **A simple FSM**: 2 states (`WAITING_FOR_PUCK`, `PUCK_CONFIRMED`). Use either Derivative's free Table-Driven FSM asset (https://derivative.ca/community-post/asset/table-driven-finite-state-machine-fsm-manage-interactive-logic-cleanly-free) or a hand-rolled CHOP/DAT pattern.
    3. **State logic**:
       - On `/puck/none` for ≥ 1 second → render DISCONNECTED state.
       - On `/puck/state` with `marker_id=0` (first test puck), compute distance between `(projector_x, projector_y)` and the locked target coords (initially hard-coded to e.g. (640, 360) — the projector centre). If distance < TOLERANCE_MM_IN_PROJECTOR_PIXELS → state = VALID, render VALID halo, advance FSM to PUCK_CONFIRMED. Else → state = INVALID-WITH-GHOST, render dashed outline at puck location + ghost at target location, FSM stays in WAITING_FOR_PUCK.
    4. **Visual rendering** per `touchdesigner/ERROR-FEEDBACK-SPEC.md` Task 6.2:
       - 4 visual states. Each renders as described in the spec (colours, line styles, animation per the spec).
       - Use `Constant TOP` + `Composite TOP` + `Switch TOP` driven by the FSM state CHOP.
    5. **Window COMP** routed to projector display, full-screen, 1280×720 (or whichever resolution was in the homography YAML).
    6. **Test mode**: a Constant CHOP on a keyboard shortcut so you can manually trigger each of the 4 states for visual verification before bringing the camera into the loop.

    TOLERANCE_MM_IN_PROJECTOR_PIXELS: convert the 15 mm tolerance from `ERROR-FEEDBACK-SPEC.md` to projector pixels. Quick estimate: if the projector covers ~1 m of table at 1280 px wide, 1 mm ≈ 1.28 px, so 15 mm ≈ 19 px. Refine empirically in Task 7.6.

    Save the `.toe` to `touchdesigner/vertical-slice.toe`. Coordinate in the group chat before saving — `.toe` files don't merge per CONTRIBUTING.md.

    Verify by running the patch with no Python script connected, hand-triggering each state with the test mode hotkey — confirm each state renders per the SPEC.md and the projection looks like `touchdesigner/error-feedback-mockup.png`.
  </how-to-verify>
  <resume-signal>Type "toe-built" with the path AND a screenshot of the patch network, OR "blocked: <what-isn't-clear>" if the spec needs more detail. If blocked: this halts Plan 07.</resume-signal>
</task>

<task type="auto">
  <name>Task 7.5: Write touchdesigner/VERTICAL-SLICE-RUNBOOK.md</name>
  <action>Create `touchdesigner/VERTICAL-SLICE-RUNBOOK.md`. The runbook walks any team member through launching the vertical-slice demo end-to-end. Use this exact structure:

  ```markdown
  # Vertical-slice runbook

  How to run the Phase 2 closed-loop CV demo end-to-end. Total launch time: ~3 minutes if everything is in place.

  ## Pre-requisites (one-time)

  - Calibration done (run `vision/calibration/RECALIBRATE.md`); both YAMLs exist in `vision/calibration/`.
  - At least 1 printed puck physically present (Plan 03 output).
  - TouchDesigner installed; pinned version per `touchdesigner/README.md`.
  - Python env set up (`vision/.venv` activated; see `vision/calibration/RECALIBRATE.md` Pre-flight step 3).
  - `touchdesigner/vertical-slice.toe` exists (Plan 07 Task 7.4).
  - Projector mounted + connected as a display; camera mounted + plugged in.

  ## Launch

  Two terminals + TouchDesigner. Order matters.

  ### Terminal 1 — TouchDesigner

  1. Open `touchdesigner/vertical-slice.toe`.
  2. Verify the OSC In CHOP is listening on port 7000 (see the patch's network).
  3. Click the Window COMP's "Open" button to push the projection to the projector.
  4. Press the test-mode hotkey (e.g. F1=VALID, F2=PENDING, F3=INVALID-GHOST, F4=DISCONNECTED) to confirm all 4 visual states render. Press F5 to return to live (OSC-driven) mode.

  ### Terminal 2 — Vision pipeline

  ```
  cd vision
  source .venv/bin/activate    # Windows: .venv\Scripts\activate
  python src/run_vertical_slice.py --device 0 --target-fps 30 --show-preview \
    --log-timing /tmp/slice_timing.csv
  ```

  A small camera-preview window opens with detection overlays. Move puck (id=0) inside the camera's view.

  ### Verify the loop

  1. With NO puck on the table → projector shows DISCONNECTED (dotted rotating outline).
  2. Place puck (id=0) at the projected target zone → projector shows VALID (solid halo) and the FSM advances to PUCK_CONFIRMED.
  3. Move puck OUTSIDE the target zone → projector shows INVALID-WITH-GHOST (dashed outline at puck + pulsing ghost at target).
  4. Remove puck for >1 s → returns to DISCONNECTED.

  ## Latency check

  After 1 minute of runtime, stop the script (Ctrl+C). Check `/tmp/slice_timing.csv`:

  ```
  python -c "
  import csv
  with open('/tmp/slice_timing.csv') as f:
      rows = list(csv.DictReader(f))
  totals = [float(r['total_ms']) for r in rows if r['n_pucks'] != '0']
  print(f'mean={sum(totals)/len(totals):.1f}ms p95={sorted(totals)[int(len(totals)*0.95)]:.1f}ms n={len(totals)}')
  "
  ```

  Pass: mean < 100 ms, p95 < 150 ms.

  ## Troubleshooting

  - **No projection** — check Window COMP "Open" button and projector display selection.
  - **Camera not detected** — increment --device 0 → 1 → 2.
  - **Detection works in preview but TD never updates** — OSC port mismatch. TD listens on 7000 by default; the script sends to 7000 by default. Verify in TD's OSC In CHOP and the script's --osc-port.
  - **VALID flickers in/out** — ArUco jitter. Either tighten the marker print quality, increase tolerance in `vision/calibration/TOLERANCE.md`, OR add a small 100 ms debounce on the TD side.
  - **Projection is offset from physical puck** — calibration drift. Re-run `vision/calibration/RECALIBRATE.md`.

  ## Tear-down

  - Ctrl+C the Python script.
  - Save the .toe (CRITICAL: per CONTRIBUTING.md `.toe` files don't merge — coordinate before saving).
  - Commit `vision/calibration/TOLERANCE.md` if Task 7.6 tuned the value.
  ```</action>
  <read_first>
    - vision/src/run_vertical_slice.py (Task 7.3)
    - touchdesigner/ERROR-FEEDBACK-SPEC.md (Plan 06)
    - vision/calibration/RECALIBRATE.md (Plan 05)
    - touchdesigner/README.md (.toe coordination rules)
  </read_first>
  <acceptance_criteria>
    - `touchdesigner/VERTICAL-SLICE-RUNBOOK.md` exists.
    - Contains exactly these sections: `## Pre-requisites`, `## Launch`, `## Verify the loop`, `## Latency check`, `## Troubleshooting`, `## Tear-down`.
    - Verify-the-loop section enumerates all 4 visual states (DISCONNECTED, VALID, INVALID-WITH-GHOST) and what triggers each.
    - Latency-check section gives a concrete pass criterion (mean < 100 ms, p95 < 150 ms).
  </acceptance_criteria>
</task>

<task type="checkpoint:human-verify">
  <name>Task 7.6: End-to-end run + latency tuning + record video demo (HUMAN — full rig + recording)</name>
  <what-built>All scripts compile; the .toe patch exists; the runbook is written. The actual end-to-end run requires the physical rig (camera + projector + 1 puck minimum + TouchDesigner running) and only humans can do it.</what-built>
  <hardware_requirement>This task REQUIRES the FULL physical rig with REAL calibration YAMLs. If Plan 02-05 Task 5.6 has used the synthetic-fallback contingency, this task slips to the Phase 2.5 catch-up sub-phase. Latency cannot be measured against synthetic YAMLs (the camera-capture timing component is missing) and the video demo would not be a true vertical-slice proof.</hardware_requirement>
  <how-to-verify>
    1. Follow `touchdesigner/VERTICAL-SLICE-RUNBOOK.md` end-to-end. Total time: ~30 min including setup, debug, and tuning.
    2. Confirm all 4 visual states render correctly (DISCONNECTED, VALID, INVALID-WITH-GHOST, PENDING).
    3. Confirm the FSM advances exactly once per puck placement (no flapping). If flapping: add 100 ms debounce in TD AND/OR widen tolerance.
    4. Run the latency check from the runbook. Mean must be < 100 ms, p95 < 150 ms.
    5. Tune tolerance: if puck visually looks "in the right place" but VALID doesn't trigger, widen tolerance by 5 mm and re-test. If VALID triggers when puck is clearly off-target, narrow tolerance by 5 mm. Iterate until VALID triggers when the user perceives placement as correct.
    6. Write `vision/calibration/TOLERANCE.md` with the chosen value AND the measured ArUco jitter:

       ```markdown
       # Tolerance — Phase 2 vertical slice

       Default visual tolerance: <CHOSEN_MM> mm radius.
       Measured ArUco centroid jitter: <JITTER_PX> px std-dev (camera frame).
       Translates to ≈ <JITTER_MM> mm at the table plane.
       Tolerance set to ~3× jitter to give comfortable headroom.

       Reasoning: <one sentence on what felt right at this rig + lighting>.
       Phase 3 may set a per-puck tolerance (tighter for walls, looser for footprint pucks).
       ```

    7. Record a 30-second video demo with phone camera (overhead or side angle):
       - Start: empty table → projection shows DISCONNECTED.
       - Pick up the puck and move it INTO the target zone → VALID halo.
       - Move it OUT → INVALID-WITH-GHOST.
       - Move it back IN → VALID, FSM advances.
       - Remove puck → DISCONNECTED.
    8. Save the video to `deliverables/vertical-slice-demo.mp4`. If file size > 50 MB, compress (HandBrake or ffmpeg `-crf 28`) — per CONTRIBUTING.md large files are not committed; if compression doesn't get it under 50 MB, drop the video in shared Drive instead and add a link in the runbook.

    9. Commit everything (.toe, TOLERANCE.md, video if small enough, all Python files).
  </how-to-verify>
  <resume-signal>Type "vertical-slice-shipped" with the latency numbers AND tolerance value, OR "blocked: <what-failed>" with details. If blocked: this halts Phase 3 — all of Phase 3's success criteria depend on this slice working.</resume-signal>
</task>

</tasks>

<verification>
- All Python files (`aruco_detect.py`, `osc_send.py`, `run_vertical_slice.py`) exist and `python -m py_compile` exits 0 for each.
- `vision/tests/test_aruco_detect.py` and `test_osc_send.py` exist and pytest passes.
- `touchdesigner/vertical-slice.toe` exists (binary; verify by `git status`). EXCEPTION: if the <contingency> block above is in effect, this slips to Phase 2.5 catch-up — record the slip in the SUMMARY.
- `touchdesigner/VERTICAL-SLICE-RUNBOOK.md` contains all 6 required sections.
- `vision/calibration/TOLERANCE.md` exists with chosen tolerance value AND measured jitter. EXCEPTION: synthetic-fallback contingency defers this to Phase 2.5.
- `deliverables/vertical-slice-demo.mp4` exists (or its location is recorded in the runbook if hosted off-repo). EXCEPTION: synthetic-fallback contingency defers this to Phase 2.5.
- Latency check from runbook: mean < 100 ms, p95 < 150 ms.
- A team-member-verifiable acceptance: anyone can re-launch the demo from `VERTICAL-SLICE-RUNBOOK.md` Pre-requisites → Launch → Verify-the-loop within 5 minutes.
- If contingency was invoked: `vision/calibration/SYNTHETIC-FALLBACK.md` exists, both synthetic YAMLs are clearly marked, and a Phase 2.5 catch-up plan is queued before Phase 3 starts.
</verification>
