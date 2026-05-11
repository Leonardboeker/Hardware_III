# System Status — Hardware III

**Last update:** 2026-05-11
**Branch:** `master` (single source of truth)

This document is the **team handoff snapshot** — what works, what doesn't,
where each role plugs in. Read this before starting any new work on the project.

---

## 1. Current Architecture (high-level)

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Camera (USB)   │     │  ESP32 + RC522   │     │   Methods DB     │
│  + ArUco markers│     │  (RFID reader)   │     │  methods_db.json │
└────────┬────────┘     └────────┬─────────┘     └────────┬─────────┘
         │ OpenCV                │ USB Serial             │ static file
         │ (Python)              │ 115200 baud            │
         ▼                       ▼                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │                      TouchDesigner                       │
   │                                                          │
   │  vision_in (OSC In CHOP)   rfid_in (Serial DAT)         │
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
                            │
                            ▼
                       Projector → Table surface
```

---

## 2. Subsystem Status

| Subsystem | Status | Owner | Where it lives |
|-----------|--------|-------|----------------|
| Vision pipeline (Python+OpenCV+ArUco) | ✅ Working | Leo | `vision/src/` |
| OSC bridge (Python → TD) | ✅ Working | Leo | `vision/src/osc_send.py` |
| TouchDesigner 9-panel UI frame | ✅ Working | Leo | `touchdesigner/scripts/footprint_viz_v5.py` |
| TD state aggregation (CHOP) | ✅ Working | Leo | `touchdesigner/scripts/state_chop_v1.py` |
| TD text panel auto-blit | ✅ Working | Leo | (in `footprint_viz_v5.py`) |
| TD method selection display | ✅ Working | Leo | `text_method_selection` Text TOP |
| ESP32 RC522 firmware | 🟡 Sketch written, hardware test in progress | Leo | `firmware/esp32-rfid/esp32_rfid.ino` |
| ESP32 hardware (PCB + tags) | 🟡 In lab — RFID detection not working yet | Leo | physical |
| Methods DB structure | ✅ 3 methods locked (no reclaimed) | Leo | `data/methods_db.json` |
| LCA data ingestion | ❌ Not started — values in research_2/*/VALUES.md not yet in DB | Data team | `docs/research_2/` |
| Phase navigation FSM in TD | ❌ Not started | TBD | TD spec exists in `.planning/FSM_TOUCHDESIGNER_SPEC.md` |
| Construction phase visuals | ❌ Not started | TBD | needs per-phase rendering |
| Comparison view (final) | ❌ Not started | TBD | spec in proposal |
| Sound layer | ❌ Not started | Sound team | — |
| Calibration (real camera) | ❌ Synthetic placeholder only | Leo | `vision/calibration/` |

Legend: ✅ done · 🟡 in progress · ❌ not started

---

## 3. What's on the screen right now (verified working)

Open `vertical-slice.toe` in TouchDesigner 2025.32050. The `projector_out`
window shows a 1280×720 image with:

- **9 bordered panels** in the layout from `reference/Panel_Ui.pdf`
- **`panel_method_selection`** (bottom-middle): color block + method name auto-update with `rfid_in`
- **`panel_main_plan_simulation`** (center): puck positions + polygon when vision pipeline is running
- **`bar_bottom_status`** (bottom): heartbeat dot (green = vision live, red = offline)

To test:
```bash
# vision pipeline
python -m vision.src.run_vertical_slice \
  --camera 0 \
  --intrinsics vision/calibration/synthetic_intrinsics.yml \
  --homography vision/calibration/synthetic_homography.yml
```

In TD: change `rfid_in` Channel 0 Value (0–3) → method color + name switches live.

---

## 4. TouchDesigner Network — Node Reference

| Node | Type | Role | Reads from |
|------|------|------|-----------|
| `vision_in` | OSC In CHOP | Puck positions from CV pipeline | UDP port 7000 |
| `rfid_in` | Constant CHOP (stub) → Serial DAT (real) | Construction method selector | ESP32 USB serial |
| `compute_state` | Script CHOP | Aggregates puck_count, area_px2, method_id, hb_alive | vision_in, rfid_in |
| `render_footprint` | Script TOP (1280×720) | Renders all 9 panels + auto-blits text TOPs | vision_in, compute_state, text_* TOPs |
| `text_method_selection` | Text TOP | Current method name (and any other `text_<panel_id>` TOPs you add) | compute_state |
| `projector_out` | Window COMP | Output to projector | `Window Operator = render_footprint` |

Old nodes removed (do not recreate): `compose_final`, `stats_text` (the old strip-style one), `switch1`, `select1`, `storage`, `script3`, all `disconnected`/`pending`/`invalid`/`valid` color blocks.

---

## 5. How to add content to a text panel

The Script TOP auto-discovers Text TOPs by name. So:

1. Add a Text TOP, rename to `text_<panel_id>` (e.g. `text_right_comparison`)
2. Set Resolution to panel size from the table in `touchdesigner/PANEL-LAYOUT-GUIDE.md`
3. Write Text content (literal string or Python expression)
4. **Don't wire it to anything** — `render_footprint` picks it up automatically

No more compose_final, no more Over TOPs, no more Translate math.

---

## 6. Current Blocker — ESP32 RFID hardware

The ESP32 sketch (`firmware/esp32-rfid/esp32_rfid.ino`) is flashed and the
heartbeat is streaming over USB serial, but **the RC522 module is not detecting
MIFARE tags**. Diagnostic in progress:
- Sending heartbeat (`HB:N` lines) → ESP32 firmware is running
- No `RFID:XXXXXXXX` lines appear when tags are placed on the reader
- Next step: load the MFRC522 library's built-in `DumpInfo` example to isolate
  whether it's our code or the hardware

See `firmware/esp32-rfid/LAB-SETUP-GUIDE.md` for the full wiring/setup/debug
walkthrough.

**Workaround until RFID is solved:** `rfid_in` runs as a Constant CHOP. Change
Channel 0 Value (0/1/2/3) manually to switch the construction method.

---

## 7. Open Architecture Decisions

These contradict between team docs and need to be resolved before further work:

### 7.1 — Prefab lifecycle vs construction phases
- **Onur's `metric_engine_ui_update.md`** says Prefab uses `lifecycle_based`
  data model (A1-A3, A4, A5, B, C) and a different UI panel.
- **`.planning/FSM_TOUCHDESIGNER_SPEC.md`** says all methods walk through the
  same 5 construction phases (Foundation → Finishing).
- **Implication:** if Prefab gets a different UI, the user can't physically
  walk through phases with pucks for Prefab. Breaks core UX.
- **Pending decision:** force Prefab into phase-based with approximated data +
  warning flag (recommended), OR build a parallel UI for it.

### 7.2 — Reclaimed brick
- Old docs: 4th method
- New docs (Onur's update): overlay on Masonry
- **Current code:** Reclaimed removed entirely (3 methods only). Leo's decision
  on 2026-05-10.

### 7.3 — Resolution
- Design docs: 1920×1080
- Current implementation: 1280×720 (TD Non-Commercial license limit)
- **Pending:** apply for TD Educational license (free for students) to get back
  to 1920×1080.

---

## 8. Per-Role Integration Points

### For the Data team (LCA values)
- Your data lives in `docs/research_2/<method>/VALUES.md`
- The TD runtime reads `data/methods_db.json` — currently only has metadata
- **What you need to do:** decide how to flow VALUES.md → methods_db.json
  - Option A: hand-curate JSON entries per phase per method
  - Option B: write a script that parses VALUES.md → JSON
  - Either way, schema should be:
    ```json
    "lca": {
      "foundation": {"co2_low": 70, "co2_high": 130, "unit": "kg CO2/m2"},
      ...
    }
    ```

### For the ESP32 / Sensor / Sound team
- Current ESP32 protocol: USB serial `RFID:<HEX>\n` (see firmware spec)
- TD reads it via Serial DAT. Mapping tag → method_id in
  `touchdesigner/scripts/serial_rfid_v1.py`
- **What you need to do:**
  - Help debug current RC522 wiring issue (see `firmware/esp32-rfid/LAB-SETUP-GUIDE.md`)
  - Once RFID is reading: write down tag UIDs, update the dictionary in `serial_rfid_v1.py`
  - Plan: add proximity sensor next (HC-SR04 or PIR), define its OSC/serial protocol

### For the FSM / Visuals team
- Current state: only `panel_main_plan_simulation` and `panel_method_selection`
  have content
- **What's missing:**
  - `text_top_phase_navigation` — current phase name
  - `text_left_info` — phase-specific info text
  - `text_right_comparison` — comparison table
  - `text_right_cost_chart` — cost data + chart visualization
  - `text_right_phase_preview` — checklist
  - `text_bar_bottom_status` — live status line
- **How to add them:** see `touchdesigner/PANEL-LAYOUT-GUIDE.md`, section
  "How to add text to any panel"
- **Phase logic:** needs a CHOP/DAT that holds the current phase index (0-4),
  with logic to advance based on FSM state. See `.planning/FSM_TOUCHDESIGNER_SPEC.md`.

### For Fabrication / CAD
- 3D printables and Rhino sources: `cad/` and `cad/rhino/`
- ArUco markers already generated: `cad/aruco-markers/`
- **What's missing:** physical puck design, method-selector models, table mock-up,
  RFID reader enclosure. See `cad/README.md` for conventions.

---

## 9. Key Files — Source of Truth Order

When older docs conflict with current implementation, prefer in this order:

1. `touchdesigner/scripts/footprint_viz_v5.py` — actual TD rendering
2. `touchdesigner/scripts/state_chop_v1.py` — actual state aggregation
3. `vision/src/run_vertical_slice.py` — actual vision pipeline entry
4. `firmware/esp32-rfid/esp32_rfid.ino` — actual ESP32 firmware
5. `data/methods_db.json` — current method definitions
6. `SYSTEM-STATUS.md` (this file)
7. `INTERFACE_CONTRACT.md` — system-level subsystem boundaries
8. `.planning/FSM_TOUCHDESIGNER_SPEC.md` — FSM canonical spec
9. `.planning/PROJECT.md` — project context

Anything in `archive/` is historical and should not be treated as current.

---

## 10. How to set up your dev environment

```bash
# Clone & checkout
git clone https://github.com/Leonardboeker/Hardware_III.git
cd Hardware_III

# Python deps
pip install opencv-contrib-python python-osc pyyaml numpy

# TouchDesigner: install 2025.32050 (do not upgrade mid-project)
#   Open vertical-slice.toe

# Arduino (only if working on ESP32)
#   Install Arduino IDE 2.x
#   Add ESP32 board support (v2.0.17 recommended for stability)
#   Install MFRC522 library by GithubCommunity
```

Run the vision-only test (no ESP32 needed):
```bash
python -m vision.src.run_vertical_slice --camera 0 \
  --intrinsics vision/calibration/synthetic_intrinsics.yml \
  --homography vision/calibration/synthetic_homography.yml
```

In TD: open `vertical-slice.toe`, you should see the 9-panel layout in
`projector_out`. Change `rfid_in` Channel 0 Value (0–3) to test method switching.

---

## 11. Where to ask questions

- **Branch hygiene / merging:** ask Leo, don't push to master without coordination
- **TD internals:** see `touchdesigner/TD-FRAMEWORK-GUIDE.md` +
  `touchdesigner/PANEL-LAYOUT-GUIDE.md`
- **Hardware wiring:** see `firmware/esp32-rfid/LAB-SETUP-GUIDE.md`
- **Architecture / interface contract:** see `INTERFACE_CONTRACT.md`
