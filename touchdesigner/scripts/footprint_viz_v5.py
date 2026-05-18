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
import json
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
    "top_phase_chip_1": ("top_phase_navigation", 14, 18, 108, 31),
    "top_phase_chip_2": ("top_phase_navigation", 130, 18, 108, 31),
    "top_phase_chip_3": ("top_phase_navigation", 246, 18, 108, 31),
    "top_phase_chip_4": ("top_phase_navigation", 362, 18, 108, 31),
    "top_phase_chip_5": ("top_phase_navigation", 478, 18, 108, 31),
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

PLAN_VIEW_W = 978
PLAN_VIEW_H = 560

BUILDING_ZONES = (
    {
        "id": "zone_facade_band",
        "label": "Facade Band",
        "area_m2": 24.0,
        "shape": {"x": 150, "y": 24, "w": 676, "h": 494, "rx": 20},
    },
    {
        "id": "zone_north_wing",
        "label": "North Wing",
        "area_m2": 68.0,
        "shape": {"x": 270, "y": 58, "w": 430, "h": 118, "rx": 14},
    },
    {
        "id": "zone_core",
        "label": "Core",
        "area_m2": 42.0,
        "shape": {"x": 386, "y": 194, "w": 198, "h": 124, "rx": 14},
    },
    {
        "id": "zone_west_wing",
        "label": "West Wing",
        "area_m2": 57.0,
        "shape": {"x": 198, "y": 208, "w": 154, "h": 262, "rx": 14},
    },
    {
        "id": "zone_east_wing",
        "label": "East Wing",
        "area_m2": 54.0,
        "shape": {"x": 617, "y": 208, "w": 166, "h": 262, "rx": 14},
    },
    {
        "id": "zone_south_wing",
        "label": "South Wing",
        "area_m2": 61.0,
        "shape": {"x": 294, "y": 352, "w": 383, "h": 130, "rx": 14},
    },
    {
        "id": "zone_courtyard",
        "label": "Courtyard",
        "area_m2": 36.0,
        "shape": {"x": 410, "y": 222, "w": 146, "h": 80, "rx": 10},
    },
)


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

METHOD_PREVIEW_TOPS = {
    "masonry": "method_preview_masonry",
    "3d_printed": "method_preview_3d_printed",
    "prefab": "method_preview_prefab",
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

    # ----- Phase 02.1 Slider state (HEIGHT cap + BUILDING_PHASE override) -----
    try:
        floor_val = int(op("compute_state")["floor"][0])
    except Exception:
        floor_val = 1
    floor_cap = _max_floors_for(method_id)
    floor_over_cap = (floor_val > floor_cap)

    try:
        wrapper_state_val = int(op("compute_state")["wrapper_state"][0])
    except Exception:
        wrapper_state_val = 0
    try:
        phase_index_val = int(op("compute_state")["phase_index"][0])
    except Exception:
        phase_index_val = 1

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
    _draw_main_plan(img, pucks, mc, owner)
    _draw_heartbeat_dot(img, hb_alive)

    # AUTO-BLIT text overlays from named Text TOPs
    _blit_text_overlays(img)

    # DISCONNECTED overlay — shown when vision pipeline is offline > 3 s
    if hb_alive == 0:
        _draw_disconnected(img)

    # Phase 02.1 — Floor-cap INVALID overlay (Slider A exceeds method's max_floors)
    if floor_over_cap:
        _draw_floor_cap_invalid(img, floor_val, floor_cap)

    # Phase 02.1 — Manual-Override indicator (Slider B moved within last 10 s)
    if wrapper_state_val == 1:
        _draw_manual_override(img, phase_index_val)

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


def _max_floors_for(method_id):
    """Read methods_db.json[method_id].max_floors via the in-network Text DAT.

    Returns 5 as a safe default if the DAT is missing or the field is absent.
    Phase 02.1 — see data/methods_db.json and CONTEXT.md.
    """
    try:
        db_dat = op("methods_db")
        if db_dat is None:
            return 5
        database = json.loads(db_dat.text)
        for method in database.get("methods", []):
            if int(method.get("id", -1)) == int(method_id):
                return int(method.get("max_floors", 5))
    except Exception:
        pass
    return 5


def _draw_floor_cap_invalid(img, floor_val, floor_cap):
    """Red border + diagonal X over the method_selection panel when floor > max_floors.

    Phase 02.1 — see .planning/phases/02.1-height-slider/02.1-CONTEXT.md (Slider A cap).
    Visual mirrors the DISCONNECTED feedback language so the operator gets immediate
    feedback that the slider exceeds the active method's allowed floor count.
    """
    bx, by, bw, bh = _panel_bounds("method_selection")
    red = (0.85, 0.15, 0.15, 1.0)
    border = 4
    for off in range(border):
        _line(img, bx + off,             by + off,             bx + bw - 1 - off, by + off,             red, 1)
        _line(img, bx + off,             by + bh - 1 - off,    bx + bw - 1 - off, by + bh - 1 - off,    red, 1)
        _line(img, bx + off,             by + off,             bx + off,           by + bh - 1 - off,   red, 1)
        _line(img, bx + bw - 1 - off,    by + off,             bx + bw - 1 - off, by + bh - 1 - off,    red, 1)
    cx = bx + bw // 2
    cy = by + bh // 2
    size = min(bw, bh) // 3
    _line(img, cx - size, cy - size, cx + size, cy + size, red, 4)
    _line(img, cx + size, cy - size, cx - size, cy + size, red, 4)


def _draw_manual_override(img, phase_index_val):
    """Orange dashed border around the method_selection panel when MANUAL_OVERRIDE is active.

    Phase 02.1 — see CONTEXT.md Slider B amendment. Triggered by Slider B movement.
    The wrapper auto-times-out after PHASE_OVERRIDE_FRAMES (~10 s @ 30 fps) of
    Slider B inactivity. Orange (not red) so operators can distinguish "you are
    overriding the phase" from the floor-cap "you exceeded the cap" red.
    """
    bx, by, bw, bh = _panel_bounds("method_selection")
    orange = (1.0, 0.55, 0.05, 1.0)
    border = 3
    dash_on = 12
    dash_off = 6
    for off in range(border):
        x = bx
        while x < bx + bw:
            x_end = min(x + dash_on, bx + bw - 1)
            _line(img, x, by + off,             x_end, by + off,             orange, 1)
            _line(img, x, by + bh - 1 - off,    x_end, by + bh - 1 - off,    orange, 1)
            x += dash_on + dash_off
    for off in range(border):
        y = by
        while y < by + bh:
            y_end = min(y + dash_on, by + bh - 1)
            _line(img, bx + off,             y, bx + off,             y_end, orange, 1)
            _line(img, bx + bw - 1 - off,    y, bx + bw - 1 - off,    y_end, orange, 1)
            y += dash_on + dash_off


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


def _selected_zone_ids(owner):
    try:
        raw_zone_ids = owner.fetch("selected_zone_ids", [])
    except Exception:
        raw_zone_ids = []
    if not raw_zone_ids:
        return set()
    return {str(zone_id) for zone_id in raw_zone_ids}


def _phase_navigation_items(owner):
    try:
        ui_state = owner.fetch("ui_state", {})
    except Exception:
        ui_state = {}
    if not isinstance(ui_state, dict):
        return []
    items = ui_state.get("phase_navigation_items")
    return items if isinstance(items, list) else []


def _ui_state_payload(owner):
    try:
        payload = owner.fetch("ui_state", {})
    except Exception:
        payload = {}
    return payload if isinstance(payload, dict) else {}


def _guidance_payload(owner):
    payload = _ui_state_payload(owner)
    blocks = payload.get("guidance_highlight_blocks")
    if not isinstance(blocks, list):
        blocks = []
    return {
        "target": payload.get("guidance_target"),
        "message": payload.get("guidance_message"),
        "highlight_blocks": [str(block) for block in blocks if block],
    }


def _region_bounds(region_id):
    if region_id in TEXT_BLOCKS:
        panel_id, lx, ly, bw, bh = TEXT_BLOCKS[region_id]
        return (*_block_bounds(panel_id, lx, ly, bw, bh), CARD_RADIUS)
    if region_id in PANELS:
        return (*_panel_bounds(region_id), PANEL_RADIUS)
    return None


def _anim_seconds():
    try:
        return float(me.time.seconds)
    except Exception:
        return 0.0


def _pulse_value(speed=1.7, phase=0.0):
    return 0.5 + 0.5 * math.sin(_anim_seconds() * speed * math.pi * 2.0 + phase)


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
        tex = _top_pixels_rgba(text_op)
        if tex is None:
            continue

        bx, by, bw, bh = bounds
        _blit_alpha(img, tex, bx, by, bw, bh)


def _top_pixels_rgba(top_op):
    if top_op is None:
        return None
    try:
        tex = top_op.numpyArray(delayed=True)
    except Exception:
        return None
    if tex is None:
        return None

    if tex.shape[-1] == 3:
        alpha = np.ones((*tex.shape[:2], 1), dtype=tex.dtype)
        tex = np.concatenate([tex, alpha], axis=-1)

    if tex.dtype == np.uint8:
        tex = tex.astype(np.float32) / 255.0
    elif tex.dtype != np.float32:
        tex = tex.astype(np.float32)
    return tex


def _resample_cover(src, target_h, target_w):
    src_h, src_w = src.shape[:2]
    if src_h <= 0 or src_w <= 0 or target_h <= 0 or target_w <= 0:
        return None

    src_aspect = float(src_w) / float(src_h)
    target_aspect = float(target_w) / float(target_h)
    cropped = src
    if src_aspect > target_aspect:
        crop_w = max(1, int(round(src_h * target_aspect)))
        x0 = max(0, (src_w - crop_w) // 2)
        cropped = src[:, x0 : x0 + crop_w]
    elif src_aspect < target_aspect:
        crop_h = max(1, int(round(src_w / target_aspect)))
        y0 = max(0, (src_h - crop_h) // 2)
        cropped = src[y0 : y0 + crop_h, :]

    ys = (np.arange(target_h) * cropped.shape[0] / target_h).astype(int)
    xs = (np.arange(target_w) * cropped.shape[1] / target_w).astype(int)
    return cropped[ys][:, xs]


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
def _draw_main_plan(img, pucks, method_color, owner):
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
    _draw_building_zones(
        img,
        shell_x,
        shell_y,
        shell_w,
        shell_h,
        method_color,
        _selected_zone_ids(owner),
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


def _draw_building_zones(img, x, y, w, h, method_color, selected_zone_ids):
    sorted_zones = sorted(BUILDING_ZONES, key=lambda zone: float(zone["area_m2"]), reverse=True)
    for zone in sorted_zones:
        shape = zone["shape"]
        zone_x = int(round(x + (float(shape["x"]) / PLAN_VIEW_W) * w))
        zone_y = int(round(y + (float(shape["y"]) / PLAN_VIEW_H) * h))
        zone_w = max(1, int(round((float(shape["w"]) / PLAN_VIEW_W) * w)))
        zone_h = max(1, int(round((float(shape["h"]) / PLAN_VIEW_H) * h)))
        zone_radius = max(6, int(round((float(shape.get("rx", 0)) / PLAN_VIEW_W) * w)))
        is_selected = str(zone["id"]) in selected_zone_ids

        if zone["id"] == "zone_facade_band":
            fill = (*method_color, 0.09) if is_selected else (0.0, 0.0, 0.0, 0.0)
            edge = (*method_color, 0.78) if is_selected else (1.0, 1.0, 1.0, 0.08)
            accent = (*method_color, 0.22) if is_selected else (0.0, 0.0, 0.0, 0.0)
        else:
            fill = (*method_color, 0.14) if is_selected else (1.0, 1.0, 1.0, 0.035)
            edge = (*method_color, 0.85) if is_selected else (1.0, 1.0, 1.0, 0.08)
            accent = (*method_color, 0.16) if is_selected else (0.0, 0.0, 0.0, 0.0)

        _draw_panel_frame(
            img,
            zone_x,
            zone_y,
            zone_w,
            zone_h,
            fill=fill,
            edge=edge,
            edge_w=1,
            radius=zone_radius,
            accent=accent,
        )


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

    for block_id, item in zip(
        (
            "top_phase_chip_1",
            "top_phase_chip_2",
            "top_phase_chip_3",
            "top_phase_chip_4",
            "top_phase_chip_5",
        ),
        _phase_navigation_items(owner),
    ):
        panel_id, lx, ly, bw, bh = TEXT_BLOCKS[block_id]
        is_active = bool(item.get("active"))
        is_disabled = bool(item.get("disabled"))
        fill = (*accent_rgb, 0.15) if is_active else (1.0, 1.0, 1.0, 0.028)
        edge = (*accent_rgb, 0.34) if is_active else (1.0, 1.0, 1.0, 0.078)
        accent = (*accent_rgb, 0.24) if is_active else (0.0, 0.0, 0.0, 0.0)
        if is_disabled:
            fill = (1.0, 1.0, 1.0, 0.020)
            edge = (1.0, 1.0, 1.0, 0.045)
            accent = (0.0, 0.0, 0.0, 0.0)
        _draw_inset_card(
            img,
            *_block_bounds(panel_id, lx, ly, bw, bh),
            fill=fill,
            edge=edge,
            accent=accent,
        )

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

    preview_methods = _draw_method_card_previews(img, selected_method)
    _draw_guidance_layer(img, owner, accent_rgb)
    _draw_phase_chip_symbols(img, _phase_navigation_items(owner), accent_rgb)
    _draw_method_card_symbols(img, selected_method, accent_rgb, skip_methods=preview_methods)


def _draw_guidance_layer(img, owner, accent_rgb):
    guidance = _guidance_payload(owner)
    highlight_blocks = guidance.get("highlight_blocks", [])
    if not highlight_blocks:
        return

    for index, region_id in enumerate(highlight_blocks):
        bounds = _region_bounds(region_id)
        if bounds is None:
            continue
        x, y, w, h, radius = bounds
        pulse = 0.45 + 0.55 * _pulse_value(1.35, index * 0.32)
        is_panel = region_id in PANELS
        _draw_guidance_halo(
            img,
            x,
            y,
            w,
            h,
            radius,
            (*accent_rgb, (0.28 if is_panel else 0.20) * pulse),
            pulse_strength=pulse,
            is_panel=is_panel,
        )


def _draw_guidance_halo(img, x, y, w, h, radius, color, pulse_strength, is_panel=False):
    spreads = (
        (28 if is_panel else 18, 0.030 if is_panel else 0.020),
        (16 if is_panel else 10, 0.060 if is_panel else 0.042),
        (7 if is_panel else 4, 0.130 if is_panel else 0.095),
    )
    for spread, alpha in spreads:
        _draw_rounded_outline_glow(
            img,
            x - spread,
            y - spread,
            w + spread * 2,
            h + spread * 2,
            radius + spread,
            max(2, spread // 4),
            (color[0], color[1], color[2], alpha * pulse_strength),
        )
    if is_panel:
        _draw_guidance_beacons(
            img,
            x,
            y,
            w,
            h,
            (color[0], color[1], color[2], 0.26 * pulse_strength),
        )
    _draw_rounded_outline_glow(
        img,
        x - 1,
        y - 1,
        w + 2,
        h + 2,
        radius + 1,
        1,
        (color[0], color[1], color[2], 0.18 * pulse_strength),
    )


def _draw_guidance_beacons(img, x, y, w, h, color):
    margin = 10
    outer = 14
    length = 18
    line_w = 1.6

    corners = (
        (x - outer, y - outer, 1, 1),
        (x + w + outer, y - outer, -1, 1),
        (x - outer, y + h + outer, 1, -1),
        (x + w + outer, y + h + outer, -1, -1),
    )
    for cx, cy, sx, sy in corners:
        _line_blend(img, cx, cy, cx + sx * length, cy, color, line_w)
        _line_blend(img, cx, cy, cx, cy + sy * length, color, line_w)
        _line_blend(
            img,
            cx + sx * (length * 0.35),
            cy,
            cx + sx * (length + margin * 0.45),
            cy,
            (color[0], color[1], color[2], color[3] * 0.45),
            1.0,
        )
        _line_blend(
            img,
            cx,
            cy + sy * (length * 0.35),
            cx,
            cy + sy * (length + margin * 0.45),
            (color[0], color[1], color[2], color[3] * 0.45),
            1.0,
        )


def _draw_rounded_outline_glow(img, x, y, w, h, radius, thickness, color):
    x = int(round(x))
    y = int(round(y))
    w = int(round(w))
    h = int(round(h))
    if w <= 0 or h <= 0 or color[3] <= 0:
        return

    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(img.shape[1], x + w)
    y1 = min(img.shape[0], y + h)
    if x1 <= x0 or y1 <= y0:
        return

    target_w = x1 - x0
    target_h = y1 - y0
    local_radius = max(0, min(int(radius), target_h // 2, target_w // 2))
    outer = _rounded_rect_mask(target_h, target_w, local_radius)
    inner = _inset_mask(target_h, target_w, local_radius, int(max(1, thickness)))
    ring = outer & ~inner
    _blend_mask(img, x0, y0, ring, color)


def _draw_phase_chip_symbols(img, phase_items, accent_rgb):
    for index, item in enumerate(phase_items):
        block_id = item.get("block_id")
        if not block_id or not item.get("label"):
            continue
        bounds = _region_bounds(str(block_id))
        if bounds is None:
            continue
        x, y, w, h, _radius = bounds
        active = bool(item.get("active"))
        disabled = bool(item.get("disabled"))
        if active:
            color = (*accent_rgb, 0.56)
        elif disabled:
            color = (0.96, 0.94, 0.90, 0.08)
        else:
            color = (0.96, 0.94, 0.90, 0.20)
        _draw_stage_symbol(
            img,
            str(item.get("stage") or ""),
            str(item.get("mode") or "phase"),
            x + 16,
            y + h / 2.0,
            color,
            scale=1.0,
        )


def _draw_method_card_previews(img, selected_method):
    drawn_methods = set()
    for method_key, block_id in (
        ("masonry", "method_card_masonry"),
        ("3d_printed", "method_card_3d_printed"),
        ("prefab", "method_card_prefab"),
    ):
        preview_op = op(METHOD_PREVIEW_TOPS.get(method_key, ""))
        preview = _top_pixels_rgba(preview_op)
        if preview is None:
            continue

        bounds = _region_bounds(block_id)
        if bounds is None:
            continue
        x, y, w, h, _radius = bounds
        inner_x = int(x + 4)
        inner_y = int(y + 4)
        inner_w = int(max(1, w - 8))
        inner_h = int(max(1, h - 8))
        texture = _resample_cover(preview, inner_h, inner_w)
        if texture is None:
            continue

        method_rgb = np.array(
            METHOD_COLORS.get(METHOD_IDS.get(method_key, 0), (0.72, 0.70, 0.66)),
            dtype=np.float32,
        ).reshape(1, 1, 3)
        texture_rgb = texture[..., :3]
        luminance = np.mean(texture_rgb, axis=2, keepdims=True)
        is_active = method_key == selected_method
        overlay_alpha = 0.34 if is_active else 0.44
        texture_rgb = texture_rgb * (0.78 if is_active else 0.66)
        texture_rgb = texture_rgb * (1.0 - overlay_alpha) + method_rgb * overlay_alpha

        xs = np.linspace(0.0, 1.0, inner_w, dtype=np.float32).reshape(1, inner_w, 1)
        ys = np.linspace(0.0, 1.0, inner_h, dtype=np.float32).reshape(inner_h, 1, 1)
        glass_color = np.array(C_BG_MID[:3], dtype=np.float32).reshape(1, 1, 3)
        text_shadow = np.clip(0.78 - xs * 0.62, 0.16, 0.78)
        top_haze = np.clip(0.22 - ys * 0.16, 0.0, 0.22)
        glass_alpha = text_shadow + top_haze
        texture_rgb = texture_rgb * (1.0 - glass_alpha) + glass_color * glass_alpha
        texture_rgb = np.clip(texture_rgb * 0.88 + luminance * 0.06, 0.0, 1.0)

        texture_alpha = texture[..., 3:4] * (0.92 if is_active else 0.82)
        mask = _rounded_rect_mask(inner_h, inner_w, 11).astype(np.float32)[..., None]
        texture_rgba = np.concatenate([texture_rgb, texture_alpha * mask], axis=-1)
        _blit_alpha(img, texture_rgba, inner_x, inner_y, inner_w, inner_h)

        _draw_rounded_outline_glow(
            img,
            inner_x,
            inner_y,
            inner_w,
            inner_h,
            11,
            1,
            (method_rgb[0, 0, 0], method_rgb[0, 0, 1], method_rgb[0, 0, 2], 0.16 if is_active else 0.08),
        )
        drawn_methods.add(method_key)

    return drawn_methods


def _draw_method_card_symbols(img, selected_method, accent_rgb, skip_methods=None):
    skip_methods = skip_methods or set()
    for method_key, block_id in (
        ("masonry", "method_card_masonry"),
        ("3d_printed", "method_card_3d_printed"),
        ("prefab", "method_card_prefab"),
    ):
        if method_key in skip_methods:
            continue
        bounds = _region_bounds(block_id)
        if bounds is None:
            continue
        x, y, w, h, _radius = bounds
        is_active = method_key == selected_method
        color = (*accent_rgb, 0.34) if is_active else (0.96, 0.94, 0.90, 0.13)
        _draw_method_symbol(
            img,
            method_key,
            x + w - 34,
            y + 28,
            color,
            scale=1.18,
        )


def _draw_method_symbol(img, method_key, cx, cy, color, scale=1.0):
    if method_key == "masonry":
        _rect_outline_blend(img, cx - 12 * scale, cy - 8 * scale, 24 * scale, 16 * scale, color, 1.2)
        _line_blend(img, cx - 12 * scale, cy - 1 * scale, cx + 12 * scale, cy - 1 * scale, color, 1.1)
        _line_blend(img, cx - 12 * scale, cy + 6 * scale, cx + 12 * scale, cy + 6 * scale, color, 1.1)
        _line_blend(img, cx - 5 * scale, cy - 8 * scale, cx - 5 * scale, cy - 1 * scale, color, 1.0)
        _line_blend(img, cx + 3 * scale, cy - 8 * scale, cx + 3 * scale, cy - 1 * scale, color, 1.0)
        _line_blend(img, cx - 9 * scale, cy - 1 * scale, cx - 9 * scale, cy + 6 * scale, color, 1.0)
        _line_blend(img, cx - 1 * scale, cy - 1 * scale, cx - 1 * scale, cy + 6 * scale, color, 1.0)
        _line_blend(img, cx + 7 * scale, cy - 1 * scale, cx + 7 * scale, cy + 6 * scale, color, 1.0)
        return

    if method_key == "3d_printed":
        _line_blend(img, cx - 9 * scale, cy - 7 * scale, cx - 2 * scale, cy - 7 * scale, color, 1.0)
        _line_blend(img, cx - 2 * scale, cy - 7 * scale, cx + 1 * scale, cy - 1 * scale, color, 1.0)
        _line_blend(img, cx + 1 * scale, cy - 1 * scale, cx - 1 * scale, cy + 2 * scale, color, 1.0)
        for offset in (-3, 2, 7):
            _line_blend(img, cx - 12 * scale, cy + offset * scale, cx + 9 * scale, cy + offset * scale, color, 1.4)
        return

    _rect_outline_blend(img, cx - 13 * scale, cy - 9 * scale, 10 * scale, 8 * scale, color, 1.0)
    _rect_outline_blend(img, cx + 3 * scale, cy - 9 * scale, 10 * scale, 8 * scale, color, 1.0)
    _rect_outline_blend(img, cx - 5 * scale, cy + 2 * scale, 10 * scale, 8 * scale, color, 1.0)
    _line_blend(img, cx - 3 * scale, cy - 1 * scale, cx - 3 * scale, cy + 2 * scale, color, 0.95)
    _line_blend(img, cx + 3 * scale, cy - 1 * scale, cx + 3 * scale, cy + 2 * scale, color, 0.95)


def _draw_stage_symbol(img, stage_key, mode, cx, cy, color, scale=1.0):
    if mode == "lifecycle":
        _draw_lifecycle_symbol(img, stage_key, cx, cy, color, scale)
        return

    if stage_key == "foundation":
        _line_blend(img, cx - 9 * scale, cy + 5 * scale, cx + 9 * scale, cy + 5 * scale, color, 1.3)
        _line_blend(img, cx - 6 * scale, cy + 1 * scale, cx - 2 * scale, cy + 1 * scale, color, 1.1)
        _line_blend(img, cx + 2 * scale, cy + 1 * scale, cx + 6 * scale, cy + 1 * scale, color, 1.1)
        _line_blend(img, cx - 4 * scale, cy - 5 * scale, cx - 4 * scale, cy + 1 * scale, color, 1.0)
        _line_blend(img, cx + 4 * scale, cy - 5 * scale, cx + 4 * scale, cy + 1 * scale, color, 1.0)
        return

    if stage_key == "structure":
        _rect_outline_blend(img, cx - 8 * scale, cy - 6 * scale, 16 * scale, 12 * scale, color, 1.1)
        _line_blend(img, cx - 3 * scale, cy - 6 * scale, cx - 3 * scale, cy + 6 * scale, color, 0.95)
        _line_blend(img, cx + 3 * scale, cy - 1 * scale, cx + 3 * scale, cy + 6 * scale, color, 0.95)
        _line_blend(img, cx - 8 * scale, cy, cx + 8 * scale, cy, color, 0.95)
        return

    if stage_key == "roof":
        _line_blend(img, cx - 9 * scale, cy + 1 * scale, cx, cy - 6 * scale, color, 1.25)
        _line_blend(img, cx, cy - 6 * scale, cx + 9 * scale, cy + 1 * scale, color, 1.25)
        _line_blend(img, cx - 11 * scale, cy + 1 * scale, cx + 11 * scale, cy + 1 * scale, color, 1.05)
        _line_blend(img, cx - 6 * scale, cy + 1 * scale, cx - 6 * scale, cy + 6 * scale, color, 0.95)
        _line_blend(img, cx + 6 * scale, cy + 1 * scale, cx + 6 * scale, cy + 6 * scale, color, 0.95)
        _line_blend(img, cx - 6 * scale, cy + 6 * scale, cx + 6 * scale, cy + 6 * scale, color, 0.9)
        return

    if stage_key == "openings":
        _rect_outline_blend(img, cx - 7 * scale, cy - 6 * scale, 14 * scale, 12 * scale, color, 1.1)
        _line_blend(img, cx, cy - 6 * scale, cx, cy + 6 * scale, color, 1.0)
        _line_blend(img, cx - 7 * scale, cy, cx + 7 * scale, cy, color, 1.0)
        return

    _line_blend(img, cx - 8 * scale, cy + 6 * scale, cx - 1 * scale, cy - 6 * scale, color, 1.2)
    _line_blend(img, cx - 1 * scale, cy - 6 * scale, cx + 8 * scale, cy - 2 * scale, color, 1.2)
    _line_blend(img, cx + 4 * scale, cy - 4 * scale, cx + 8 * scale, cy - 2 * scale, color, 1.0)
    _line_blend(img, cx + 4 * scale, cy - 4 * scale, cx + 2 * scale, cy + 1 * scale, color, 1.0)


def _draw_lifecycle_symbol(img, stage_key, cx, cy, color, scale=1.0):
    if stage_key == "A1-A3":
        _rect_outline_blend(img, cx - 8 * scale, cy - 6 * scale, 16 * scale, 12 * scale, color, 1.0)
        _line_blend(img, cx - 8 * scale, cy - 1 * scale, cx + 8 * scale, cy - 1 * scale, color, 0.95)
        _line_blend(img, cx - 4 * scale, cy - 6 * scale, cx - 4 * scale, cy - 1 * scale, color, 0.9)
        _line_blend(img, cx + 2 * scale, cy - 6 * scale, cx + 2 * scale, cy - 1 * scale, color, 0.9)
        return

    if stage_key == "A4":
        _rect_outline_blend(img, cx - 9 * scale, cy - 4 * scale, 7 * scale, 8 * scale, color, 0.95)
        _line_blend(img, cx - 1 * scale, cy, cx + 8 * scale, cy, color, 1.2)
        _line_blend(img, cx + 4 * scale, cy - 4 * scale, cx + 8 * scale, cy, color, 1.2)
        _line_blend(img, cx + 4 * scale, cy + 4 * scale, cx + 8 * scale, cy, color, 1.2)
        return

    if stage_key == "A5":
        _rect_outline_blend(img, cx - 9 * scale, cy - 5 * scale, 7 * scale, 10 * scale, color, 0.95)
        _rect_outline_blend(img, cx + 2 * scale, cy - 5 * scale, 7 * scale, 10 * scale, color, 0.95)
        _line_blend(img, cx - 1 * scale, cy - 3 * scale, cx + 1 * scale, cy - 3 * scale, color, 0.95)
        _line_blend(img, cx - 1 * scale, cy + 3 * scale, cx + 1 * scale, cy + 3 * scale, color, 0.95)
        return

    if stage_key == "B":
        _circle_ring_blend(img, cx, cy, 6 * scale, color, thickness=1.1, arc_span=1.0)
        _stamp_disc(img, cx, cy, 1.4 * scale, color)
        return

    _circle_ring_blend(img, cx, cy, 6 * scale, color, thickness=1.0, arc_span=0.84)
    _line_blend(img, cx + 1 * scale, cy - 7 * scale, cx + 7 * scale, cy - 3 * scale, color, 0.95)
    _line_blend(img, cx + 7 * scale, cy - 3 * scale, cx + 4 * scale, cy + 2 * scale, color, 0.95)


def _rect_outline_blend(img, x, y, w, h, color, thickness=1.0):
    _draw_rounded_outline_glow(img, x, y, w, h, 3, max(1, int(round(thickness))), color)


def _circle_ring_blend(img, cx, cy, radius, color, thickness=1.0, arc_span=1.0):
    steps = max(18, int(radius * 8))
    sweep = max(0.15, min(1.0, float(arc_span))) * math.pi * 2.0
    start = -math.pi * 0.5
    for index in range(steps):
        theta = start + (index / max(1, steps - 1)) * sweep
        _stamp_disc(
            img,
            cx + math.cos(theta) * radius,
            cy + math.sin(theta) * radius,
            max(0.8, thickness / 2.0),
            color,
        )


def _line_blend(img, x0, y0, x1, y1, color, thickness=1.0):
    length = max(abs(x1 - x0), abs(y1 - y0))
    steps = max(8, int(length * 2))
    for index in range(steps + 1):
        t = index / max(1, steps)
        _stamp_disc(
            img,
            x0 + (x1 - x0) * t,
            y0 + (y1 - y0) * t,
            max(0.8, thickness / 2.0),
            color,
        )


def _stamp_disc(img, cx, cy, radius, color):
    if color[3] <= 0 or radius <= 0:
        return
    bx0 = max(0, int(math.floor(cx - radius - 1)))
    by0 = max(0, int(math.floor(cy - radius - 1)))
    bx1 = min(img.shape[1], int(math.ceil(cx + radius + 1)))
    by1 = min(img.shape[0], int(math.ceil(cy + radius + 1)))
    if bx1 <= bx0 or by1 <= by0:
        return

    y_grid, x_grid = np.mgrid[by0:by1, bx0:bx1]
    mask = ((x_grid - cx) ** 2 + (y_grid - cy) ** 2) <= radius**2
    _blend_mask(img, bx0, by0, mask, color)


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
