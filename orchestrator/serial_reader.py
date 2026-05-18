"""Background thread that reads from the ESP32 USB Serial port and updates State.

Expected firmware (firmware/esp32-rfid/esp32_rfid/esp32_rfid.ino @115200 baud):
- BOOT:rfid_reader_ready
- HB:<sec>
- RFID:<HEX>
- FLOOR:<int>
- SLIDER:<0.xxx>
- PSLIDER:<0.xxx>

Resilient: reconnects automatically if the port disappears (ESP32 unplug, reset).
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Optional

try:
    import serial  # pyserial
    from serial import SerialException
except ImportError:
    serial = None  # type: ignore
    SerialException = Exception  # type: ignore

from . import config
from .methods import MethodDB
from .state import StateManager

logger = logging.getLogger(__name__)

_HEX = set("0123456789ABCDEF")


class SerialReader:
    def __init__(self, sm: StateManager, db: MethodDB,
                 port: str = config.SERIAL_PORT,
                 baud: int = config.SERIAL_BAUD,
                 reconnect_s: float = config.SERIAL_RECONNECT_S):
        if serial is None:
            raise RuntimeError("pyserial is not installed — `pip install pyserial`")
        self.sm = sm
        self.db = db
        self.port = port
        self.baud = baud
        self.reconnect_s = reconnect_s
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="SerialReader", daemon=True)
        self._thread.start()
        logger.info("SerialReader started on %s @ %d baud", self.port, self.baud)

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self._thread = None

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                with serial.Serial(self.port, self.baud, timeout=0.5) as ser:
                    logger.info("Serial connected: %s", self.port)
                    self.sm.write(lambda s: setattr(s, "serial_alive", True))
                    while not self._stop.is_set():
                        line = ser.readline()
                        if not line:
                            continue
                        try:
                            text = line.decode("utf-8", errors="replace").strip()
                        except Exception:
                            continue
                        if text:
                            self._parse_line(text)
            except SerialException as e:
                logger.warning("Serial error (%s) — reconnecting in %.1fs", e, self.reconnect_s)
            except Exception as e:
                logger.exception("Serial unexpected error: %s", e)
            self.sm.write(lambda s: setattr(s, "serial_alive", False))
            if self._stop.wait(self.reconnect_s):
                return

    def _parse_line(self, line: str) -> None:
        # Tolerant — handle leading noise like "!RFID:..."
        now = time.monotonic()

        if "BOOT:" in line:
            self.sm.write(lambda s: setattr(s, "last_boot_msg", line))
            logger.info("ESP32 boot: %s", line)
            return

        if "HB:" in line:
            # Heartbeat from ESP32 — currently informational only
            return

        if "PSLIDER:" in line:
            # PSLIDER must come before SLIDER (substring match)
            try:
                value = float(line[line.index("PSLIDER:") + 8:].strip())
            except ValueError:
                logger.debug("Malformed PSLIDER line: %r", line)
                return
            def _w(s):
                s.phase_slider_raw = value
                s.phase_slider_last_t = now
            self.sm.write(_w)
            return

        if "SLIDER:" in line:
            try:
                value = float(line[line.index("SLIDER:") + 7:].strip())
            except ValueError:
                logger.debug("Malformed SLIDER line: %r", line)
                return
            def _w(s):
                s.slider_raw = value
                s.slider_last_t = now
            self.sm.write(_w)
            return

        if "FLOOR:" in line:
            try:
                value = int(line[line.index("FLOOR:") + 6:].strip())
            except ValueError:
                logger.debug("Malformed FLOOR line: %r", line)
                return
            def _w(s):
                s.floor = value
            self.sm.write(_w)
            logger.info("FLOOR -> %d", value)
            return

        if "RFID:" in line:
            raw = line[line.index("RFID:") + 5:].strip().upper()
            tag = "".join(c for c in raw if c in _HEX)
            if not tag:
                logger.warning("Malformed RFID line: %r", line)
                return
            method = self.db.by_tag(tag)
            if method is None:
                logger.warning("UNKNOWN RFID tag %s — add to data/methods_db.json", tag)
                def _w(s):
                    s.last_rfid_tag = tag
                    s.last_rfid_t = now
                self.sm.write(_w)
                return
            def _w(s):
                s.last_rfid_tag = tag
                s.last_rfid_t = now
                if s.method_id != method.id:
                    s.method_id = method.id
                    s.method_name = method.name
            self.sm.write(_w)
            logger.info("RFID %s -> method_id=%d (%s)", tag, method.id, method.name)
            return

        # Unknown line — quiet by default
        logger.debug("Unparsed serial line: %r", line)
