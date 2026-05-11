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
    "top_phase_navigation": (271, 15, 600, 67),
    "left_info": (17, 15, 213, 467),
    "left_assembly_sequence": (17, 493, 307, 173),
    "main_plan_simulation": (245, 108, 652, 373),
    "method_selection": (337, 493, 560, 173),
    "right_comparison": (910, 15, 353, 292),
    "right_cost_chart": (910, 321, 353, 160),
    "right_phase_preview": (910, 493, 353, 173),
    "bar_bottom_status": (0, 687, 1280, 33),
}


def _panel_bounds(panel_id):
    """Convert top-left layout coordinates to Script TOP image coordinates."""
    x, y, w, h = PANELS[panel_id]
    return x, PROJ_H - y - h, w, h


TEXT_BLOCKS = {
    "left_info_hero": ("left_info", 16, 44, 181, 94),
    "left_info_details": ("left_info", 16, 150, 181, 168),
    "left_info_scale": ("left_info", 16, 330, 181, 108),
    "left_info_scale_minus": ("left_info", 30, 394, 24, 24),
    "left_info_scale_value": ("left_info", 62, 394, 44, 24),
    "left_info_scale_plus": ("left_info", 114, 394, 24, 24),
    "method_card_masonry": ("method_selection", 18, 54, 164, 102),
    "method_card_3d_printed": ("method_selection", 198, 54, 164, 102),
    "method_card_prefab": ("method_selection", 378, 54, 164, 102),
    "right_comparison_summary": ("right_comparison", 16, 48, 321, 54),
    "right_comparison_metrics": ("right_comparison", 16, 112, 321, 162),
    "right_cost_hero": ("right_cost_chart", 16, 44, 321, 40),
    "right_cost_grid_left": ("right_cost_chart", 16, 92, 152, 52),
    "right_cost_grid_right": ("right_cost_chart", 184, 92, 153, 52),
    "right_phase_preview_state": ("right_phase_preview", 16, 42, 321, 40),
    "right_phase_preview_left": ("right_phase_preview", 16, 90, 152, 58),
    "right_phase_preview_right": ("right_phase_preview", 184, 90, 153, 58),
}


def _block_bounds(panel_id, local_x, local_y, width, height):
    px, py, _pw, ph = _panel_bounds(panel_id)
    return px + local_x, py + ph - local_y - height, width, height

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
C_BG_TOP = (0.063, 0.075, 0.106)
C_BG_MID = (0.039, 0.051, 0.075)
C_BG_BOTTOM = (0.027, 0.031, 0.051)
C_BG_HAZE = (0.97, 0.95, 0.90)

C_PANEL_BG = (0.055, 0.070, 0.094, 0.84)
C_PANEL_EDGE = (1.0, 1.0, 1.0, 0.08)
C_PANEL_INNER = (1.0, 1.0, 1.0, 0.025)
C_PANEL_SHEEN = (1.0, 1.0, 1.0, 0.035)
C_CARD_BG = (1.0, 1.0, 1.0, 0.030)
C_CARD_EDGE = (1.0, 1.0, 1.0, 0.075)
C_CARD_INNER = (1.0, 1.0, 1.0, 0.018)
C_LINE = (1.0, 1.0, 1.0, 0.85)

PANEL_RADIUS = 18
CARD_RADIUS = 14
PANEL_EDGE_W = 1

# Sourced from data/methods_db.json → methods[*].color_rgb
METHOD_COLORS = {
    0: (0.40, 0.40, 0.40),  # NONE — grey
    1: (0.85, 0.45, 0.15),  # MASONRY — terracotta
    2: (0.18, 0.62, 0.85),  # 3D PRINTED — steel blue
    3: (0.25, 0.72, 0.45),  # PREFAB — green
    4: (0.72, 0.30, 0.22),  # RECLAIMED BRICK — dark red
}

METHOD_IDS = {
    "masonry": 1,
    "3d_printed": 2,
    "prefab": 3,
    "reclaimed_brick": 4,
}

METHOD_NAMES = {
    0: "NONE",
    1: "MASONRY",
    2: "3D PRINTED",
    3: "PREFAB",
    4: "RECLAIMED BRICK",
}

FOOTPRINT_IDS = list(range(10))
LIVENESS_FRAMES = 10


# ---------------------------------------------------------------------------
# Cook
# ---------------------------------------------------------------------------
def cook(scriptOp):
    owner = scriptOp.parent()
    vision = op("vision_in")

    # heartbeat
    try:
        hb = int(vision["vision/heartbeat:0"][0])
    except Exception:
        hb = -1

    # puck positions
    pucks = {}
    for pid in FOOTPRINT_IDS:
        try:
            pf = int(vision[f"puck/{pid}:0"][0])
            if hb >= 0 and abs(hb - pf) <= LIVENESS_FRAMES:
                pucks[pid] = (
                    float(vision[f"puck/{pid}:1"][0]),
                    float(vision[f"puck/{pid}:2"][0]),
                )
        except Exception:
            pass

    # current method id
    method_id = _resolve_method_id(owner)
    mc = METHOD_COLORS.get(method_id, METHOD_COLORS[0])
    accent = mc if method_id != 0 else (0.79, 0.71, 0.55)

    hb_alive = _resolve_hb_alive(owner, hb)

    # ----- render -----
    img = np.zeros((PROJ_H, PROJ_W, 4), dtype=np.float32)
    _paint_background(img, accent)

    # panel frames
    for panel_id in PANELS:
        bounds = _panel_bounds(panel_id)
        _draw_panel_frame(
            img,
            *bounds,
            fill=C_PANEL_BG,
            edge=C_PANEL_EDGE,
            edge_w=PANEL_EDGE_W,
            radius=PANEL_RADIUS,
            accent=_panel_accent(accent, panel_id),
        )

    # secondary cards and simulation-like shells
    _draw_panel_cards(img, owner, accent, method_id)

    # interactive content into specific panels
    _draw_main_plan(img, pucks, mc)
    _draw_heartbeat_dot(img, hb_alive)

    # AUTO-BLIT text overlays from named Text TOPs
    _blit_text_overlays(img)

    # DISCONNECTED overlay — shown when vision pipeline is offline > 3 s
    if hb_alive == 0:
        _draw_disconnected(img)

    scriptOp.copyNumpyArray(img)


def _resolve_method_id(owner):
    """Prefer the new storage-driven state, then fall back to compute_state."""
    try:
        method_key = owner.fetch("current_method", None)
    except Exception:
        method_key = None
    if method_key in METHOD_IDS:
        return METHOD_IDS[method_key]

    try:
        return int(op("compute_state")["method_id"][0])
    except Exception:
        return 0


def _resolve_hb_alive(owner, heartbeat):
    """Keep demo / storage state aligned with the renderer when vision is absent."""
    try:
        stored = owner.fetch("hb_alive", None)
    except Exception:
        stored = None
    if stored is not None:
        try:
            return int(stored)
        except Exception:
            pass

    try:
        return int(op("compute_state")["hb_alive"][0])
    except Exception:
        return 1 if heartbeat >= 0 else 0


def _panel_accent(accent_rgb, panel_id):
    strong = {
        "top_phase_navigation",
        "main_plan_simulation",
        "method_selection",
        "right_comparison",
        "right_cost_chart",
    }
    alpha = 0.18 if panel_id in strong else 0.10
    return (*accent_rgb, alpha)


# ---------------------------------------------------------------------------
# Auto text overlay
# ---------------------------------------------------------------------------
def _blit_text_overlays(img):
    """For each panel, look for op('text_<panel_id>') and composite it in.

    The Text TOP can be any resolution — we resample (nearest-neighbor) to
    match the panel size if needed.
    """
    regions = [(panel_id, _panel_bounds(panel_id)) for panel_id in PANELS]
    regions.extend(
        [
            (block_id, _block_bounds(panel_id, lx, ly, bw, bh))
            for block_id, (panel_id, lx, ly, bw, bh) in TEXT_BLOCKS.items()
        ]
    )

    for region_id, bounds in regions:
        text_op = op(f"text_{region_id}")
        if text_op is None:
            continue
        try:
            tex = text_op.numpyArray(delayed=True)
        except Exception:
            continue
        if tex is None:
            continue

        if tex.shape[-1] == 3:
            alpha = np.ones((*tex.shape[:2], 1), dtype=tex.dtype)
            tex = np.concatenate([tex, alpha], axis=-1)

        if tex.dtype == np.uint8:
            tex = tex.astype(np.float32) / 255.0
        elif tex.dtype != np.float32:
            tex = tex.astype(np.float32)

        bx, by, bw, bh = bounds
        _blit_alpha(img, tex, bx, by, bw, bh)


def _blit_alpha(img, src, x, y, w, h):
    """Alpha-composite src into img at (x, y) with size (w, h)."""
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
    bx, by, bw, bh = _panel_bounds("main_plan_simulation")
    shell_x, shell_y, shell_w, shell_h = _block_bounds(
        "main_plan_simulation", 20, 60, bw - 40, bh - 92
    )
    _draw_inset_card(
        img,
        shell_x,
        shell_y,
        shell_w,
        shell_h,
        fill=(1.0, 1.0, 1.0, 0.022),
        edge=(1.0, 1.0, 1.0, 0.045),
        accent=(*method_color, 0.10),
    )
    focus_x, focus_y, focus_w, focus_h = _block_bounds(
        "main_plan_simulation", 88, 92, bw - 176, bh - 176
    )
    _draw_inset_card(
        img,
        focus_x,
        focus_y,
        focus_w,
        focus_h,
        fill=(1.0, 1.0, 1.0, 0.010),
        edge=(1.0, 1.0, 1.0, 0.030),
        accent=(0.0, 0.0, 0.0, 0.0),
    )
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


def _draw_heartbeat_dot(img, hb_alive):
    bx, by, bw, bh = _panel_bounds("bar_bottom_status")
    cy = by + bh // 2
    cx = bx + 16
    color = (0.0, 0.9, 0.3, 1.0) if hb_alive else (0.85, 0.15, 0.15, 1.0)
    _circle(img, cx, cy, 6, color, width=10)


def _draw_disconnected(img):
    """Full-canvas overlay when vision pipeline is offline."""
    bx, by, bw, bh = _panel_bounds("main_plan_simulation")
    img[by : by + bh, bx : bx + bw, :3] *= 0.38
    cx = bx + bw // 2
    cy = by + bh // 2
    size = 30
    _line(img, cx - size, cy - size, cx + size, cy + size, (0.85, 0.15, 0.15, 0.92), 4)
    _line(img, cx + size, cy - size, cx - size, cy + size, (0.85, 0.15, 0.15, 0.92), 4)


def _draw_panel_cards(img, owner, accent_rgb, method_id):
    try:
        selected_method = owner.fetch("current_method", None)
    except Exception:
        selected_method = None

    hero_fill = (*accent_rgb, 0.12)
    card_specs = [
        ("left_info_hero", hero_fill, C_CARD_EDGE, (*accent_rgb, 0.20)),
        ("left_info_details", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("left_info_scale", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_comparison_summary", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_comparison_metrics", C_CARD_BG, C_CARD_EDGE, (*accent_rgb, 0.10)),
        ("right_cost_hero", hero_fill, C_CARD_EDGE, (*accent_rgb, 0.18)),
        ("right_cost_grid_left", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_cost_grid_right", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_phase_preview_state", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_phase_preview_left", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
        ("right_phase_preview_right", C_CARD_BG, C_CARD_EDGE, (0.0, 0.0, 0.0, 0.0)),
    ]

    for block_id, fill, edge, accent in card_specs:
        panel_id, lx, ly, bw, bh = TEXT_BLOCKS[block_id]
        _draw_inset_card(
            img,
            *_block_bounds(panel_id, lx, ly, bw, bh),
            fill=fill,
            edge=edge,
            accent=accent,
        )

    for block_id in ("left_info_scale_minus", "left_info_scale_value", "left_info_scale_plus"):
        panel_id, lx, ly, bw, bh = TEXT_BLOCKS[block_id]
        _draw_inset_card(
            img,
            *_block_bounds(panel_id, lx, ly, bw, bh),
            fill=(1.0, 1.0, 1.0, 0.040),
            edge=(1.0, 1.0, 1.0, 0.090),
            accent=(*accent_rgb, 0.16) if block_id == "left_info_scale_value" else (0.0, 0.0, 0.0, 0.0),
        )

    method_cards = {
        "masonry": "method_card_masonry",
        "3d_printed": "method_card_3d_printed",
        "prefab": "method_card_prefab",
    }
    fallback_selected = {
        1: "masonry",
        2: "3d_printed",
        3: "prefab",
    }.get(method_id)
    selected_method = selected_method or fallback_selected

    for method_key, block_id in method_cards.items():
        panel_id, lx, ly, bw, bh = TEXT_BLOCKS[block_id]
        is_active = method_key == selected_method
        fill = (*accent_rgb, 0.13) if is_active else C_CARD_BG
        edge = (*accent_rgb, 0.28) if is_active else C_CARD_EDGE
        accent = (*accent_rgb, 0.20) if is_active else (0.0, 0.0, 0.0, 0.0)
        _draw_inset_card(
            img,
            *_block_bounds(panel_id, lx, ly, bw, bh),
            fill=fill,
            edge=edge,
            accent=accent,
        )


def _draw_inset_card(img, x, y, w, h, fill, edge, accent):
    _draw_panel_frame(
        img,
        x,
        y,
        w,
        h,
        fill=fill,
        edge=edge,
        edge_w=1,
        radius=CARD_RADIUS,
        accent=accent,
    )


# ---------------------------------------------------------------------------
# Frames + geometry
# ---------------------------------------------------------------------------
def _paint_background(img, accent_rgb):
    """Approximate the simulation's gradient + haze background."""
    y = np.linspace(0.0, 1.0, PROJ_H, dtype=np.float32)[:, None]
    x = np.linspace(0.0, 1.0, PROJ_W, dtype=np.float32)[None, :]

    top = np.array(C_BG_TOP, dtype=np.float32)
    mid = np.array(C_BG_MID, dtype=np.float32)
    bottom = np.array(C_BG_BOTTOM, dtype=np.float32)
    haze = np.array(C_BG_HAZE, dtype=np.float32)
    accent = np.array(accent_rgb, dtype=np.float32)

    upper_mix = np.clip(y / 0.55, 0.0, 1.0)
    lower_mix = np.clip((y - 0.40) / 0.60, 0.0, 1.0)
    base = top * (1.0 - upper_mix[..., None]) + mid * upper_mix[..., None]
    base = base * (1.0 - lower_mix[..., None]) + bottom * lower_mix[..., None]
    base = np.broadcast_to(base, (PROJ_H, PROJ_W, 3)).copy()

    top_left_haze = np.exp(-(((x - 0.05) / 0.22) ** 2 + ((y - 0.02) / 0.18) ** 2))
    accent_glow = np.exp(-(((x - 0.72) / 0.34) ** 2 + ((y - 0.22) / 0.28) ** 2))
    bottom_glow = np.exp(-(((x - 0.35) / 0.45) ** 2 + ((y - 0.96) / 0.10) ** 2))

    base += haze * (top_left_haze[..., None] * 0.05)
    base += accent * (accent_glow[..., None] * 0.08)
    base += np.array((0.28, 0.20, 0.10), dtype=np.float32) * (bottom_glow[..., None] * 0.03)

    img[..., :3] = np.clip(base, 0.0, 1.0)
    img[..., 3] = 1.0


def _draw_panel_frame(img, x, y, w, h, fill, edge, edge_w, radius, accent):
    h_img, w_img = img.shape[:2]
    x1 = min(x + w, w_img)
    y1 = min(y + h, h_img)
    if x1 <= x or y1 <= y:
        return

    target_h = y1 - y
    target_w = x1 - x
    outer = _rounded_rect_mask(target_h, target_w, radius)
    inner = _inset_mask(target_h, target_w, radius, edge_w)

    _blend_mask(img, x, y, outer, fill)
    _blend_mask(img, x, y, outer & ~inner, edge)
    _blend_mask(img, x, y, outer & ~inner, accent)
    _blend_mask(img, x + 1, y + 1, _inset_mask(target_h - 2, target_w - 2, radius - 1, 0), C_PANEL_INNER)

    sheen_h = min(target_h, 46)
    sheen_mask = outer[:sheen_h]
    _blend_mask_with_alpha_ramp(img, x, y, sheen_mask, sheen_h, C_PANEL_SHEEN)


def _rounded_rect_mask(height, width, radius):
    mask = np.zeros((height, width), dtype=bool)
    if height <= 0 or width <= 0:
        return mask

    radius = max(0, min(radius, height // 2, width // 2))
    if radius == 0:
        mask[:, :] = True
        return mask

    mask[radius : height - radius, :] = True
    mask[:, radius : width - radius] = True

    yy, xx = np.ogrid[:radius, :radius]
    corner = (xx - radius + 0.5) ** 2 + (yy - radius + 0.5) ** 2 <= radius**2
    mask[:radius, :radius] |= corner
    mask[:radius, width - radius :] |= np.fliplr(corner)
    mask[height - radius :, :radius] |= np.flipud(corner)
    mask[height - radius :, width - radius :] |= np.flipud(np.fliplr(corner))
    return mask


def _inset_mask(height, width, radius, inset):
    if inset <= 0:
        return _rounded_rect_mask(height, width, radius)
    inner_h = max(height - inset * 2, 0)
    inner_w = max(width - inset * 2, 0)
    inner_radius = max(radius - inset, 0)
    inner = np.zeros((height, width), dtype=bool)
    if inner_h == 0 or inner_w == 0:
        return inner
    inner[inset : inset + inner_h, inset : inset + inner_w] = _rounded_rect_mask(
        inner_h, inner_w, inner_radius
    )
    return inner


def _blend_mask(img, x, y, mask, color):
    if mask.size == 0 or color[3] <= 0:
        return
    y1 = min(y + mask.shape[0], img.shape[0])
    x1 = min(x + mask.shape[1], img.shape[1])
    if x1 <= x or y1 <= y:
        return

    sub = img[y:y1, x:x1]
    local = mask[: y1 - y, : x1 - x].astype(np.float32)[..., None] * color[3]
    sub[..., :3] = np.array(color[:3], dtype=np.float32) * local + sub[..., :3] * (1.0 - local)
    sub[..., 3:4] = np.maximum(sub[..., 3:4], local)


def _blend_mask_with_alpha_ramp(img, x, y, mask, height, color):
    if mask.size == 0 or color[3] <= 0:
        return
    ramp = np.linspace(1.0, 0.0, height, dtype=np.float32)[:, None]
    ramped = mask.astype(np.float32) * ramp
    y1 = min(y + ramped.shape[0], img.shape[0])
    x1 = min(x + ramped.shape[1], img.shape[1])
    if x1 <= x or y1 <= y:
        return
    sub = img[y:y1, x:x1]
    local = ramped[: y1 - y, : x1 - x][..., None] * color[3]
    sub[..., :3] = np.array(color[:3], dtype=np.float32) * local + sub[..., :3] * (1.0 - local)


def _apply_vertical_sheen(src, color):
    height = src.shape[0]
    ramp = np.linspace(1.0, 0.0, height, dtype=np.float32)[:, None]
    local = ramp[..., None] * color[3]
    src[..., :3] = np.array(color[:3], dtype=np.float32) * local + src[..., :3] * (1.0 - local)
    src[..., 3:4] = np.maximum(src[..., 3:4], local)


def _remap_to_panel(px, py, bx, by, bw, bh):
    x = bx + (px / PROJ_W) * bw
    y = by + bh - (py / PROJ_H) * bh
    return x, y


def _fill_polygon(img, pts, color, bounds):
    bx0, by0, bx1, by1 = bounds
    bx1 = min(bx1, img.shape[1])
    by1 = min(by1, img.shape[0])
    if bx1 <= bx0 or by1 <= by0 or len(pts) < 3:
        return
    y_grid, x_grid = np.mgrid[by0:by1, bx0:bx1]
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
        cond = ((yi > y_grid) != (yj > y_grid)) & (
            x_grid < (xj - xi) * (y_grid - yi) / denom + xi
        )
        inside ^= cond
        j = i
    a = color[3]
    for c in range(3):
        img[by0:by1, bx0:bx1, c][inside] = (
            img[by0:by1, bx0:bx1, c][inside] * (1 - a) + color[c] * a
        )


def _line(img, x0, y0, x1, y1, color, width=2):
    h_img, w_img = img.shape[:2]
    n = max(int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 2), 2)
    t = np.linspace(0, 1, n)
    xs = (x0 + t * (x1 - x0)).astype(int)
    ys = (y0 + t * (y1 - y0)).astype(int)
    half = width // 2
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            xc = np.clip(xs + dx, 0, w_img - 1)
            yc = np.clip(ys + dy, 0, h_img - 1)
            img[yc, xc] = color


def _circle(img, cx, cy, r, color, width=3):
    h_img, w_img = img.shape[:2]
    bx0 = max(0, int(cx - r - width))
    bx1 = min(w_img, int(cx + r + width + 1))
    by0 = max(0, int(cy - r - width))
    by1 = min(h_img, int(cy + r + width + 1))
    if bx1 <= bx0 or by1 <= by0:
        return
    y_grid, x_grid = np.mgrid[by0:by1, bx0:bx1]
    d = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2)
    img[by0:by1, bx0:bx1][(d >= r - width / 2) & (d <= r + width / 2)] = color
