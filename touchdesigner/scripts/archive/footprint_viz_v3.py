"""Footprint visualizer — Script TOP callbacks v3 (numpy only, HD 1920x1080).

CHANGES v3: removed scriptOp.resize() (not available in TD 2025),
            resolution set by numpy array shape passed to copyNumpyArray.

Layout (1920x1080):
  Top-left  (0,0)→(1440,810) : footprint geometry (circles + lines)
  Top-right (1440,0)→(1920,540): status color block
  Bottom    (0,810)→(1920,1080): reserved for Text TOP overlay

OSC channels from oscin1 (osc_send.py /puck/N protocol):
  puck/N:0 = frame, puck/N:1 = proj_x, puck/N:2 = proj_y
  vision/heartbeat:0 = frame counter
"""
import numpy as np

PROJ_W = 1920
PROJ_H = 1080

FP  = (0,    0,    1440, 810)
ST  = (1440, 0,    1920, 540)
TX  = (0,    810,  1920, 1080)

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10

C_LINE    = (1.0, 1.0, 1.0, 0.8)
C_PUCK    = (0.0, 1.0, 0.4, 1.0)
C_DIVIDER = (0.25, 0.25, 0.25, 1.0)


def _status_color(hb, n_pucks):
    if hb < 0:
        return (0.15, 0.15, 0.15, 1.0)
    if n_pucks == 0:
        return (0.8, 0.8, 0.8, 1.0)
    if n_pucks < 3:
        return (0.9, 0.5, 0.0, 1.0)
    return (0.1, 0.85, 0.2, 1.0)


def cook(scriptOp):
    osc = op('oscin1')

    try:
        hb = int(osc['vision/heartbeat:0'][0])
    except Exception:
        hb = -1

    pucks = {}
    for pid in FOOTPRINT_IDS:
        try:
            pf = int(osc[f'puck/{pid}:0'][0])
            if hb >= 0 and abs(hb - pf) <= LIVENESS_FRAMES:
                pucks[pid] = (
                    float(osc[f'puck/{pid}:1'][0]),
                    float(osc[f'puck/{pid}:2'][0]),
                )
        except Exception:
            pass

    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)
    img[:, :, 3] = 1.0

    _draw_dividers(img)
    _draw_footprint(img, pucks)
    _draw_status(img, hb, len(pucks))

    scriptOp.copyNumpyArray(img)


def _draw_footprint(img, pucks):
    ids = sorted(pucks.keys())
    pts = [_remap(*pucks[i]) for i in ids]

    if len(pts) >= 2:
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            _line(img, *p1, *p2, C_LINE, 2)

    for pid, pos in pucks.items():
        _circle(img, *_remap(*pos), 14, C_PUCK, 3)


def _draw_status(img, hb, n_pucks):
    color = _status_color(hb, n_pucks)
    x0, y0, x1, y1 = ST
    pad = 12
    img[y0+pad:y1-pad, x0+pad:x1-pad] = color


def _draw_dividers(img):
    img[FP[3]:FP[3]+2, :] = C_DIVIDER
    img[:ST[3], ST[0]:ST[0]+2] = C_DIVIDER


def _remap(px, py):
    x = FP[0] + (px / PROJ_W) * (FP[2] - FP[0])
    y = FP[1] + (py / PROJ_H) * (FP[3] - FP[1])
    return x, y


def _line(img, x0, y0, x1, y1, color, width=2):
    h, w = img.shape[:2]
    n = max(int(((x1-x0)**2 + (y1-y0)**2)**0.5 * 2), 2)
    t  = np.linspace(0, 1, n)
    xs = (x0 + t*(x1-x0)).astype(int)
    ys = (y0 + t*(y1-y0)).astype(int)
    half = width // 2
    for dx in range(-half, half+1):
        for dy in range(-half, half+1):
            xc = np.clip(xs+dx, 0, w-1)
            yc = np.clip(ys+dy, 0, h-1)
            img[yc, xc] = color


def _circle(img, cx, cy, r, color, width=3):
    h, w = img.shape[:2]
    x0 = max(0, int(cx-r-width)); x1 = min(w, int(cx+r+width+1))
    y0 = max(0, int(cy-r-width)); y1 = min(h, int(cy+r+width+1))
    if x1 <= x0 or y1 <= y0:
        return
    Y, X = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((X-cx)**2 + (Y-cy)**2)
    img[y0:y1, x0:x1][(d >= r-width/2) & (d <= r+width/2)] = color
