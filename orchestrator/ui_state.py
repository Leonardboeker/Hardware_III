"""Builds the UI-state payload that TouchDesigner's panel_text.py expects.

This replaces Onur's `metrics_engine.compute_and_store_touchdesigner()` +
`ui_state.compute_and_store_touchdesigner_ui()` chain — which was failing on
the CSV schema mismatch (`KeyError: 'method'`).

Output is a dict with keys panel_text.py reads via `_state(key, default)`.
The dict is shipped to TD as individual OSC messages from td_sender.
"""
from __future__ import annotations

from typing import Any

from .methods import Method
from .state import State


def build_payload(state: State, active_method: Method) -> dict[str, Any]:
    """Convert the current State + active Method into a flat dict that TD
    can stash into its compute_state CHOP channels via OSC.

    Keys here mirror what panel_text.py reads in the current TD setup
    PLUS the Slider B additions (floor, phase_index, etc.).
    """
    n_phases = active_method.n_phases
    phase_idx = max(1, min(state.phase_index, n_phases))
    phase_name = (
        active_method.phase_names[phase_idx - 1]
        if 0 < phase_idx <= len(active_method.phase_names)
        else f"Phase {phase_idx}"
    )

    # Re-quantize floor from slider_raw against this method's max_floors.
    # The firmware always emits FLOOR:1..5 but methods can allow up to 8
    # (e.g. PREFAB) or as few as 2 (e.g. 3D PRINTED). We override.
    floor = _quantize_floor(state.slider_raw, active_method.max_floors)

    return {
        # ----- Identity -----
        "method_id":         int(state.method_id),
        "method_name":       active_method.name,

        # ----- Slider A -----
        "floor":             floor,
        "max_floors":        int(active_method.max_floors),
        "slider_raw":        round(float(state.slider_raw), 4),
        "slider_alive":      int(_is_fresh(state.slider_last_t)),

        # ----- Slider B -----
        "phase_slider_raw":  round(float(state.phase_slider_raw), 4),
        "phase_index":       int(phase_idx),
        "n_phases":          int(n_phases),
        "phase_name":        phase_name,
        "phase_slider_alive":int(_is_fresh(state.phase_slider_last_t)),
        "wrapper_state":     int(state.wrapper_state),

        # ----- Vision -----
        "puck_count":        int(state.puck_count),
        "area_m2":           round(float(state.area_m2), 2),
        "hb_alive":          int(state.hb_alive),

        # ----- Vision passthroughs -----
        "sketch_points":     int(state.sketch_points),
        "sketch_walls":      int(state.sketch_walls),
        "sketch_windows":    int(state.sketch_windows),
        "sketch_perim_m":    round(float(state.sketch_perim_m), 2),
        "is_extruded":       int(state.is_extruded),
        "gesture_id":        int(state.gesture_id),
        "gesture_dwell":     round(float(state.gesture_dwell), 3),
        "gesture_action":    int(state.gesture_action),
        "fsm_state":         int(state.fsm_state),
        "fsm_state_name":    state.fsm_state_name,

        # ----- Convenience pre-formatted strings (so TD doesn't have to compute them) -----
        "status_label":      "VISION LIVE" if state.hb_alive else "VISION OFFLINE",
        "bar_bottom_text":   _bar_bottom_text(state, active_method, phase_idx, phase_name),
    }


def _quantize_floor(raw: float, max_floors: int) -> int:
    """Map slider_raw [0..1] into floor [1..max_floors] using same scheme
    as PhaseQuantizer. Pure function, no hysteresis (slider noise is
    smoothed in firmware via median+EMA already)."""
    n = max(1, int(max_floors))
    if n <= 1:
        return 1
    r = max(0.0, min(1.0, float(raw)))
    idx = 1 + int(round(r * (n - 1)))
    return max(1, min(n, idx))


def _bar_bottom_text(state: State, method: Method, phase_idx: int, phase_name: str) -> str:
    """Pre-baked status bar string ready to drop into a TD Text TOP."""
    status = "VISION LIVE" if state.hb_alive else "VISION OFFLINE"
    floor = _quantize_floor(state.slider_raw, method.max_floors)
    return (
        f"{status}   ·   "
        f"METHOD {method.name}   ·   "
        f"PUCKS {state.puck_count}   ·   "
        f"AREA {state.area_m2:.1f} m²   ·   "
        f"FLOOR {floor}/{method.max_floors}   ·   "
        f"PHASE {phase_idx}/{method.n_phases} ({phase_name})"
    )


def _is_fresh(last_t: float, max_age_s: float = 2.0) -> bool:
    """True if a timestamp is recent enough to be considered live."""
    if last_t <= 0.0:
        return False
    import time as _time
    return (_time.monotonic() - last_t) < max_age_s
