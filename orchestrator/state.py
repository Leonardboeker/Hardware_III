"""Central application state. Thread-safe via a single lock."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PuckObservation:
    """One puck visible to the camera. Position in normalised projector space."""
    aruco_id: int
    x: float
    y: float
    frame: int
    last_seen_t: float


@dataclass
class State:
    """Mutable snapshot of everything the system knows right now.

    Updated from:
      - Serial reader thread (RFID, slider A/B values)
      - Vision OSC listener thread (pucks, heartbeat, sketch/gesture/fsm)
      - Main loop (derived fields: floor, phase_index, wrapper_state, hb_alive)
    """
    # ----- Method (RFID-driven, vision can override) -----
    method_id: int = 0
    method_name: str = "NONE"
    last_rfid_tag: Optional[str] = None
    last_rfid_t: float = 0.0

    # ----- Slider A (HEIGHT) -----
    floor: int = 1                     # firmware-quantized
    slider_raw: float = 0.0            # smoothed [0..1]
    slider_last_t: float = 0.0

    # ----- Slider B (BUILDING_PHASE) -----
    phase_slider_raw: float = 0.0
    phase_slider_last_t: float = 0.0
    phase_index: int = 1               # TD-side / orchestrator-quantized, 1..n_phases
    phase_name: str = "Foundation"
    wrapper_state: int = 0             # 1 = MANUAL_OVERRIDE active

    # ----- Vision -----
    pucks: dict[int, PuckObservation] = field(default_factory=dict)
    puck_count: int = 0
    area_m2: float = 0.0
    hb_alive: int = 0
    last_hb_value: int = -1
    last_hb_t: float = 0.0

    # ----- Optional vision passthroughs -----
    sketch_points: int = 0
    sketch_walls: int = 0
    sketch_windows: int = 0
    sketch_perim_m: float = 0.0
    is_extruded: int = 0
    gesture_id: int = 0
    gesture_dwell: float = 0.0
    gesture_action: int = 0
    fsm_state: int = 0
    fsm_state_name: str = ""
    vision_method_id: int = -1         # if vision sends /method/selected; -1 = unused

    # ----- Bookkeeping -----
    last_boot_msg: str = ""
    serial_alive: bool = False


class StateManager:
    """Owns the State + a lock. All reads/writes go through `with sm.snapshot()`."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state = State()
        # Phase quantizer kept here so it persists across cooks even when methods change
        # (it's reset on method change from the main loop, not from the threads)
        from .phase_quantizer import PhaseQuantizer
        self.phase_quantizer = PhaseQuantizer()

    def write(self, fn) -> None:
        """Apply `fn(state)` under the lock. fn may mutate state in place."""
        with self._lock:
            fn(self._state)

    def snapshot(self) -> State:
        """Return a shallow copy of the State for read-only use outside the lock."""
        with self._lock:
            return State(
                method_id=self._state.method_id,
                method_name=self._state.method_name,
                last_rfid_tag=self._state.last_rfid_tag,
                last_rfid_t=self._state.last_rfid_t,
                floor=self._state.floor,
                slider_raw=self._state.slider_raw,
                slider_last_t=self._state.slider_last_t,
                phase_slider_raw=self._state.phase_slider_raw,
                phase_slider_last_t=self._state.phase_slider_last_t,
                phase_index=self._state.phase_index,
                phase_name=self._state.phase_name,
                wrapper_state=self._state.wrapper_state,
                pucks=dict(self._state.pucks),
                puck_count=self._state.puck_count,
                area_m2=self._state.area_m2,
                hb_alive=self._state.hb_alive,
                last_hb_value=self._state.last_hb_value,
                last_hb_t=self._state.last_hb_t,
                sketch_points=self._state.sketch_points,
                sketch_walls=self._state.sketch_walls,
                sketch_windows=self._state.sketch_windows,
                sketch_perim_m=self._state.sketch_perim_m,
                is_extruded=self._state.is_extruded,
                gesture_id=self._state.gesture_id,
                gesture_dwell=self._state.gesture_dwell,
                gesture_action=self._state.gesture_action,
                fsm_state=self._state.fsm_state,
                fsm_state_name=self._state.fsm_state_name,
                vision_method_id=self._state.vision_method_id,
                last_boot_msg=self._state.last_boot_msg,
                serial_alive=self._state.serial_alive,
            )
