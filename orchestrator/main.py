"""Entry point. Wires every component together and runs the orchestration loop.

Architecture:
    Serial (ESP32)  ─┐
                     ├─→  StateManager  ─→  ui_state.build_payload  ─→  TDSender  ─→  TouchDesigner
    Vision OSC ──────┘            ↑
                                  Main loop derives:
                                    - phase_index (from PhaseQuantizer)
                                    - wrapper_state (from PhaseQuantizer)
                                    - hb_alive (timeout check)
                                    - method_id (RFID + vision priority resolution)
                                    - puck_count (from pucks dict)
                                    - area_m2 (from puck polygon shoelace)

Run from repo root:
    python -m orchestrator.main
"""
from __future__ import annotations

import logging
import math
import signal
import sys
import time

from . import config
from .methods import MethodDB
from .serial_reader import SerialReader
from .state import StateManager
from .td_sender import TDSender
from .ui_state import build_payload
from .vision_listener import VisionListener

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s.%(msecs)03d  %(levelname)-5s  %(name)-22s  %(message)s",
        datefmt="%H:%M:%S",
    )


def _shoelace_area(points: list[tuple[float, float]]) -> float:
    """Polygon area for a list of (x,y) pixel/normalised coordinates.
    Sort by polar angle around centroid before applying the shoelace formula
    so non-convex orderings still work."""
    if len(points) < 3:
        return 0.0
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    pts = sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    total = 0.0
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        total += p[0] * q[1] - q[0] * p[1]
    return abs(total) / 2.0


def main() -> int:
    setup_logging()
    logger.info("Hardware III orchestrator starting up")

    db = MethodDB()
    sm = StateManager()
    td = TDSender()

    serial_reader = SerialReader(sm, db)
    serial_reader.start()

    vision = VisionListener(sm)
    vision.start()

    stop_flag = {"now": False}

    def _shutdown(*_):
        stop_flag["now"] = True

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    # Send a full state snapshot on first tick so TD lights up immediately
    first_tick = True
    last_n_phases = -1

    try:
        next_t = time.monotonic()
        while not stop_flag["now"]:
            now_t = time.monotonic()
            snap = sm.snapshot()

            # ----- Resolve method (vision /method/selected overrides RFID unless flipped) -----
            method_id = snap.method_id
            if snap.vision_method_id >= 0:
                method_id = snap.vision_method_id
            active_method = db.by_id(method_id)

            # If method changed (= phase count may differ), reset the quantizer
            if active_method.n_phases != last_n_phases:
                sm.phase_quantizer.reset_for_method(active_method.n_phases)
                last_n_phases = active_method.n_phases
                logger.info("Phase quantizer reset for %s (n_phases=%d)",
                            active_method.name, active_method.n_phases)

            # ----- Slider B -> phase_index, wrapper_state -----
            phase_idx, wrapper = sm.phase_quantizer.update(snap.phase_slider_raw, now_t)

            # ----- Heartbeat liveness -----
            hb_alive = 1 if (now_t - snap.last_hb_t) < config.HB_TIMEOUT_S and snap.last_hb_t > 0 else 0

            # ----- Puck count + area -----
            # Drop stale pucks (>2s without an OSC update)
            alive_pucks = {
                pid: obs for pid, obs in snap.pucks.items()
                if (now_t - obs.last_seen_t) < config.SLIDER_TIMEOUT_S
            }
            puck_count = len(alive_pucks)
            area_m2 = _shoelace_area([(p.x, p.y) for p in alive_pucks.values()])

            # ----- Write derived back into state -----
            def _derive(s):
                s.method_id = active_method.id
                s.method_name = active_method.name
                s.phase_index = phase_idx
                s.wrapper_state = wrapper
                s.hb_alive = hb_alive
                s.puck_count = puck_count
                s.area_m2 = area_m2
                # phase_name update
                if 0 < phase_idx <= len(active_method.phase_names):
                    s.phase_name = active_method.phase_names[phase_idx - 1]
                # prune stale pucks too
                s.pucks = alive_pucks
            sm.write(_derive)

            # ----- Build UI payload + send to TD -----
            payload = build_payload(sm.snapshot(), active_method)
            if first_tick:
                td.send_full(payload)
                first_tick = False
            else:
                td.send(payload)

            # ----- Sleep until next tick -----
            next_t += config.TICK_DT
            sleep_for = next_t - time.monotonic()
            if sleep_for > 0:
                time.sleep(sleep_for)
            else:
                # We're behind schedule. Resync to avoid spiral of death.
                next_t = time.monotonic()
    finally:
        serial_reader.stop()
        vision.stop()
        logger.info("Hardware III orchestrator stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())
