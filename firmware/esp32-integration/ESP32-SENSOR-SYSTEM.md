# ESP32 Sensor Integration System

**Role:** Hardware interface layer — proximity detection, RFID model identification, and WiFi communication to TouchDesigner.

**Owner:** ESP32 / Sensor + Sound + QA / Ops

**Last Updated:** 2026-05-04

---

## Overview

The ESP32-WROOM-32 microcontroller sits at the junction between the physical interaction layer and the software FSM. Its job is to:

1. **Detect user engagement** via proximity sensor (HC-SR04 ultrasonic or PIR) → triggers data zoom/focus in projection
2. **Identify construction method** via RFID reader (MFRC522) → tells TouchDesigner which model was placed
3. **Stream sensor data** over WiFi/OSC to TouchDesigner at 50–100 Hz
4. **Log all events** locally for debugging and post-demo analysis

This document specifies the hardware, firmware architecture, OSC protocol, calibration procedure, and QA checklist.

---

## 1. Hardware Setup

### 1.1 Components

| Component | Spec | Quantity | Notes |
|-----------|------|----------|-------|
| Microcontroller | ESP32-WROOM-32 (38 GPIO, 4MB Flash) | 1 | ~12€, buys WiFi + Bluetooth |
| RFID Reader | MFRC522 (13.56 MHz, SPI interface) | 1 | Read range: 0–3cm; coin tags embedded in model bases |
| Proximity Sensor | HC-SR04 ultrasonic **OR** PIR motion | 1 | HC-SR04: ~0–400cm range; better angular resolution. PIR: ~5m range; simpler but less precise. **Recommend HC-SR04.** |
| RFID Tags | MIFARE Classic 1K, coin type (25mm × 3mm) | 3 | One per construction method |
| Power | USB or 3.3V battery pack | 1 | USB = tethered but simpler; battery = untethered |
| Antenna | Wire or chip antenna (built into MFRC522) | — | Most MFRC522 boards have integrated antenna |
| Cabling | Male-to-female dupont / jumper wires | — | Keep <50cm between ESP32 and sensors to avoid noise |
| Enclosure | Optional 3D-printed or laser-cut | — | Protects PCB; mounted on table edge or overhead rig |

### 1.2 Wiring Diagram

#### A. MFRC522 RFID → ESP32 (SPI)

| MFRC522 Pin | Signal | ESP32 Pin | Notes |
|-------------|--------|-----------|-------|
| SDA (SS) | Chip Select | GPIO 5 | Active LOW |
| SCK | Serial Clock | GPIO 18 | Max 5 MHz for stable comms |
| MOSI | Master Out | GPIO 23 | Data: MCU → reader |
| MISO | Master In | GPIO 19 | Data: reader → MCU |
| GND | Ground | GND | **Must be common ground** |
| RST | Reset | GPIO 27 | Active LOW pulse to reset reader |
| 3.3V | Power | 3.3V | MFRC522 draws ~50mA during read |

**Schematic notes:**
- Keep CS line low during comms; high when idle
- RST normally high; pulse low (~10µs) to reset
- Add 100nF decoupling cap between 3.3V and GND near MFRC522

#### B. HC-SR04 Ultrasonic → ESP32 (GPIO)

| HC-SR04 Pin | Signal | ESP32 Pin | Notes |
|-------------|--------|-----------|-------|
| GND | Ground | GND | Common ground |
| VCC | Power | 5V (from USB) **or** 3.3V (with level shifter) | HC-SR04 prefers 5V |
| TRIG | Trigger pulse | GPIO 4 | 10µs pulse to start measurement |
| ECHO | Echo pulse | GPIO 2 | Rising edge = sent; falling edge = received |

**Timing:**
- Send 10µs LOW-HIGH pulse on TRIG
- Wait for ECHO to go HIGH, measure time until LOW
- Distance (cm) = echo_time (µs) / 58

**Level shifting (if using 3.3V):**
- HC-SR04 ECHO outputs ~5V logic levels
- Use 1kΩ + 2kΩ resistor divider: `ECHO → 1kΩ → GPIO2 → (2kΩ to GND)`

#### C. PIR Alternative (if using instead of HC-SR04)

| PIR Pin | Signal | ESP32 Pin |
|---------|--------|-----------|
| GND | Ground | GND |
| VCC | Power | 3.3V |
| OUT | Motion detect | GPIO 4 | HIGH when motion detected; time-out ~30s |

**Pros:** No measurement loop needed; just read GPIO state  
**Cons:** Less precise distance; longer timeout; can't distinguish "leaning in" from "walking past"  
**Verdict:** HC-SR04 is preferred for this use case.

#### D. Power & USB

- **USB:** Provides 5V (1A typical) — enough for ESP32 + MFRC522 + HC-SR04
- **Battery:** 3.7V LiPo (500–1000 mAh) with voltage regulator → 3.3V
- **Decoupling:** Add 10µF + 100nF caps across 3.3V rail near ESP32

---

## 2. Firmware Architecture

### 2.1 File Structure

```
firmware/
├── platformio.ini              # Project config
├── src/
│   ├── main.cpp               # Setup + main loop
│   ├── rfid_handler.cpp/h     # RFID read + tag lookup
│   ├── proximity_handler.cpp/h # HC-SR04 distance measurement
│   ├── osc_sender.cpp/h       # WiFi + OSC message transmission
│   ├── config.h               # Pin definitions, constants
│   └── secrets.h.example      # WiFi credentials template (gitignored)
├── lib/
│   └── [Arduino libraries managed by PlatformIO]
└── docs/
    ├── CALIBRATION.md         # Proximity threshold tuning
    └── UIDs.txt               # Scanned tag UIDs + model mapping
```

### 2.2 Execution Flow

```
SETUP
  ├─ Serial.begin(115200)
  ├─ SPI.begin() + RFID.PCD_Init()
  ├─ WiFi.begin(SSID, password)
  ├─ Wait for WiFi connected
  └─ Print IP address

LOOP (50–100 Hz, ~10–20ms per iteration)
  ├─ Measure HC-SR04 distance
  │  └─ Send if distance < threshold (e.g., 30cm = "leaning in")
  ├─ Check for new RFID tag
  │  └─ If found: match against model table → send OSC
  ├─ Send OSC batch (proximity + any state change)
  └─ Yield to WiFi stack (delay ~10ms)
```

### 2.3 Key Constants & Configuration

```cpp
// config.h

// ===== Pins =====
#define RFID_SS_PIN     5      // Chip Select
#define RFID_RST_PIN    27     // Reset
#define HC_TRIG_PIN     4      // Trigger
#define HC_ECHO_PIN     2      // Echo (input)

// ===== Timing (milliseconds) =====
#define PROXIMITY_POLL_INTERVAL   20    // Read HC-SR04 every 20ms
#define RFID_DEBOUNCE_TIME       1000   // Ignore same tag for 1s
#define PROXIMITY_THRESHOLD_CM    30    // "Leaning in" = closer than 30cm

// ===== WiFi =====
#define WIFI_RECONNECT_TIMEOUT   30000  // Retry connection every 30s
#define OSC_SEND_RATE            50     // Hz (20ms per batch)

// ===== Sensor calibration =====
#define HC_DISTANCE_MIN_CM        5     // Ignore readings < 5cm (noise)
#define HC_DISTANCE_MAX_CM      400     // Max range of HC-SR04
```

---

## 3. Firmware Implementation

### 3.1 Main Loop (pseudocode)

```cpp
// main.cpp

#include "config.h"
#include "rfid_handler.h"
#include "proximity_handler.h"
#include "osc_sender.h"

unsigned long lastProximityRead = 0;
unsigned long lastOSCSend = 0;
unsigned long lastRFIDRead = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Initialize SPI for RFID
  SPI.begin(RFID_CLK, RFID_MISO, RFID_MOSI, RFID_SS_PIN);
  rfidInit();

  // Initialize GPIO for HC-SR04
  proximityInit();

  // Connect WiFi
  wifiConnect();

  Serial.println("Setup complete. Listening for tags and proximity...");
}

void loop() {
  uint32_t now = millis();

  // === Read proximity sensor every 20ms ===
  if (now - lastProximityRead >= PROXIMITY_POLL_INTERVAL) {
    lastProximityRead = now;
    float distance = measureDistance();
    if (distance >= HC_DISTANCE_MIN_CM && distance <= HC_DISTANCE_MAX_CM) {
      bool userLeaningIn = (distance < PROXIMITY_THRESHOLD_CM);
      sendProximityUpdate(distance, userLeaningIn);
    }
  }

  // === Check for new RFID tag ===
  if (now - lastRFIDRead >= 100) {  // Poll RFID at ~10 Hz
    lastRFIDRead = now;
    if (rfidCheckNewCard()) {
      int modelID = rfidIdentifyModel();
      if (modelID > 0) {
        sendRFIDUpdate(modelID);
        // Debounce: ignore same tag for 1 second
        delay(RFID_DEBOUNCE_TIME);
      }
    }
  }

  // === Maintain WiFi connection ===
  if (WiFi.status() != WL_CONNECTED) {
    wifiReconnect();
  }

  delay(5);  // Yield to WiFi/other tasks
}
```

### 3.2 RFID Handler (tag identification)

```cpp
// rfid_handler.h / rfid_handler.cpp

#include <MFRC522.h>

MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);

struct ModelMapping {
  byte uid[4];           // UID bytes to match
  int  model_id;         // 1, 2, or 3
  const char* method;    // "masonry", "3d_print", "prefab"
};

ModelMapping models[] = {
  {{0x12, 0x34, 0x56, 0x78}, 1, "masonry"},
  {{0xAA, 0xBB, 0xCC, 0xDD}, 2, "3d_print"},
  {{0x11, 0x22, 0x33, 0x44}, 3, "prefab"}
};

int numModels = sizeof(models) / sizeof(models[0]);

void rfidInit() {
  rfid.PCD_Init();
  rfid.PCD_SetAntennaGain(rfid.RxGain_max);
  Serial.println("RFID initialized");
}

bool rfidCheckNewCard() {
  return rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial();
}

int rfidIdentifyModel() {
  for (int i = 0; i < numModels; i++) {
    if (rfidMatchUID(models[i].uid)) {
      Serial.printf("Model found: %s (ID %d)\n", models[i].method, models[i].model_id);
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();
      return models[i].model_id;
    }
  }
  Serial.println("Unknown RFID tag");
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  return -1;
}

bool rfidMatchUID(byte targetUID[4]) {
  for (int i = 0; i < 4; i++) {
    if (rfid.uid.uidByte[i] != targetUID[i]) {
      return false;
    }
  }
  return true;
}
```

### 3.3 Proximity Handler (HC-SR04)

```cpp
// proximity_handler.h / proximity_handler.cpp

#include "config.h"

volatile unsigned long pulseStart = 0;
volatile unsigned long pulseEnd = 0;

void proximityInit() {
  pinMode(HC_TRIG_PIN, OUTPUT);
  pinMode(HC_ECHO_PIN, INPUT);
  digitalWrite(HC_TRIG_PIN, LOW);
}

float measureDistance() {
  // Send 10 µs trigger pulse
  digitalWrite(HC_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(HC_TRIG_PIN, LOW);

  // Wait for echo pulse
  long timeout = micros() + 30000;  // 30ms timeout
  while (digitalRead(HC_ECHO_PIN) == LOW && micros() < timeout) {}

  unsigned long pulseStart = micros();

  while (digitalRead(HC_ECHO_PIN) == HIGH && micros() < timeout) {}

  unsigned long pulseEnd = micros();
  unsigned long pulseDuration = pulseEnd - pulseStart;

  // Convert time (µs) to distance (cm)
  // Sound speed = 343 m/s; round trip = 2x
  // distance = (343 m/s * 1e-6 s/µs * duration) / 2 * 100
  //          ≈ duration / 58
  float distanceCM = pulseDuration / 58.0;

  return distanceCM;
}
```

### 3.4 OSC Sender (WiFi communication)

```cpp
// osc_sender.h / osc_sender.cpp

#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOSC.h>

const char* SSID = SECRET_SSID;
const char* PASSWORD = SECRET_PASSWORD;
const char* TD_IP = SECRET_TD_IP;
const int   TD_PORT = 9000;

WiFiUDP udp;

void wifiConnect() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.print("WiFi connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed!");
  }
}

void wifiReconnect() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reconnecting WiFi...");
    WiFi.disconnect();
    delay(500);
    WiFi.reconnect();
  }
}

void sendProximityUpdate(float distanceCM, bool userLeaningIn) {
  OscWiFi.send(TD_IP, TD_PORT, "/proximity/distance", distanceCM);
  OscWiFi.send(TD_IP, TD_PORT, "/proximity/lean_in", userLeaningIn ? 1 : 0);
}

void sendRFIDUpdate(int modelID) {
  OscWiFi.send(TD_IP, TD_PORT, "/rfid/model", modelID);
}

void sendHeartbeat() {
  static unsigned long lastHB = 0;
  if (millis() - lastHB > 5000) {
    OscWiFi.send(TD_IP, TD_PORT, "/esp32/heartbeat", 1);
    lastHB = millis();
  }
}
```

### 3.5 Secrets Template

```cpp
// secrets.h.example
// Copy to secrets.h and fill in your values (secrets.h is .gitignored)

#define SECRET_SSID         "YOUR_WIFI_NETWORK"
#define SECRET_PASSWORD     "YOUR_WIFI_PASSWORD"
#define SECRET_TD_IP        "192.168.X.Y"  // Your laptop IP
```

---

## 4. OSC Protocol Specification

All messages are sent **from ESP32 → TouchDesigner** over WiFi UDP on port **9000**.

### 4.1 Message Format

```
/proximity/distance       <float>  distance in cm (0–400)
/proximity/lean_in        <int>    1 if distance < 30cm, else 0
/rfid/model              <int>    1, 2, or 3 (model identifier)
/esp32/heartbeat         <int>    1 (sent every 5 seconds, for health check)
/esp32/error             <string> error message (if something fails)
```

### 4.2 Example OSC Sequence

```
t=0s:    [User walks toward table]
         /proximity/distance  150.2
         /proximity/lean_in   0

t=1s:    [User leans in to place model]
         /proximity/distance   28.5
         /proximity/lean_in    1

t=1.5s:  [Model placed, RFID detected]
         /rfid/model           2
         /proximity/distance   45.0
         /proximity/lean_in    0

t=6s:    [Heartbeat]
         /esp32/heartbeat      1
```

### 4.3 TouchDesigner Integration

In **TouchDesigner**, receive these messages with an **OSC In CHOP**:

```
OSC In CHOP
  Active:       On
  Network Port: 9000
  
Outputs:
  - /proximity/distance  → float channel [0, 400]
  - /proximity/lean_in   → int channel {0, 1}
  - /rfid/model          → int channel {1, 2, 3}
```

Then route to your FSM logic:
- If `/rfid/model` changes → transition state (IDLE → GUIDING)
- If `/proximity/lean_in` = 1 → zoom/highlight active piece
- Monitor `/esp32/heartbeat` for connectivity (should arrive every 5s)

---

## 5. Calibration & Setup

### 5.1 Scanning RFID Tags (First Time)

1. **Load test sketch:** Upload `firmware/test_rfid_scan.ino` to ESP32
2. **Open Serial Monitor** (115200 baud)
3. **Present each RFID tag** to the reader in sequence
4. **Copy the 4-byte UID** printed for each tag
5. **Update `models[]` array** in `rfid_handler.cpp` with the actual UIDs
6. **Re-upload main firmware**

Example Serial output:
```
Card UID: 12:34:56:78
Card UID: AA:BB:CC:DD
Card UID: 11:22:33:44
```

### 5.2 Proximity Threshold Tuning

1. **Mount HC-SR04** on table edge or overhead rig (facing user)
2. **Upload firmware** with **Serial logging enabled**
3. **Open Serial Monitor** to see real-time distance values
4. **Stand at table** and note distance at:
   - Arm's length (normal placement) → ~60–80cm
   - Leaning in (face close to table) → ~20–40cm
5. **Set `PROXIMITY_THRESHOLD_CM`** to a value in the middle (e.g., 30cm)
6. **Test a few times** to confirm detection is smooth (not flickering on/off)

### 5.3 WiFi Connection Check

1. **Open Serial Monitor** and look for:
   ```
   Connecting to WiFi: [SSID]
   WiFi connected. IP: 192.168.X.Y
   ```
2. **If "WiFi connection failed!"** appears:
   - Check SSID/password in `secrets.h`
   - Verify 2.4 GHz WiFi (not 5 GHz; ESP32 prefers 2.4)
   - Check that your laptop and ESP32 are on same network

3. **If connection drops during demo:**
   - Firmware includes auto-reconnect; should recover within 10s
   - Consider adding a battery to eliminate USB cable interference

### 5.4 Full Integration Test

1. **Start TouchDesigner** with OSC In CHOP listening on port 9000
2. **Power up ESP32** (USB or battery)
3. **Verify heartbeat messages** arrive every 5 seconds
4. **Present RFID tag** → `/rfid/model` message should appear in OSC In CHOP
5. **Lean toward HC-SR04** → `/proximity/lean_in` should toggle to 1
6. **Check Serial Monitor** for any error messages

---

## 6. PlatformIO Configuration

```ini
# platformio.ini

[env:esp32]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino
monitor_speed = 115200
monitor_port = COM3  ; adjust to your USB port
upload_port = COM3

lib_deps =
    MFRC522
    ArduinoOSC

build_flags =
    -DCORE_DEBUG_LEVEL=4  ; verbose logging
    -DBOARD_HAS_PSRAM
```

---

## 7. Troubleshooting & Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **RFID tag not detected** | Reader not initialized / wrong pins | Check SPI wiring; verify pin #s in `config.h`; test with `test_rfid_scan.ino` |
| **RFID tag detected but wrong model ID** | UID mismatch in `models[]` array | Re-scan tag UIDs with test sketch; update array |
| **WiFi connects but OSC not received** | Wrong laptop IP in `secrets.h` / OSC port mismatch | Run `ipconfig` on Windows to get laptop IP; verify TD OSC In CHOP port = 9000 |
| **WiFi drops frequently** | Poor signal / 5GHz interference | Move router closer; check 2.4GHz only; add ferrite bead on USB cable |
| **HC-SR04 measures wildly (0cm or 500cm)** | Electrical noise / wrong pin assignment | Check wiring; add 100nF cap across TRIG/GND; reduce cable length |
| **HC-SR04 doesn't detect user at all** | Sensor mounted wrong / threshold too low | Verify HC_ECHO_PIN rising edge is captured; increase `PROXIMITY_THRESHOLD_CM` |
| **ESP32 crashes after 10 seconds** | Stack overflow / memory leak | Reduce OSC send rate; add `delay()` in main loop; check for circular string operations |
| **Serial Monitor shows garbage** | Baud rate mismatch | Set Serial Monitor to **115200** (not 9600) |

---

## 8. Assembly, Mounting & Cable Management

### 8.1 Table Integration

- **Pedestal location:** Underneath or beside the main table (out of sight of camera)
- **Proximity sensor:** Mounted horizontally on table edge, ~20cm from where user stands
- **RFID reader:** Mounted vertically under the table surface (reads tags on model bases from below)
- **ESP32 + antenna:** Inside 3D-printed enclosure near reader to keep SPI cable short

### 8.2 Cable Routing

1. **RFID wires (SPI):** ~20cm from reader to ESP32; use shielded cable if available
2. **HC-SR04 wires:** ~30cm from sensor to ESP32; keep ECHO and TRIG twisted
3. **USB power:** Routed along table leg; tape down to prevent tripping
4. **WiFi:** No cable; ensure antenna is vertical for best signal

### 8.3 Enclosure (Optional 3D Print)

Design a box with:
- Hole for USB micro-B connector
- Holes for RFID reader SPI wires
- Holes for HC-SR04 connector
- Mounting bracket for overhead rig or table edge

```
+---+---+
| E | H |  E = ESP32 PCB
| S | C |  H = HC-SR04 breakout
| P |   |
| 3 +---+
| 2 | R |  R = RFID reader
|   | F |
+---+ I +
    | D |
    +---+
```

---

## 9. QA / Demo Checklist

Before final presentation:

- [ ] **RFID:** All 3 tags read correctly; right model ID sent for each
- [ ] **Proximity:** Distance values update smoothly; lean-in toggle works at 30cm
- [ ] **WiFi:** Heartbeat messages arrive every 5s; no reconnects during 10-minute demo
- [ ] **Serial/Logging:** No crash messages; CPU load stable
- [ ] **TouchDesigner:** OSC messages appear in monitor; FSM state changes correctly on tag read
- [ ] **Power:** USB cable secure; no data corruption if cable briefly loose
- [ ] **Cables:** No dangling wires; neatly routed; no interference with camera/projector
- [ ] **Enclosure:** Neat appearance; all labels visible; mounting secure
- [ ] **Backup:** Firmware .hex backed up; secrets.h with correct credentials saved safely
- [ ] **Documentation:** UIDs written in `firmware/docs/UIDs.txt`; calibration values logged

---

## 10. Post-Demo Analysis & Logging

To aid debugging after the demo:

- **Serial logging** is always enabled; redirect to file:
  ```
  Serial.println("RFID_READ,timestamp," + String(modelID));
  Serial.println("PROX_LEAN," + String(distance) + "," + String(userLeaningIn));
  ```

- **Manual event log:**
  - Note times when tags were read
  - Note any WiFi disconnections
  - Note any sensor false positives

- **Data playback:** If needed, replay OSC messages from a log file to test TouchDesigner FSM in isolation

---

## 11. Future Enhancements

- **Multi-sensor:** Add temperature, humidity, or capacitive touch to model bases
- **BLE beacon:** Alternative to OSC for lower-power operation
- **MQTT:** Replace OSC with MQTT for better reliability (requires broker)
- **Onboard SD card:** Log all sensor data to SD for detailed analysis
- **LED feedback:** RGB LED on enclosure to show WiFi/RFID status
- **Audio cue:** Piezo buzzer to confirm tag read or proximity event

---

## 12. Repository Structure

Final firmware directory:

```
firmware/
├── README.md                         # General overview
├── ESP32-SENSOR-SYSTEM.md           # This file (comprehensive spec)
├── platformio.ini                    # Build config
├── src/
│   ├── main.cpp                      # Main loop
│   ├── rfid_handler.cpp
│   ├── rfid_handler.h
│   ├── proximity_handler.cpp
│   ├── proximity_handler.h
│   ├── osc_sender.cpp
│   ├── osc_sender.h
│   ├── config.h
│   └── secrets.h.example
├── test/
│   └── test_rfid_scan.ino            # Utility: scan tag UIDs
└── docs/
    ├── CALIBRATION.md                # Detailed tuning steps
    ├── UIDs.txt                      # Scanned tag mapping
    └── WIRING.png                    # High-res wiring diagram
```

---

**Author:** ESP32 / Sensor + Sound + QA / Ops  
**Reviewed by:** System Architecture Lead (integration sign-off)  
**Status:** Draft → Ready for fabrication & firmware coding

