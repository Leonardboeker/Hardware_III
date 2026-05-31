"""ui_state.build_payload unit tests."""
from __future__ import annotations

import time

from orchestrator.methods import Method
from orchestrator.state import State
from orchestrator.ui_state import build_payload


def _masonry() -> Method:
    return Method(
        id=1, name="MASONRY", color_rgb=(0.6, 0.3, 0.2),
        rfid_tag="ABCD1234", min_pucks=3, max_pucks=10,
        max_floors=5, n_phases=5,
        phase_names=["Foundation", "Structure", "Roof", "Openings", "Finishing"],
    )


def _3dp() -> Method:
    return Method(
        id=2, name="3D PRINTED", color_rgb=(0.2, 0.6, 0.8),
        rfid_tag="EEEE1111", min_pucks=3, max_pucks=10,
        max_floors=1, n_phases=3,
        phase_names=["Foundation", "Print", "Finishing"],
    )


def test_payload_has_all_required_keys():
    state = State(method_id=1, method_name="MASONRY",
                  floor=3, slider_raw=0.5, phase_index=3,
                  phase_slider_raw=0.5, wrapper_state=0,
                  puck_count=4, hb_alive=1)
    payload = build_payload(state, _masonry())
    required = {
        "method_id", "method_name", "floor", "max_floors",
        "slider_raw", "slider_alive",
        "phase_slider_raw", "phase_index", "n_phases", "phase_name",
        "phase_slider_alive", "wrapper_state",
        "puck_count", "area_m2", "hb_alive",
        "status_label", "bar_bottom_text",
    }
    assert required.issubset(set(payload.keys()))


def test_phase_name_matches_method_config():
    state = State(method_id=2, method_name="3D PRINTED", phase_index=2)
    payload = build_payload(state, _3dp())
    assert payload["phase_name"] == "Print"
    assert payload["n_phases"] == 3


def test_phase_index_clamped_to_n_phases():
    """If state has phase_index > n_phases (stale after method change),
    clamp to within range."""
    state = State(method_id=2, method_name="3D PRINTED", phase_index=5)
    payload = build_payload(state, _3dp())
    assert payload["phase_index"] == 3


def test_bar_bottom_text_contains_key_info():
    # floor is derived from slider_raw + active_method.max_floors
    # MASONRY max_floors=5: raw=0.5 -> floor 3
    state = State(method_id=1, method_name="MASONRY",
                  slider_raw=0.5, phase_index=2,
                  puck_count=4, hb_alive=1)
    payload = build_payload(state, _masonry())
    text = payload["bar_bottom_text"]
    assert "MASONRY" in text
    assert "FLOOR 3" in text
    assert "PHASE 2" in text
    assert "VISION LIVE" in text


def test_status_label_changes_with_hb():
    method = _masonry()
    live = build_payload(State(hb_alive=1), method)
    offline = build_payload(State(hb_alive=0), method)
    assert live["status_label"] == "VISION LIVE"
    assert offline["status_label"] == "VISION OFFLINE"


def test_slider_alive_zero_when_no_data():
    state = State()  # all defaults, no slider activity ever
    payload = build_payload(state, _masonry())
    assert payload["slider_alive"] == 0
    assert payload["phase_slider_alive"] == 0


def test_slider_alive_one_when_fresh():
    state = State()
    state.slider_last_t = time.monotonic()
    state.phase_slider_last_t = time.monotonic()
    payload = build_payload(state, _masonry())
    assert payload["slider_alive"] == 1
    assert payload["phase_slider_alive"] == 1
