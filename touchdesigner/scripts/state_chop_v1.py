"""compute_state - Script CHOP callbacks.

Aggregates live pipeline state into one CHOP so the rest of the TD network
only references a single operator.

Output channels:
  puck_count   int    how many live pucks are visible
  area_px2     float  footprint polygon area in projector pixels squared
  area_m2      float  footprint area converted to real-world square metres
  method_id    int    0=none 1=masonry 2=3d_printed 3=prefab 4=reclaimed_brick
  hb_alive     int    1 = vision pipeline is running, 0 = offline / timed out

Reads from these TD nodes:
  vision_in    OSC In CHOP   - puck data and /method/selected fallback
  rfid_in      Constant CHOP or Serial DAT - exposes method_id

Method priority:
  rfid_in (non-negative) > vision /method/selected > 0 (none)

-1 means "no signal from RFID". 0 means an explicit NONE/reset state.
"""
import math

# Physical table dimensions in metres. Update after measuring the real table.
_TABLE_W_M = 0.9
_TABLE_H_M = 0.6
_PROJ_W = 1280
_PROJ_H = 720
_PX2_TO_M2 = (_TABLE_W_M / _PROJ_W) * (_TABLE_H_M / _PROJ_H)

FOOTPRINT_IDS = list(range(10))
LIVENESS_FRAMES = 10

_last_hb_value = -1
_last_hb_frame = -1
_last_synced_method_id = None
_last_synced_hb_alive = None

METHOD_STATE = {
    0: {"current_method": None, "selected_material": None, "current_phase_name": None},
    1: {
        "current_method": "masonry",
        "selected_material": "fired_clay_brick",
        "current_phase_name": "foundation",
    },
    2: {
        "current_method": "3d_printed",
        "selected_material": "printed_concrete_or_earth_proxy",
        "current_phase_name": "foundation",
    },
    3: {
        "current_method": "prefab",
        "selected_material": "timber_clt_prefab",
        "current_phase_name": "A1-A3",
    },
    4: {
        "current_method": "reclaimed_brick",
        "selected_material": "reclaimed_fired_clay_brick",
        "current_phase_name": "foundation",
    },
}


def cook(scriptOp):
    scriptOp.clear()
    scriptOp.appendChan("puck_count")
    scriptOp.appendChan("area_px2")
    scriptOp.appendChan("method_id")
    scriptOp.appendChan("hb_alive")
    scriptOp.appendChan("area_m2")

    vision = op("vision_in")

    global _last_hb_value, _last_hb_frame
    try:
        hb = int(vision["vision/heartbeat:0"][0])
        td_frame = me.time.frame
        if hb != _last_hb_value:
            _last_hb_value = hb
            _last_hb_frame = td_frame
        hb_alive = 1 if (td_frame - _last_hb_frame) < 90 else 0
    except Exception:
        hb = -1
        hb_alive = 0

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

    method_id = -1
    rfid = op("rfid_in")
    if rfid is not None:
        try:
            method_id = int(rfid["method_id"][0])
        except Exception:
            try:
                method_id = int(rfid.fetch("method_id", -1))
            except Exception:
                pass
        if method_id < 0:
            print("[state_chop] rfid_in not returning method_id - check node type/name")

    if method_id < 0 and vision is not None:
        try:
            method_id = int(vision["method/selected:0"][0])
        except Exception:
            method_id = 0

    if method_id < 0:
        method_id = 0

    area = 0.0
    if len(pucks) >= 3:
        pts = list(pucks.values())
        cx = sum(point[0] for point in pts) / len(pts)
        cy = sum(point[1] for point in pts) / len(pts)
        pts_sorted = sorted(pts, key=lambda point: math.atan2(point[1] - cy, point[0] - cx))
        area = _shoelace(pts_sorted)

    scriptOp["puck_count"][0] = len(pucks)
    scriptOp["area_px2"][0] = area
    scriptOp["area_m2"][0] = area * _PX2_TO_M2
    scriptOp["method_id"][0] = method_id
    scriptOp["hb_alive"][0] = hb_alive
    _sync_owner_state(scriptOp, method_id, hb_alive)


def _shoelace(points):
    total = 0.0
    for index, point in enumerate(points):
        next_point = points[(index + 1) % len(points)]
        total += point[0] * next_point[1] - next_point[0] * point[1]
    return abs(total) / 2.0


def _sync_owner_state(scriptOp, method_id, hb_alive):
    global _last_synced_method_id, _last_synced_hb_alive

    owner = scriptOp.parent()
    method_changed = method_id != _last_synced_method_id
    hb_changed = hb_alive != _last_synced_hb_alive
    if not method_changed and not hb_changed:
        return

    try:
        owner.store("hb_alive", int(hb_alive))
    except Exception:
        pass

    if method_changed:
        next_state = METHOD_STATE.get(int(method_id), METHOD_STATE[0])
        for key, value in next_state.items():
            try:
                owner.store(key, value)
            except Exception:
                pass

    try:
        refresh = owner.op("refresh_metrics_ui")
        if method_changed and refresh is not None:
            refresh.module.refresh(owner=owner)
        elif hb_changed:
            ui_state = owner.op("ui_state")
            if ui_state is not None:
                ui_state.module.compute_and_store_touchdesigner_ui(owner=owner)
    except Exception as exc:
        print(f"[state_chop] owner sync failed: {exc}")

    _last_synced_method_id = method_id
    _last_synced_hb_alive = hb_alive
