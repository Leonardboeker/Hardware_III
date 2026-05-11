"""Panel layout renderer — Script TOP.

Renders the 9-panel UI defined in the design spec (Panel_Ui.pdf), scaled from
1920×1080 to 1280×720 for the TD Non-Commercial resolution limit (scale = 2/3).

Each panel is drawn as a bordered rectangle. Two panels carry live content:
  - panel_main_plan_simulation : footprint geometry (pucks + polygon)
  - panel_method_selection      : current construction method color

Text content for the other panels comes from separate Text TOPs composed on
top of this image — see TD-FRAMEWORK-GUIDE.md for the network layout.

Reads from these TD nodes (must exist with these names):
  vision_in        OSC In CHOP   — puck positions from CV pipeline
  compute_state    Script CHOP   — method_id channel (optional)
"""
import math
import numpy as np

# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
PROJ_W = 1280
PROJ_H = 720

# ---------------------------------------------------------------------------
# Panel layout — coords scaled from 1920×1080 design × (2/3)
# Each entry: (x, y, w, h)
# ---------------------------------------------------------------------------
PANELS = {
    'top_phase_navigation':   (271,  15,  600,  67),
    'left_info':              ( 17,  15,  213, 467),
    'left_assembly_sequence': ( 17, 493,  307, 173),
    'main_plan_simulation':   (245, 108,  652, 373),
    'method_selection':       (337, 493,  560, 173),
    'right_comparison':       (910,  15,  353, 292),
    'right_cost_chart':       (910, 321,  353, 160),
    'right_phase_preview':    (910, 493,  353, 173),
    'bar_bottom_status':      (  0, 687, 1280,  33),
}

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
C_BG          = (0.04, 0.04, 0.05, 1.0)
C_PANEL_BG    = (0.08, 0.08, 0.10, 1.0)
C_PANEL_EDGE  = (0.25, 0.25, 0.28, 1.0)
C_LINE        = (1.0,  1.0,  1.0,  0.85)
C_PUCK_RING   = (1.0,  1.0,  1.0,  1.0)

METHOD_COLORS = {
    0: (0.40, 0.40, 0.40),   # NONE        — grey
    1: (0.85, 0.40, 0.20),   # MASONRY     — terracotta
    2: (0.10, 0.70, 0.90),   # 3D PRINTED  — cyan
    3: (0.95, 0.75, 0.00),   # PREFAB      — yellow
}

METHOD_NAMES = {
    0: "NO METHOD",
    1: "MASONRY",
    2: "3D PRINTED",
    3: "PREFAB",
}

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10


# ---------------------------------------------------------------------------
# Cook
# ---------------------------------------------------------------------------
def cook(scriptOp):
    vision = op('vision_in')

    # heartbeat
    try:
        hb = int(vision['vision/heartbeat:0'][0])
    except Exception:
        hb = -1

    # puck positions
    pucks = {}
    for pid in FOOTPRINT_IDS:
        try:
            pf = int(vision[f'puck/{pid}:0'][0])
            if hb >= 0 and abs(hb - pf) <= LIVENESS_FRAMES:
                pucks[pid] = (
                    float(vision[f'puck/{pid}:1'][0]),
                    float(vision[f'puck/{pid}:2'][0]),
                )
        except Exception:
            pass

    # current method id
    method_id = 0
    try:
        method_id = int(op('compute_state')['method_id'][0])
    except Exception:
        pass

    mc = METHOD_COLORS.get(method_id, METHOD_COLORS[0])

    # ----- render -----
    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)
    img[:, :] = C_BG

    # draw all panel frames
    for pid, bounds in PANELS.items():
        _draw_panel_frame(img, *bounds, fill=C_PANEL_BG, edge=C_PANEL_EDGE, edge_w=2)

    # content into specific panels
    _draw_main_plan(img, pucks, mc)
    _draw_method_selection(img, method_id, mc, hb)
    _draw_heartbeat_dot(img, hb)

    scriptOp.copyNumpyArray(img)


# ---------------------------------------------------------------------------
# Panel content
# ---------------------------------------------------------------------------
def _draw_main_plan(img, pucks, method_color):
    """Footprint geometry inside panel_main_plan_simulation."""
    bx, by, bw, bh = PANELS['main_plan_simulation']

    if not pucks:
        return

    pts = [_remap_to_panel(*pos, bx, by, bw, bh) for pos in pucks.values()]

    if len(pts) >= 3:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        pts_sorted = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

        _fill_polygon(img, pts_sorted, (*method_color, 0.18), (bx, by, bx + bw, by + bh))

        for i in range(len(pts_sorted)):
            p1 = pts_sorted[i]
            p2 = pts_sorted[(i + 1) % len(pts_sorted)]
            _line(img, *p1, *p2, (*method_color, 0.9), 2)

    elif len(pts) == 2:
        _line(img, *pts[0], *pts[1], C_LINE, 2)

    for pt in pts:
        _circle(img, *pt, 8, (*method_color, 1.0), 3)


def _draw_method_selection(img, method_id, method_color, hb):
    """Method color band inside panel_method_selection."""
    bx, by, bw, bh = PANELS['method_selection']
    pad = 14

    # left part: method color block
    block_w = int(bh * 1.4)  # roughly square area on the left
    alpha = 0.9 if hb >= 0 else 0.3
    img[by + pad : by + bh - pad, bx + pad : bx + pad + block_w] = (*method_color, alpha)

    # right part of panel left empty — Text TOP will write the method name here


def _draw_heartbeat_dot(img, hb):
    """Small alive/offline indicator inside the bottom status bar."""
    bx, by, bw, bh = PANELS['bar_bottom_status']
    cy = by + bh // 2
    cx = bx + 16
    color = (0.0, 0.9, 0.3, 1.0) if hb >= 0 else (0.85, 0.15, 0.15, 1.0)
    _circle(img, cx, cy, 6, color, width=10)  # filled-ish dot


# ---------------------------------------------------------------------------
# Panel frame
# ---------------------------------------------------------------------------
def _draw_panel_frame(img, x, y, w, h, fill, edge, edge_w):
    h_img, w_img = img.shape[:2]
    x1 = min(x + w, w_img)
    y1 = min(y + h, h_img)
    if x1 <= x or y1 <= y:
        return
    img[y:y1, x:x1] = fill
    # top + bottom edges
    img[y : y + edge_w,        x:x1] = edge
    img[y1 - edge_w : y1,      x:x1] = edge
    # left + right edges
    img[y:y1, x : x + edge_w]        = edge
    img[y:y1, x1 - edge_w : x1]      = edge


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def _remap_to_panel(px, py, bx, by, bw, bh):
    """Map projector-space puck (px,py) into the given panel rectangle.
    Assumes the CV pipeline outputs coords in 0..PROJ_W, 0..PROJ_H space."""
    x = bx + (px / PROJ_W) * bw
    y = by + (py / PROJ_H) * bh
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
    a = color[3]
    for c in range(3):
        img[by0:by1, bx0:bx1, c][inside] = (
            img[by0:by1, bx0:bx1, c][inside] * (1 - a) + color[c] * a
        )


def _line(img, x0, y0, x1, y1, color, width=2):
    h, w = img.shape[:2]
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
