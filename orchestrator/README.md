# Hardware III — Python Orchestrator

A Python application that reads all physical inputs (ESP32 RFID + Slider A + Slider B via Serial, ArUco pucks via OSC from the vision laptop), computes the derived application state (method, floor, phase, manual-override, etc.), and pushes the final state to TouchDesigner via OSC for rendering.

**TD becomes a dumb renderer.** All business logic, state machines, and data joins live here in Python — easier to test, debug, version, and onboard new collaborators.

## Why this exists

The previous architecture put all logic inside TouchDesigner Script CHOPs and DAT callbacks. That works but has several pain points the team has hit repeatedly:

- Binary `.toe` files don't diff in git — merges between teammates require coordination
- TD's File-Sync feature is bidirectional and silently overwrites local edits
- Debugging Python inside TD is awkward (textport vs IDE, no breakpoints, weird stack traces)
- Cross-machine setups need every File-Sync path repointed by hand
- Different sub-issues (BOM accumulation, inline-script-vs-callback-DAT priority, etc.)

By moving the logic out, TD's only job is rendering — and that's what it's actually good at.

## Architecture

```
ESP32 (Serial, COM4) ─┐
                       ├─→  orchestrator (Python)  ─→  OSC /state/*  ─→  TouchDesigner  ─→  Projector
Vision (OSC :7000) ────┘             │
                                      ↓
                                 derives:
                                   method_id, floor, phase_index,
                                   wrapper_state, puck_count, area_m2,
                                   hb_alive, bar_bottom_text, …
```

The orchestrator runs on the **TD machine**. It listens on UDP 7000 for the vision pipeline (same port TD used before — vision laptop is unchanged) and pushes derived state to TD on UDP 7001.

## Module map

| File | Purpose |
|------|---------|
| `main.py` | Entry point. Wires everything together; runs the 30 Hz orchestration loop. |
| `config.py` | All constants. Override via `HW3_*` environment variables. |
| `state.py` | Central `State` dataclass + thread-safe `StateManager`. |
| `methods.py` | Loads `data/methods_db.json` into typed `Method` objects with safe defaults. |
| `phase_quantizer.py` | Slider B → phase_index with hysteresis + 10 s MANUAL_OVERRIDE timer. Pure logic; fully unit-tested. |
| `serial_reader.py` | Background thread reading ESP32 USB Serial. Parses `BOOT:` / `HB:` / `RFID:` / `FLOOR:` / `SLIDER:` / `PSLIDER:` lines. Auto-reconnects. |
| `vision_listener.py` | Background OSC server (`python-osc`) handling vision pipeline messages. Tolerant of flat-1-indexed channel naming. |
| `ui_state.py` | Converts current `State` + active `Method` into the dict payload TD consumes. |
| `td_sender.py` | OSC client to TD. Sends each payload key as `/state/<key>` only when its value changes (cheap pipe). |

## Setup

```cmd
cd D:\IAAC\Hardware_III
python -m venv .venv
.venv\Scripts\activate
pip install -r orchestrator\requirements.txt
```

## Run

From the repo root:
```cmd
python -m orchestrator.main
```

Or via the launcher:
```cmd
orchestrator\run.bat
```

The launcher activates `.venv\` if present and sets the default env vars. Edit `run.bat` if your Serial port or vision laptop differ.

## Configuration (env vars)

| Var | Default | Notes |
|-----|---------|-------|
| `HW3_SERIAL_PORT` | `COM4` | ESP32 USB Serial port |
| `HW3_SERIAL_BAUD` | `115200` | Must match firmware |
| `HW3_VISION_OSC_HOST` | `0.0.0.0` | Bind address for incoming vision OSC (use 0.0.0.0 to accept from any IP) |
| `HW3_VISION_OSC_PORT` | `7000` | Vision pipeline sends here |
| `HW3_TD_OSC_HOST` | `127.0.0.1` | TouchDesigner listens here (local) |
| `HW3_TD_OSC_PORT` | `7001` | Different from 7000 so vision and orchestrator-to-TD don't clash |
| `HW3_TICK_HZ` | `30` | Orchestration loop rate |
| `HW3_PHASE_OVERRIDE_S` | `10.0` | Manual-Override duration after Slider B move |
| `HW3_PHASE_OVERRIDE_THRESHOLD` | `0.05` | Slider B Δ that triggers override |
| `HW3_PHASE_HYST_EPSILON` | `0.02` | TD-side hysteresis nudge |
| `HW3_HB_TIMEOUT_S` | `3.0` | Vision heartbeat staleness threshold |
| `HW3_RFID_PRIORITY` | `0` | Set to `1` to make RFID method-id win over vision's `/method/selected` |
| `HW3_LOG_LEVEL` | `INFO` | `DEBUG` for raw Serial / OSC traces |

## TD-side setup (Day 2 work — not done yet)

To consume the `/state/*` stream from this orchestrator, TouchDesigner needs:

1. A new **OSC In CHOP** named `state_in` on UDP **7001**, OSC Address Scope `/state/*`. This is separate from the existing `vision_in` on 7000 (which keeps receiving vision pipeline data directly — that path is unchanged).
2. Reduce `compute_state` (Script CHOP) to a thin shim that reads from `state_in` instead of computing things itself. Or keep `compute_state` and add a new `state_in` that surfaces the new keys.
3. Optionally wire individual text TOPs to expressions like:
   ```python
   op('state_in')['state/bar_bottom_text'][0]
   ```
   For text channels OSC In CHOP receives the strings as channel names, not numeric values — use a DAT bridge or `Renderer Sample Op` instead. (Detailed instructions will be in `orchestrator/TD-INTEGRATION.md` when Day 2 work starts.)

For now the orchestrator can run **standalone** — it'll happily print state to the console even with no TD listening on 7001.

## Tests

```cmd
cd D:\IAAC\Hardware_III
pytest orchestrator\tests -v
```

Tests are fast (<1 s) and require no hardware — pure logic only:
- `test_phase_quantizer.py` — quantization correctness, hysteresis, manual-override timer
- `test_methods.py` — JSON loading, lookups, defaults for missing fields
- `test_ui_state.py` — payload key coverage, phase clamping, bar text formatting

## Debugging tips

- `HW3_LOG_LEVEL=DEBUG` to see every parsed Serial line and OSC packet.
- Run with `python -X dev -m orchestrator.main` to catch Python warnings (deprecations, ResourceWarning on socket leaks).
- The orchestrator prints `[wiring]` lines whenever method or phase changes — visual confirmation that inputs are being processed.
- If no Serial data: check `HW3_SERIAL_PORT` matches Device Manager. Make sure Arduino Serial Monitor isn't holding the COM port.
- If no vision data: check Windows Firewall allows UDP 7000 inbound. Run `netstat -an | findstr :7000` to verify TD or this orchestrator is bound.

## Roadmap

- [x] **Phase A** — Read all inputs in Python, compute state, send to TD as OSC
- [ ] **Phase B** — TD-side adapter DAT that converts `/state/*` OSC into `owner.store('ui_state', dict)` so Onur's panel_text functions work unchanged
- [ ] **Phase C** — Move Onur's `metrics_engine` + `ui_state` logic out of TD entirely; UI payload built fully in Python
- [ ] **Phase D** — `.toe` becomes minimal renderer-only; cleaned up to ship
