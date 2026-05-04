"""ArUco puck detection + camera-pixel to projector-pixel mapping.

Per-frame CV core for the Phase 2 vertical slice and Phase 3 full FSM.
Reads calibration files from vision/calibration/ produced by Plan 02-05.
ARUCO_DICT_NAME MUST match cad/PUCK-SPEC.md — do not change here alone.
"""
from __future__ import annotations

import functools
from pathlib import Path

import cv2
import numpy as np
import yaml

ARUCO_DICT_NAME = "DICT_4X4_50"  # MUST match cad/PUCK-SPEC.md


@functools.lru_cache(maxsize=4)
def _load_intrinsics(path: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path) as f:
        data = yaml.safe_load(f)
    return (
        np.array(data["camera_matrix"], dtype=np.float64),
        np.array(data["dist_coeffs"], dtype=np.float64),
    )


@functools.lru_cache(maxsize=4)
def _load_homography(path: str) -> np.ndarray:
    with open(path) as f:
        data = yaml.safe_load(f)
    return np.array(data["homography"], dtype=np.float64)


def _get_aruco_detector() -> cv2.aruco.ArucoDetector:
    aruco_dict = cv2.aruco.getPredefinedDictionary(
        getattr(cv2.aruco, ARUCO_DICT_NAME)
    )
    params = cv2.aruco.DetectorParameters()
    # Tighter params to reduce false positives under projector light
    params.adaptiveThreshConstant = 7
    params.minMarkerPerimeterRate = 0.03
    params.polygonalApproxAccuracyRate = 0.04
    return cv2.aruco.ArucoDetector(aruco_dict, params)


_DETECTOR = _get_aruco_detector()


def detect_pucks_in_projector_coords(
    frame: np.ndarray,
    intrinsics_path: str,
    homography_path: str,
) -> list[dict]:
    """Detect ArUco pucks and return positions in projector-pixel space.

    Returns list of dicts:
        {
            "id": int,
            "camera_xy": (cx, cy),       # undistorted centroid in camera px
            "projector_xy": (px, py),    # mapped to projector px
            "corners_camera": ndarray    # shape (4,2), undistorted
        }
    """
    camera_matrix, dist_coeffs = _load_intrinsics(intrinsics_path)
    homography = _load_homography(homography_path)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = _DETECTOR.detectMarkers(gray)

    if ids is None:
        return []

    results = []
    for marker_corners, marker_id in zip(corners, ids.flatten()):
        # Undistort corners
        undistorted = cv2.undistortPoints(
            marker_corners, camera_matrix, dist_coeffs, P=camera_matrix
        ).reshape(4, 2)

        cx = float(undistorted[:, 0].mean())
        cy = float(undistorted[:, 1].mean())

        # Apply camera→projector homography
        cam_pt = np.array([[[cx, cy]]], dtype=np.float64)
        proj_pt = cv2.perspectiveTransform(cam_pt, homography)
        px = float(proj_pt[0, 0, 0])
        py = float(proj_pt[0, 0, 1])

        results.append({
            "id": int(marker_id),
            "camera_xy": (cx, cy),
            "projector_xy": (px, py),
            "corners_camera": undistorted,
        })

    return results


def open_camera(device_index: int = 0, width: int = 1920, height: int = 1080) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(device_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # disable autofocus — keep focus locked
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera device {device_index}")
    return cap
