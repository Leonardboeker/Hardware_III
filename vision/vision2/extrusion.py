"""
3D AR extrusion — camera pose estimation and wall rendering.

Physical coordinate system (world space, all units in mm):
  Origin  = ID-0 marker centre (Top-Left corner)
  X-axis  = rightward toward ID-1 (Top-Right)
  Y-axis  = downward toward ID-3 (Bot-Left)
  Z-axis  = upward from table surface (toward camera)

SETUP REQUIRED:
  1. Measure the physical distance between marker centres on your printed sheet.
  2. Update PHYSICAL_W_MM and PHYSICAL_H_MM below to match.
  3. Run calibrate.py once and ensure calibration.npz is in the same folder.

MODULAR FBX:
  Use ModularFBX to place your own FBX models along wall segments.
  FBX convention: model runs along +X, height in +Z, origin at bottom-left face corner.
  Requires:  pip install trimesh
"""

import os
import cv2
import numpy as np

# ── CONFIGURE THESE to match your printed sheet ──────────────────────────────
PHYSICAL_W_MM  = 594.0   # mm between ID-0 and ID-1 marker centres (measure!)
PHYSICAL_H_MM  = 420.0   # mm between ID-0 and ID-3 marker centres (measure!)
WALL_HEIGHT_MM = 80.0    # virtual wall height in mm — tune to taste
# ─────────────────────────────────────────────────────────────────────────────

_CAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibration.npz')

# 3-D world positions of the 4 ArUco corner markers, order TL TR BR BL (z = 0)
_CORNERS_3D = np.array([
    [0,             0,             0],
    [PHYSICAL_W_MM, 0,             0],
    [PHYSICAL_W_MM, PHYSICAL_H_MM, 0],
    [0,             PHYSICAL_H_MM, 0],
], dtype=np.float32)

_WALL_COLOR    = (210, 210, 210)
_WINWALL_COLOR = (200, 130,  50)
_WIN_COLOR     = (210, 185, 100)
_OUTLINE_COLOR = ( 70,  70,  70)
_TOPEDGE_COLOR = (255, 255, 255)


# ── Calibration ───────────────────────────────────────────────────────────────

def load_calibration():
    """Load K and dist from calibration.npz. Returns (None, None) if file missing."""
    if not os.path.exists(_CAL_PATH):
        print("[WARN] calibration.npz not found — run calibrate.py for accurate AR.")
        print("       Falling back to approximate K (may drift at frame edges).")
        return None, None
    d = np.load(_CAL_PATH)
    print(f"[OK] Camera calibration loaded from {_CAL_PATH}")
    return d['K'].astype(np.float64), d['dist'].astype(np.float64)


def _approx_K(frame):
    h, w = frame.shape[:2]
    f = float(max(w, h))
    return (np.array([[f, 0, w/2], [0, f, h/2], [0, 0, 1]], np.float64),
            np.zeros((4, 1), np.float64))


# ── Pose estimation ───────────────────────────────────────────────────────────

def estimate_pose(corner_pixels, K, dist, frame=None):
    """
    Compute camera pose each frame using the 4 ArUco corner pixel positions.

    corner_pixels : (4, 2) float array, order TL TR BR BL — from working_plane.py
    K, dist       : from load_calibration() — pass None to use approximation
    frame         : needed only when K is None (to derive image size for approx K)

    Returns (rvec, tvec) or (None, None) if fewer than 4 corners visible.
    """
    if corner_pixels is None:
        return None, None
    if K is None:
        if frame is None:
            return None, None
        K, dist = _approx_K(frame)

    pts = np.array(corner_pixels, dtype=np.float32).reshape(4, 2)
    ok, rvec, tvec = cv2.solvePnP(
        _CORNERS_3D, pts, K, dist,
        flags=cv2.SOLVEPNP_SQPNP,
    )
    return (rvec, tvec) if ok else (None, None)


# ── Coordinate helpers ────────────────────────────────────────────────────────

def _to_world(pt_plane, z=0.0):
    """Convert working-plane pixel coord → world mm coord."""
    from working_plane import PLANE_W, PLANE_H
    return [
        float(pt_plane[0]) * PHYSICAL_W_MM / PLANE_W,
        float(pt_plane[1]) * PHYSICAL_H_MM / PLANE_H,
        z,
    ]


def _proj(pts_3d, rvec, tvec, K, dist):
    p, _ = cv2.projectPoints(
        np.array(pts_3d, np.float32), rvec, tvec, K, dist
    )
    return p.reshape(-1, 2).astype(int)


def _wall_quad(a, b, h, rvec, tvec, K, dist):
    """
    Project the 4 corners of wall face A→B at height h.
    Returns int array shape (4, 2): [A_base, B_base, B_top, A_top].
    """
    a3 = _to_world(a, 0)
    b3 = _to_world(b, 0)
    return _proj([a3, b3, [b3[0], b3[1], h], [a3[0], a3[1], h]],
                 rvec, tvec, K, dist)


def _lerp(p, q, t):
    return (int(p[0] + (q[0] - p[0]) * t),
            int(p[1] + (q[1] - p[1]) * t))


def _window_poly(pts):
    """
    pts: [A_base, B_base, B_top, A_top] in image coords.
    Returns a 4-point window polygon spanning 25–75 % of width, 15–70 % of height.
    """
    def face_pt(t, s):
        bot = _lerp(pts[0], pts[1], t)
        top = _lerp(pts[3], pts[2], t)
        return _lerp(bot, top, s)

    return np.array([
        face_pt(0.25, 0.15),
        face_pt(0.75, 0.15),
        face_pt(0.75, 0.70),
        face_pt(0.25, 0.70),
    ], dtype=np.int32)


# ── Main draw function ────────────────────────────────────────────────────────

def draw_walls(frame, sketch, rvec, tvec, K, dist):
    """
    Overlay extruded 3-D walls onto frame in place.
    Walls are semi-transparent filled quads; window segments show an opening.
    """
    if rvec is None:
        return

    if K is None:
        K, dist = _approx_K(frame)

    segs = sketch.get_wall_segments()
    if not segs:
        return

    # Collect quads first for depth sorting (far → near)
    quads = []
    for i, (a, b) in enumerate(segs):
        pts  = _wall_quad(a, b, WALL_HEIGHT_MM, rvec, tvec, K, dist)
        # centroid depth: use base midpoint projected depth as proxy
        mid3 = np.array(_to_world(
            ((a[0]+b[0])/2, (a[1]+b[1])/2)
        ), dtype=np.float32)
        R, _ = cv2.Rodrigues(rvec)
        depth = float((R @ mid3.reshape(3,1) + tvec)[2])
        quads.append((depth, i, pts))

    quads.sort(key=lambda x: -x[0])   # far to near

    overlay = frame.copy()
    for depth, i, pts in quads:
        has_win = i in sketch.windows
        color   = _WINWALL_COLOR if has_win else _WALL_COLOR
        cv2.fillPoly(overlay, [pts], color)
        if has_win:
            cv2.fillPoly(overlay, [_window_poly(pts)], _WIN_COLOR)

    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    # Sharp outlines and top edges drawn after blend
    for _, i, pts in quads:
        cv2.polylines(frame, [pts.reshape(1, -1, 2)], True, _OUTLINE_COLOR, 1)
        cv2.line(frame, tuple(pts[2]), tuple(pts[3]), _TOPEDGE_COLOR, 2)
        if i in sketch.windows:
            win = _window_poly(pts)
            cv2.polylines(frame, [win.reshape(1, -1, 2)], True, (255, 220, 80), 1)


# ── Optional: modular FBX walls ───────────────────────────────────────────────

class ModularFBX:
    """
    Render FBX models along each wall segment.

    Requires:  pip install trimesh

    Expected FBX coordinate convention:
      +X  = along wall length  (model will be scaled and rotated to fit)
      +Z  = upward (wall height)
      +Y  = outward (wall depth/thickness)
      Origin at bottom-left face corner of the module.

    Example:
        mfbx = ModularFBX('wall_panel.fbx', window_fbx='wall_window.fbx')
        # in the draw loop (when extruded):
        mfbx.draw(frame, sketch, rvec, tvec, K, dist)
    """

    def __init__(self, wall_fbx, window_fbx=None):
        try:
            import trimesh
            self._trimesh = trimesh
        except ImportError:
            raise RuntimeError("trimesh is not installed — run: pip install trimesh")

        self._wall_mesh   = trimesh.load(wall_fbx,   force='mesh')
        self._win_mesh    = (trimesh.load(window_fbx, force='mesh')
                             if window_fbx else None)
        print(f"[FBX] Wall module loaded: {wall_fbx}")
        if window_fbx:
            print(f"[FBX] Window module loaded: {window_fbx}")

    def draw(self, frame, sketch, rvec, tvec, K, dist):
        """Project and render FBX modules for every wall segment."""
        if rvec is None:
            return
        if K is None:
            K, dist = _approx_K(frame)

        segs = sketch.get_wall_segments()
        for i, (a, b) in enumerate(segs):
            mesh = (self._win_mesh if (i in sketch.windows and self._win_mesh)
                    else self._wall_mesh)
            self._render_segment(frame, mesh, a, b, rvec, tvec, K, dist)

    def _render_segment(self, frame, mesh, a, b, rvec, tvec, K, dist):
        a3 = np.array(_to_world(a), dtype=np.float64)
        b3 = np.array(_to_world(b), dtype=np.float64)

        wall_vec = b3 - a3
        wall_len = float(np.linalg.norm(wall_vec[:2]))
        if wall_len < 1e-6:
            return

        angle    = float(np.arctan2(wall_vec[1], wall_vec[0]))
        mesh_len = float(mesh.bounds[1][0] - mesh.bounds[0][0])
        sx       = wall_len / mesh_len if mesh_len > 1e-6 else 1.0

        ca, sa = np.cos(angle), np.sin(angle)
        T = np.array([
            [sx * ca, -sa, 0, a3[0]],
            [sx * sa,  ca, 0, a3[1]],
            [0,         0, 1, 0    ],
            [0,         0, 0, 1    ],
        ], dtype=np.float64)

        verts   = np.hstack([mesh.vertices, np.ones((len(mesh.vertices), 1))])
        world_v = (T @ verts.T).T[:, :3].astype(np.float32)

        proj, _ = cv2.projectPoints(world_v, rvec, tvec, K, dist)
        proj    = proj.reshape(-1, 2).astype(int)

        # depth-sort faces (far to near)
        R, _ = cv2.Rodrigues(rvec)
        centroids   = world_v[mesh.faces].mean(axis=1)
        cam_depths  = (R @ centroids.T + tvec).T[:, 2]
        order       = np.argsort(-cam_depths)

        overlay = frame.copy()
        for fi in order:
            face_idx = mesh.faces[fi]
            pts_2d   = proj[face_idx]
            cv2.fillConvexPoly(overlay, pts_2d, (210, 210, 210))
            cv2.polylines(frame, [pts_2d.reshape(-1, 1, 2)], True, (70, 70, 70), 1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
