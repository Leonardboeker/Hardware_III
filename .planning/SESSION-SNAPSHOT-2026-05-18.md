# Session Snapshot — Phase 02.1 Integration + Vision Pipeline Connection

**Date:** 2026-05-18
**Branch:** `claude/objective-leakey-a3a366`
**Pushed to GitHub:** ✓ (latest commit `f055625`)

## TL;DR — What is the system status right now?

End-to-end demo path verified live in TouchDesigner with all four input sources
flowing into `compute_state` Script CHOP:

| Input | Path | Verification |
|-------|------|--------------|
| **RFID method tag** | RC522 → ESP32 USB Serial → `serial1_callbacks` parser → `rfid_in.fetch('method_id')` → `compute_state.method_id` | `method_id: 3.0` (PREFAB tag detected) |
| **Slider A — HEIGHT** | DollaTek 10K pot → ESP32 GPIO34 → median+EMA+hysteresis in firmware → `FLOOR:<int>` Serial → `compute_state.floor` | `floor: 1..5` swept verified, `[serial_rfid] floor=2,3,4,5` observed |
| **Slider B — BUILDING_PHASE** | DollaTek 10K pot → ESP32 GPIO35 → raw smoothing in firmware → `PSLIDER:<0.xxx>` Serial → TD-side quantization w/ per-method `n_phases` → `compute_state.phase_index` + `wrapper_state` | `phase_slider_raw: 0.2`, `phase_index: 2`, `wrapper_state: 0` (auto-clears after 300 frames of inactivity) |
| **Vision pucks** | Camera on Elias's laptop → `main.py` OSC sender (UDP 7000, IAAC WLAN) → `vision_in` OSC In CHOP → patched `vision2_state_chop.py` → `compute_state.puck_count` + `hb_alive` | `hb_alive: 1.0`, `puck_count: 4.0` (4 ArUco markers tracked live) |

Bottom-bar in the rendered UI shows live `VISION LIVE · METHOD PREFAB · PUCKS 4 · FLOOR 1 · PHASE 2/5`.

## File-system layout — what was changed

### Firmware (committed earlier in session)

| File | Change |
|------|--------|
| `firmware/esp32-rfid/esp32_rfid/esp32_rfid.ino` | Added Slider A (GPIO34) + Slider B (GPIO35) reads with median window=8, EMA alpha=0.2, hysteresis epsilon=0.02. Emits `FLOOR:<int>` on quantized change, `SLIDER:<0.xxx>` every 200 ms, `PSLIDER:<0.xxx>` every 200 ms. No quantized `PHASE:` emit — TD-side does that. |

Flashed successfully on May 18. Firmware verified via Serial Monitor sweeping `FLOOR:1` through `FLOOR:5` cleanly, no boundary jitter.

### TouchDesigner Python scripts

| File | Change |
|------|--------|
| `touchdesigner/scripts/serial_rfid_v1.py` | Added `PSLIDER:`, `SLIDER:`, `FLOOR:` branches in `onReceive`. PSLIDER **must** be tested before SLIDER (substring match collision). Defaults in `onConnect`/`onDisconnect`. |
| `touchdesigner/scripts/vision2_state_chop.py` | (1) Added 7 slider channels: `floor`, `slider_raw`, `slider_alive`, `phase_slider_raw`, `phase_index`, `phase_slider_alive`, `wrapper_state`. (2) Per-method `n_phases` quantization for Slider B w/ TD-side hysteresis. (3) `wrapper_state=1` when Slider B moves >0.05; auto-clears after `PHASE_OVERRIDE_FRAMES=300`. (4) **Patched OSC channel-naming tolerance**: handles `vision/heartbeat` vs `vision/heartbeat:0`, auto-detects flat-1/colon/flat-0 puck naming, discovers puck IDs dynamically (variable ArUco IDs, not just 0-9). (5) `_int_chan`/`_float_chan` helpers tolerant of both formats. (6) Cached `methods_db.json` parse by content-hash. |
| `touchdesigner/scripts/panel_text.py` | `bar_bottom_status()` now reads `floor`, `phase_index`, `n_phases` and appends `FLOOR n · PHASE i/N` segments. |
| `touchdesigner/scripts/footprint_viz_v5.py` | Added `_max_floors_for(method_id)` helper, floor-cap red border + diagonal X overlay when `floor > max_floors`, manual-override orange dashed border when `wrapper_state == 1`. |

### Planning documents

`.planning/phases/02.1-height-slider/` contains the complete Phase 02.1 plan + 4 plan files + CONTEXT.md + .gitkeep. All 6 documents reflect the locked decisions including the Slider B amendment (2026-05-16) and per-method `n_phases` values.

### Diagnostic + repair scripts (added during this session)

Live in `touchdesigner/`:

| Script | Purpose |
|--------|---------|
| `wiring_fix.py` | Repoints all File-Sync paths after `.toe` is opened on a new machine. Bulk fix when paths point to wrong locations. |
| `wiring_diag.py` / `wiring_diag2.py` | Lists nodes + identifies file-sync mismatches. |
| `verify_slider_b.py` | Checks `compute_state` exposes the 7 slider channels. |
| `fix_compute_state.py` | Redirects `compute_state.par.callbacks` if pointing at wrong DAT. |
| `force_load_scripts.py` / `force_load_v2.py` | Force-pushes `.py` content into DATs with BOM strip + sync disabled (file-sync had been overwriting worktree edits). |
| `nuke_compute_state.py` | Resolves Script CHOP inline-script-overrides-callbacks-DAT issue. Sets both `par.callbacks` and `par.script` to vision2_state_callbacks DAT. |
| `restore_compute_state.py` | Re-push `vision2_state_chop.py` content into `compute_state_callbacks` DAT after module-toggle cascades. |
| `presentation_safe.py` | Minimal, touches ONLY compute_state — leaves all text TOPs at Onur's original state. **This is the script to run for a clean session setup.** |
| `make_text_tops_live.py` / `revert_text_tops.py` / `make_reactive_v2.py` | Attempts to make text TOPs live-reactive. **Avoid running these** — they overwrote Onur's working layout in some sessions. |
| `rebuild_onur_ui.py` / `rebuild_v2.py` | Attempted to re-run Onur's bootstrap function. Fails because `metric_ui_bootstrap` module is missing the `bootstrap_metric_ui()` attribute (the function name in the DAT is different from what `LEO-TD-INTEGRATION-GUIDE.md` documents). |
| `diag_text_tops.py` | Calls each `panel_text` function and prints output. Used to verify Onur's metrics pipeline is publishing to `ui_state` (it is — all 20 keys present). |
| `slider_live_check.py` | Live-print compute_state slider values for diagnostics. |
| `one_shot_slider_b.py` | Variant of `presentation_safe.py` that also sets `text_bar_bottom_status` as an expression. |
| `fix_rfid_callbacks.py` | Repoint `rfid_in.par.callbacks` after BOM corruption. |
| `fix_ui_text_top.py` | (Avoid) Earlier text TOP overwrite attempt — replaced by `make_reactive_v2.py`. |

### Wiring documentation

| File | Purpose |
|------|---------|
| `firmware/esp32-rfid/WIRING-DIAGRAM.html` | Self-contained HTML wiring diagram with SVG, color-coded wire legend, pin table, and notes. Browser-printable. Shows both sliders + RC522 wiring on ESP32. |

## TouchDesigner configuration state (live in `.toe`)

### `compute_state` Script CHOP

- `par.callbacks` → `/project1/vision2_state_callbacks` (DAT with patched `vision2_state_chop.py` text)
- `par.script` → `/project1/vision2_state_callbacks`
- Output channels (20): `puck_count, area_px2, area_m2, method_id, hb_alive, sketch_points, sketch_walls, sketch_windows, is_extruded, gesture_id, gesture_dwell, gesture_action, fsm_state, floor, slider_raw, slider_alive, phase_slider_raw, phase_index, phase_slider_alive, wrapper_state`

### `vision_in` OSC In CHOP

- Active: **On**
- Protocol: Messaging (UDP)
- Network Port: **7000**
- Network Address: (empty — accepts from any IP)
- OSC Address Scope: `*`
- 31 channels currently received (during Elias's `run.bat` running):
  ```
  vision/heartbeat
  puck/detected1..5            (multi-arg list of currently detected IDs)
  puck/lost
  puck/171, puck/172, puck/173 (per-puck data, flat-1-indexed; ArUco ID 17)
  puck/41, puck/42, puck/43    (ArUco ID 4)
  puck/101, puck/102, puck/103 (ArUco ID 10)
  puck/81, puck/82, puck/83    (ArUco ID 8)
  puck/371, puck/372, puck/373 (ArUco ID 37)
  puck/01, puck/02, puck/03    (ArUco ID 0)
  puck/11, puck/12, puck/13    (ArUco ID 1)
  method/selected, sketch/{points,walls,windows,extruded}, gesture/{id,dwell,action}, fsm/state
  ```
- **Naming convention received: flat-1-indexed** — `/puck/<id>` with 3 args becomes `puck/<id>1`, `puck/<id>2`, `puck/<id>3`.

### `text_bar_bottom_status` Text TOP

- `par.text.mode` = EXPRESSION
- `par.text.expr` = `op('panel_text').module.bar_bottom_status()`
- Renders live: `VISION LIVE · METHOD PREFAB · PUCKS 4 · AREA 0.0 m² · FLOOR 1 · PHASE 2/5`

### Other text TOPs

Left at Onur's pristine static content from the restored `.toe`. They do **NOT** react to RFID method change in the current setup — see Known Issue below.

### `methods_db` Text DAT

Loaded from `data/methods_db.json` (master version). Does **not yet** include `n_phases` or `phase_names` fields per method — Plan 03 Task 1 is not yet executed. Slider B falls back to default `n_phases=5` for all methods until those fields are added.

## Network setup (cross-machine)

- TD machine IP (WiFi): **`172.16.21.109`** (verified via `ipconfig` on the IAAC WLAN)
- Vision laptop sends to: `TD_HOST=172.16.21.109` UDP 7000
- Vision laptop runs: `run.bat` → Python venv → `main.py` (CAM_INDEX=2)
- Windows Firewall rule **NOT yet added** on TD machine — OSC packets are flowing anyway (some other allow rule active). For robustness on other machines:
  ```cmd
  netsh advfirewall firewall add rule name="TouchDesigner OSC In" protocol=UDP dir=in localport=7000 action=allow
  ```
  (run from Admin command prompt)

## `.toe` versions on disk — recovery references

| File | Size | Status |
|------|------|--------|
| `vertical-slice.leo-integration.toe` | currently working state (after restore + presentation_safe.py + save) | latest |
| `vertical-slice.leo-integration.10.toe` | 68050 bytes | Known-good baseline saved during session |
| `vertical-slice.leo-integration.11.toe` | 68018 bytes | Intermediate auto-save |
| `vertical-slice.leo-integration.14.toe` | 58162 bytes | **BROKEN** — UI overlapping mess from text TOP overrides |
| `vertical-slice.leo-integration.broken-backup.toe` | 58162 bytes | Manual backup of broken version (kept for reference) |
| `vertical-slice.GOOD-BASELINE-AUTO.toe` | 68050 bytes | Filesystem snapshot of .10.toe |
| `origin/Onur:vertical-slice.leo-integration.toe` | 65138 bytes | Pristine Onur version on git remote |

## Session recovery procedure (if .toe gets broken again)

1. In TD: `File → Quit` → **Don't Save**
2. Bash: `cd D:/IAAC/Hardware_III && git checkout origin/Onur -- vertical-slice.leo-integration.toe`
3. Reopen the `.toe`
4. In TD textport:
   ```python
   exec(open('D:/IAAC/Hardware_III/touchdesigner/presentation_safe.py').read())
   ```
5. Verify:
   ```python
   cs = op('/project1/compute_state'); print('hb_alive:', cs['hb_alive'][0], 'puck_count:', cs['puck_count'][0], 'method_id:', cs['method_id'][0])
   ```
6. If all green: `Ctrl+S` to save the working state.

## Known issues (pre-existing, not blocking demo)

### 1. Onur's metrics pipeline CSV schema mismatch

**Symptom:** `[vision2_state] owner sync failed: 'method'` spam every cook (or on every method change).

**Root cause:** `metrics_engine.py` calls `metrics/pipeline.py:load_normalized_rows()` which expects CSV files with 17 columns (`method, data_model, display_mode, phase, ...`). Actual `data/methods/*.csv` files have only 8 columns (`phase, parameter, value_low, value_high, unit, assumption, source, source_tier`). When the function tries `raw["method"]`, it raises `KeyError: 'method'`.

**Impact:** Right-side panels (`YOUR SELECTION`, `SELECTED PART IMPACT`, `TOTAL PROJECT IMPACT`, `CURRENT STATE`, `CHOOSE METHOD`) don't update when RFID method changes. They show static content from whenever Onur last ran a successful bootstrap.

**Why Slider B is unaffected:** Slider B reads only `compute_state` channels and `methods_db.json`. Never touches the metrics pipeline.

**Fix path:** Onur (or whoever maintains metrics) needs to either (a) run `python -m metrics.build_normalized_data` to regenerate normalized CSVs and commit them, or (b) patch `pipeline.py:load_normalized_rows` to derive missing columns from filename + raw columns. See `docs/LEO-TD-INTEGRATION-GUIDE.md` notes from this session.

### 2. `bootstrap_metric_ui` function not exported

**Symptom:** `AttributeError: module '/project1/bootstrap_metric_ui' has no attribute 'bootstrap_metric_ui'`

**Likely cause:** The function name in `metric_ui_bootstrap.py` may be different from what `LEO-TD-INTEGRATION-GUIDE.md` documents, or the DAT has stale inline content.

**Workaround:** We don't actually need bootstrap to run for Slider B. `presentation_safe.py` does the minimum required.

### 3. BOM accumulation in some DAT contents

**Symptom:** `SyntaxError: invalid non-printable character U+FEFF` on `serial1_callbacks` or other DATs.

**Root cause:** TD's "Sync to File" wrote DAT contents (which had BOM) back to disk; subsequent reads picked up the BOM. Multiple sync cycles caused 2-3 BOMs to accumulate.

**Mitigation in code:** All force-load scripts now strip BOM bytes before writing to DATs:
```python
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
```

### 4. Text TOPs are not reactive on method change

**Symptom:** Tapping a different RFID tag updates `compute_state.method_id` but the visual UI panels (other than bottom bar) don't change.

**Why:** Onur's design uses `bootstrap_metric_ui()` and `refresh_metrics_ui.refresh()` to write text into Text TOPs as STATIC content. Both of these crash on issue #1 above. So text TOPs never get refreshed.

**Could fix by:** Setting text TOPs as live Python expressions. But during this session, doing that produced visual overlap/sizing issues (likely because the Text TOP resolutions don't accommodate fully-evaluated function output). For the presentation, accept that only bottom bar updates live.

## Commits this session (worktree branch)

```
f055625 fix(td-02.1-02): tolerant OSC channel naming for vision_in
d7046ad tools(td): nuke_compute_state.py - resolve Script CHOP inline-script override
8e8780c tools(td): TD integration diagnostic + repair scripts for Slider B
ac4da33 feat(td-02.1-02): wire Slider A + B through TouchDesigner runtime
a9bbe31 Merge remote-tracking branch 'origin/Onur' into claude/objective-leakey-a3a366
1d55109 Merge remote-tracking branch 'origin/master' into claude/objective-leakey-a3a366
6303df4 feat(firmware-02.1-01): Task 3 - slider B GPIO35 constants, state, poll loop, PSLIDER emit
2c3b9f9 feat(firmware-02.1-01): Task 2 - slider A ADC config, poll loop, FLOOR/SLIDER Serial emit
32237f9 feat(firmware-02.1-01): Task 1 - slider A constants, ring buffer, EMA state, helpers
```

## Demo path for finals presentation

### Session start checklist

1. **TD machine:** open `D:\IAAC\Hardware_III\vertical-slice.leo-integration.toe`
2. **TD textport (Alt+T):**
   ```python
   exec(open('D:/IAAC/Hardware_III/touchdesigner/presentation_safe.py').read())
   ```
3. **Vision laptop:** start `run.bat` (CAM_INDEX=2, TD_HOST=172.16.21.109)
4. **Verify:**
   ```python
   cs = op('/project1/compute_state'); print('hb_alive:', cs['hb_alive'][0], 'puck_count:', cs['puck_count'][0], 'method_id:', cs['method_id'][0])
   ```
5. **Save** if all green: `Ctrl+S`

### During presentation

- Click `compute_state` Script CHOP → press `S` → live channel viewer floats. Visible: floor, phase_index, wrapper_state, slider_raw, phase_slider_raw, puck_count, hb_alive, method_id.
- Bottom bar in rendered output shows live `VISION LIVE · METHOD <name> · PUCKS <n> · FLOOR <n> · PHASE <i>/<N>`
- Tap RFID tags → `method_id` updates live in channel viewer + bottom bar METHOD changes
- Move Slider A → `floor` quantizes 1→5, bottom bar FLOOR updates
- Move Slider B → `phase_slider_raw` changes smoothly, `phase_index` quantizes per-method, `wrapper_state` flips to 1 for 10 s, orange dashed border appears around `method_selection` panel
- Place ArUco pucks under camera → `puck_count` increases in channel viewer + bottom bar PUCKS updates

### Talking points

- Closed-loop CV remains primary (locked decision #1). Slider B is a MANUAL_OVERRIDE wrapper — auto-clears after 10 s.
- Hysteresis prevents boundary jitter; verified on hardware sweep.
- Per-method phase count is data-driven via `methods_db.json[method_id].n_phases` (when populated; currently defaults to 5 for all methods since Plan 03 Task 1 — adding `n_phases` field — has not been executed yet).
- Vision pipeline runs on separate laptop, communicates via OSC over WLAN — clean separation of concerns.

## Open work for after the finals

1. Plan 03 Task 1: add `n_phases` + `phase_names` per method to `data/methods_db.json` (so Slider B quantizes 3 for 3DP, 4 for Prefab, 5 for masonry).
2. Plan 03 Tasks 2/3/4: extend `INTERFACE_CONTRACT.md` §4 + §9, update `FSM_TOUCHDESIGNER_SPEC.md` and `PROJECT.md`, add Slider B wiring to firmware READMEs.
3. Plan 04: write smoke-test runbook with Test A/B/C/D/E procedures.
4. Onur metrics CSV pipeline (separate, blocking RFID-reactive UI).

---

*Generated 2026-05-18. Branch `claude/objective-leakey-a3a366` is the canonical state.*
