# TouchDesigner Framework Setup Guide

Build this network from scratch in `vertical-slice.toe` (or a new .toe).  
TD build: **2025.32050** — do not upgrade mid-project.

## Node naming convention

Short names that say what the node **does**, not what type it is:

| TD Node name | Type | Role |
|---|---|---|
| `cam` | OSC In CHOP | receives puck positions from vision pipeline |
| `rfid` | Serial DAT | receives RFID tag scans from ESP32 |
| `state` | Script CHOP | aggregates all state into 4 channels |
| `viz` | Script TOP | renders the 1280×720 projection image |
| `stats` | Text TOP | stats text overlay |
| `comp` | Over TOP | composites viz + stats |
| `out` | Window COMP | projector output |

---

## Architecture overview

```
cam  ────────────────────────────┐
                                 ▼
rfid ──► state (Script CHOP) ──► viz (Script TOP)
  └── serial_rfid_v1.py   state_chop_v1.py    footprint_viz_v5.py
                                 │
                         stats (Text TOP)
                                 │
                          comp (Over TOP)
                                 │
                          out (Window COMP)
```

---

## Step 1 — Clean up old nodes

Delete if they exist from the previous session:
- `switch1`, `script1`, `script2`, `text1`, `over1` (all replaced by new names above)

Keep: `oscin1` (rename it to `cam`), `window1` (rename to `out`).

To rename a node: double-click its name label in the network editor.

---

## Step 2 — `cam` — OSC In CHOP

Already exists as `oscin1`. Rename it to `cam`.

Verify settings:
- **Protocol** → UDP
- **Port** → 7000
- **Active** → On

---

## Step 3 — `rfid` — Serial DAT

Add → DAT → Serial → rename to `rfid`

| Parameter | Value |
|-----------|-------|
| Port | your ESP32 COM port (e.g. COM5) |
| Baud Rate | 115200 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Active | On |

Callbacks:
1. Right-click `rfid` → **Edit Callbacks**
2. Paste contents of `touchdesigner/scripts/serial_rfid_v1.py`
3. Update `RFID_TO_METHOD` with your actual tag IDs (shown in Textport on first scan)

> **No ESP32 yet?** Leave `rfid` inactive — `state` defaults `method_id = 0`.

---

## Step 4 — `state` — Script CHOP

Add → CHOP → Script → rename to `state`

1. Right-click → **Edit Script**
2. Paste contents of `touchdesigner/scripts/state_chop_v1.py`
3. **Cook Type** → Every Frame

Output channels: `puck_count`, `area_px2`, `method_id`, `hb_alive`

> The script references `op('cam')` and `op('rfid')` by name — make sure both nodes are named exactly that.

---

## Step 5 — `viz` — Script TOP

Add → TOP → Script → rename to `viz`

1. Right-click → **Edit Script**
2. Paste contents of `touchdesigner/scripts/footprint_viz_v5.py`
3. Resolution: **1280 × 720**
4. **Cook Type** → Every Frame

> References `op('cam')` and `op('state')` by name.

---

## Step 6 — `stats` — Text TOP

Add → TOP → Text → rename to `stats`

**Text** parameter — click `=` to switch to Expression mode:

```python
'Pucks: ' + str(int(op('state')['puck_count'][0])) + '   Area: ' + str(int(op('state')['area_px2'][0])) + ' px²   ' + ['OFFLINE','LIVE'][int(op('state')['hb_alive'][0])]
```

| Parameter | Value |
|-----------|-------|
| Font Size | 28 |
| Color | 1, 1, 1, 1 (white) |
| Horizontal Align | Left |
| Resolution | 1280 × 180 |

---

## Step 7 — `comp` — Over TOP

Add → TOP → Over → rename to `comp`

- Input 1: `viz`
- Input 2: `stats`

In Over parameters → **Translate Y** of input 2: `-270`  
(shifts the 180px text strip to the bottom of the 720px frame)

---

## Step 8 — `out` — Window COMP

Rename existing `window1` to `out`. Connect: `comp` → `out`

| Parameter | Value |
|-----------|-------|
| Resolution | 1280 × 720 |
| Monitor | projector display index |

To preview without projector: **Open** → On

---

## Data flow summary

| Node | Type | Reads from | Provides |
|------|------|-----------|----------|
| `cam` | OSC In CHOP | vision pipeline (port 7000) | puck positions + heartbeat |
| `rfid` | Serial DAT | ESP32 (USB serial) | RFID tag → method_id |
| `state` | Script CHOP | `cam`, `rfid` | puck_count, area_px2, method_id, hb_alive |
| `viz` | Script TOP | `cam`, `state` | 1280×720 render |
| `stats` | Text TOP | `state` | stats string |
| `comp` | Over TOP | `viz`, `stats` | composited frame |
| `out` | Window COMP | `comp` | projector |

---

## Running the full pipeline

```bash
python -m vision.src.run_vertical_slice \
  --camera 0 \
  --intrinsics vision/calibration/camera_intrinsics.yml \
  --homography vision/calibration/homography.yml
```

---

## Adding a new construction method

1. Add entry to `data/methods_db.json`
2. Add color + name in `footprint_viz_v5.py` → `METHOD_COLORS` / `METHOD_NAMES`
3. Add RFID tag in `serial_rfid_v1.py` → `RFID_TO_METHOD`
4. Re-paste updated scripts into `viz` and `rfid` Script OPs in TD
