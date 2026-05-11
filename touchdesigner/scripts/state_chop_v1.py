"""compute_state — Script CHOP callbacks.

Aggregates all pipeline state into a single CHOP with named channels
so the rest of the TD network only references one operator.

Output channels:
  puck_count   int    how many live pucks are currently visible
  area_px2     float  footprint polygon area in projector-space pixels²
                      (0 if fewer than 3 pucks)
  method_id    int    0=none 1=masonry 2=3d_printed 3=prefab 4=reclaimed_brick
  hb_alive     int    1 = vision pipeline is running, 0 = offline / timed out

Reads from these TD nodes (must exist with these names):
  vision_in    OSC In CHOP   — puck data from CV pipeline; also receives
               /method/id from vision/main.py as fallback method source
  rfid_in      Constant CHOP (stub) or Serial DAT (real ESP32)
               — must expose method_id either as channel or via .fetch

Method priority: rfid_in (non-zero) > vision /method/id > 0 (none)
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

    vision = op('vision_in')

    # heartbeat
    try:
        hb = int(vision['vision/heartbeat:0'][0])
        hb_alive = 1
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

    # method id — priority: RFID pedestal > vision ArUco token > 0 (none)
    method_id = 0
    rfid = op('rfid_in')
    if rfid is not None:
        try:
            method_id = int(rfid['method_id'][0])
        except Exception:
            try:
                method_id = int(rfid.fetch('method_id', 0))
            except Exception:
                pass

    # vision fallback: vision/main.py sends /method/id on the same OSC port
    # so vision_in already has it — no extra TD node needed
    if method_id == 0 and vision is not None:
        try:
            method_id = int(vision['method/id:0'][0])
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
