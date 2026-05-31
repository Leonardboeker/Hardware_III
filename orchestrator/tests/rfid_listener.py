"""Standalone RFID listener — opens COM4, appends every RFID: line to
rfid_log.txt with timestamp. Used for interactive tag-registration:
user taps a tag, tells the assistant which method it represents, and
the assistant reads the latest UID from the log.

Run:  python orchestrator/tests/rfid_listener.py
Stop: Ctrl+C
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import serial

PORT = "COM4"
BAUD = 115200
LOG = Path(__file__).parent / "rfid_log.txt"


def main() -> None:
    LOG.write_text("", encoding="utf-8")  # clear previous run
    print(f"[rfid_listener] opening {PORT} @ {BAUD} baud, log -> {LOG}")
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1.0)
    except serial.SerialException as e:
        print(f"[rfid_listener] FAILED to open {PORT}: {e}")
        sys.exit(2)

    print(f"[rfid_listener] listening — tap a tag")
    try:
        while True:
            line = ser.readline().decode("ascii", errors="replace").strip()
            if not line:
                continue
            if line.startswith("RFID:"):
                stamp = time.strftime("%H:%M:%S")
                entry = f"{stamp}  {line}"
                print(entry, flush=True)
                with LOG.open("a", encoding="utf-8") as f:
                    f.write(entry + "\n")
    except KeyboardInterrupt:
        print("\n[rfid_listener] stopped")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
