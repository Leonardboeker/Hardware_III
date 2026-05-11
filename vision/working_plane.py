"""
Working plane computation from 4 ArUco corner markers (DICT_4X4_100).

Uses 4 footprint markers from PRINT_A3.pdf as table corners:
    ID 0 (Top-Left)  ───────  ID 1 (Top-Right)
         │                         │
         │        workspace        │
         │                         │
    ID 3 (Bot-Left) ───────  ID 2 (Bot-Right)

Building-type selectors (also from PRINT_A3.pdf):
    ID 20 = Masonry  |  ID 21 = 3D Print  |  ID 22 = Prefab
"""

import cv2
import numpy as np

ARUCO_DICT  = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
DETECTOR    = cv2.aruco.ArucoDetector(ARUCO_DICT, cv2.aruco.DetectorParameters())

CORNER_IDS  = {0: 0, 1: 1, 2: 2, 3: 3}   # id → corner index (TL TR BR BL)
BUILD_IDS   = [20, 21, 22]                 # building-type markers

PLANE_W, PLANE_H = 900, 600                     # virtual working-plane size (px)

# Destination corners: TL, TR, BR, BL
_DST = np.array(
    [[0, 0], [PLANE_W, 0], [PLANE_W, PLANE_H], [0, PLANE_H]],
    dtype=np.float32,
)


def detect_working_plane(frame):
    """
    Returns (H, H_inv, build_markers, corner_pixels) where:
      H             camera → working plane  (None if < 4 corners visible)
      H_inv         working plane → camera  (None if < 4 corners visible)
      build_markers {id: center_px}  for building-type markers found this frame
      corner_pixels (4, 2) float32 array of marker centres TL TR BR BL, or None
    """
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners_raw, ids, _ = DETECTOR.detectMarkers(grey)

    H = H_inv = None
    build_markers  = {}
    corner_pixels  = None

    if ids is None:
        return H, H_inv, build_markers, corner_pixels

    src_corners = [None, None, None, None]
    for i, mid in enumerate(ids.flatten().tolist()):
        if mid in CORNER_IDS:
            center = corners_raw[i][0].mean(axis=0)
            src_corners[CORNER_IDS[mid]] = center
        elif mid in BUILD_IDS:
            center = corners_raw[i][0].mean(axis=0)
            build_markers[mid] = center

    if all(c is not None for c in src_corners):
        src = np.array(src_corners, dtype=np.float32)
        H,     _ = cv2.findHomography(src, _DST)
        H_inv, _ = cv2.findHomography(_DST, src)
        if H is not None:
            corner_pixels = src   # shape (4, 2), order TL TR BR BL

    return H, H_inv, build_markers, corner_pixels


def cam_to_plane(pt_cam, H):
    """Map a camera-space (x, y) point to working-plane coords. Returns None if H is None."""
    if H is None or pt_cam is None:
        return None
    pt = np.array([[[float(pt_cam[0]), float(pt_cam[1])]]], dtype=np.float32)
    res = cv2.perspectiveTransform(pt, H)
    return (float(res[0][0][0]), float(res[0][0][1]))


def plane_to_cam(pt_plane, H_inv):
    """Map a working-plane (x, y) back to camera pixel coords. Returns None if H_inv is None."""
    if H_inv is None or pt_plane is None:
        return None
    pt = np.array([[[float(pt_plane[0]), float(pt_plane[1])]]], dtype=np.float32)
    res = cv2.perspectiveTransform(pt, H_inv)
    return (int(res[0][0][0]), int(res[0][0][1]))


def is_inside_plane(pt_plane):
    """Return True if the working-plane point is within the plane bounds."""
    if pt_plane is None:
        return False
    x, y = pt_plane
    return 0 <= x <= PLANE_W and 0 <= y <= PLANE_H


def draw_working_plane(frame, H_inv, color=(0, 220, 80), thickness=2):
    """Draw the working-plane boundary onto the camera frame."""
    if H_inv is None:
        return
    pts = [
        plane_to_cam((0,       0),       H_inv),
        plane_to_cam((PLANE_W, 0),       H_inv),
        plane_to_cam((PLANE_W, PLANE_H), H_inv),
        plane_to_cam((0,       PLANE_H), H_inv),
    ]
    if any(p is None for p in pts):
        return
    poly = np.array(pts, dtype=np.int32)
    cv2.polylines(frame, [poly], isClosed=True, color=color, thickness=thickness)
