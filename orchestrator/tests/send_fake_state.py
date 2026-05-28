"""Manual smoke test — send a few /state/* OSC packets to TD on UDP 7001.

Used to verify the state_in OSC In CHOP + state_to_storage Execute DAT
bridge writes to owner.fetch('ui_state', {}) before running the full
orchestrator.

Run:  python orchestrator/tests/send_fake_state.py
"""
from __future__ import annotations

import time

from pythonosc.udp_client import SimpleUDPClient


def main() -> None:
    client = SimpleUDPClient("127.0.0.1", 7001)
    payload = [
        ("method_id", 1),
        ("floor", 3),
        ("phase_index", 2),
        ("puck_count", 4),
        ("hb_alive", 1),
        ("wrapper_state", 0),
        ("slider_raw", 0.42),
        ("phase_slider_raw", 0.55),
        ("area_m2", 12.5),
        ("n_phases", 5),
    ]
    for key, val in payload:
        client.send_message(f"/state/{key}", val)
        time.sleep(0.01)
    print(f"sent {len(payload)} /state/* messages to 127.0.0.1:7001")


if __name__ == "__main__":
    main()
