# TouchDesigner Framework Setup Guide

Build this network in `vertical-slice.toe`.  
TD build: **2025.32050** — do not upgrade mid-project.

---

## Node naming convention

Names describe **what the node does**, not its operator type:

| Node name | Type | Role |
|-----------|------|------|
| `vision_in`        | OSC In CHOP    | OSC data from OpenCV pipeline (puck positions + heartbeat) |
| `rfid_in`          | Constant CHOP (stub) → Serial DAT (real) | construction method selector |
| `compute_state`    | Script CHOP    | aggregates puck_count, area, method_id, hb_alive |
| `render_footprint` | Script TOP     | renders the 1280×720 projection image |
| `stats_text`       | Text TOP       | text overlay (Pucks / Area / Status) |
| `compose_final`    | Over TOP       | merges render_footprint + stats_text |
| `projector_out`    | Window COMP    | sends image to the projector |

---

## Architecture

```
vision_in ─────────┐
                   ├──► compute_state ──► render_footprint ──┐
rfid_in   ─────────┘                                         ├──► compose_final ──► projector_out
                              │                              │
                              └──► stats_text ───────────────┘
```

---

## Step 0 — Clean up old nodes

Delete (right-click → Delete):
- `script1`, `script2`, `script3` (and their `_callbacks` DATs)
- `text1`, `over1`, `over2`, `transform1`
- `select1`, `storage`
- `disconnected`, `pending`, `invalid`, `valid` (FSM color blocks)

Keep: `cam` (we'll rename it), `window1` (we'll rename it).

---

## Step 1 — `vision_in` (OSC In CHOP)

You already have this as `cam`. **Rename** it:
- Double-click the name label `cam` → type `vision_in` → Enter

Verify settings:
| Parameter | Value |
|-----------|-------|
| Protocol | UDP |
| Port | 7000 |
| Active | On |

---

## Step 2 — `rfid_in` (stub: Constant CHOP)

For now, fake the RFID input with a Constant CHOP. Later we replace it with a real Serial DAT when the ESP32 hardware is built.

1. **Add → CHOP → Constant**
2. Rename to `rfid_in`
3. In parameters → **Channel 0**:
   - **Name**: `method_id`
   - **Value**: `0`

To test methods later, manually change Value to 1, 2, 3, or 4 — the visualization will update its color.

---

## Step 3 — `compute_state` (Script CHOP)

1. **Add → CHOP → Script**
2. Rename to `compute_state`
3. Right-click → **Edit Script** → paste contents of [`touchdesigner/scripts/state_chop_v1.py`](scripts/state_chop_v1.py)
4. Parameters → **Cook Type** → Every Frame

Outputs 4 channels: `puck_count`, `area_px2`, `method_id`, `hb_alive`

> Reads `op('vision_in')` and `op('rfid_in')` by name — make sure both exist.

---

## Step 4 — `render_footprint` (Script TOP)

1. **Add → TOP → Script**
2. Rename to `render_footprint`
3. Right-click → **Edit Script** → paste contents of [`touchdesigner/scripts/footprint_viz_v5.py`](scripts/footprint_viz_v5.py)
4. Parameters → **Common** → Resolution → **1280 × 720**
5. Parameters → **Cook Type** → Every Frame

> Reads `op('vision_in')` and `op('compute_state')` by name.

---

## Step 5 — `stats_text` (Text TOP)

1. **Add → TOP → Text**
2. Rename to `stats_text`
3. Click the `=` button next to the **Text** parameter to switch to Expression mode
4. Paste:

```python
'Pucks: ' + str(int(op('compute_state')['puck_count'][0])) + '   Area: ' + str(int(op('compute_state')['area_px2'][0])) + ' px²   ' + ['OFFLINE','LIVE'][int(op('compute_state')['hb_alive'][0])]
```

5. Other params:

| Parameter | Value |
|-----------|-------|
| Font Size | 28 |
| Color | 1, 1, 1, 1 (white) |
| Horizontal Align | Left |
| Resolution | 1280 × 180 |

---

## Step 6 — `compose_final` (Over TOP)

1. **Add → TOP → Over**
2. Rename to `compose_final`
3. Connect:
   - Input 1: `render_footprint`
   - Input 2: `stats_text`
4. In Over parameters → **Translate** of Input 2:
   - **ty** = `-270` (shifts the 180-px text strip to the bottom of the 720-px frame)

---

## Step 7 — `projector_out` (Window COMP)

Rename existing `window1` to `projector_out`. Connect:
- `compose_final` → `projector_out`

| Parameter | Value |
|-----------|-------|
| Resolution | 1280 × 720 |
| Monitor | projector display index (or 0 for primary) |

To preview without a projector: set **Open** → On in projector_out.

---

## Final layout check

```
vision_in (OSC In CHOP, port 7000)
rfid_in   (Constant CHOP, method_id = 0)
                    │
                    ▼
            compute_state (Script CHOP)
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
   render_footprint         stats_text
   (Script TOP 1280×720)    (Text TOP, expression)
        │                        │
        └─────► compose_final ◄──┘
                     │
                     ▼
              projector_out
              (Window COMP)
```

---

## Testing without hardware

1. Run the vision pipeline:
   ```bash
   python -m vision.src.run_vertical_slice \
     --camera 0 \
     --intrinsics vision/calibration/synthetic_intrinsics.yml \
     --homography vision/calibration/synthetic_homography.yml
   ```
2. Watch the puck markers move on the camera preview.
3. In TD, change `rfid_in` → Channel 0 → Value (0–4) to switch construction methods. The polygon outline color in `render_footprint` should change.

---

## When the ESP32 + RFID hardware arrives

Replace the `rfid_in` Constant CHOP with a Serial DAT:
1. Delete `rfid_in` (the Constant CHOP)
2. **Add → DAT → Serial**, rename to `rfid_in`
3. Set **Port** = COM port, **Baud** = 115200, **Active** = On
4. Right-click → **Edit Callbacks** → paste [`touchdesigner/scripts/serial_rfid_v1.py`](scripts/serial_rfid_v1.py)
5. `compute_state` works with both — no script changes needed

---

## Adding a new construction method

1. Add entry to [`data/methods_db.json`](../data/methods_db.json)
2. Add color + name in `footprint_viz_v5.py` → `METHOD_COLORS` / `METHOD_NAMES`
3. Add RFID tag mapping in `serial_rfid_v1.py` → `RFID_TO_METHOD` (only when hardware is in use)
4. Re-paste updated scripts into `render_footprint` and `rfid_in` Script OPs in TD
