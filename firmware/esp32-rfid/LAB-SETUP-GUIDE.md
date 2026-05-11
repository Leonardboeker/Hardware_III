# ESP32 + RC522 RFID — Lab Setup Walkthrough

Komplette Schritt-für-Schritt Anleitung für's Electronics Lab. Druck es notfalls
aus oder hab's auf'm Handy auf.

**Ziel:** ESP32 sendet bei jedem RFID-Tag-Scan eine Zeile `RFID:A1B2C3D4\n` über
USB-Serial an den Laptop. TouchDesigner liest das mit Serial DAT.

---

## 1. Was du brauchst

### Hardware

- [ ] **ESP32 Dev Board** (z.B. ESP32-WROOM-32, 38 Pins) × 1
- [ ] **RC522 RFID Modul** × 1
- [ ] **MIFARE Classic 1K Tags (S50)** × 3+ (eine pro Methode + Backup)
- [ ] **Jumper-Kabel female-female** × 7 (für saubere Verkabelung)
- [ ] **USB-Kabel** (Micro-USB oder USB-C, je nach ESP32) × 1
- [ ] **Breadboard** optional (falls ESP32 noch ohne Pin-Header)

### Software (am Laptop)

- [ ] **Arduino IDE 2.x** installiert
- [ ] **TouchDesigner 2025.32050** läuft

---

## 2. Verkabelung

> ⚠️ **VR4 3.3V — NICHT 5V!** Das RC522 brennt bei 5V durch. Doppelt prüfen.

### Pinout Tabelle

| RC522 Pin | Signal | → | ESP32 Pin | Farbe (Vorschlag) |
|-----------|--------|---|-----------|-------------------|
| `SDA` (oder `SS`) | Chip Select | → | **GPIO 5** | Gelb |
| `SCK` | SPI Clock | → | **GPIO 18** | Grün |
| `MOSI` | Data Out (Master→Slave) | → | **GPIO 23** | Blau |
| `MISO` | Data In (Slave→Master) | → | **GPIO 19** | Violett |
| `RST` | Reset | → | **GPIO 27** | Weiß |
| `3.3V` | **VCC (3.3V only!)** | → | **3V3** | Rot |
| `GND` | Masse | → | **GND** | Schwarz |
| `IRQ` | Interrupt | → | **nicht verbinden** | — |

### ASCII-Diagramm

```
            RC522                                ESP32
        ┌──────────┐                          ┌─────────┐
        │  SDA  ●──┼──────────GELB──────────●─┤ GPIO 5  │
        │  SCK  ●──┼──────────GRÜN──────────●─┤ GPIO 18 │
        │  MOSI ●──┼──────────BLAU──────────●─┤ GPIO 23 │
        │  MISO ●──┼──────────VIOLETT───────●─┤ GPIO 19 │
        │  IRQ  ●──┼────  (nicht verbinden)    │         │
        │  GND  ●──┼──────────SCHWARZ───────●─┤ GND     │
        │  RST  ●──┼──────────WEISS─────────●─┤ GPIO 27 │
        │  3.3V ●──┼──────────ROT───────────●─┤ 3V3 ⚠️  │
        └──────────┘                          └─────────┘
```

### Reihenfolge zum Verkabeln (empfohlen)

1. **Erst GND** (Masse) verbinden — verhindert Kurzschluss-Spitzen
2. **Dann 3.3V** (NICHT 5V!)
3. **Dann SPI-Pins** (SDA, SCK, MOSI, MISO) — beliebige Reihenfolge
4. **Dann RST**
5. IRQ leer lassen
6. Vor USB-Anschluss: **alle Drähte nochmal prüfen** — besonders 3.3V!

---

## 3. Arduino IDE — Einmal-Setup

### a) ESP32 Board Support installieren

1. Arduino IDE öffnen
2. **File → Preferences**
3. Bei **Additional Boards Manager URLs** diese URL einfügen:
   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```
4. OK
5. **Tools → Board → Boards Manager** öffnen
6. Suchfeld: `esp32`
7. **`esp32` by Espressif Systems** → **Install** (dauert 1-3 Min)

### b) MFRC522 Library installieren

1. **Tools → Manage Libraries** (Strg+Shift+I)
2. Suchfeld: `MFRC522`
3. **`MFRC522` by GithubCommunity** → **Install**

### c) Board + Port auswählen

1. ESP32 per USB anstecken
2. **Tools → Board → ESP32 Arduino → ESP32 Dev Module**
3. **Tools → Port → COM?** — wähle den Port aus, der **dazukam** als du den ESP32 eingesteckt hast
   - Wenn unsicher: ESP32 abstecken, schauen welcher Port verschwindet, wieder anstecken
4. Andere Settings auf Default lassen (115200 Baud, etc.)

---

## 4. Sketch laden und flashen

### a) Sketch öffnen

1. **File → Open**
2. Navigiere zu: `D:\IAAC\Hardware_III\firmware\esp32-rfid\esp32_rfid.ino`
3. Öffnen

### b) Kompilieren testen

1. **Sketch → Verify/Compile** (Strg+R) — kein Upload, nur Test
2. Unten in der Konsole sollte stehen `Done compiling.`
3. Falls Fehler: lies die letzte Zeile, oft fehlt die MFRC522-Library

### c) Upload (Flash)

1. **Sketch → Upload** (Strg+U) oder den **→ Pfeil** oben links klicken
2. Console zeigt: `Writing at 0x...`
3. **WICHTIG:** Bei manchen ESP32-Boards musst du den **`BOOT` Button gedrückt halten** während des Uploads bis "Writing..." erscheint
4. Bei Erfolg: `Done uploading.` — und der ESP32 startet neu

### d) Wenn Upload fehlschlägt

| Problem | Lösung |
|---------|--------|
| `Failed to connect to ESP32` | BOOT-Button gedrückt halten beim Start des Uploads, loslassen wenn Writing beginnt |
| `Port not found / busy` | Anderen Port wählen, oder Serial Monitor schließen (blockiert den Port) |
| `A fatal error occurred` | Anderes USB-Kabel probieren (manche sind nur Lade-Kabel, ohne Daten) |

---

## 5. Test im Serial Monitor (ohne TouchDesigner)

1. **Tools → Serial Monitor** öffnen (oder Lupe-Icon oben rechts)
2. Unten rechts Baudrate auf **`115200`** stellen
3. Du solltest sofort sehen:
   ```
   BOOT:rfid_reader_ready
   HB:1
   HB:2
   HB:3
   ...
   ```
4. **Tag auf den Reader legen** (auflegen, nicht nur drüberwischen)
5. Zwischen den `HB:` Zeilen erscheint:
   ```
   RFID:A1B2C3D4
   ```
   (deine Tag-UID — wird bei jedem Tag anders sein)

### Was die Ausgaben bedeuten

- `BOOT:rfid_reader_ready` — Firmware ist gestartet, RC522 läuft
- `HB:N` — Heartbeat alle 1 Sek (sek seit Start) → zeigt dass der ESP32 läuft
- `RFID:XXXXXXXX` — Tag wurde gescannt, das ist die Unique ID (Hex)

### Notiere dir die UIDs!

Scanne jeden der 3 Tags einmal und schreib dir auf:

```
Tag 1 → Methode: MASONRY      UID: _________________
Tag 2 → Methode: 3D PRINTED   UID: _________________
Tag 3 → Methode: PREFAB       UID: _________________
```

Brauchst du gleich für TouchDesigner.

### Falls keine Ausgabe kommt

| Problem | Diagnose | Lösung |
|---------|----------|--------|
| Gar nichts in Serial Monitor | Falsche Baudrate | Auf 115200 setzen |
| Nur `BOOT` aber keine `HB:` | Sketch hängt oder nicht hochgeladen | Re-flashen |
| `BOOT` + `HB:` aber kein `RFID:` beim Tag-Auflegen | Verkabelung oder RC522 defekt | Pins prüfen, anderen Tag probieren, näher dran halten |
| `BOOT` aber gefolgt von garbage characters | Falsche Baudrate auf ESP32 oder Monitor | Baudrate beidseitig 115200 |

---

## 6. TouchDesigner Integration

Wenn der Serial Monitor `RFID:` Ausgaben zeigt, ist die Hardware fertig.
Jetzt in TD:

1. **Serial Monitor in Arduino IDE schließen** (blockiert sonst den COM-Port!)
2. In TD: aktuellen **`rfid_in` Constant CHOP löschen** (war der Stub)
3. **Add → DAT → Serial** → rename zu **`rfid_in`**
4. Parameter:
   - **Port**: gleicher COM-Port wie in Arduino
   - **Baud Rate**: `115200`
   - **Active**: `On`
5. Rechtsklick auf `rfid_in` → **Edit Callbacks** → das öffnet ein zweites DAT
6. In das Callbacks-DAT: kompletten Inhalt aus
   `D:\IAAC\Hardware_III\touchdesigner\scripts\serial_rfid_v1.py` reinpasten
7. Im Code oben den `RFID_TO_METHOD` Dictionary mit **deinen UIDs** befüllen:
   ```python
   RFID_TO_METHOD = {
       'A1B2C3D4': 1,   # ← deine MASONRY UID
       'E5F6A7B8': 2,   # ← deine 3D PRINTED UID
       'C9D0E1F2': 3,   # ← deine PREFAB UID
   }
   ```
8. Strg+S, schließen

### Test in TD

- Tag scannen → TD-Textport zeigt `[serial_rfid] tag=...  method_id=1 (MASONRY)`
- Der Methoden-Farbblock in `panel_method_selection` wechselt Farbe
- Der Text im `text_method_selection` wechselt zu `MASONRY` / `3D PRINTED` / `PREFAB`

### Falls TD-Textport eine "UNKNOWN TAG" Meldung zeigt

Das passiert wenn du einen Tag scannst der nicht im Dictionary ist. Die Meldung
zeigt die UID — kopiere sie und füge eine neue Zeile in `RFID_TO_METHOD` hinzu.

---

## 7. Häufige Probleme — Quick Reference

| Symptom | Wahrscheinlichste Ursache | Fix |
|---------|---------------------------|-----|
| Upload-Fehler `Failed to connect` | BOOT-Button-Logik | Beim Upload BOOT-Button gedrückt halten |
| COM-Port doppelt belegt | Arduino Serial Monitor + TD gleichzeitig offen | Eins von beiden schließen |
| RC522 wird heiß | 5V angeschlossen | SOFORT abstecken, neu verkabeln mit 3.3V |
| Tag-Reichweite < 1cm | RC522-Antenne von Metall gestört | RC522 in 3D-gedruckte Halterung packen, Abstand zu Metall halten |
| Heartbeat aber kein RFID | SPI-Pin falsch verkabelt | SDA/SCK/MOSI/MISO/RST nochmal prüfen |
| RFID UIDs ändern sich pro Scan | Es sind UID-randomisierte Tags (selten) | Andere Tag-Charge benutzen |

---

## 8. Was tun nach dem Lab

1. **Foto vom Aufbau** machen (für Doku)
2. **UIDs in dieses Repo committen**:
   - `firmware/esp32-rfid/TAG-REGISTRY.md` anlegen mit Tag → Methode Mapping
   - Update `touchdesigner/scripts/serial_rfid_v1.py` mit echten UIDs
   - Push zu GitHub
3. **Mir Bescheid geben** wenn was nicht geklappt hat oder TD-Integration noch Probleme macht

---

## 9. Pin-Übersicht — Tabelle für's Lab (auch zum Ausdrucken)

```
═══════════════════════════════════════════════════
  HARDWARE III — RFID READER PIN MAP
═══════════════════════════════════════════════════
  RC522 SDA  → ESP32 GPIO 5    (Gelb)
  RC522 SCK  → ESP32 GPIO 18   (Grün)
  RC522 MOSI → ESP32 GPIO 23   (Blau)
  RC522 MISO → ESP32 GPIO 19   (Violett)
  RC522 RST  → ESP32 GPIO 27   (Weiß)
  RC522 GND  → ESP32 GND       (Schwarz)
  RC522 3.3V → ESP32 3V3       (Rot)  ⚠️ NICHT 5V!
  RC522 IRQ  → nicht verbunden

  Baud:  115200
  Tag:   MIFARE Classic 1K (S50)
═══════════════════════════════════════════════════
```

Viel Erfolg im Lab! 🔌
