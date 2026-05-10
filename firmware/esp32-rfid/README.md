# esp32-rfid

ESP32 + MFRC522 firmware for the RFID method selector.

Reads MIFARE Classic 1K (S50) tag UIDs and streams them to TouchDesigner
over USB serial.

## Wiring

```
RC522        ESP32
─────────────────────────
SDA  (SS) -> GPIO 5
SCK       -> GPIO 18
MOSI      -> GPIO 23
MISO      -> GPIO 19
RST       -> GPIO 27
3.3V      -> 3V3  (NOT 5V — RC522 is 3.3V only)
GND       -> GND
IRQ       -> (not connected)
```

## Build & flash

1. Install the **Arduino IDE** (>= 2.0).
2. Add ESP32 board support: File → Preferences → Additional Boards Manager URLs:
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
3. Tools → Board → Boards Manager → search "esp32" → install `esp32 by Espressif`.
4. Tools → Manage Libraries → search "MFRC522" → install `MFRC522 by GithubCommunity`.
5. Open `esp32_rfid.ino`.
6. Select board: Tools → Board → ESP32 Arduino → ESP32 Dev Module.
7. Select port: Tools → Port → COMx (the one that appears when ESP32 is plugged in).
8. Click upload (→ arrow).

## Test (without TouchDesigner)

Tools → Serial Monitor → set baud to **115200**. You should see:

```
BOOT:rfid_reader_ready
HB:1
HB:2
HB:3
RFID:A1B2C3D4    ← appears when you tap a tag on the reader
HB:4
...
```

The `BOOT` line confirms firmware loaded. `HB:N` is a per-second heartbeat so
TD knows the reader is alive even with no tag. `RFID:<HEX>` is the tag UID.

## Tag → method ID mapping

The mapping lives in TD, not in the firmware: see
[`touchdesigner/scripts/serial_rfid_v1.py`](../../touchdesigner/scripts/serial_rfid_v1.py)
→ `RFID_TO_METHOD`.

To register a new tag:
1. Tap it on the reader, note the hex UID printed in the Serial Monitor.
2. Add a line in `RFID_TO_METHOD`:
   ```python
   'A1B2C3D4': 1,   # Masonry
   ```
3. Re-paste the updated script into the `rfid_in` Serial DAT in TD.
