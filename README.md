# Hardware III — Guided Comparative Assembly

**Course:** Hardware III — Human-in-the-Loop: Interactive Systems
**Institute:** IAAC, MRAC + MAAI 2025/2026
**Schedule:** April 10 – June (extended for final demo)
**Team:** Leo, Elais, Rafik, Seid, Onur, Nithik

> **👉 Quick boot:** `.\start_all.bat` from the worktree root — starts vision + orchestrator together.
> Then turn on TouchDesigner Perform Mode (F1) for the projector output.

---

## Mission

We compare construction methods by letting people physically configure a small
building scenario on a table and immediately see the environmental, labor, time,
and economic consequences through projection.

## Core Interaction

The visitor selects a construction method (RFID tag on pedestal), configures
the footprint (red pucks on a 66×33 cm working area defined by 4 ArUco corner
markers), sets the height (slider A → floor count), picks the building phase
(slider B → which phase of the construction is being shown), and sees the
phase-specific cost / CO₂ / labour estimates projected back onto the table.

---

## Architecture (current)

```
ESP32 (COM4, USB Serial @115200) ──┐
   RFID + Slider A + Slider B      │
                                   │
                                   ├──→ Python Orchestrator (30 Hz)
                                   │       │
Vision (vision2/main.py, local) ───┘       │
   Camera + ArUco + sketch                 │
   OSC → 127.0.0.1:7000                    │
                                            ↓
                                     state_in (CHOP) + state_in_dat (DAT)
                                            │
                                            ↓
                                     chopexec → owner.store('ui_state', dict)
                                            │
                                            ↓
                                     text_* TOPs + sketch_render Script TOP
                                            │
                                            ↓
                                     final_composite (Over TOP)
                                            │
                                            ↓
                                     projector_out (Window COMP) → Beamer
```

**Single laptop hosts everything.** No cross-machine OSC, no firewall stress.
The Python orchestrator owns all business logic; TouchDesigner is a pure
renderer.

### Why this layout

The previous architecture put FSM logic, state derivation, and CSV-backed
metric computation inside TouchDesigner Script CHOPs and DAT callbacks. That
hit several pain points:

- `.toe` binary files don't diff in git — merges between teammates require coordination
- TD's File-Sync feature is bidirectional and silently overwrites local edits
- Debugging Python inside TD is awkward (textport vs IDE, no breakpoints, weird stack traces)
- Onur's `metrics_engine` CSV pipeline was broken (`KeyError: 'method'`) for weeks

The Python orchestrator solved all of these. See
[`docs/SESSION-2026-05-31-summary.md`](docs/SESSION-2026-05-31-summary.md) for the
full migration story.

---

## Tech Stack

| Tool | Role |
|------|------|
| **Python 3 orchestrator** (`orchestrator/`) | Owns state, RFID→method, slider quantization, vision intake, cost/CO₂/labor scaling, OSC out to TD |
| **TouchDesigner** | Pure renderer — receives `/state/*` OSC, composes panels + sketch overlay, drives projector |
| **Python 3 + OpenCV** (`C:\Users\leona\Downloads\vision2`) | Camera capture, ArUco detection, hand-gesture detection, sketch geometry, OSC to orchestrator |
| **ESP32 + MFRC522 + 2× sliders** (firmware in `firmware/esp32-rfid/`) | Method RFID, height slider, phase slider — USB Serial to orchestrator @ 115200 baud |
| **Rhino + Grasshopper** | Offline only — designing physical parts (pucks, table mock-up) |
| **Logitech BRIO 4K** | Overhead USB camera, mounted above table |
| **Short-throw projector** | Table projection (mirrored on horizontal axis by setup) |

The interactive runtime is **Python (orchestrator + vision) + TouchDesigner (renderer)** on a single laptop.

---

## Canonical State Model

### Method (RFID-driven)

| ID | Name | RFID UID | n_phases | max_floors |
|----|------|----------|----------|------------|
| 1 | MASONRY | `0430BF011F5713` | 5 (Foundation, Structure, Roof, Openings, Finishing) | 5 |
| 2 | 3D PRINTED | `04500701235713` | 3 (Foundation, Print, Finishing) | 2 |
| 3 | PREFAB | `04003001F85713` | 4 (Foundation, Assemble, Roof, Openings) | 8 |
| 4 | RECLAIMED BRICK | `A3B4C5D6` (placeholder) | 5 | 5 |

Slider A → floor index 1..max_floors (per-method quantization).
Slider B → phase index 1..n_phases (per-method quantization, plus 10 s manual-override timer).

Source of truth: [`data/methods_db.json`](data/methods_db.json).

### Wrapper states

`MANUAL_OVERRIDE` triggers when slider B moves > 5 %; clears after 10 s of no
movement. Manual-override is the only wrapper state currently active.

`CALIBRATION_CHECK`, `ERROR`, `RESET` are defined in the FSM spec but not yet
enforced at runtime.

Full FSM details: [`.planning/FSM_TOUCHDESIGNER_SPEC.md`](.planning/FSM_TOUCHDESIGNER_SPEC.md)

---

## Quick Start

### One-command boot (recommended)

```powershell
cd D:\IAAC\Hardware_III\.claude\worktrees\objective-leakey-a3a366
.\start_all.bat
```

This spawns:
- **HW3 Vision** window — runs `vision2/main.py`, opens camera, sends OSC
- **Orchestrator window** — runs `python -m orchestrator.main`, sends OSC to TD

Then in TouchDesigner:
- Open `td_verify_final2.21_ON.toe` (or current latest)
- Press **F1** for Perform Mode → projector output

Ctrl+C in the orchestrator window stops both processes.

### Manual / debugging

Run pieces individually if something hangs:

```powershell
# Orchestrator only (no vision):
.\orchestrator\run.bat

# Vision only (no orchestrator):
cd C:\Users\leona\Downloads\vision2
.\.venv\Scripts\python.exe main.py --cam-index 0 --td-host 127.0.0.1
```

### Configuration

All env vars are in `orchestrator/run.bat` / `start_all.bat`:

| Var | Default | Notes |
|-----|---------|-------|
| `HW3_SERIAL_PORT` | `COM4` | ESP32 USB Serial port |
| `HW3_VISION_OSC_PORT` | `7000` | Vision OSC arrives here |
| `HW3_TD_OSC_HOST` | `127.0.0.1` | TouchDesigner host |
| `HW3_TD_OSC_PORT` | `7001` | TouchDesigner listens here |
| `HW3_RFID_PRIORITY` | `1` | `1` = RFID wins over vision's `/method/selected` |
| `HW3_TICK_HZ` | `30` | Orchestrator main-loop rate |
| `VISION_CAM_INDEX` | `0` | Camera index for vision2/main.py |

Full list: see [`orchestrator/README.md`](orchestrator/README.md).

---

## Repository layout

```
README.md                        — this file
start_all.bat                    — single-command launcher (vision + orchestrator)

orchestrator/                    — Python orchestrator (Phase A+)
  main.py                        — 30 Hz event loop
  state.py                       — State dataclass + thread-safe StateManager
  methods.py                     — methods_db.json loader
  phase_quantizer.py             — slider → phase quantization w/ hysteresis + 10s override
  serial_reader.py               — ESP32 USB Serial reader thread
  vision_listener.py             — python-osc server (port 7000)
  ui_state.py                    — build payload dict for TD (cost scaling, puck coords)
  td_sender.py                   — diff-only OSC client to TD (port 7001)
  run.bat                        — orchestrator-only launcher
  tests/                         — 37 unit tests (pytest)
    rfid_listener.py             — interactive RFID-UID capture helper
    slider_inspector.py          — live SLIDER/PSLIDER range+direction inspector
    udp_sniffer.py               — passive UDP dump on port 7000 for OSC debugging
    send_fake_state.py           — fake /state/* sender for TD bridge testing
  TD-INTEGRATION.md              — how the TD-side bridge is wired

data/                            — JSON databases (methods_db.json, etc.)
firmware/                        — ESP32 firmware (Arduino sketches)
  esp32-rfid/                    — RFID + Slider A + Slider B reader

touchdesigner/                   — TD-side scripts (Onur's panel_text.py, footprint_viz_v5.py)
  scripts/                       — Python code pasted into TD Script OPs
  PANEL-LAYOUT-GUIDE.md          — Onur's 9-panel UI layout reference

docs/                            — design notes, meeting records, research
  SESSION-2026-05-31-summary.md  — single-day migration story + lessons learned
  fsm/, meetings/, research/

cad/                             — Rhino + 3D-printable parts
.planning/                       — milestones, FSM spec, roadmap
archive/                         — historical proposals, FSM drafts

td_verify_final2.*_ON.toe        — current renderer + bridge wiring (main repo)
```

External (not in this repo):
- `C:\Users\leona\Downloads\vision2\` — Onur's camera-vision script (cloned from his repo)

---

## Phases (course schedule)

| Phase | Goal | Deadline |
|-------|------|----------|
| 1 — Proposal & FSM Foundation | S1 deliverables, lock concept | April 17 ✅ |
| 2 — Data Research & Physical Model Design | Source data, fabricate parts, CV vertical slice | May 4 ✅ |
| 3 — FSM Implementation & Assembly Logic | Full FSM + piece detection | May 4 ✅ |
| 4 — Human-in-the-Loop Assembly & Sound | Guided loop, sound layer | May 11 ✅ |
| 5 — Projection Mapping & Comparison View | Calibrated projector, comparison stats | May 18 ✅ |
| 6 — Integration, Testing & Finals | Reliable end-to-end demo | Final extended |

Status: [`.planning/STATE.md`](.planning/STATE.md)

---

## Source-of-truth order

When older documents conflict with current runtime, prefer in this order:

1. [`orchestrator/`](orchestrator/) — Python source (the actual runtime)
2. [`data/methods_db.json`](data/methods_db.json) — method definitions
3. [`docs/SESSION-2026-05-31-summary.md`](docs/SESSION-2026-05-31-summary.md) — what changed in the migration
4. [`orchestrator/TD-INTEGRATION.md`](orchestrator/TD-INTEGRATION.md) — how TD is wired
5. [`touchdesigner/scripts/`](touchdesigner/scripts/) — Onur's panel rendering (still used as-is)
6. [`.planning/FSM_TOUCHDESIGNER_SPEC.md`](.planning/FSM_TOUCHDESIGNER_SPEC.md) — canonical FSM contract

Anything in `archive/` or older Phase 1 docs may still describe a
Grasshopper + Anemone + Firefly approach. That's **proposal history** — the
current runtime is Python orchestrator + TouchDesigner renderer.

---

## Branches

- `master` — last green pre-orchestrator state + auto-save snapshots
- `feat/orchestrator-hybrid` — current architecture (Python orchestrator + TD bridge). **This is where the live demo runs from.**
- `claude/objective-leakey-a3a366` — worktree branch, ahead/behind tracking
