"""Live slider inspector — opens COM4 and prints SLIDER + PSLIDER lines
with min/max tracking so you can verify direction + range.

Run:  python orchestrator/tests/slider_inspector.py
Stop: Ctrl+C
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import serial

PORT = "COM4"
BAUD = 115200
LOG = Path(__file__).parent / "slider_log.txt"


def main() -> None:
    LOG.write_text("", encoding="utf-8")
    print(f"[inspector] opening {PORT} @ {BAUD} baud")
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1.0)
    except serial.SerialException as e:
        print(f"[inspector] FAILED to open {PORT}: {e}")
        sys.exit(2)

    # Track min/max per channel
    stats = {"SLIDER": [None, None, None], "PSLIDER": [None, None, None],
             "FLOOR": [None, None, None]}
    last_print = time.monotonic()
    PRINT_EVERY_S = 0.5

    print(f"[inspector] move both sliders through full range. Ctrl+C to stop.")
    try:
        while True:
            line = ser.readline().decode("ascii", errors="replace").strip()
            if not line:
                continue
            for key in stats:
                if line.startswith(f"{key}:"):
                    val_str = line[len(key) + 1:]
                    try:
                        val = float(val_str)
                    except ValueError:
                        continue
                    mn, mx, cur = stats[key]
                    stats[key] = [
                        val if mn is None else min(mn, val),
                        val if mx is None else max(mx, val),
                        val,
                    ]
                    with LOG.open("a", encoding="utf-8") as f:
                        f.write(f"{time.strftime('%H:%M:%S')}  {line}\n")
                    break
            now = time.monotonic()
            if now - last_print >= PRINT_EVERY_S:
                parts = []
                for key, (mn, mx, cur) in stats.items():
                    if cur is None:
                        parts.append(f"{key}=  -  ")
                    else:
                        parts.append(
                            f"{key}={cur:.3f} [{mn:.3f}..{mx:.3f}]"
                        )
                print("  |  ".join(parts), flush=True)
                last_print = now
    except KeyboardInterrupt:
        print("\n[inspector] stopped")
        print("\n=== final ranges ===")
        for key, (mn, mx, cur) in stats.items():
            if cur is None:
                print(f"  {key}: NO DATA")
            else:
                print(f"  {key}: range {mn:.3f} .. {mx:.3f}  (span {mx-mn:.3f})")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
