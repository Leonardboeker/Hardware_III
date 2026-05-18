"""Sends derived state to TouchDesigner via OSC.

TD listens on a separate port (default 7001) for state updates from this
orchestrator. Each payload key gets sent as a separate OSC message so TD
can bind text TOPs / channels directly to single addresses.

OSC addresses used:
    /state/<key>  with one argument

Plus a single combined heartbeat:
    /state/tick   <int>   (incremented every send)
"""
from __future__ import annotations

import logging
from typing import Any

try:
    from pythonosc import udp_client
except ImportError:
    udp_client = None  # type: ignore

from . import config

logger = logging.getLogger(__name__)


class TDSender:
    def __init__(self, host: str = config.TD_OSC_HOST, port: int = config.TD_OSC_PORT):
        if udp_client is None:
            raise RuntimeError("python-osc is not installed — `pip install python-osc`")
        self.host = host
        self.port = port
        self._client = udp_client.SimpleUDPClient(host, port)
        self._tick = 0
        self._last_payload: dict[str, Any] = {}
        logger.info("TDSender ready -> %s:%d", host, port)

    def send(self, payload: dict[str, Any]) -> None:
        """Send each key as its own OSC message at /state/<key>.

        Optimisation: only send a key if its value changed since the last
        send. Keeps the OSC pipe quiet and TD-side cooks cheaper.
        """
        for key, value in payload.items():
            if self._last_payload.get(key) == value:
                continue
            self._client.send_message(f"/state/{key}", value)
        self._last_payload = dict(payload)

        self._tick += 1
        self._client.send_message("/state/tick", self._tick)

    def send_full(self, payload: dict[str, Any]) -> None:
        """Send ALL keys regardless of change (use on startup or after a TD reload)."""
        for key, value in payload.items():
            self._client.send_message(f"/state/{key}", value)
        self._last_payload = dict(payload)
        self._tick += 1
        self._client.send_message("/state/tick", self._tick)
