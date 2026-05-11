"""vision2_state_chop.py - Script CHOP.

Drop-in upgrade for state_chop_v1.py when the richer vision/FSM channels are
available from the OSC bridge.
"""
import math

FOOTPRINT_IDS = list(range(10))
LIVENESS_FRAMES = 10
HB_TIMEOUT_TICKS = 90

_TABLE_W_M = 0.9
_TABLE_H_M = 0.6
_PROJ_W = 1280
_PROJ_H = 720
_PX2_TO_M2 = (_TABLE_W_M / _PROJ_W) * (_TABLE_H_M / _PROJ_H)

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
    for channel_name in (
        "puck_count",
        "area_px2",
        "area_m2",
        "method_id",
        "hb_alive",
        "sketch_points",
        "sketch_walls",
        "sketch_windows",
        "is_extruded",
        "gesture_id",
        "gesture_dwell",
        "gesture_action",
        "fsm_state",
    ):
        scriptOp.appendChan(channel_name)

    vision = op("vision_in")

    global _last_hb_value, _last_hb_frame
    try:
        hb = int(vision["vision/heartbeat:0"][0])
        td_frame = me.time.frame
        if hb != _last_hb_value:
            _last_hb_value = hb
            _last_hb_frame = td_frame
        hb_alive = 1 if (td_frame - _last_hb_frame) < HB_TIMEOUT_TICKS else 0
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

    area = 0.0
    if len(pucks) >= 3:
        points = list(pucks.values())
        cx = sum(point[0] for point in points) / len(points)
        cy = sum(point[1] for point in points) / len(points)
        points = sorted(points, key=lambda point: math.atan2(point[1] - cy, point[0] - cx))
        area = _shoelace(points)

    method_id = -1
    try:
        method_id = int(vision["method/selected:0"][0])
    except Exception:
        pass

    if method_id < 0:
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
            method_id = 0

    scriptOp["puck_count"][0] = len(pucks)
    scriptOp["area_px2"][0] = area
    scriptOp["area_m2"][0] = area * _PX2_TO_M2
    scriptOp["method_id"][0] = method_id
    scriptOp["hb_alive"][0] = hb_alive
    scriptOp["sketch_points"][0] = _int_chan(vision, "sketch/points:0")
    scriptOp["sketch_walls"][0] = _int_chan(vision, "sketch/walls:0")
    scriptOp["sketch_windows"][0] = _int_chan(vision, "sketch/windows:0")
    scriptOp["is_extruded"][0] = _int_chan(vision, "sketch/extruded:0")
    scriptOp["gesture_id"][0] = _int_chan(vision, "gesture/id:0")
    scriptOp["gesture_dwell"][0] = _float_chan(vision, "gesture/dwell:0")
    scriptOp["gesture_action"][0] = _int_chan(vision, "gesture/action:0")
    scriptOp["fsm_state"][0] = _int_chan(vision, "fsm/state:0")
    _sync_owner_state(scriptOp, method_id, hb_alive)


def _shoelace(points):
    total = 0.0
    for index, point in enumerate(points):
        next_point = points[(index + 1) % len(points)]
        total += point[0] * next_point[1] - next_point[0] * point[1]
    return abs(total) / 2.0


def _int_chan(op_node, channel, default=0):
    try:
        return int(op_node[channel][0])
    except Exception:
        return default


def _float_chan(op_node, channel, default=0.0):
    try:
        return float(op_node[channel][0])
    except Exception:
        return default


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
        print(f"[vision2_state] owner sync failed: {exc}")

    _last_synced_method_id = method_id
    _last_synced_hb_alive = hb_alive
