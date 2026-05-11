"""Panel layout renderer — Script TOP.

Renders the 9-panel UI from Panel_Ui.pdf at 1280×720 (TD Non-Commercial limit).

This script does EVERYTHING in one node:
  - Panel frames (all 9 panels with borders)
  - Footprint geometry inside panel_main_plan_simulation
  - Method color block inside panel_method_selection
  - Heartbeat indicator in bar_bottom_status
  - AUTO-BLIT any Text TOP named text_<panel_id> into its panel position

So to add text in any panel: create a Text TOP, rename to text_<panel_id>,
set resolution to match the panel size (see PANELS dict below), and write
your text content. This script picks it up automatically — no compose_final,
no transform math, no over chain.

Wire-up of the network:
  render_footprint (this script TOP)  →  projector_out

That's it. No compose_final needed.

Reads from these TD nodes (must exist with these names):
  vision_in        OSC In CHOP   — puck data from CV pipeline
  compute_state    Script CHOP   — method_id channel (optional)
  text_<panel_id>  Text TOP      — optional per-panel text overlay
                                   e.g. text_method_selection
  lca_data         Script DAT    — optional; not used here but in the same network

Colors and method names below must stay in sync with data/methods_db.json.
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

# Sourced from data/methods_db.json → methods[*].color_rgb
METHOD_COLORS = {
    0: (0.40, 0.40, 0.40),   # NONE           — grey
    1: (0.85, 0.45, 0.15),   # MASONRY        — terracotta
    2: (0.18, 0.62, 0.85),   # 3D PRINTED     — steel blue
    3: (0.25, 0.72, 0.45),   # PREFAB         — green
    4: (0.72, 0.30, 0.22),   # RECLAIMED BRICK — dark red (baseline)
}

METHOD_NAMES = {
    0: "NONE",
    1: "MASONRY",
    2: "3D PRINTED",
    3: "PREFAB",
    4: "RECLAIMED BRICK",
}

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10


# ---------------------------------------------------------------------------
# Cook
# ---------------------------------------------------------------------------
def cook(scriptOp):
    vision = op('vision_in')

    # Detect which channel-name convention this TD uses ONCE per cook,
    # then read all puck args consistently. Trying variants per-arg led
    # to collisions (arg 1 stealing arg 0's channel).
    naming = 'colon'  # default
    if vision is not None:
        try:
            vision['puck/0:0']
        except Exception:
            try:
                vision['puck/00']
                naming = 'flat0'
            except Exception:
                try:
                    vision['puck/01']
                    naming = 'flat1'
                except Exception:
                    naming = 'colon'  # nothing found; stick with default

    def _ch(name):
        if vision is None:
            return None
        for variant in (name, f'{name}:0'):
            try:
                return vision[variant][0]
            except Exception:
                pass
        return None

    def _puck_arg(pid, arg_idx):
        if naming == 'colon':
            name = f'puck/{pid}:{arg_idx}'
        elif naming == 'flat0':
            name = f'puck/{pid}{arg_idx}'
        else:  # flat1
            name = f'puck/{pid}{arg_idx + 1}'
        try:
            return vision[name][0]
        except Exception:
            return None

    # heartbeat
    hb_raw = _ch('vision/heartbeat')
    try:
        hb = int(hb_raw) if hb_raw is not None else -1
    except Exception:
        hb = -1

    # puck positions
    pucks = {}
    for pid in FOOTPRINT_IDS:
        pf = _puck_arg(pid, 0)
        if pf is None:
            continue
        try:
            pf = int(pf)
        except Exception:
            continue
        if hb < 0 or abs(hb - pf) > LIVENESS_FRAMES:
            continue
        px = _puck_arg(pid, 1)
        py = _puck_arg(pid, 2)
        if px is None or py is None:
            continue
        try:
            pucks[pid] = (float(px), float(py))
        except Exception:
            pass

    # current method id
    method_id = 0
    try:
        method_id = int(op('compute_state')['method_id'][0])
    except Exception:
        pass
    mc = METHOD_COLORS.get(method_id, METHOD_COLORS[0])

    try:
        hb_alive = int(op('compute_state')['hb_alive'][0])
    except Exception:
        hb_alive = 1 if hb >= 0 else 0

    # ----- render -----
    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)
    img[:, :] = C_BG

    # panel frames
    for pid, bounds in PANELS.items():
        _draw_panel_frame(img, *bounds, fill=C_PANEL_BG, edge=C_PANEL_EDGE, edge_w=2)

    # interactive content into specific panels
    _draw_main_plan(img, pucks, mc)
    _draw_method_color_block(img, mc, hb)
    _draw_heartbeat_dot(img, hb)

    # AUTO-BLIT text overlays from named Text TOPs
    _blit_text_overlays(img)

    # DISCONNECTED overlay — shown when vision pipeline has been offline > 3 s
    if hb_alive == 0:
        _draw_disconnected(img)

    # TD's TOPs use bottom-left origin while our drawing uses top-left.
    # Flip vertically once at the end so the layout reads right-side-up.
    scriptOp.copyNumpyArray(np.flipud(img).copy())


# ---------------------------------------------------------------------------
# Auto text overlay
# ---------------------------------------------------------------------------
def _blit_text_overlays(img):
    """For each panel, look for op('text_<panel_id>') and composite it in.

    The Text TOP can be any resolution — we resample (nearest-neighbor) to
    match the panel size if needed.
    """
    for panel_id, bounds in PANELS.items():
        text_op = op(f'text_{panel_id}')
        if text_op is None:
            continue
        try:
            tex = text_op.numpyArray(delayed=True)
        except Exception:
            continue
        if tex is None:
            continue
        # TD numpy arrays have origin bottom-left; we use top-left → flip Y
        tex = np.flipud(tex)
        # ensure 4 channels
        if tex.shape[-1] == 3:
            alpha = np.ones((*tex.shape[:2], 1), dtype=tex.dtype)
            tex = np.concatenate([tex, alpha], axis=-1)
        # match dtype
        if tex.dtype == np.uint8:
            tex = tex.astype(np.float32) / 255.0
        elif tex.dtype != np.float32:
            tex = tex.astype(np.float32)
        bx, by, bw, bh = bounds
        _blit_alpha(img, tex, bx, by, bw, bh)


def _blit_alpha(img, src, x, y, w, h):
    """Alpha-composite src into img at (x, y) with size (w, h).
    Resamples src to (h, w) with nearest-neighbor if shape doesn't match."""
    img_h, img_w = img.shape[:2]
    x1 = min(x + w, img_w)
    y1 = min(y + h, img_h)
    if x1 <= x or y1 <= y:
        return
    target_h = y1 - y
    target_w = x1 - x
    if src.shape[0] != target_h or src.shape[1] != target_w:
        ys = (np.arange(target_h) * src.shape[0] / target_h).astype(int)
        xs = (np.arange(target_w) * src.shape[1] / target_w).astype(int)
        src = src[ys][:, xs]
    a = src[..., 3:4]
    img[y:y1, x:x1, :3] = src[..., :3] * a + img[y:y1, x:x1, :3] * (1 - a)
    img[y:y1, x:x1, 3:4] = np.maximum(img[y:y1, x:x1, 3:4], a)


# ---------------------------------------------------------------------------
# Panel content
# ---------------------------------------------------------------------------
def _draw_main_plan(img, pucks, method_color):
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


def _draw_method_color_block(img, method_color, hb):
    """Color block on the LEFT side of method_selection panel.
    Right side is left empty so text_method_selection can show there."""
    bx, by, bw, bh = PANELS['method_selection']
    pad = 14
    block_w = bh - pad * 2  # square-ish
    alpha = 1.0 if hb >= 0 else 0.3
    src = np.zeros((bh - 2 * pad, block_w, 4), dtype=np.float32)
    src[..., 0] = method_color[0]
    src[..., 1] = method_color[1]
    src[..., 2] = method_color[2]
    src[..., 3] = alpha
    _blit_alpha(img, src, bx + pad, by + pad, block_w, bh - 2 * pad)


def _draw_heartbeat_dot(img, hb):
    bx, by, bw, bh = PANELS['bar_bottom_status']
    cy = by + bh // 2
    cx = bx + 16
    color = (0.0, 0.9, 0.3, 1.0) if hb >= 0 else (0.85, 0.15, 0.15, 1.0)
    _circle(img, cx, cy, 6, color, width=10)


def _draw_disconnected(img):
    """Full-canvas overlay when vision pipeline is offline."""
    bx, by, bw, bh = PANELS['main_plan_simulation']
    # dim the main panel
    img[by:by+bh, bx:bx+bw, :3] *= 0.3
    # draw centred warning text as a simple rectangle marker
    cx = bx + bw // 2
    cy = by + bh // 2
    # red X lines
    size = 30
    _line(img, cx - size, cy - size, cx + size, cy + size, (0.85, 0.15, 0.15, 1.0), 4)
    _line(img, cx + size, cy - size, cx - size, cy + size, (0.85, 0.15, 0.15, 1.0), 4)
    # pulsing dot already handled by _draw_heartbeat_dot (turns red)


# ---------------------------------------------------------------------------
# Frames + geometry
# ---------------------------------------------------------------------------
def _draw_panel_frame(img, x, y, w, h, fill, edge, edge_w):
    h_img, w_img = img.shape[:2]
    x1 = min(x + w, w_img)
    y1 = min(y + h, h_img)
    if x1 <= x or y1 <= y:
        return
    img[y:y1, x:x1] = fill
    img[y : y + edge_w,        x:x1] = edge
    img[y1 - edge_w : y1,      x:x1] = edge
    img[y:y1, x : x + edge_w]        = edge
    img[y:y1, x1 - edge_w : x1]      = edge


def _remap_to_panel(px, py, bx, by, bw, bh):
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
