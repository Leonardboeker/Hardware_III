"""compute_state — Script CHOP callbacks.

Aggregates all pipeline state into a single CHOP with named channels
so the rest of the TD network only references one operator.

Output channels:
  puck_count   int    how many live pucks are currently visible
  area_px2     float  footprint polygon area in projector-space pixels²
                      (0 if fewer than 3 pucks)
  area_m2      float  footprint area converted to real-world m²
  method_id    int    0=none 1=masonry 2=3d_printed 3=prefab 4=reclaimed_brick
  hb_alive     int    1 = vision pipeline is running, 0 = offline / timed out

Reads from these TD nodes (must exist with these names):
  vision_in    OSC In CHOP   — puck data from CV pipeline; also receives
               /method/id from vision/main.py as fallback method source
  rfid_in      Constant CHOP (stub) or Serial DAT (real ESP32)
               — must expose method_id either as channel or via .fetch

Method priority: rfid_in (non-negative) > vision /method/id > 0 (none)
-1 = no signal from RFID; 0 = explicit NONE/reset tag scanned
"""
import math

# Physical table dimensions in metres — update after measuring the actual table.
# Used to convert area_px2 (projector pixels²) → area_m2.
# Default assumes the 900×600 working plane maps to a 0.9 m × 0.6 m table.
_TABLE_W_M = 0.9
_TABLE_H_M = 0.6
_PROJ_W    = 1280
_PROJ_H    = 720
_PX2_TO_M2 = (_TABLE_W_M / _PROJ_W) * (_TABLE_H_M / _PROJ_H)

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10

_last_hb_value  = -1
_last_hb_frame  = -1


def cook(scriptOp):
    scriptOp.clear()
    scriptOp.appendChan('puck_count')
    scriptOp.appendChan('area_px2')
    scriptOp.appendChan('method_id')
    scriptOp.appendChan('hb_alive')
    scriptOp.appendChan('area_m2')

    vision = op('vision_in')

    # heartbeat — hb_alive only goes 1 if the counter is actually advancing
    global _last_hb_value, _last_hb_frame
    try:
        hb = int(vision['vision/heartbeat:0'][0])
        td_frame = me.time.frame
        if hb != _last_hb_value:
            _last_hb_value = hb
            _last_hb_frame = td_frame
        # alive if heartbeat changed within the last 90 TD frames (~3 s at 30 fps)
        hb_alive = 1 if (td_frame - _last_hb_frame) < 90 else 0
    except Exception:
        hb = -1
        hb_alive = 0

    # live puck positions
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

    # method id — priority: RFID pedestal (non-negative) > vision ArUco token > 0 (none)
    # -1 = no signal from RFID; 0 = explicit NONE/reset tag scanned
    method_id = -1
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
            print('[state_chop] rfid_in not returning method_id — check node type/name')

    # vision fallback: osc_bridge.py sends /method/selected each frame
    if method_id < 0 and vision is not None:
        try:
            method_id = int(vision['method/selected:0'][0])
        except Exception:
            method_id = 0   # true default: no method

    if method_id < 0:
        method_id = 0

    # polygon area via shoelace on sorted points
    area = 0.0
    if len(pucks) >= 3:
        pts = list(pucks.values())
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        pts_sorted = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        area = _shoelace(pts_sorted)

    scriptOp['puck_count'][0] = len(pucks)
    scriptOp['area_px2'][0]   = area
    scriptOp['area_m2'][0]    = area * _PX2_TO_M2
    scriptOp['method_id'][0]  = method_id
    scriptOp['hb_alive'][0]   = hb_alive


def _shoelace(pts):
    n = len(pts)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return abs(a) / 2.0
