"""OSC sender: streams puck detections from vision pipeline to TouchDesigner.

Protocol (all to TD host:port, default localhost:7000):
  /puck/detected   i i f f i
      args: id, frame_number, projector_x, projector_y, in_target (0|1)
  /puck/lost       i
      args: id  (sent once when a previously-seen puck disappears for >= LOST_FRAMES)
  /vision/heartbeat  i
      args: frame_number  (sent every frame so TD knows the pipeline is alive)

TD OSC In CHOP listens on port 7000 by default.
"""
from __future__ import annotations

from pythonosc import udp_client


DEFAULT_TD_HOST = "127.0.0.1"
DEFAULT_TD_PORT = 7000

# Frames a puck must be absent before /puck/lost fires
LOST_FRAMES = 10


class PuckOSCSender:
    def __init__(self, host: str = DEFAULT_TD_HOST, port: int = DEFAULT_TD_PORT):
        self._client = udp_client.SimpleUDPClient(host, port)
        self._prev_ids: set[int] = set()
        self._frame = 0

    def send_frame(self, detections: list[dict], target_zones: dict[int, tuple]) -> None:
        """Send one frame of detections.

        target_zones: {puck_id: (target_px, target_py)} — comes from FSM state.
        in_target is 1 if puck centroid is within the current tolerance.
        """
        from vision.src.aruco_detect import ARUCO_DICT_NAME  # noqa: F401 (import guard)
        import importlib
        tol_mod = importlib.import_module("vision.calibration.tolerance_loader")
        tolerance = tol_mod.get_tolerance()

        current_ids: set[int] = set()

        for d in detections:
            pid = d["id"]
            px, py = d["projector_xy"]
            current_ids.add(pid)

            in_target = 0
            if pid in target_zones:
                tx, ty = target_zones[pid]
                dist = ((px - tx) ** 2 + (py - ty) ** 2) ** 0.5
                in_target = 1 if dist <= tolerance else 0

            self._client.send_message(
                "/puck/detected",
                [pid, self._frame, px, py, in_target],
            )

        # Fire /puck/lost for each id that vanished this frame
        for lost_id in self._prev_ids - current_ids:
            self._client.send_message("/puck/lost", [lost_id])

        self._client.send_message("/vision/heartbeat", [self._frame])

        self._prev_ids = current_ids
        self._frame += 1


def make_sender(host: str = DEFAULT_TD_HOST, port: int = DEFAULT_TD_PORT) -> PuckOSCSender:
    return PuckOSCSender(host, port)
