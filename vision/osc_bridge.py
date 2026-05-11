"""osc_bridge.py — Links vision2 pipeline to TouchDesigner via OSC.

Drop-in companion to main.py. Import VisionBridge and call send_frame()
once per loop iteration (see integration snippet at the bottom of this file).

OSC target: localhost:7000 — the same port TouchDesigner's `vision_in`
OSC In CHOP already listens on.  No changes needed inside TouchDesigner for
the existing nodes; new channels appear automatically once data arrives.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROTOCOL — all messages sent to TD host:port (default 127.0.0.1:7000)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backward-compatible (existing osc_send.py / state_chop_v1.py protocol):
  /vision/heartbeat        i         frame counter — pipeline liveness
  /puck/{0-9}              i f f     frame, proj_x, proj_y
                                     Sketch footprint points mapped into
                                     projector space (0..1280, 0..720).
                                     Puck ID = sketch point index.
  /puck/lost               i         puck id removed from sketch this frame

Method selection  (ArUco IDs 20-22 on the table → construction method):
  /method/selected         i         0=NONE  1=MASONRY  2=3D_PRINT  3=PREFAB
                                     Latches on last visible token.
  /method/detected         i i f f   method_id, marker_id, cam_x_norm, cam_y_norm
                                     Sent each frame the token is in view.

Gesture layer:
  /gesture/id              i         0=none  1=index_only  2=peace
                                     3=three_fingers  4=fist
  /gesture/dwell           f         seconds the current gesture has been held
  /gesture/action          i         Fires for ONE frame when an action triggers:
                                     0=none  1=place_point  2=add_window
                                     3=extrude  4=undo  5=reset
                                     Resets to 0 the following frame.

Sketch state  (updated every frame):
  /sketch/points           i         footprint point count
  /sketch/walls            i         wall segment count (includes closing wall)
  /sketch/windows          i         window count
  /sketch/extruded         i         1 when 3-D extrusion is active, else 0

FSM content state  (inferred from sketch + method + calibration):
  /fsm/state               i         0=IDLE  1=METHOD  2=FOOTPRINT  3=HEIGHT
                                     4=VALIDATED  5=PHASE_N
  /fsm/state_name          s         same value as a human-readable string

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FSM INFERENCE LOGIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  H is None (table corners not all visible)  →  IDLE
  H visible, no method token, no points      →  IDLE
  method token (ID 20/21/22) visible         →  METHOD
  1-2 sketch points placed                   →  FOOTPRINT
  3+ sketch points (closed polygon)          →  HEIGHT
  extrusion gesture fired (is_extruded=True) →  VALIDATED
  extruded AND at least one window added     →  PHASE_N

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOUCHDESIGNER INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • vision_in (OSC In CHOP, port 7000) — no change required.
  • Replace state_chop_v1.py with vision2_state_chop.py to expose all
    new channels in compute_state.
  • The /fsm/state_name string channel lands in vision_in as a string
    channel; read it with a DAT String CHOP if needed for text overlays.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTEGRATION SNIPPET FOR main.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  from osc_bridge import VisionBridge
  bridge = VisionBridge()                 # before the loop

  # inside the while-True loop, after gesture detection:
  bridge.send_frame(
      build_markers=build_markers,
      gesture_result=g,
      sketch=sketch,
      is_extruded=is_extruded,
      H=H,
  )
"""

from __future__ import annotations

from pythonosc import udp_client

from working_plane import PLANE_W, PLANE_H

# ── Configuration ──────────────────────────────────────────────────────────────

TD_HOST = "127.0.0.1"
TD_PORT = 7000

PROJ_W = 1280   # projector canvas width  (must match footprint_viz_v5.py)
PROJ_H = 720    # projector canvas height

# ArUco IDs printed on the method-token cards (working_plane.py BUILD_IDS)
# mapped to methods_db.json method IDs
_MARKER_TO_METHOD: dict[int, int] = {20: 1, 21: 2, 22: 3}

_GESTURE_ID: dict[str, int] = {
    "none":          0,
    "index_only":    1,
    "peace":         2,
    "three_fingers": 3,
    "fist":          4,
    "puck":          1,   # RedPuckDetector — maps to same slot as index_only
}

_ACTION_ID: dict[str, int] = {
    "place_point": 1,
    "add_window":  2,
    "extrude":     3,
    "undo":        4,
    "reset":       5,
}

_FSM_ID: dict[str, int] = {
    "IDLE":      0,
    "METHOD":    1,
    "FOOTPRINT": 2,
    "HEIGHT":    3,
    "VALIDATED": 4,
    "PHASE_N":   5,
}


# ── Bridge class ───────────────────────────────────────────────────────────────

class VisionBridge:
    """Send the full vision2 pipeline state to TouchDesigner each frame.

    Backward-compatible with the /puck/ and /vision/heartbeat protocol
    consumed by state_chop_v1.py and footprint_viz_v5.py.
    """

    def __init__(self, host: str = TD_HOST, port: int = TD_PORT) -> None:
        self._client = udp_client.SimpleUDPClient(host, port)
        self._frame: int = 0
        self._prev_puck_ids: set[int] = set()
        self._current_method: int = 0
        print(f"[OSC] VisionBridge → {host}:{port}")

    # ── Public API ─────────────────────────────────────────────────────────────

    def send_frame(
        self,
        *,
        build_markers: dict,
        gesture_result: dict,
        sketch,
        is_extruded: bool,
        H,
    ) -> None:
        """Encode and transmit one frame of vision pipeline state.

        Parameters
        ----------
        build_markers   {marker_id: (cam_x, cam_y)} from detect_working_plane()
        gesture_result  dict from GestureDetector.process()
        sketch          BuildingSketch instance
        is_extruded     bool — 3-D extrusion currently active
        H               homography matrix or None (None = table not calibrated)
        """
        f = self._frame

        self._send_heartbeat(f)
        self._send_method_tokens(build_markers)
        self._send_sketch_pucks(sketch, f)
        self._send_sketch_state(sketch, is_extruded)
        self._send_gesture(gesture_result)
        self._send_fsm_state(sketch, is_extruded, H)

        self._frame += 1

    @property
    def current_method(self) -> int:
        """Currently selected construction method ID (0 = none)."""
        return self._current_method

    # ── Private senders ────────────────────────────────────────────────────────

    def _send_heartbeat(self, frame: int) -> None:
        self._client.send_message("/vision/heartbeat", [frame])

    def _send_method_tokens(self, build_markers: dict) -> None:
        detected = 0
        for marker_id, center in build_markers.items():
            method_id = _MARKER_TO_METHOD.get(marker_id, 0)
            if not method_id:
                continue
            # Normalize from camera pixel space to 0..1
            nx = float(center[0]) / PROJ_W
            ny = float(center[1]) / PROJ_H
            self._client.send_message(
                "/method/detected",
                [method_id, marker_id, nx, ny],
            )
            detected = method_id

        if detected != self._current_method:
            self._current_method = detected

        self._client.send_message("/method/selected", [self._current_method])

    def _send_sketch_pucks(self, sketch, frame: int) -> None:
        """Map sketch footprint points to puck IDs 0-9 in projector space.

        Puck ID = sketch point index.  Points beyond index 9 are silently
        dropped (TD uses FOOTPRINT_IDS = range(10)).
        """
        current_ids: set[int] = set()

        for idx, pt in enumerate(sketch.points[:10]):
            proj_x = pt[0] / PLANE_W * PROJ_W
            proj_y = pt[1] / PLANE_H * PROJ_H
            self._client.send_message(
                f"/puck/{idx}",
                [frame, float(proj_x), float(proj_y)],
            )
            current_ids.add(idx)

        for lost_id in self._prev_puck_ids - current_ids:
            self._client.send_message("/puck/lost", [lost_id])

        self._prev_puck_ids = current_ids

    def _send_sketch_state(self, sketch, is_extruded: bool) -> None:
        walls = sketch.get_wall_segments()
        self._client.send_message("/sketch/points",   [len(sketch.points)])
        self._client.send_message("/sketch/walls",    [len(walls)])
        self._client.send_message("/sketch/windows",  [len(sketch.windows)])
        self._client.send_message("/sketch/extruded", [int(is_extruded)])

    def _send_gesture(self, result: dict) -> None:
        gesture = result.get("gesture", "none")
        dwell   = float(result.get("dwell", 0.0))
        actions = result.get("actions", [])

        self._client.send_message("/gesture/id",    [_GESTURE_ID.get(gesture, 0)])
        self._client.send_message("/gesture/dwell", [dwell])

        # Only the first action per frame is forwarded; resets to 0 next frame
        action_id = _ACTION_ID.get(actions[0], 0) if actions else 0
        self._client.send_message("/gesture/action", [action_id])

    def _send_fsm_state(self, sketch, is_extruded: bool, H) -> None:
        name = _infer_fsm_state(sketch, is_extruded, H, self._current_method)
        self._client.send_message("/fsm/state",      [_FSM_ID[name]])
        self._client.send_message("/fsm/state_name", [name])


# ── FSM inference ──────────────────────────────────────────────────────────────

def _infer_fsm_state(sketch, is_extruded: bool, H, method: int) -> str:
    if H is None:
        return "IDLE"
    if is_extruded:
        return "PHASE_N" if sketch.windows else "VALIDATED"
    n = len(sketch.points)
    if n >= 3:
        return "HEIGHT"
    if n >= 1:
        return "FOOTPRINT"
    if method > 0:
        return "METHOD"
    return "IDLE"
