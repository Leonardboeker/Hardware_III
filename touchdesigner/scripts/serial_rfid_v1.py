"""rfid_in — Serial DAT callbacks (real hardware path).

Use this ONLY when the ESP32 + RFID reader is physically connected.
For now (no hardware), use a Constant CHOP named 'rfid_in' instead.

ESP32 firmware sends one line per tag scan over USB serial (115200 baud):
    RFID:<8-char-hex-id>
Example:
    RFID:A1B2C3D4

The callback maps the tag to a method_id and stores it on the DAT so that
compute_state can read it via op('rfid_in').fetch('method_id', 0).

To add tags: scan each physical tag, note the hex ID printed to the TD
Textport, and add it to RFID_TO_METHOD below.
"""

# Map RFID hex IDs → method index.
# Sourced from data/methods_db.json → methods[*].rfid_tag
# NOTE: these are placeholder UIDs — Person 7 (hardware) must replace them
# with real tag IDs read from the physical RFID pedestal before the demo.
RFID_TO_METHOD = {
    '00000000': 0,   # NONE / Reset
    'A1B2C3D4': 1,   # MASONRY
    'E5F6A7B8': 2,   # 3D PRINTED
    'C9D0E1F2': 3,   # PREFAB
    'A3B4C5D6': 4,   # RECLAIMED BRICK (baseline)
}

METHOD_NAMES = {0: 'NONE', 1: 'MASONRY', 2: '3D PRINTED', 3: 'PREFAB', 4: 'RECLAIMED BRICK'}


def onReceive(dat, rowIndex, message, bytes):
    """Called by TD for each complete line received on the serial port."""
    line = message.strip()

    # Discovery mode: print any unrecognised tag so you can add it above
    if line.startswith('RFID:'):
        tag = line[5:].upper()
        method_id = RFID_TO_METHOD.get(tag, None)
        if method_id is None:
            print(f'[serial_rfid] UNKNOWN TAG: {tag}  — add it to RFID_TO_METHOD')
            return
        dat.store('method_id', method_id)
        print(f'[serial_rfid] tag={tag}  method_id={method_id} ({METHOD_NAMES[method_id]})')

    elif line.startswith('HB:'):
        # optional heartbeat from ESP32 firmware, e.g. "HB:42"
        pass

    elif line:
        print(f'[serial_rfid] raw: {line}')


def onConnect(dat):
    print(f'[serial_rfid] connected on {dat.par.port.val}')
    dat.store('method_id', 0)


def onDisconnect(dat):
    print('[serial_rfid] disconnected — method_id reset to 0')
    dat.store('method_id', 0)
