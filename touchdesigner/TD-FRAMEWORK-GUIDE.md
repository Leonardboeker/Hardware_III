# TouchDesigner Framework Setup Guide

Build this network from scratch in `vertical-slice.toe` (or a new .toe).  
TD build: **2025.32050** — do not upgrade mid-project.

---

## Architecture overview

```
oscin1  ───────────────────────────────────┐
                                           ▼
serial1 (Serial DAT) ──► state1 (Script CHOP) ──► script_viz1 (Script TOP)
  └── serial_rfid_v1.py    state_chop_v1.py         footprint_viz_v5.py
                                                          │
                                           text_stats1 (Text TOP)
                                                          │
                                               over1 (Over TOP)
                                                          │
                                              window1 (Window COMP)
```

---

## Step 1 — Clean up old nodes

Delete any of these if they exist from the previous session:
- `switch1`
- `script2` (old Script CHOP with only puck_count/area)
- `text1` (old Text TOP with broken expression)

Keep: `oscin1`, `script1` (Script TOP), `over1`, `window1`.

---

## Step 2 — OSC In CHOP (`oscin1`)

Already exists. Verify settings:
- **Protocol** → UDP
- **Port** → 7000
- **Active** → On

---

## Step 3 — Serial DAT (`serial1`)

Add → DAT → Serial

Parameters:
| Parameter | Value |
|-----------|-------|
| Port | your ESP32 COM port (e.g. COM5) |
| Baud Rate | 115200 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Active | On |

Callbacks DAT:
1. Right-click `serial1` → **Edit Callbacks**
2. Paste the entire contents of `touchdesigner/scripts/serial_rfid_v1.py` into the DAT.
3. Update `RFID_TO_METHOD` dict with your actual RFID tag IDs (printed to Textport on first scan).

> **No ESP32 yet?** Leave `serial1` inactive. `state1` will default `method_id = 0`.

---

## Step 4 — State CHOP (`state1`)

Add → CHOP → Script

1. Right-click → **Edit Script**
2. Paste contents of `touchdesigner/scripts/state_chop_v1.py`
3. Set **Cook Type** → Every Frame

Outputs 4 channels: `puck_count`, `area_px2`, `method_id`, `hb_alive`

---

## Step 5 — Main Visualization (`script_viz1`)

Replace the old `script1` Script TOP or add a new one.

Add → TOP → Script

1. Right-click → **Edit Script**
2. Paste contents of `touchdesigner/scripts/footprint_viz_v5.py`
3. Set resolution to **1280 × 720** in the Script TOP parameters
4. Set **Cook Type** → Every Frame

The script reads `oscin1` and `state1` directly by name — no wire connections needed for data.

---

## Step 6 — Stats text overlay (`text_stats1`)

Add → TOP → Text

**Text** parameter (Expression mode — click the `=` button):

```python
'Pucks: ' + str(int(op('state1')['puck_count'][0])) + '   Area: ' + str(int(op('state1')['area_px2'][0])) + ' px²   ' + ['OFFLINE','LIVE'][int(op('state1')['hb_alive'][0])]
```

Parameters:
| Parameter | Value |
|-----------|-------|
| Font Size | 28 |
| Color | white (1,1,1,1) |
| Horizontal Align | Left |
| Resolution | 1280 × 180 |
| Extend (outside image) | Black |

---

## Step 7 — Composite (`over1`)

Add → TOP → Over

- Input 1: `script_viz1`
- Input 2: `text_stats1`

In the Over TOP parameters, set the **Translate Y** of input 2 to **-270** (moves text to the bottom 180px strip of the 720px frame).

Actually, the easier way: use a **Layout TOP** instead of Over:

Add → TOP → Layout
- Input 1 (top area): `script_viz1`  
- Input 2 (bottom strip): `text_stats1`

Set Layout mode to **Vertical**, heights 540 / 180.

---

## Step 8 — Projector output (`window1`)

Already exists. Connect:
`over1` (or `layout1`) → `window1`

Window parameters:
| Parameter | Value |
|-----------|-------|
| Resolution | 1280 × 720 |
| Perform Mode | On (for actual projection) |
| Monitor | your projector display index |

To preview without a projector: set **Open** → On in the Window COMP.

---

## Data flow summary

| Source | Operator | What it provides |
|--------|----------|-----------------|
| Vision Python pipeline | `oscin1` | Per-puck positions + heartbeat |
| ESP32/RFID | `serial1` + `serial_rfid_v1.py` | `method_id` stored on DAT |
| — | `state1` (Script CHOP) | `puck_count`, `area_px2`, `method_id`, `hb_alive` |
| — | `script_viz1` (Script TOP) | 1280×720 footprint render |
| — | `text_stats1` (Text TOP) | Stats overlay text |
| — | `over1` / `layout1` | Composited frame |
| — | `window1` | Projected output |

---

## Running the full pipeline

```bash
# Terminal 1 — vision pipeline
python -m vision.src.run_vertical_slice \
  --camera 0 \
  --intrinsics vision/calibration/camera_intrinsics.yml \
  --homography vision/calibration/homography.yml

# TouchDesigner — open vertical-slice.toe
# Scan an RFID tag → Textport shows the tag ID → add to serial_rfid_v1.py
```

---

## Adding a new construction method

1. Add entry to `data/methods_db.json`
2. Add `METHOD_COLORS` and `METHOD_NAMES` entries in `footprint_viz_v5.py`
3. Add RFID tag mapping in `serial_rfid_v1.py` → `RFID_TO_METHOD`
4. Re-paste updated scripts into their respective Script OPs in TD
