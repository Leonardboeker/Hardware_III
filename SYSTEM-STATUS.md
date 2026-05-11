# System Status — Hardware III

**Last update:** 2026-05-11 (post team-merge)
**Branch:** `master` (single source of truth)

This is the **team handoff snapshot** — what works, what doesn't, where each role
plugs in. Read this before starting any new work.

---

## ⚠️ Recently landed from team — read this first

In the last few days the team pushed several large updates that converged on
Onur's metric-engine vision:

| What | Owner | Where |
|------|-------|-------|
| Full LCA data per method (CO₂, labour, time, cost — sourced ranges) | Rafik | `data/methods_db.json` + `data/methods/*.csv` |
| Source registry (45+ citations) | Rafik | `data/SOURCES.md` |
| Normalization rules (shape factor, units) | Rafik | `data/normalization_rules.json` |
| Metrics engine gaps doc | Rafik | `data/METRICS_ENGINE_GAPS.md` |
| Reclaimed brick reintroduced as **baseline** (not 4th competitor) | Rafik | `methods_db.json` id=4 |
| HSV-red-blob puck tracker (replaces ArUco) | Vision team | `vision/puck_detector.py` |
| Top-level vision app with gesture/calibration support | Vision team | `vision/main.py`, `vision/gestures.py`, `vision/calibrate.py` |
| Onur metric-engine merge | Onur | `4ce6d42 merge(Onur): metrics engine + UI prototype + data pipeline` |

**Implications for what we built earlier:**
- Methods are now 4 (3 competitive + 1 baseline) — see Section 7 below
- LCA data is **in** the JSON, not a future task
- There are now **two vision approaches** in the repo (ArUco vertical-slice
  vs HSV-red puck tracker) — see Section 8

---

## 1. Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Camera (USB)   │     │  ESP32 + RC522   │     │  methods_db.json │
│  ArUco OR HSV   │     │  (RFID reader)   │     │  + methods/*.csv │
└────────┬────────┘     └────────┬─────────┘     └────────┬─────────┘
         │ OSC (Python)          │ USB Serial             │ static
         ▼                       ▼                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │                      TouchDesigner                       │
   │                                                          │
   │  vision_in (OSC In CHOP)   rfid_in (Constant or Serial) │
   │              │                       │                   │
   │              └──────────┬────────────┘                   │
   │                         ▼                                │
   │                  compute_state (Script CHOP)             │
   │                         │                                │
   │                         ▼                                │
   │                  render_footprint (Script TOP)           │
   │                  ┌──────┴──────┐                         │
   │                  │ auto-reads  │                         │
   │                  │ text_<panel>│ (1 per text panel)      │
   │                  └─────────────┘                         │
   │                         │                                │
   │                         ▼                                │
   │                  projector_out (Window COMP)             │
   └──────────────────────────────────────────────────────────┘
```

---

## 2. Subsystem Status

| Subsystem | Status | Owner |
|-----------|--------|-------|
| TD 9-panel UI frame + auto text blit | ✅ Working | Leo |
| TD state aggregation (`compute_state`) | ✅ Working | Leo |
| TD method-selection display | ✅ Working | Leo |
| Vision: ArUco vertical-slice (`vision/src/`) | ✅ Working (synthetic calib) | Leo |
| Vision: HSV red puck tracker (`vision/puck_detector.py`) | ✅ Functional (new) | Vision team |
| OSC bridge (Python → TD) | ✅ Working | Leo (& vision team) |
| **LCA data per method (sourced ranges + confidence)** | ✅ **In place** | Rafik |
| **Source registry (45+ citations)** | ✅ Done | Rafik |
| Methods DB structure (4 methods + shape factor + phases) | ✅ Done | Rafik |
| ESP32 RC522 sketch + lab guide | ✅ Written, hardware test in progress | Leo |
| ESP32 hardware (RFID detection) | 🟡 **Blocker — RC522 not reading tags yet** | Leo (in lab) |
| Phase navigation FSM in TD | ❌ Not started | TBD |
| Per-phase visualisation logic | ❌ Not started | TBD |
| Comparison view (final state) | ❌ Not started | TBD |
| Sound layer | ❌ Not started | Sound team |
| Real camera calibration (replace synthetic) | ❌ Not started | Leo |
| Prefab lifecycle UI (per Onur metric_engine_ui_update) | ❌ Open question — see Section 7 | — |

Legend: ✅ done · 🟡 in progress · ❌ not started

---

## 3. What works right now

Open `vertical-slice.toe` in TouchDesigner 2025.32050 — `projector_out` shows
a 1280×720 image with:

- 9 bordered panels (from `reference/Panel_Ui.pdf`, scaled from 1920×1080)
- `panel_method_selection` (bottom-middle): color block + name auto-update with `rfid_in`
- `panel_main_plan_simulation` (center): puck positions + polygon when vision is running
- `bar_bottom_status`: heartbeat dot (green = vision live)

Test without ArUco / RFID hardware:
```bash
python -m vision.src.run_vertical_slice --camera 0 \
  --intrinsics vision/calibration/synthetic_intrinsics.yml \
  --homography vision/calibration/synthetic_homography.yml
```
Or new HSV-puck path (no markers needed):
```bash
python vision/main.py  # check vision/README.md for current usage
```

Change `rfid_in` Channel 0 Value (0–4) in TD → method color + name switches live.

---

## 4. TouchDesigner Network Reference

| Node | Type | Role |
|------|------|------|
| `vision_in` | OSC In CHOP, port 7000 | Puck positions from CV pipeline |
| `rfid_in` | Constant CHOP (stub) → Serial DAT (real) | Method selector |
| `compute_state` | Script CHOP | `puck_count`, `area_px2`, `method_id`, `hb_alive` |
| `render_footprint` | Script TOP (1280×720) | All 9 panels + auto-blits `text_<panel_id>` TOPs |
| `text_method_selection` | Text TOP | Method name (and any other `text_<panel>` you add) |
| `projector_out` | Window COMP | Output (`Window Operator = render_footprint`) |

Removed (don't recreate): `compose_final`, old `stats_text`, `switch1`, `select1`, `storage`, `script3`, all FSM colour blocks.

---

## 5. Adding content to a text panel

The Script TOP auto-discovers Text TOPs by name. Workflow:

1. Add a Text TOP, rename to `text_<panel_id>` (e.g. `text_right_comparison`)
2. Set Resolution to the panel size (table in `touchdesigner/PANEL-LAYOUT-GUIDE.md`)
3. Write text (literal or Python expression)
4. **Don't wire it** — `render_footprint` picks it up automatically

No `compose_final`, no Over chain, no Translate math.

---

## 6. Current Blocker — ESP32 RFID hardware

The ESP32 sketch is flashed and the heartbeat is streaming. But **the RC522 is
not detecting MIFARE tags**.

- Firmware OK: `HB:N` lines visible in serial monitor → ESP32 alive
- No `RFID:XXXXXXXX` lines on tag scans
- Next step: load MFRC522 library's `DumpInfo` example to isolate hardware vs code

Walk-through: `firmware/esp32-rfid/LAB-SETUP-GUIDE.md`

Workaround for now: `rfid_in` runs as a Constant CHOP. Change Channel 0 Value
(0/1/2/3/4) manually to switch the construction method.

---

## 7. Methods — current canonical list

| id | Name | Role | RFID Tag | data CSV |
|----|------|------|----------|----------|
| 0 | NONE | Empty / no selection | — | — |
| 1 | MASONRY | Competitive method | `A1B2C3D4` (PLACEHOLDER) | `data/methods/masonry.csv` |
| 2 | 3D PRINTED | Competitive method | `E5F6A7B8` (PLACEHOLDER) | `data/methods/3d-printed.csv` |
| 3 | PREFAB | Competitive method (CLT + modular concrete sub-methods) | `C9D0E1F2` (PLACEHOLDER) | `data/methods/prefab.csv` |
| 4 | RECLAIMED BRICK | **Baseline / floor** — not a 4th competitor | `A3B4C5D6` (PLACEHOLDER) | `data/methods/reclaimed-brick.csv` |

Reclaimed brick was removed earlier ("ohne reclaimed", 2026-05-10) but Rafik's
data team brought it back as **BASELINE** (against which other methods are
plotted), not as a competitor. This is consistent with Onur's `metric_engine_ui_update.md`.

RFID tag UIDs above are placeholders — to be assigned after the ESP32 reader
is working and the physical tags are mapped (see `serial_rfid_v1.py`).

---

## 8. Open Architecture Decisions

### 8.1 — Two vision approaches in the repo

- `vision/src/run_vertical_slice.py` — **ArUco markers** (Leo, vertical slice)
- `vision/main.py` + `puck_detector.py` — **HSV red blob tracking** (vision team, newer)

Both write OSC to TD on `vision_in`. **Which is the demo path?** The team
should pick one — likely HSV is simpler operationally (no printed markers) but
ArUco is more robust to lighting. Currently both exist; the TD side reads
whichever is running.

### 8.2 — Prefab lifecycle UI vs phase-based UI

- Onur's `metric_engine_ui_update.md` (recent): Prefab uses `lifecycle_based`
  data model with a different panel (`panel_prefab_lifecycle_card`)
- `.planning/FSM_TOUCHDESIGNER_SPEC.md`: all methods walk through the same 5 phases
- **Current code:** single UI for all methods, prefab approximated into phases

**Decision needed:** does Prefab get its own UI panel or stay in the unified
5-phase flow? See `data/METRICS_ENGINE_GAPS.md` for the data-side implications.

### 8.3 — Resolution

- Design docs say 1920×1080
- Current implementation: 1280×720 (TD Non-Commercial license limit)
- **Recommended action:** apply for TD Educational license (free for students
  with academic email) → 1920×1080 unlocked, also removes watermark

---

## 9. Per-Role Integration Points

### Data team (Rafik)
- LCA data is already wired into `methods_db.json` with sourced ranges
- Next: decide engine implementation (Python script reading CSVs, or TD-side Script DAT)
- Resolve `METRICS_ENGINE_GAPS.md` — especially prefab lifecycle mapping

### Vision team
- Two pipelines exist (`vision/src/` ArUco vs `vision/main.py` HSV). Pick one
  for demo, document the choice in `vision/README.md`
- Real camera calibration still needed (current YAMLs are synthetic placeholders)

### ESP32 / Sensor / Sound (Onur + team)
- Help debug RC522 wiring (see `firmware/esp32-rfid/LAB-SETUP-GUIDE.md`)
- Plan proximity sensor (HC-SR04 or PIR) + sound layer integration
- Define OSC/serial protocols for any new sensor

### FSM / Visuals team
- 7 text panels still empty — see Section 5 to add content
- Phase navigation logic: needs a CHOP/DAT holding current phase index (0-4)
- Per-phase visual variations TBD

### Fabrication / CAD
- ArUco markers: `cad/aruco-markers/`
- Still needed: physical puck design, method-selector models, RFID pedestal
  enclosure, table mock-up

---

## 10. Source-of-Truth Order

When older docs conflict with current code, prefer in this order:

1. `touchdesigner/scripts/footprint_viz_v5.py` — actual TD rendering
2. `touchdesigner/scripts/state_chop_v1.py` — actual state aggregation
3. `vision/src/run_vertical_slice.py` OR `vision/main.py` — actual vision (TBD which is canonical)
4. `firmware/esp32-rfid/esp32_rfid.ino` — actual firmware
5. `data/methods_db.json` — current method definitions
6. `data/SOURCES.md` — citation registry
7. `SYSTEM-STATUS.md` (this file)
8. `INTERFACE_CONTRACT.md` — subsystem boundaries
9. `.planning/FSM_TOUCHDESIGNER_SPEC.md` — FSM canonical spec
10. `data/METRICS_ENGINE_GAPS.md` — open data engineering questions

Anything in `archive/` is historical, not current.

---

## 11. Dev environment

```bash
git clone https://github.com/Leonardboeker/Hardware_III.git
cd Hardware_III

# Python deps
pip install opencv-contrib-python python-osc pyyaml numpy

# TouchDesigner: install 2025.32050 (do NOT upgrade mid-project)
# Open vertical-slice.toe

# Arduino (only for ESP32 work)
# Install Arduino IDE 2.x + ESP32 board support v2.0.17 + MFRC522 library
```

Quick test (vision only):
```bash
python -m vision.src.run_vertical_slice --camera 0 \
  --intrinsics vision/calibration/synthetic_intrinsics.yml \
  --homography vision/calibration/synthetic_homography.yml
```

Or the new HSV path:
```bash
python vision/main.py   # consult vision/README.md for current usage
```

In TD: open `vertical-slice.toe`, see 9-panel layout in `projector_out`.

---

## 12. Where to ask

- **Branch hygiene:** Leo — don't push to master without coordination
- **TD internals:** `touchdesigner/TD-FRAMEWORK-GUIDE.md` + `touchdesigner/PANEL-LAYOUT-GUIDE.md`
- **Hardware:** `firmware/esp32-rfid/LAB-SETUP-GUIDE.md`
- **Data:** `data/SOURCES.md` + `data/METRICS_ENGINE_GAPS.md`
- **Architecture:** `INTERFACE_CONTRACT.md`
