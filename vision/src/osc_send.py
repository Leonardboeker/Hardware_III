"""OSC sender: streams puck detections from vision pipeline to TouchDesigner.

Protocol (all to TD host:port, default localhost:7000):
  /puck/N   i f f
      args: frame_number, projector_x, projector_y
      (sent each frame the puck is visible; N = ArUco marker ID)
  /puck/lost  i
      args: id  (sent once when a puck disappears)
  /vision/heartbeat  i
      args: frame_number  (sent every frame so TD knows the pipeline is alive)

TD OSC In CHOP listens on port 7000 by default.
"""
from __future__ import annotations

from pythonosc import udp_client

DEFAULT_TD_HOST = "127.0.0.1"
DEFAULT_TD_PORT = 7000


class PuckOSCSender:
    def __init__(self, host: str = DEFAULT_TD_HOST, port: int = DEFAULT_TD_PORT):
        self._client = udp_client.SimpleUDPClient(host, port)
        self._prev_ids: set[int] = set()
        self._frame = 0

    def send_frame(self, detections: list[dict]) -> None:
        """Send one frame of detections.

        Each detected puck gets its own OSC address /puck/ID with
        (frame, proj_x, proj_y) so TD can track liveness per-puck.
        """
        current_ids: set[int] = set()

        for d in detections:
            pid = d["id"]
            px, py = d["projector_xy"]
            current_ids.add(pid)
            self._client.send_message(
                f"/puck/{pid}",
                [self._frame, float(px), float(py)],
            )

        for lost_id in self._prev_ids - current_ids:
            self._client.send_message("/puck/lost", [lost_id])

        self._client.send_message("/vision/heartbeat", [self._frame])

        self._prev_ids = current_ids
        self._frame += 1


def make_sender(host: str = DEFAULT_TD_HOST, port: int = DEFAULT_TD_PORT) -> PuckOSCSender:
    return PuckOSCSender(host, port)
