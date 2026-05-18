"""vision2_state_chop.py - Script CHOP.

Drop-in upgrade for state_chop_v1.py when the richer vision/FSM channels are
available from the OSC bridge.
"""
import json
import math

FOOTPRINT_IDS = list(range(10))
LIVENESS_FRAMES = 10
HB_TIMEOUT_TICKS = 90

# Phase 02.1 Slider integration — see .planning/phases/02.1-height-slider/02.1-CONTEXT.md
SLIDER_TIMEOUT_TICKS = 60       # frames of silence on SLIDER:/PSLIDER: before *_alive → 0 (~2s @ 30 fps)
PHASE_OVERRIDE_FRAMES = 300     # 10 s @ 30 fps — wrapper_state stays MANUAL_OVERRIDE this long
PHASE_OVERRIDE_THRESHOLD = 0.05 # raw value delta to trigger override (5 % travel)
PHASE_HYST_EPSILON = 0.02       # TD-side hysteresis nudge for phase_index quantization

_TABLE_W_M = 0.9
_TABLE_H_M = 0.6
_PROJ_W = 1280
_PROJ_H = 720
_PX2_TO_M2 = (_TABLE_W_M / _PROJ_W) * (_TABLE_H_M / _PROJ_H)

_last_hb_value = -1
_last_hb_frame = -1
_last_synced_method_id = None
_last_synced_hb_alive = None

# Phase-slider state (persists between cooks) — Slider B (BUILDING_PHASE) amendment
_last_phase_slider_value = -1.0     # last raw value seen, for movement detection
_last_phase_index = 1               # last quantized phase
_last_phase_center = 0.0            # for TD-side hysteresis
_manual_override_until_frame = -1   # me.time.frame at which override expires

# methods_db cache (avoid re-parsing JSON every cook — 30 Hz file I/O is expensive)
_methods_db_cache = None
_methods_db_text_hash = None

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
        # --- Phase 02.1 Slider A (HEIGHT) ---
        "floor",
        "slider_raw",
        "slider_alive",
        # --- Phase 02.1 Slider B (BUILDING_PHASE, Manual-Override-Only) ---
        "phase_slider_raw",
        "phase_index",
        "phase_slider_alive",
        "wrapper_state",
    ):
        scriptOp.appendChan(channel_name)

    vision = op("vision_in")

    # Heartbeat - tolerate both 'vision/heartbeat' (single-arg) and 'vision/heartbeat:0'
    global _last_hb_value, _last_hb_frame
    hb = -1
    for hb_name in ("vision/heartbeat", "vision/heartbeat:0"):
        try:
            hb = int(vision[hb_name][0])
            break
        except Exception:
            pass
    if hb >= 0:
        td_frame = me.time.frame
        if hb != _last_hb_value:
            _last_hb_value = hb
            _last_hb_frame = td_frame
        hb_alive = 1 if (td_frame - _last_hb_frame) < HB_TIMEOUT_TICKS else 0
    else:
        hb_alive = 0

    # Puck channel naming auto-detection. Elias's main.py uses flat-1-indexed:
    #   /puck/<id> arg0 arg1 arg2  -> channels puck/<id>1, puck/<id>2, puck/<id>3
    # Older builds may use colon: puck/<id>:0, puck/<id>:1, puck/<id>:2
    # Or flat-0: puck/<id>0, puck/<id>1, puck/<id>2
    import re as _re
    _puck_re_flat1 = _re.compile(r'^puck/(\d+)1$')
    _puck_re_colon = _re.compile(r'^puck/(\d+):0$')
    _puck_re_flat0 = _re.compile(r'^puck/(\d+)0$')

    chan_names = [c.name for c in vision.chans('*')]
    puck_ids_flat1 = set()
    puck_ids_colon = set()
    puck_ids_flat0 = set()
    for name in chan_names:
        m = _puck_re_flat1.match(name)
        if m and not name.endswith(':0'):
            puck_ids_flat1.add(int(m.group(1)))
            continue
        m = _puck_re_colon.match(name)
        if m:
            puck_ids_colon.add(int(m.group(1)))
            continue
        m = _puck_re_flat0.match(name)
        if m:
            puck_ids_flat0.add(int(m.group(1)))

    # Pick the mode that found the most puck IDs
    if len(puck_ids_flat1) >= len(puck_ids_colon) and len(puck_ids_flat1) >= len(puck_ids_flat0):
        puck_mode = 'flat1'
        puck_ids = sorted(puck_ids_flat1)
    elif len(puck_ids_colon) >= len(puck_ids_flat0):
        puck_mode = 'colon'
        puck_ids = sorted(puck_ids_colon)
    else:
        puck_mode = 'flat0'
        puck_ids = sorted(puck_ids_flat0)

    def _puck_arg(pid, idx):
        """Read arg idx (0-based) for puck pid. 0=frame, 1=x, 2=y."""
        if puck_mode == 'flat1':
            name = f'puck/{pid}{idx + 1}'
        elif puck_mode == 'colon':
            name = f'puck/{pid}:{idx}'
        else:  # flat0
            name = f'puck/{pid}{idx}'
        try:
            return vision[name][0]
        except Exception:
            return None

    pucks = {}
    for pid in puck_ids:
        try:
            pf_raw = _puck_arg(pid, 0)
            if pf_raw is None:
                continue
            pf = int(pf_raw)
            if hb >= 0 and abs(hb - pf) <= LIVENESS_FRAMES:
                px = _puck_arg(pid, 1)
                py = _puck_arg(pid, 2)
                if px is not None and py is not None:
                    pucks[pid] = (float(px), float(py))
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

    rfid = op("rfid_in")
    if method_id < 0:
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

    # --- Slider A (HEIGHT) — read from Serial DAT storage ---
    floor_val = 1
    slider_raw_val = 0.0
    slider_alive = 0
    if rfid is not None:
        try:
            floor_val = int(rfid.fetch("floor", 1))
        except Exception:
            pass
        try:
            slider_raw_val = float(rfid.fetch("slider_raw", 0.0))
        except Exception:
            pass
        try:
            slider_last = int(rfid.fetch("slider_last_frame", -1))
            if slider_last >= 0 and (me.time.frame - slider_last) < SLIDER_TIMEOUT_TICKS:
                slider_alive = 1
        except Exception:
            pass

    # --- Slider B (BUILDING_PHASE, Manual-Override-Only) — read + TD-side quantization ---
    global _last_phase_slider_value, _last_phase_index, _last_phase_center, _manual_override_until_frame
    phase_slider_raw_val = 0.0
    phase_slider_alive = 0
    if rfid is not None:
        try:
            phase_slider_raw_val = float(rfid.fetch("phase_slider_raw", 0.0))
        except Exception:
            pass
        try:
            phase_last = int(rfid.fetch("phase_slider_last_frame", -1))
            if phase_last >= 0 and (me.time.frame - phase_last) < SLIDER_TIMEOUT_TICKS:
                phase_slider_alive = 1
        except Exception:
            pass

    # Per-method n_phases from methods_db Text DAT, cached by content-hash
    # (avoid re-parsing JSON every cook — methods_db rarely changes at runtime)
    global _methods_db_cache, _methods_db_text_hash
    n_phases = 5
    try:
        db_dat = op("methods_db")
        if db_dat is not None:
            cur_hash = hash(db_dat.text)
            if cur_hash != _methods_db_text_hash:
                _methods_db_cache = json.loads(db_dat.text)
                _methods_db_text_hash = cur_hash
            if _methods_db_cache is not None:
                for method in _methods_db_cache.get("methods", []):
                    if int(method.get("id", -1)) == method_id:
                        n_phases = max(1, int(method.get("n_phases", 5)))
                        break
    except Exception:
        pass

    # Movement detection → MANUAL_OVERRIDE wrapper_state for PHASE_OVERRIDE_FRAMES
    if _last_phase_slider_value < 0.0:
        _last_phase_slider_value = phase_slider_raw_val
        _last_phase_center = 0.0
        _last_phase_index = 1
    if abs(phase_slider_raw_val - _last_phase_slider_value) > PHASE_OVERRIDE_THRESHOLD:
        _manual_override_until_frame = me.time.frame + PHASE_OVERRIDE_FRAMES
        _last_phase_slider_value = phase_slider_raw_val

    wrapper_state_val = 1 if me.time.frame < _manual_override_until_frame else 0

    # Per-method phase_index quantization with TD-side hysteresis
    if n_phases <= 1:
        phase_index_val = 1
    else:
        half_step = 1.0 / (2.0 * (n_phases - 1))
        if abs(phase_slider_raw_val - _last_phase_center) > (half_step + PHASE_HYST_EPSILON):
            new_index = 1 + int(round(phase_slider_raw_val * (n_phases - 1)))
            if new_index < 1:
                new_index = 1
            if new_index > n_phases:
                new_index = n_phases
            _last_phase_index = new_index
            _last_phase_center = float(new_index - 1) / float(n_phases - 1)
        phase_index_val = _last_phase_index

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

    # --- Phase 02.1 Slider outputs ---
    scriptOp["floor"][0] = floor_val
    scriptOp["slider_raw"][0] = slider_raw_val
    scriptOp["slider_alive"][0] = slider_alive
    scriptOp["phase_slider_raw"][0] = phase_slider_raw_val
    scriptOp["phase_index"][0] = phase_index_val
    scriptOp["phase_slider_alive"][0] = phase_slider_alive
    scriptOp["wrapper_state"][0] = wrapper_state_val

    _sync_owner_state(scriptOp, method_id, hb_alive)


def _shoelace(points):
    total = 0.0
    for index, point in enumerate(points):
        next_point = points[(index + 1) % len(points)]
        total += point[0] * next_point[1] - next_point[0] * point[1]
    return abs(total) / 2.0


def _int_chan(op_node, channel, default=0):
    """Read int channel. Tolerates both 'name' and 'name:0' (single-arg vs multi-arg OSC)."""
    bare = channel.rsplit(':', 1)[0] if channel.endswith(':0') else channel
    for cand in (channel, bare):
        try:
            return int(op_node[cand][0])
        except Exception:
            pass
    return default


def _float_chan(op_node, channel, default=0.0):
    """Read float channel. Tolerates both 'name' and 'name:0'."""
    bare = channel.rsplit(':', 1)[0] if channel.endswith(':0') else channel
    for cand in (channel, bare):
        try:
            return float(op_node[cand][0])
        except Exception:
            pass
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
        for key, value in (
            ("floor_control_dirty", 0),
            ("phase_control_dirty", 0),
            ("building_part_interacted", 0),
        ):
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
