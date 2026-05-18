"""Background OSC server that receives packets from the vision pipeline.

Compatible with Elias's main.py — uses flat-1-indexed channel layout
discovered in this repo's vision pipeline:
- /vision/heartbeat <int>
- /puck/<id> <frame> <x> <y>     (per-puck data, variable ArUco IDs)
- /puck/detected <id1> <id2>...  (multi-arg list of currently detected)
- /puck/lost <id>
- /method/selected <int>         (overrides RFID — see note)
- /sketch/{points,walls,windows,extruded} <int>
- /gesture/{id,dwell,action} <val>
- /fsm/state <int>

Note on method_id priority: vision's /method/selected takes precedence over
RFID, matching Onur's vision2_state_chop.py behavior. Set HW3_RFID_PRIORITY=1
in the environment to invert (RFID wins) — useful when running RFID-only demos.
"""
from __future__ import annotations

import logging
import os
import threading
import time
from typing import Optional

try:
    from pythonosc import dispatcher as _disp
    from pythonosc import osc_server
except ImportError:
    _disp = None  # type: ignore
    osc_server = None  # type: ignore

from . import config
from .state import PuckObservation, StateManager

logger = logging.getLogger(__name__)


class VisionListener:
    def __init__(self, sm: StateManager,
                 host: str = config.VISION_OSC_HOST,
                 port: int = config.VISION_OSC_PORT):
        if _disp is None or osc_server is None:
            raise RuntimeError("python-osc is not installed — `pip install python-osc`")
        self.sm = sm
        self.host = host
        self.port = port
        self._server: Optional[osc_server.ThreadingOSCUDPServer] = None
        self._thread: Optional[threading.Thread] = None
        self._rfid_priority = os.environ.get("HW3_RFID_PRIORITY", "0") == "1"

    def start(self) -> None:
        if self._server is not None:
            return
        disp = _disp.Dispatcher()
        disp.map("/vision/heartbeat", self._on_heartbeat)
        disp.map("/puck/*", self._on_puck)
        disp.map("/method/selected", self._on_method_selected)
        disp.map("/sketch/*", self._on_sketch)
        disp.map("/gesture/*", self._on_gesture)
        disp.map("/fsm/state", self._on_fsm)
        disp.set_default_handler(self._on_unknown)

        self._server = osc_server.ThreadingOSCUDPServer((self.host, self.port), disp)
        self._thread = threading.Thread(
            target=self._server.serve_forever, name="VisionListener", daemon=True
        )
        self._thread.start()
        logger.info("VisionListener bound %s:%d", self.host, self.port)

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    # ----- OSC handlers -----

    def _on_heartbeat(self, addr: str, *args) -> None:
        if not args:
            return
        try:
            hb = int(args[0])
        except (TypeError, ValueError):
            return
        now = time.monotonic()
        def _w(s):
            s.last_hb_value = hb
            s.last_hb_t = now
        self.sm.write(_w)

    def _on_puck(self, addr: str, *args) -> None:
        # Addresses:
        #   /puck/<id>          with 3+ args -> per-puck frame/x/y
        #   /puck/detected      with N args -> list of detected IDs
        #   /puck/lost          with 1 arg  -> single lost ID
        tail = addr.rsplit("/", 1)[1]
        now = time.monotonic()

        if tail == "detected":
            # update which pucks are currently active; main loop derives puck_count
            detected_ids = []
            for a in args:
                try:
                    detected_ids.append(int(a))
                except (TypeError, ValueError):
                    pass
            def _w(s):
                # Remove pucks not in the detected list
                stale = [pid for pid in s.pucks if pid not in detected_ids]
                for pid in stale:
                    s.pucks.pop(pid, None)
            self.sm.write(_w)
            return

        if tail == "lost":
            if not args:
                return
            try:
                pid = int(args[0])
            except (TypeError, ValueError):
                return
            def _w(s):
                s.pucks.pop(pid, None)
            self.sm.write(_w)
            return

        # /puck/<id> with frame, x, y
        try:
            aruco_id = int(tail)
        except ValueError:
            return
        if len(args) < 3:
            return
        try:
            frame = int(args[0])
            x = float(args[1])
            y = float(args[2])
        except (TypeError, ValueError):
            return
        obs = PuckObservation(aruco_id=aruco_id, x=x, y=y, frame=frame, last_seen_t=now)
        def _w(s):
            s.pucks[aruco_id] = obs
        self.sm.write(_w)

    def _on_method_selected(self, addr: str, *args) -> None:
        if not args:
            return
        try:
            mid = int(args[0])
        except (TypeError, ValueError):
            return
        if self._rfid_priority:
            return  # RFID wins, ignore vision
        def _w(s):
            s.vision_method_id = mid
        self.sm.write(_w)

    def _on_sketch(self, addr: str, *args) -> None:
        if not args:
            return
        tail = addr.rsplit("/", 1)[1]
        try:
            val = int(args[0])
        except (TypeError, ValueError):
            return
        def _w(s):
            if tail == "points":
                s.sketch_points = val
            elif tail == "walls":
                s.sketch_walls = val
            elif tail == "windows":
                s.sketch_windows = val
            elif tail == "extruded":
                s.is_extruded = val
        self.sm.write(_w)

    def _on_gesture(self, addr: str, *args) -> None:
        if not args:
            return
        tail = addr.rsplit("/", 1)[1]
        try:
            num = float(args[0])
        except (TypeError, ValueError):
            return
        def _w(s):
            if tail == "id":
                s.gesture_id = int(num)
            elif tail == "dwell":
                s.gesture_dwell = float(num)
            elif tail == "action":
                s.gesture_action = int(num)
        self.sm.write(_w)

    def _on_fsm(self, addr: str, *args) -> None:
        if not args:
            return
        try:
            val = int(args[0])
        except (TypeError, ValueError):
            return
        def _w(s):
            s.fsm_state = val
        self.sm.write(_w)

    def _on_unknown(self, addr: str, *args) -> None:
        logger.debug("Unhandled OSC %s args=%s", addr, args)
