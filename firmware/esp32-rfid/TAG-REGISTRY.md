# RFID Tag Registry

How to map your physical RFID chips to construction methods.

## Source of truth

The mapping lives in **[`data/methods_db.json`](../../data/methods_db.json)**
in the `rfid_tag` field of each method:

```json
{
  "id": 1,
  "name": "MASONRY",
  "rfid_tag": "A1B2C3D4",        ← this field
  ...
}
```

When TD's `serial_rfid_v1.py` callback receives a tag, it looks up the UID in
this JSON to determine the method. **No Python edit needed** to register tags.

## Registration workflow (5 minutes per tag)

### Step 1 — Get the tag UID

Two ways, pick one:

**Option A — Arduino Serial Monitor**
1. ESP32 connected to your laptop, sketch flashed
2. Open Arduino IDE → Tools → Serial Monitor (115200 baud)
3. Tap the tag on the RC522
4. Note the line: `RFID:A1B2C3D4` — the part after `RFID:` is your UID
5. **Close the Serial Monitor** before going to TouchDesigner (it blocks the COM port)

**Option B — TouchDesigner Textport**
1. ESP32 connected, `rfid_in` Serial DAT configured + Active
2. TD: Dialogs → Textport (Alt+T)
3. Tap the tag
4. Textport shows: `[serial_rfid] UNKNOWN TAG: A1B2C3D4 — add it to data/methods_db.json…`
5. That hex string is your UID

### Step 2 — Assign to method

1. Open `data/methods_db.json` in any text editor
2. Find the method you want this tag to control (e.g. MASONRY, id=1)
3. Replace the placeholder in `rfid_tag` with the real UID:
   ```json
   "rfid_tag": "A1B2C3D4",     ← your real UID, uppercase, no 0x prefix, no dashes
   ```
4. Save the file

### Step 3 — Apply in TouchDesigner

If you have a `methods_db` Text DAT in TD that loads the JSON:
- Click on it → **Reload** button (or Active toggle off/on) → it re-reads the file

If not:
- The serial callback re-reads the JSON on every tag scan, so it picks up the
  change on the **next tag tap**

### Step 4 — Verify

Tap the tag again. TD textport should now show:
```
[serial_rfid] tag=A1B2C3D4  method_id=1 (MASONRY)
```

And the `panel_method_selection` in the projection should switch to MASONRY's color (terracotta).

## Current placeholders

The JSON currently has these placeholder UIDs:

| Method ID | Name | Current Tag (PLACEHOLDER!) |
|-----------|------|----------------------------|
| 0 | NONE / Reset | `00000000` (reserved) |
| 1 | MASONRY | `A1B2C3D4` |
| 2 | 3D PRINTED | `E5F6A7B8` |
| 3 | PREFAB | `C9D0E1F2` |
| 4 | RECLAIMED BRICK | `A3B4C5D6` |

**These will not match your physical tags.** Replace them with real UIDs from
your S50/MIFARE Classic 1K chips.

## Rules / Conventions

- UID format: **8 uppercase hex characters, no 0x prefix, no dashes/spaces**
  - Good: `A1B2C3D4`, `7F00DEAD`, `12345678`
  - Bad: `a1b2c3d4`, `0xA1B2C3D4`, `A1-B2-C3-D4`, `A1 B2 C3 D4`
- One UID per method only — don't reuse across methods
- `00000000` is reserved for "no tag" / reset

## What if I lose a tag or get a new chip?

1. Get the new UID via Step 1 above
2. Find the method in `methods_db.json` and replace `rfid_tag` with the new UID
3. Save — next scan picks it up

## What if I have more methods than tags?

You'd need to extend `methods_db.json` with a new entry. But the current
project scope is fixed at 4 methods (3 competitive + 1 baseline) per
`SYSTEM-STATUS.md` Section 7. Don't add more without team discussion.

## What if I want the SAME tag to do different things in different phases?

That's phase-state logic, not RFID-mapping logic. The tag → method binding
should stay 1:1. Phase navigation is handled separately in TD.
