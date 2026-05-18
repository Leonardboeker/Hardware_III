"""Hardware III Python orchestrator.

Reads physical inputs (ESP32 RFID + Slider A + Slider B via Serial,
Vision pucks via OSC), computes derived state (method, floor, phase,
manual-override, etc.), and pushes the final state to TouchDesigner
via OSC for rendering.

TD becomes a "dumb renderer" — all business logic lives here.

Run:
    python -m orchestrator.main
"""

__version__ = "0.1.0"
