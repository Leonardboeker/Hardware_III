"""Footprint visualizer — Script TOP v5.

CHANGES v5:
  - Polygon fill (ray-casting, numpy-only) with per-method color
  - Pucks sorted by angle from centroid → correct convex outline
  - Status zone shows method color band + heartbeat bar
  - Reads method_id from Script CHOP named 'state1'
  - Still 1280×720 (TD Non-Commercial limit)

Layout (1280×720):
  FP  (0,0)→(960,540)    top-left : footprint geometry
  ST  (960,0)→(1280,540)  top-right: method status panel
  TX  (0,540)→(1280,720)  bottom   : stats text (Text TOP overlay)

OSC (oscin1):
  puck/N:0 = frame   puck/N:1 = proj_x   puck/N:2 = proj_y
  vision/heartbeat:0 = frame counter

state1 CHOP channels (optional — falls back to OSC-only if absent):
  method_id   (int 0-4)
  hb_alive    (1 = pipeline running, 0 = offline)
"""
import math
import numpy as np

PROJ_W = 1280
PROJ_H = 720

FP = (0,   0,    960,  540)
ST = (960, 0,   1280,  540)
TX = (0,   540, 1280,  720)

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10

C_LINE    = (1.0, 1.0, 1.0, 0.85)
C_PUCK    = (1.0, 1.0, 1.0, 1.0)
C_DIVIDER = (0.2, 0.2, 0.2, 1.0)
C_BG      = (0.05, 0.05, 0.05, 1.0)

METHOD_COLORS = {
    0: (0.4,  0.4,  0.4),   # none / offline
    1: (0.0,  0.55, 1.0),   # cantilever — blue
    2: (1.0,  0.38, 0.0),   # column grid — orange
    3: (0.75, 0.08, 0.82),  # arch — purple
    4: (0.95, 0.75, 0.0),   # truss — yellow
}

METHOD_NAMES = {
    0: "NO METHOD",
    1: "CANTILEVER",
    2: "COLUMN GRID",
    3: "ARCH",
    4: "TRUSS",
}


def cook(scriptOp):
    osc = op('osc')

    # --- heartbeat ---
    try:
        hb = int(osc['vision/heartbeat:0'][0])
    except Exception:
        hb = -1

    # --- puck positions ---
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

    # --- method id from state CHOP (optional) ---
    method_id = 0
    try:
        method_id = int(op('state')['method_id'][0])
    except Exception:
        pass

    mc = METHOD_COLORS.get(method_id, METHOD_COLORS[0])

    # --- render ---
    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)
    img[:, :] = (*C_BG[:3], 1.0)

    _draw_footprint(img, pucks, mc)
    _draw_status(img, hb, len(pucks), method_id, mc)
    _draw_dividers(img)

    scriptOp.copyNumpyArray(img)


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------

def _draw_footprint(img, pucks, method_color):
    if not pucks:
        return

    pts = [_remap(*pos) for pos in pucks.values()]

    if len(pts) >= 3:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        pts_sorted = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

        fill_color = (*method_color, 0.18)
        _fill_polygon(img, pts_sorted, fill_color, FP)

        edge_color = (*method_color, 0.9)
        for i in range(len(pts_sorted)):
            p1 = pts_sorted[i]
            p2 = pts_sorted[(i + 1) % len(pts_sorted)]
            _line(img, *p1, *p2, edge_color, 2)

    elif len(pts) == 2:
        _line(img, *pts[0], *pts[1], C_LINE, 2)

    for pos in pucks.values():
        _circle(img, *_remap(*pos), 10, (*method_color, 1.0), 3)


def _draw_status(img, hb, n_pucks, method_id, method_color):
    x0, y0, x1, y1 = ST
    pad = 16

    # background strip
    img[y0:y1, x0:x1] = (0.08, 0.08, 0.08, 1.0)

    # method color band (top ~40% of status zone)
    band_h = int((y1 - y0) * 0.4)
    alpha = 0.85 if hb >= 0 else 0.3
    img[y0 + pad : y0 + band_h, x0 + pad : x1 - pad] = (*method_color, alpha)

    # heartbeat indicator bar (bottom 8 px of status zone)
    hb_color = (0.0, 0.9, 0.3, 1.0) if hb >= 0 else (0.6, 0.1, 0.1, 1.0)
    img[y1 - 8 : y1, x0 : x1] = hb_color


def _draw_dividers(img):
    # horizontal line between FP and TX
    img[FP[3] : FP[3] + 2, :] = C_DIVIDER
    # vertical line between FP and ST
    img[: ST[3], ST[0] : ST[0] + 2] = C_DIVIDER


# ---------------------------------------------------------------------------
# geometry / rasterisation
# ---------------------------------------------------------------------------

def _remap(px, py):
    x = FP[0] + (px / PROJ_W) * (FP[2] - FP[0])
    y = FP[1] + (py / PROJ_H) * (FP[3] - FP[1])
    return x, y


def _fill_polygon(img, pts, color, bounds):
    bx0, by0, bx1, by1 = bounds
    bx1 = min(bx1, img.shape[1])
    by1 = min(by1, img.shape[0])
    if bx1 <= bx0 or by1 <= by0 or len(pts) < 3:
        return

    Y, X = np.mgrid[by0:by1, bx0:bx1]
    inside = np.zeros((by1 - by0, bx1 - bx0), dtype=bool)

    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        denom = yj - yi
        if abs(denom) < 1e-9:
            j = i
            continue
        cond = ((yi > Y) != (yj > Y)) & (X < (xj - xi) * (Y - yi) / denom + xi)
        inside ^= cond
        j = i

    # blend fill color over existing pixels
    a = color[3]
    for c in range(3):
        img[by0:by1, bx0:bx1, c][inside] = (
            img[by0:by1, bx0:bx1, c][inside] * (1 - a) + color[c] * a
        )


def _line(img, x0, y0, x1, y1, color, width=2):
    w, h = img.shape[1], img.shape[0]
    n = max(int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 2), 2)
    t  = np.linspace(0, 1, n)
    xs = (x0 + t * (x1 - x0)).astype(int)
    ys = (y0 + t * (y1 - y0)).astype(int)
    half = width // 2
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            xc = np.clip(xs + dx, 0, w - 1)
            yc = np.clip(ys + dy, 0, h - 1)
            img[yc, xc] = color


def _circle(img, cx, cy, r, color, width=3):
    h, w = img.shape[:2]
    bx0 = max(0, int(cx - r - width))
    bx1 = min(w, int(cx + r + width + 1))
    by0 = max(0, int(cy - r - width))
    by1 = min(h, int(cy + r + width + 1))
    if bx1 <= bx0 or by1 <= by0:
        return
    Y, X = np.mgrid[by0:by1, bx0:bx1]
    d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    img[by0:by1, bx0:bx1][(d >= r - width / 2) & (d <= r + width / 2)] = color
