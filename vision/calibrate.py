"""
Camera calibration — saves intrinsic matrix K and distortion coefficients to calibration.npz.

How to use:
  1. Print a 9x6 inner-corner checkerboard at 100% scale (search "opencv checkerboard 9x6 pdf").
  2. Measure one square side in mm and set SQUARE_MM below.
  3. Run:  python calibrate.py
  4. Press SPACE to capture a frame — aim for 15-20 from varied angles/distances/rotations.
  5. Press C once you have enough — calibration runs and saves calibration.npz.
  6. Press R to discard all frames and start over.
  7. Press Q to quit without saving.

A good RMS reprojection error is below 0.5 px. Above 1.0 px means the AR projection
will visibly drift — recapture with more varied angles.
"""

import cv2
import numpy as np
import os

CHESSBOARD = (9, 6)     # inner corner count (cols, rows)
SQUARE_MM  = 25.0       # physical size of one square in mm — measure your printout
MIN_FRAMES = 10
OUT_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibration.npz')

_obj_template = np.zeros((CHESSBOARD[0] * CHESSBOARD[1], 3), np.float32)
_obj_template[:, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)
_obj_template *= SQUARE_MM

_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def _find_external_camera():
    for idx in range(1, 5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return idx
    return 0


def _reprojection_error(obj_pts, img_pts, rvecs, tvecs, K, dist):
    total, count = 0.0, 0
    for op, ip, rv, tv in zip(obj_pts, img_pts, rvecs, tvecs):
        proj, _ = cv2.projectPoints(op, rv, tv, K, dist)
        total  += cv2.norm(ip, proj, cv2.NORM_L2) ** 2
        count  += len(op)
    return (total / count) ** 0.5


def main():
    cam_id = _find_external_camera()
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(cam_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print(__doc__)
    print(f"[CAM] Using camera index {cam_id}")

    obj_pts, img_pts = [], []

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        grey  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(grey, CHESSBOARD, None)
        display = frame.copy()

        if found:
            corners2 = cv2.cornerSubPix(grey, corners, (11, 11), (-1, -1), _criteria)
            cv2.drawChessboardCorners(display, CHESSBOARD, corners2, found)
            cv2.putText(display, "Checkerboard FOUND — SPACE to capture",
                        (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 220, 0), 2)
        else:
            cv2.putText(display, "Checkerboard not found",
                        (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 50, 255), 2)

        n       = len(obj_pts)
        ready   = n >= MIN_FRAMES
        status  = f"Frames: {n}  |  {'Press C to calibrate' if ready else f'{MIN_FRAMES - n} more needed'}"
        cv2.putText(display, status, (10, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        cv2.putText(display, "SPACE capture | C calibrate | R reset | Q quit",
                    (10, display.shape[0] - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (140, 140, 140), 1)

        cv2.imshow("Camera Calibration", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        if key == ord(' ') and found:
            obj_pts.append(_obj_template.copy())
            img_pts.append(corners2)
            print(f"[+] Captured frame {n + 1}")

        if key == ord('r'):
            obj_pts.clear()
            img_pts.clear()
            print("[R] All captures discarded.")

        if key == ord('c') and ready:
            print(f"\n[CAL] Calibrating with {n} frames...")
            h, w = frame.shape[:2]
            rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
                obj_pts, img_pts, (w, h), None, None
            )
            mean_err = _reprojection_error(obj_pts, img_pts, rvecs, tvecs, K, dist)
            print(f"[CAL] RMS reprojection error : {rms:.4f} px  ({'OK' if rms < 0.5 else 'acceptable' if rms < 1.0 else 'HIGH — recapture'})")
            print(f"[CAL] Mean point error       : {mean_err:.4f} px")
            print(f"[CAL] K =\n{K}")
            np.savez(OUT_PATH, K=K, dist=dist, image_size=np.array([w, h]))
            print(f"[OK] Saved to: {OUT_PATH}")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
