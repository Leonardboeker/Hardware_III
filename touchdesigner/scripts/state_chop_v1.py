"""State CHOP — Script CHOP callbacks v1.

Aggregates all pipeline state into a single CHOP with named channels
so the rest of the TD network only needs to reference one operator.

Output channels:
  puck_count   int    how many live pucks are currently visible
  area_px2     float  footprint polygon area in projector-space pixels²
                      (0 if fewer than 3 pucks)
  method_id    int    0=none 1=cantilever 2=column_grid 3=arch 4=truss
                      set by RFID reader via serial1 DAT storage
  hb_alive     int    1 = vision pipeline is running, 0 = offline / timed out

Dependencies (named operators in the same base COMP):
  oscin1       OSC In CHOP    — vision pipeline data
  serial1      Serial DAT     — ESP32/RFID data (optional; method_id=0 if absent)
"""
import math

FOOTPRINT_IDS   = list(range(10))
LIVENESS_FRAMES = 10


def cook(scriptOp):
    scriptOp.clear()
    scriptOp.appendChan('puck_count')
    scriptOp.appendChan('area_px2')
    scriptOp.appendChan('method_id')
    scriptOp.appendChan('hb_alive')

    osc = op('osc')

    # heartbeat
    try:
        hb = int(osc['vision/heartbeat:0'][0])
        hb_alive = 1
    except Exception:
        hb = -1
        hb_alive = 0

    # live puck positions
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

    # method id from serial DAT storage (written by serial_rfid_v1 callbacks)
    method_id = 0
    try:
        method_id = int(op('rfid').fetch('method_id', 0))
    except Exception:
        pass

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
    scriptOp['method_id'][0]  = method_id
    scriptOp['hb_alive'][0]   = hb_alive


def _shoelace(pts):
    n = len(pts)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return abs(a) / 2.0
