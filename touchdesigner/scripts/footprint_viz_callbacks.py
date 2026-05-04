"""Footprint visualizer — Script TOP callbacks for TouchDesigner (numpy only).

Reads per-puck OSC data from oscin1, draws:
  - Circles at each detected puck center
  - Lines connecting pucks in ID order (polygon)

Resolution: 1280x720. No external libs required — pure numpy.
Text labels (distances, area) are handled by a separate Text TOP in TD.
"""
import numpy as np

PROJ_W = 1280
PROJ_H = 720
FOOTPRINT_IDS = list(range(10))
LIVENESS_FRAMES = 10

COLOR_LINE  = (1.0, 1.0, 1.0, 0.8)
COLOR_PUCK  = (0.0, 1.0, 0.4, 1.0)
COLOR_NONE  = (0.3, 0.3, 0.3, 1.0)  # single dot when vision offline


def cook(scriptOp):
    osc = op('oscin1')

    try:
        hb = int(osc['vision/heartbeat:0'][0])
    except Exception:
        hb = -1

    pucks = {}
    for pid in FOOTPRINT_IDS:
        try:
            puck_frame = int(osc[f'puck/{pid}:0'][0])
            if hb >= 0 and abs(hb - puck_frame) <= LIVENESS_FRAMES:
                px = float(osc[f'puck/{pid}:1'][0])
                py = float(osc[f'puck/{pid}:2'][0])
                pucks[pid] = (px, py)
        except Exception:
            pass

    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)

    ids_sorted = sorted(pucks.keys())
    pts = [pucks[i] for i in ids_sorted]

    if len(pts) >= 2:
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            _draw_line(img, p1[0], p1[1], p2[0], p2[1], COLOR_LINE, width=2)

    for pid, (px, py) in pucks.items():
        _draw_circle(img, px, py, 14, COLOR_PUCK, width=3)

    scriptOp.copyNumpyArray(img)


def _draw_line(img, x0, y0, x1, y1, color, width=2):
    h, w = img.shape[:2]
    length = max(int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 2), 2)
    t = np.linspace(0, 1, length)
    xs = (x0 + t * (x1 - x0)).astype(int)
    ys = (y0 + t * (y1 - y0)).astype(int)
    half = width // 2
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            xc = np.clip(xs + dx, 0, w - 1)
            yc = np.clip(ys + dy, 0, h - 1)
            img[yc, xc] = color


def _draw_circle(img, cx, cy, r, color, width=3):
    h, w = img.shape[:2]
    x0 = max(0, int(cx - r - width))
    x1 = min(w, int(cx + r + width + 1))
    y0 = max(0, int(cy - r - width))
    y1 = min(h, int(cy + r + width + 1))
    if x1 <= x0 or y1 <= y0:
        return
    Y, X = np.mgrid[y0:y1, x0:x1]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    mask = (dist >= r - width / 2) & (dist <= r + width / 2)
    img[y0:y1, x0:x1][mask] = color
