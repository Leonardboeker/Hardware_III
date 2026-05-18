"""rfid_in - Serial DAT callbacks.

Reads tag-to-method mapping from data/methods_db.json so hardware updates do
not require Python edits.

ESP32 firmware is expected to send one line per tag scan:
  RFID:<8-char-hex-id>
"""
import json
import os


FALLBACK_RFID_TO_METHOD = {
    "00000000": 0,
}

FALLBACK_METHOD_NAMES = {
    0: "NONE",
    1: "MASONRY",
    2: "3D PRINTED",
    3: "PREFAB",
    4: "RECLAIMED BRICK",
}

_HEX = set("0123456789ABCDEF")


def _load_mapping():
    """Build {uid_hex_upper: method_id} from methods_db.json."""
    db_dat = op("methods_db")
    if db_dat is not None:
        try:
            database = json.loads(db_dat.text)
            return _extract_mapping(database), _extract_names(database)
        except Exception as exc:
            print(f"[serial_rfid] methods_db DAT parse failed: {exc}")

    try:
        project_dir = project.folder
        path = os.path.join(project_dir, "data", "methods_db.json")
        with open(path, "r", encoding="utf-8") as handle:
            database = json.load(handle)
        return _extract_mapping(database), _extract_names(database)
    except Exception as exc:
        print(f"[serial_rfid] methods_db.json read failed: {exc}")

    print("[serial_rfid] using FALLBACK_RFID_TO_METHOD")
    return FALLBACK_RFID_TO_METHOD, FALLBACK_METHOD_NAMES


def _extract_mapping(database):
    mapping = {}
    for method in database.get("methods", []):
        tag = method.get("rfid_tag")
        if tag:
            mapping[str(tag).upper()] = method["id"]
    return mapping


def _extract_names(database):
    return {method["id"]: method["name"] for method in database.get("methods", [])}


def onReceive(dat, rowIndex, message, bytes):
    line = message.strip()

    if "RFID:" in line:
        start = line.index("RFID:") + 5
        raw = line[start:].strip().upper()
        tag = "".join(char for char in raw if char in _HEX)
        if not tag:
            print(f"[serial_rfid] dropped malformed RFID line: {line!r}")
            return

        mapping, names = _load_mapping()
        method_id = mapping.get(tag)
        if method_id is None:
            print(
                "[serial_rfid] UNKNOWN TAG: "
                f"{tag} - add it to data/methods_db.json -> methods[*].rfid_tag, then save"
            )
            dat.store("method_id", 0)
            return

        dat.store("method_id", method_id)
        name = names.get(method_id, "?")
        print(f"[serial_rfid] tag={tag}  method_id={method_id} ({name})")
        return

    if "HB:" in line:
        return

    # PSLIDER MUST be tested BEFORE SLIDER — `"SLIDER:" in "PSLIDER:0.5"` returns True
    # (substring match at index 1). Reversed order would mis-route Slider B values
    # into Slider A storage. See .planning/phases/02.1-height-slider/02.1-CONTEXT.md.
    if "PSLIDER:" in line:
        start = line.index("PSLIDER:") + 8
        raw = line[start:].strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"[serial_rfid] dropped malformed PSLIDER line: {line!r}")
            return
        dat.store("phase_slider_raw", value)
        dat.store("phase_slider_last_frame", absTime.frame)
        return

    if "SLIDER:" in line:
        start = line.index("SLIDER:") + 7
        raw = line[start:].strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"[serial_rfid] dropped malformed SLIDER line: {line!r}")
            return
        dat.store("slider_raw", value)
        dat.store("slider_last_frame", absTime.frame)
        return

    if "FLOOR:" in line:
        start = line.index("FLOOR:") + 6
        raw = line[start:].strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"[serial_rfid] dropped malformed FLOOR line: {line!r}")
            return
        dat.store("floor", value)
        print(f"[serial_rfid] floor={value}")
        return

    if line:
        print(f"[serial_rfid] raw: {line!r}")


def onConnect(dat):
    print(f"[serial_rfid] connected on {dat.par.port.val}")
    dat.store("method_id", 0)
    dat.store("floor", 1)
    dat.store("slider_raw", 0.0)
    dat.store("slider_last_frame", -1)
    dat.store("phase_slider_raw", 0.0)
    dat.store("phase_slider_last_frame", -1)


def onDisconnect(dat):
    print("[serial_rfid] disconnected - method_id reset to 0")
    dat.store("method_id", 0)
    dat.store("floor", 1)
    dat.store("slider_raw", 0.0)
    dat.store("slider_last_frame", -1)
    dat.store("phase_slider_raw", 0.0)
    dat.store("phase_slider_last_frame", -1)
