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

Red puck (point placement — puck must be inside the working plane)
------------------------------------------------------------------
  Hold puck still 3 s          → place a footprint corner point
  Move puck away then back      → re-arm for next placement

Hand gestures (secondary interactions — anywhere in frame)
----------------------------------------------------------
  Flat fist   (palm down, horizontal)  hold 2 s → undo last point
  Upright fist (raised vertically)     hold 5 s → reset entire sketch
  Index finger up                      hold 3 s → extrude walls into 3-D
  Peace / V   (index + middle up)      hold 2 s → add window to nearest wall

Keys
----
  Q  quit
  P  toggle working-plane debug window
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
from puck_detector    import RedPuckDetector
from gesture_detector import GestureDetector
from sketch           import BuildingSketch
from extrusion        import load_calibration, estimate_pose, draw_walls
from osc_bridge       import VisionBridge

SHOW_PLANE = True

BUILD_LABELS = {
    20: "Masonry",
    21: "3D Print",
    22: "Prefab",
}


def _find_external_camera():
    for idx in range(1, 5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print(f"[CAM] Using external camera at index {idx}")
                return idx
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

    # Camera calibration (needed for accurate 3-D projection)
    K, dist = load_calibration()

    puck     = RedPuckDetector()
    gestures = GestureDetector()
    sketch   = BuildingSketch()
    bridge   = VisionBridge()

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

        # ── 3. Detection — puck (placement) + hand (secondary actions) ──
        g_puck = puck.process(frame)
        g_hand = gestures.process(frame)

        # ── 3b. Send all state to TouchDesigner via OSC ──────────────────
        # Hand gesture takes priority in the bridge when it is active.
        bridge.send_frame(
            build_markers=build_markers,
            gesture_result=g_hand if g_hand['gesture'] != 'none' else g_puck,
            sketch=sketch,
            is_extruded=is_extruded,
            H=H,
        )

        # ── 4. Map positions → working plane ────────────────────────────
        # Puck centre → point placement
        tip_cam   = g_puck['index_tip_cam']
        tip_plane = cam_to_plane(tip_cam, H)
        tip_valid = is_inside_plane(tip_plane)

        # Hand index tip → wall selection for add_window
        hand_cam   = g_hand['index_tip_cam']
        hand_plane = cam_to_plane(hand_cam, H)
        hand_valid = is_inside_plane(hand_plane)

        # ── 5. Handle puck actions ───────────────────────────────────────
        for action in g_puck['actions']:
            if action == 'place_point':
                if tip_valid:
                    sketch.add_point(tip_plane)
                    print(f"[+] Point {len(sketch.points)} placed at "
                          f"({tip_plane[0]:.0f}, {tip_plane[1]:.0f})")
                else:
                    print("[!] Puck outside working plane — move inside to place point")

        # ── 5b. Handle gesture actions ───────────────────────────────────
        for action in g_hand['actions']:
            if action == 'undo':
                sketch.undo()
                print("[<] Undo")

            elif action == 'reset':
                sketch.reset()
                is_extruded = False
                print("[X] Reset")

            elif action == 'extrude':
                if len(sketch.get_wall_segments()) >= 1:
                    is_extruded = True
                    print("[3D] Extrusion activated")
                else:
                    print("[!] Draw at least 2 points before extruding")

            elif action == 'add_window':
                walls = sketch.get_wall_segments()
                if walls:
                    ref = hand_plane if hand_valid else tip_plane
                    idx = sketch.nearest_wall(ref) if ref else 0
                    sketch.add_window(idx)
                    print(f"[W] Window added to wall {idx}")
                else:
                    print("[!] No walls yet — place at least 2 points first")

        # ── 6. Draw ──────────────────────────────────────────────────────
        draw_working_plane(frame, H_inv)
        _draw_build_markers(frame, build_markers)

        if is_extruded:
            draw_walls(frame, sketch, rvec, tvec, K, dist)
        else:
            sketch.draw_on_camera(frame, H_inv,
                                  finger_tip_plane=tip_plane if tip_valid else None)

        puck.draw(frame, g_puck)
        gestures.draw(frame, g_hand)
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

    gestures.close()
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
                  f"|  puck:{in_out}  |  {mode}")
        color  = (0, 200, 100) if is_extruded else (200, 200, 200)

    cv2.putText(frame, msg, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)


def _draw_build_markers(frame, build_markers):
    for mid, center in build_markers.items():
        label = BUILD_LABELS.get(mid, f"Type {mid}")
        cx, cy = int(center[0]), int(center[1])
        cv2.circle(frame, (cx, cy), 8, (200, 80, 255), -1)
        cv2.putText(frame, label, (cx + 12, cy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 80, 255), 2)


if __name__ == '__main__':
    main()
