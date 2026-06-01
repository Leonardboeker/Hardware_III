# firmware/

ESP32 microcontroller code — RFID method selector, Slider A (height/floor),
Slider B (building phase), comms with the Python orchestrator over **USB
Serial @ 115200 baud**.

> **Note:** Comms is USB Serial, NOT OSC/WiFi. The earlier proposal used OSC
> over WiFi but the orchestrator-side architecture made USB Serial simpler:
> no network config, no firewall, plug-and-play. `pyserial` handles
> auto-reconnect on the host side.

## Current sketch

`esp32-rfid/esp32_rfid/esp32_rfid.ino` — Arduino-IDE sketch for ESP32 Dev
Module + MFRC522 RFID + 2× DollaTek 10K linear slide potentiometers on
GPIO34 (Slider A) and GPIO35 (Slider B).

Hardware spec: [`esp32-rfid/README.md`](esp32-rfid/README.md)

## Serial protocol (one event per line)

| Prefix | Format | Notes |
|--------|--------|-------|
| `BOOT:rfid_reader_ready` | string | Emitted once after boot |
| `HB:<sec>` | int | Heartbeat, ~1 Hz |
| `RFID:<HEX>` | 14-char hex | Tag UID. Re-emit on tag change, or every 2 s if held |
| `FLOOR:<int>` | int 1..5 | Slider A → quantized floor. Firmware-side hysteresis. |
| `SLIDER:<0.xxx>` | float | Slider A raw, smoothed (median + EMA) |
| `PSLIDER:<0.xxx>` | float | Slider B raw, smoothed |

`SLIDER` and `PSLIDER` are emitted periodically (every ~30 ms).
The orchestrator re-quantizes per-method `max_floors` / `n_phases` from
the raw values, ignoring the firmware's `FLOOR:` for floor mapping (kept
emitted for backward compat / debugging).

## Conventions

- Arduino IDE for now (Onur has the workspace). PlatformIO migration
  optional.
- Pin assignments and wiring diagrams go in `esp32-rfid/`, not buried in
  commit messages. There's a step-by-step `wiring-diagram.html` for
  printing/iPad reference.
- Never hardcode WiFi credentials — not needed for USB Serial setup
  anyway. If WiFi is ever added back, use a `secrets.h` (gitignored).
