"""
Building sketch state: footprint points, wall segments, and window openings.

All coordinates are in working-plane space (0..PLANE_W, 0..PLANE_H).
"""

import cv2
import numpy as np


class BuildingSketch:
    def __init__(self):
        self.points  = []    # [(x, y), ...] in working-plane coords
        self.windows = set() # wall segment indices that have windows
        self._history = []   # undo stack

    # ------------------------------------------------------------------
    # Mutation helpers (all changes go through these so undo works)
    # ------------------------------------------------------------------
    def add_point(self, pt):
        self._history.append(('del_point', len(self.points)))
        self.points.append((float(pt[0]), float(pt[1])))

    def add_window(self, wall_idx):
        if wall_idx not in self.windows:
            self._history.append(('del_window', wall_idx))
            self.windows.add(wall_idx)

    def undo(self):
        if not self._history:
            return
        op, data = self._history.pop()
        if op == 'del_point' and self.points:
            self.points.pop()
            # drop any window referencing the now-gone last segment
            last_wall = len(self.points) - 1
            self.windows.discard(last_wall)
            self.windows.discard(len(self.points))
        elif op == 'del_window':
            self.windows.discard(data)

    def reset(self):
        self.points.clear()
        self.windows.clear()
        self._history.clear()

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def get_wall_segments(self):
        """Return list of ((x0,y0),(x1,y1)) for every wall segment."""
        n = len(self.points)
        if n < 2:
            return []
        segs = [(self.points[i], self.points[i + 1]) for i in range(n - 1)]
        if n >= 3:
            segs.append((self.points[-1], self.points[0]))   # closing segment
        return segs

    def nearest_wall(self, pt_plane):
        """Return index of the wall segment whose midline is closest to pt_plane."""
        segs = self.get_wall_segments()
        if not segs:
            return None
        pt   = np.array(pt_plane, dtype=np.float64)
        best_i, best_d = 0, float('inf')
        for i, (a, b) in enumerate(segs):
            a = np.array(a, dtype=np.float64)
            b = np.array(b, dtype=np.float64)
            ab = b - a
            denom = float(np.dot(ab, ab))
            if denom < 1e-9:
                proj = a
            else:
                t    = np.clip(np.dot(pt - a, ab) / denom, 0.0, 1.0)
                proj = a + t * ab
            d = float(np.linalg.norm(pt - proj))
            if d < best_d:
                best_d, best_i = d, i
        return best_i

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw_on_plane(self, plane_img):
        """Render the sketch onto a working-plane image (pure top-down view)."""
        segs = self.get_wall_segments()
        for i, (a, b) in enumerate(segs):
            ai = _ipt(a)
            bi = _ipt(b)
            if i in self.windows:
                _draw_wall_with_window(plane_img, ai, bi)
            else:
                cv2.line(plane_img, ai, bi, (220, 220, 220), 2)

        for idx, pt in enumerate(self.points):
            pi = _ipt(pt)
            cv2.circle(plane_img, pi, 7, (0, 230, 100), -1)
            cv2.putText(plane_img, str(idx + 1),
                        (pi[0] + 9, pi[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 230, 100), 1)

    def draw_on_camera(self, frame, H_inv, finger_tip_plane=None):
        """Project the sketch back onto the camera frame using the inverse homography."""
        from working_plane import plane_to_cam

        segs = self.get_wall_segments()
        for i, (a, b) in enumerate(segs):
            ac = plane_to_cam(a, H_inv)
            bc = plane_to_cam(b, H_inv)
            if ac is None or bc is None:
                continue
            if i in self.windows:
                _draw_wall_with_window(frame, ac, bc, color=(255, 140, 0), bg=(80, 50, 0))
            else:
                cv2.line(frame, ac, bc, (220, 220, 220), 2)

        for pt in self.points:
            pc = plane_to_cam(pt, H_inv)
            if pc:
                cv2.circle(frame, pc, 7, (0, 230, 100), -1)

        if finger_tip_plane is not None:
            tc = plane_to_cam(finger_tip_plane, H_inv)
            if tc:
                cv2.circle(frame, tc, 6, (0, 180, 255), -1)
                cv2.circle(frame, tc, 12, (0, 180, 255), 1)


# ------------------------------------------------------------------
# Private helpers
# ------------------------------------------------------------------

def _ipt(pt):
    return (int(pt[0]), int(pt[1]))


def _draw_wall_with_window(img, a, b, color=(255, 140, 0), bg=(60, 30, 0)):
    """Draw a wall segment with a centred window cutout marker."""
    cv2.line(img, a, b, color, 3)
    # small rectangle at midpoint to indicate window
    mx, my = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
    dx,  dy  = b[0] - a[0], b[1] - a[1]
    length   = max((dx**2 + dy**2) ** 0.5, 1)
    nx, ny   = int(-dy / length * 8), int(dx / length * 8)  # perpendicular
    hx, hy   = int(dx / length * 12), int(dy / length * 12)  # along wall
    rect = np.array([
        [mx - hx + nx, my - hy + ny],
        [mx + hx + nx, my + hy + ny],
        [mx + hx - nx, my + hy - ny],
        [mx - hx - nx, my - hy - ny],
    ], dtype=np.int32)
    cv2.fillPoly(img, [rect], bg)
    cv2.polylines(img, [rect], True, color, 2)
