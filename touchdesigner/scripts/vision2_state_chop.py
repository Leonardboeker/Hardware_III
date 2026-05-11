"""vision2_state_chop.py — Script CHOP (drop-in upgrade for state_chop_v1.py).

Paste into the `compute_state` Script CHOP in TouchDesigner.
Cook Type: Every Frame.

Reads from:
  vision_in   OSC In CHOP  — all data from osc_bridge.py (port 7000)
  rfid_in     Constant/Serial — physical RFID fallback for method_id
              (kept for backward-compatibility; OSC method takes priority)

Output channels  (all float, consumed by render_footprint and stats_text):

  ── Backward-compatible (state_chop_v1.py) ──────────────────────────────
  puck_count      int   active footprint points sent as pucks
  area_px2        float shoelace area of the footprint polygon in proj px²
  method_id       int   0=NONE  1=MASONRY  2=3D_PRINT  3=PREFAB
  hb_alive        int   1 = pipeline alive, 0 = timed out / offline

  ── Sketch state ─────────────────────────────────────────────────────────
  sketch_points   int   footprint points placed
  sketch_walls    int   wall segments (includes closing wall when ≥3 pts)
  sketch_windows  int   windows added to walls
  is_extruded     int   1 when 3-D extrusion is active

  ── Gesture ──────────────────────────────────────────────────────────────
  gesture_id      int   0=none 1=index_only 2=peace 3=three_fingers 4=fist
  gesture_dwell   float seconds current gesture has been held
  gesture_action  int   last action: 0=none 1=place_point 2=add_window
                        3=extrude 4=undo 5=reset  (pulses for one cook)

  ── FSM content state ─────────────────────────────────────────────────
  fsm_state       int   0=IDLE 1=METHOD 2=FOOTPRINT 3=HEIGHT
                        4=VALIDATED 5=PHASE_N

Usage in expressions elsewhere in the TD network:
  op('compute_state')['method_id'][0]
  op('compute_state')['fsm_state'][0]
  op('compute_state')['gesture_action'][0]
"""

import math

FOOTPRINT_IDS   = list(range(10))   # puck IDs 0-9 (sketch point slots)
LIVENESS_FRAMES = 10                # max heartbeat lag before marking offline

# Physical table → projector calibration. Update before demo.
# Defaults: 0.9 m × 0.6 m table, 1280×720 projector.
_TABLE_W_M = 0.9
_TABLE_H_M = 0.6
_PROJ_W    = 1280
_PROJ_H    = 720
_PX2_TO_M2 = (_TABLE_W_M / _PROJ_W) * (_TABLE_H_M / _PROJ_H)

# Staleness tracking for hb_alive (module-level, persists between cooks)
_last_hb_value = -1
_last_hb_frame = -1


def cook(scriptOp):
    scriptOp.clear()

    # ── Declare all output channels ───────────────────────────────────────────
    for ch in (
        'puck_count', 'area_px2', 'area_m2', 'method_id', 'hb_alive',
        'sketch_points', 'sketch_walls', 'sketch_windows', 'is_extruded',
        'gesture_id', 'gesture_dwell', 'gesture_action',
        'fsm_state',
    ):
        scriptOp.appendChan(ch)

    vision = op('vision_in')

    # ── Heartbeat / liveness ──────────────────────────────────────────────────
    global _last_hb_value, _last_hb_frame
    try:
        hb = int(vision['vision/heartbeat:0'][0])
        td_frame = me.time.frame
        if hb != _last_hb_value:
            _last_hb_value = hb
            _last_hb_frame = td_frame
        hb_alive = 1 if (td_frame - _last_hb_frame) < 90 else 0
    except Exception:
        hb = -1
        hb_alive = 0

    # ── Puck positions (sketch footprint points) ──────────────────────────────
    pucks: dict[int, tuple[float, float]] = {}
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

    # Shoelace area over live puck positions
    area = 0.0
    if len(pucks) >= 3:
        pts = list(pucks.values())
        cx  = sum(p[0] for p in pts) / len(pts)
        cy  = sum(p[1] for p in pts) / len(pts)
        pts_sorted = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        area = _shoelace(pts_sorted)

    # ── Method ID ─────────────────────────────────────────────────────────────
    # Priority: VisionBridge /method/selected > rfid_in > 0 (NONE)
    # -1 = no signal; 0 = explicit NONE/reset; 1-4 = method selected
    method_id = -1
    try:
        method_id = int(vision['method/selected:0'][0])
    except Exception:
        pass

    if method_id < 0:
        # Fallback to rfid_in (Constant CHOP stub or Serial DAT)
        rfid = op('rfid_in')
        if rfid is not None:
            try:
                method_id = int(rfid['method_id'][0])
            except Exception:
                try:
                    method_id = int(rfid.fetch('method_id', -1))
                except Exception:
                    pass
        if method_id < 0:
            method_id = 0   # true default: no method

    # ── Sketch state ──────────────────────────────────────────────────────────
    sketch_points  = _int_chan(vision, 'sketch/points:0')
    sketch_walls   = _int_chan(vision, 'sketch/walls:0')
    sketch_windows = _int_chan(vision, 'sketch/windows:0')
    is_extruded    = _int_chan(vision, 'sketch/extruded:0')

    # ── Gesture ───────────────────────────────────────────────────────────────
    gesture_id     = _int_chan(vision,   'gesture/id:0')
    gesture_dwell  = _float_chan(vision, 'gesture/dwell:0')
    gesture_action = _int_chan(vision,   'gesture/action:0')

    # ── FSM state ─────────────────────────────────────────────────────────────
    fsm_state = _int_chan(vision, 'fsm/state:0')

    # ── Write outputs ─────────────────────────────────────────────────────────
    scriptOp['puck_count'][0]      = len(pucks)
    scriptOp['area_px2'][0]        = area
    scriptOp['area_m2'][0]         = area * _PX2_TO_M2
    scriptOp['method_id'][0]       = method_id
    scriptOp['hb_alive'][0]        = hb_alive

    scriptOp['sketch_points'][0]   = sketch_points
    scriptOp['sketch_walls'][0]    = sketch_walls
    scriptOp['sketch_windows'][0]  = sketch_windows
    scriptOp['is_extruded'][0]     = is_extruded

    scriptOp['gesture_id'][0]      = gesture_id
    scriptOp['gesture_dwell'][0]   = gesture_dwell
    scriptOp['gesture_action'][0]  = gesture_action

    scriptOp['fsm_state'][0]       = fsm_state


# ── Helpers ────────────────────────────────────────────────────────────────────

def _shoelace(pts: list) -> float:
    n = len(pts)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return abs(a) / 2.0


def _int_chan(op_node, channel: str, default: int = 0) -> int:
    try:
        return int(op_node[channel][0])
    except Exception:
        return default


def _float_chan(op_node, channel: str, default: float = 0.0) -> float:
    try:
        return float(op_node[channel][0])
    except Exception:
        return default
