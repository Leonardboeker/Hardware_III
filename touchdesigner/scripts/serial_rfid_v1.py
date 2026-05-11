"""rfid_in — Serial DAT callbacks (real hardware path).

Reads tag→method mapping directly from data/methods_db.json so that the
hardware team can update tag IDs by editing the JSON (no Python edits).

Wiring:
  ESP32 firmware sends one line per tag scan over USB serial (115200 baud):
      RFID:<8-char-hex-id>
      Example: RFID:A1B2C3D4

  This callback parses the line, looks up the tag in methods_db.json,
  and stores the matching method_id on this DAT.
  compute_state reads it via op('rfid_in').fetch('method_id', 0).

Tag registration workflow:
  1. Put a Serial Monitor on the ESP32 OR watch the TD textport
  2. Tap each physical tag once — UID prints as "[serial_rfid] UNKNOWN TAG: XXXX"
  3. Open data/methods_db.json
  4. Replace the rfid_tag placeholder for that method with the real UID
  5. Save — TD reads the JSON live, no restart needed
"""
import json
import os


# Optional: hardcoded fallback if methods_db.json can't be found.
# In normal operation this is overridden by the JSON.
FALLBACK_RFID_TO_METHOD = {
    '00000000': 0,
}

FALLBACK_METHOD_NAMES = {
    0: 'NONE',
    1: 'MASONRY',
    2: '3D PRINTED',
    3: 'PREFAB',
    4: 'RECLAIMED BRICK',
}


# ---------------------------------------------------------------------------
# Mapping loader
# ---------------------------------------------------------------------------
def _load_mapping():
    """Build {uid_hex_upper: method_id} from methods_db.json.

    Looks for the JSON in two places:
      1. op('methods_db').text — if a Text DAT named 'methods_db' loads it
      2. project.folder + '/data/methods_db.json' — direct file read

    Falls back to FALLBACK_RFID_TO_METHOD on any failure.
    """
    # Try DAT first (preferred — picks up edits live)
    db_dat = op('methods_db')
    if db_dat is not None:
        try:
            db = json.loads(db_dat.text)
            return _extract_mapping(db), _extract_names(db)
        except Exception as e:
            print(f'[serial_rfid] methods_db DAT parse failed: {e}')

    # Try direct file read as fallback
    try:
        project_dir = project.folder
        path = os.path.join(project_dir, 'data', 'methods_db.json')
        with open(path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        return _extract_mapping(db), _extract_names(db)
    except Exception as e:
        print(f'[serial_rfid] methods_db.json read failed: {e}')

    print('[serial_rfid] using FALLBACK_RFID_TO_METHOD')
    return FALLBACK_RFID_TO_METHOD, FALLBACK_METHOD_NAMES


def _extract_mapping(db):
    mapping = {}
    for m in db.get('methods', []):
        tag = m.get('rfid_tag')
        if tag:
            mapping[tag.upper()] = m['id']
    return mapping


def _extract_names(db):
    return {m['id']: m['name'] for m in db.get('methods', [])}


# ---------------------------------------------------------------------------
# Serial DAT callbacks
# ---------------------------------------------------------------------------
_HEX = set('0123456789ABCDEF')


def onReceive(dat, rowIndex, message, bytes):
    line = message.strip()

    # Tolerant RFID match — handle leading transmission noise like "!RFID:..."
    if 'RFID:' in line:
        idx = line.index('RFID:') + 5
        raw = line[idx:].strip().upper()
        tag = ''.join(c for c in raw if c in _HEX)  # strip any non-hex artifacts
        if not tag:
            print(f'[serial_rfid] dropped malformed RFID line: {line!r}')
            return

        mapping, names = _load_mapping()
        method_id = mapping.get(tag, None)
        if method_id is None:
            print(f'[serial_rfid] UNKNOWN TAG: {tag}  '
                  f'— add it to data/methods_db.json → methods[*].rfid_tag, then save')
            dat.store('method_id', 0)
            return
        dat.store('method_id', method_id)
        name = names.get(method_id, '?')
        print(f'[serial_rfid] tag={tag}  method_id={method_id} ({name})')

    elif 'HB:' in line:
        # heartbeat from ESP32 — confirms reader is alive (silent in textport)
        pass

    elif line:
        print(f'[serial_rfid] raw: {line!r}')


def onConnect(dat):
    print(f'[serial_rfid] connected on {dat.par.port.val}')
    dat.store('method_id', 0)


def onDisconnect(dat):
    print('[serial_rfid] disconnected — method_id reset to 0')
    dat.store('method_id', 0)
