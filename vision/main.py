"""
Guided Building Sketch — main application
==========================================

Setup
-----
1. Print PRINT_A3.pdf at 100% on A3.
2. Tape ID 0 (Top-Left), ID 1 (Top-Right), ID 2 (Bot-Right), ID 3 (Bot-Left)
   at the 4 corners of your table.
3. Place ID 20 / 21 / 22 cards for the 3 construction methods.
4. Measure the physical distance (mm) between marker centres and update
   PHYSICAL_W_MM / PHYSICAL_H_MM in extrusion.py.
5. Run calibrate.py once (checkerboard) — saves calibration.npz.
6. Run:  python main.py

Gestures (hand must be inside the working plane area)
------------------------------------------------------
  Index finger     hold 3 s   → place a footprint point
  Peace (V)        hold 3 s   → add window to nearest wall
  Three fingers    hold 4 s   → extrude footprint into 3-D walls
  Fist             release ~4 s → undo last action
  Fist             release ~5 s → reset / clear everything

Keys
----
  Q  quit
  P  toggle working-plane debug window
  E  toggle extrusion on/off manually
"""

import cv2
import numpy as np

from working_plane import (
    detect_working_plane,
    draw_working_plane,
    cam_to_plane,
    is_inside_plane,
    PLANE_W, PLANE_H,
    BUILD_IDS,
)
from gestures  import GestureDetector
from sketch    import BuildingSketch
from extrusion import load_calibration, estimate_pose, draw_walls

SHOW_PLANE = True

BUILD_LABELS = {
    20: "Masonry",
    21: "3D Print",
    22: "Prefab",
}

# ---------------------------------------------------------------------------
# OSC → TouchDesigner bridge (optional — requires python-osc)
# Sends sketch footprint points as /puck/N and /vision/heartbeat so the TD
# network reacts to gesture input without any code changes on the TD side.
# TD OSC In CHOP must listen on 127.0.0.1:7000 (default).
# ---------------------------------------------------------------------------
try:
    from pythonosc import udp_client as _osc_udp
    _TD_CLIENT = _osc_udp.SimpleUDPClient("127.0.0.1", 7000)
    _OSC_ENABLED = True
    print("[OSC] TouchDesigner bridge active on 127.0.0.1:7000")
except ImportError:
    _TD_CLIENT = None
    _OSC_ENABLED = False
    print("[OSC] python-osc not installed — TD bridge disabled. pip install python-osc")

# ArUco method marker → method_id (matches data/methods_db.json)
_MARKER_TO_METHOD = {20: 1, 21: 2, 22: 3}
_osc_frame = 0


def _find_external_camera():
    for idx in range(1, 5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()   # always release before deciding
            if ret:
                print(f"[CAM] Using external camera at index {idx}")
                return idx
        else:
            cap.release()   # release even if isOpened() returned False
    print("[CAM] WARNING: no external camera found — falling back to built-in webcam (index 0)")
    return 0


def main():
    cam_id = _find_external_camera()
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        print(f"Cannot open camera {cam_id}")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)   # minimise buffer to reduce gesture lag

    # Camera calibration (needed for accurate 3-D projection)
    K, dist = load_calibration()

    detector = GestureDetector()
    sketch   = BuildingSketch()

    H = H_inv = None          # homography — persists between frames
    rvec = tvec = None        # camera pose — persists between frames
    corner_pixels = None      # last known marker pixel positions
    is_extruded   = False     # whether 3-D extrusion is active
    show_plane    = SHOW_PLANE

    print(__doc__)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # ── 1. ArUco: update working plane ──────────────────────────────
        new_H, new_H_inv, build_markers, new_corners = detect_working_plane(frame)
        if new_H is not None:
            H, H_inv = new_H, new_H_inv
            corner_pixels = new_corners

        # ── 2. Camera pose for 3-D projection ───────────────────────────
        new_rv, new_tv = estimate_pose(corner_pixels, K, dist, frame)
        if new_rv is not None:
            rvec, tvec = new_rv, new_tv

        # ── 3. Hand gesture detection ────────────────────────────────────
        g = detector.process(frame)

        # ── 4. Map finger tip → working plane ───────────────────────────
        tip_cam   = g['index_tip_cam']
        tip_plane = cam_to_plane(tip_cam, H)
        tip_valid = is_inside_plane(tip_plane)

        # ── 5. Handle actions ────────────────────────────────────────────
        for action in g['actions']:
            if action == 'place_point':
                if tip_valid:
                    sketch.add_point(tip_plane)
                    print(f"[+] Point {len(sketch.points)} placed at "
                          f"({tip_plane[0]:.0f}, {tip_plane[1]:.0f})")
                else:
                    print("[!] Finger outside working plane — move inside to place point")

            elif action == 'add_window':
                walls = sketch.get_wall_segments()
                if walls:
                    idx = sketch.nearest_wall(tip_plane) if tip_valid else 0
                    sketch.add_window(idx)
                    print(f"[W] Window added to wall {idx}")
                else:
                    print("[!] No walls yet — place at least 2 points first")

            elif action == 'extrude':
                if len(sketch.get_wall_segments()) >= 1:
                    is_extruded = True
                    print("[3D] Extrusion activated")
                else:
                    print("[!] Draw at least 2 points before extruding")

            elif action == 'undo':
                sketch.undo()
                print("[<] Undo")

            elif action == 'reset':
                sketch.reset()
                is_extruded = False
                print("[X] Reset")

        # ── 5b. OSC → TouchDesigner ──────────────────────────────────────
        if _OSC_ENABLED:
            _send_to_td(sketch.points, build_markers)

        # ── 6. Draw ──────────────────────────────────────────────────────
        draw_working_plane(frame, H_inv)
        _draw_build_markers(frame, build_markers)

        if is_extruded:
            draw_walls(frame, sketch, rvec, tvec, K, dist)
        else:
            sketch.draw_on_camera(frame, H_inv,
                                  finger_tip_plane=tip_plane if tip_valid else None)

        detector.draw(frame, g)
        _draw_status(frame, H, sketch, tip_valid, is_extruded)

        cv2.imshow("Building Sketch", frame)

        if show_plane:
            plane_img = np.zeros((PLANE_H, PLANE_W, 3), dtype=np.uint8)
            sketch.draw_on_plane(plane_img)
            if tip_valid:
                tx, ty = int(tip_plane[0]), int(tip_plane[1])
                cv2.circle(plane_img, (tx, ty), 6, (0, 180, 255), -1)
            cv2.imshow("Working Plane (top-down)", plane_img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('p'):
            show_plane = not show_plane
            if not show_plane:
                cv2.destroyWindow("Working Plane (top-down)")
        if key == ord('e'):
            is_extruded = not is_extruded
            print(f"[E] Extrusion {'ON' if is_extruded else 'OFF'}")

    detector.close()
    cap.release()
    cv2.destroyAllWindows()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _draw_status(frame, H, sketch, tip_valid, is_extruded):
    h      = frame.shape[0]
    n_pts  = len(sketch.points)
    n_seg  = len(sketch.get_wall_segments())
    n_win  = len(sketch.windows)

    if H is None:
        msg   = "WORKING PLANE NOT DETECTED  — show IDs 0,1,2,3 at table corners"
        color = (0, 60, 255)
    else:
        in_out = "IN PLANE" if tip_valid else "outside"
        mode   = "3D EXTRUDED" if is_extruded else "2D sketch"
        msg    = (f"Pts:{n_pts}  Walls:{n_seg}  Win:{n_win}  "
                  f"|  finger:{in_out}  |  {mode}")
        color  = (0, 200, 100) if is_extruded else (200, 200, 200)

    cv2.putText(frame, msg, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)


def _draw_build_markers(frame, build_markers):
    for mid, center in build_markers.items():
        label = BUILD_LABELS.get(mid, f"Type {mid}")
        cx, cy = int(center[0]), int(center[1])
        cv2.circle(frame, (cx, cy), 8, (200, 80, 255), -1)
        cv2.putText(frame, label, (cx + 12, cy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 80, 255), 2)


def _send_to_td(points, build_markers):
    """Send current sketch state to TouchDesigner via OSC (legacy schema).

    Sketch points → /puck/N [frame, proj_x, proj_y]
    Heartbeat     → /vision/heartbeat [frame]
    Method token  → /method/id [method_id]  (TD needs a separate OSC In CHOP for this)

    Coords are remapped from working-plane pixels (PLANE_W×PLANE_H) to
    projector pixels (1280×720) so the TD footprint panel renders correctly.
    """
    global _osc_frame
    proj_w, proj_h = 1280, 720

    for i, (px, py) in enumerate(points):
        proj_x = float(np.clip((px / PLANE_W) * proj_w, 0, proj_w))
        proj_y = float(np.clip((py / PLANE_H) * proj_h, 0, proj_h))
        _TD_CLIENT.send_message(f"/puck/{i}", [_osc_frame, proj_x, proj_y])

    if not points:
        # Explicit clear: age out all 10 puck channels so TD stops drawing them.
        # Sending a frame value guaranteed to fail the liveness check (hb - LIVENESS_FRAMES - 1).
        stale_frame = max(0, _osc_frame - 11)
        for i in range(10):
            _TD_CLIENT.send_message(f"/puck/{i}", [stale_frame, 0.0, 0.0])

    _TD_CLIENT.send_message("/vision/heartbeat", [_osc_frame])

    method_id = 0
    for mid in build_markers:
        mapped = _MARKER_TO_METHOD.get(mid)
        if mapped is not None:
            method_id = mapped
            break
    _TD_CLIENT.send_message("/method/id", [method_id])

    _osc_frame = (_osc_frame + 1) % 100000


if __name__ == '__main__':
    main()
