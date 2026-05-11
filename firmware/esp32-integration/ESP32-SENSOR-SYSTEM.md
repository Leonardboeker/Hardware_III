# ESP32 Sensor Integration System

**Role:** Hardware interface layer — proximity detection, RFID model identification, and WiFi communication to TouchDesigner.

**Owner:** ESP32 / Sensor + Sound + QA / Ops

**Last Updated:** 2026-05-04

---

## Overview

The ESP32-WROOM-32 microcontroller sits at the junction between the physical interaction layer and the software FSM. Its job is to:

1. **Trigger user engagement** via proximity sensor (HC-SR04 ultrasonic or PIR) → initiates IDLE → ONBOARDING transition when user approaches
2. **Detect user presence & absence** → maintains session active while user is present; triggers timeout/reset if user leaves for >30s
3. **Identify construction method** via RFID reader (MFRC522) → tells TouchDesigner which model was placed on table
4. **Stream sensor data** over WiFi/OSC to TouchDesigner at 50–100 Hz
5. **Coordinate sound cues** (via audio layer integration point) on key state transitions
6. **Log all events** locally for debugging and post-demo analysis

This document specifies the hardware, firmware architecture, OSC protocol, calibration procedure, QA checklist, and demo operation runbook.

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
  │  ├─ If distance < PROXIMITY_THRESHOLD → userPresent = true
  │  │  └─ Send /proximity/presence 1 → triggers IDLE → ONBOARDING
  │  └─ If distance > ABSENCE_TIMEOUT_CM for >30s → userPresent = false
  │     └─ Send /proximity/presence 0 → triggers timeout/reset
  │
  ├─ Check for new RFID tag
  │  └─ If found: match against model table → send /rfid/model + /rfid/method
  │
  ├─ Track user session (proximity timer)
  │  └─ If no proximity for >30s while system active → suggest timeout
  │
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
#define PROXIMITY_POLL_INTERVAL       20    // Read HC-SR04 every 20ms
#define RFID_DEBOUNCE_TIME           1000   // Ignore same tag for 1s
#define PROXIMITY_THRESHOLD_CM         30    // User "present" = closer than 30cm
#define USER_ABSENCE_TIMEOUT_MS    30000    // 30s of no proximity → trigger reset/idle
#define ABSENCE_CHECK_INTERVAL      5000    // Check timeout every 5s

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
/proximity/presence       <int>    1 if user present (< 30cm), 0 if absent (>30s no detection)
/rfid/model              <int>    1, 2, or 3 (model identifier)
/rfid/method             <string> "masonry", "3d_print", or "prefab" (human-readable)
/esp32/heartbeat         <int>    1 (sent every 5 seconds, for health check)
/esp32/state_trigger     <string> "user_entered", "user_left", "model_placed" (FSM events)
/esp32/error             <string> error message (if something fails)
```

### 4.2 FSM State Triggering via Proximity

The proximity sensor drives the main FSM transitions:

```
No user detected → /proximity/presence = 0
↓
(IDLE state, ambient display)
↓
User approaches (distance < 30cm) → /proximity/presence = 1 + /esp32/state_trigger "user_entered"
↓
(FSM transitions: IDLE → ONBOARDING)
↓
User places model → /rfid/model arrives
↓
(FSM processes placement and validates)
↓
User leaves (no proximity for 30s) → /proximity/presence = 0 + /esp32/state_trigger "user_left"
↓
(FSM may trigger timeout/reset if mid-workflow)
```

### 4.3 Example OSC Sequence

```
t=0s:    [System in IDLE, no user]
         /proximity/presence   0
         /esp32/heartbeat      1

t=15s:   [User walks toward table, approaches]
         /proximity/distance   80.5
         /proximity/presence   1
         /esp32/state_trigger  "user_entered"

t=16s:   [User leans in to place model]
         /proximity/distance   25.0
         /esp32/heartbeat      1

t=17s:   [Model placed, RFID detected]
         /rfid/model           2
         /rfid/method          "3d_print"
         /proximity/distance   45.0

t=25s:   [User continues, still present]
         /proximity/presence   1
         /esp32/heartbeat      1

t=60s:   [User walks away, no proximity for >30s]
         /proximity/presence   0
         /esp32/state_trigger  "user_left"
```

### 4.4 TouchDesigner Integration

In **TouchDesigner**, receive these messages with an **OSC In CHOP**:

```
OSC In CHOP
  Active:       On
  Network Port: 9000
  
Key inputs:
  - /proximity/presence    → int {0, 1} — drives IDLE ↔ ONBOARDING transition
  - /proximity/distance    → float [0, 400] — optional viz feedback (zoom on lean-in)
  - /rfid/model            → int {1, 2, 3} — identifies model for state validation
  - /esp32/state_trigger   → string — logs FSM events
  - /esp32/heartbeat       → int — monitors ESP32 connectivity
```

**FSM integration logic:**

```python
# Pseudocode in TouchDesigner

def onProximityChange(presence):
    if presence == 1 and currentState == "IDLE":
        triggerStateChange("ONBOARDING")
        playSound("user_entered")
    elif presence == 0 and currentState != "IDLE":
        if timeInState > 30s:
            triggerStateChange("RESET")
            playSound("timeout")

def onRFIDDetected(modelID):
    if currentState == "ONBOARDING":
        triggerStateChange("VALIDATING")
        playSound("model_accepted")
```

---

## 5. Sound Cueing System

The ESP32 does not generate audio directly. Instead, it **signals key events** via `/esp32/state_trigger` OSC messages, which TouchDesigner or an external audio layer maps to sound cues.

### 5.1 Sound Events & Triggers

| Event | OSC Message | Recommended Sound | Purpose |
|-------|-------------|-------------------|---------|
| User enters | `/esp32/state_trigger` = `"user_entered"` | Bright tone / welcome chime | Signal attention → system active |
| Piece accepted | `/rfid/model` arrives + valid | Ascending tone / success ding | Confirm model identification |
| Validation starts | FSM → VALIDATING | Pulsing / scanning tone | Feedback that system is checking |
| Validation complete | FSM → ANALYSING | Resolved tone | Placement confirmed |
| Error / rejection | FSM → ERROR | Low tone / buzz | Piece placement wrong → try again |
| Confirmation | FSM → RESULT | Celebratory chime | Data calculated, ready for next |
| User leaves | `/esp32/state_trigger` = `"user_left"` | Fade-out tone | Session ending |
| Timeout / reset | FSM → IDLE (after timeout) | Reset tone | Return to start state |

### 5.2 Integration Points

**Option A: TouchDesigner audio layer (preferred)**

```python
# In TouchDesigner CHOP Execute DAT

def onStateChange(newState):
    if newState == "VALIDATING":
        op('audio_out').play("validation_loop.wav")
    elif newState == "RESULT":
        op('audio_out').play("success_chord.wav")
```

**Option B: External audio system**

- ESP32 sends `/esp32/state_trigger` → external audio controller listens
- Audio controller maps string → WAV file → speaker output
- Decouples firmware from audio; allows live sound design

**Option C: Piezo buzzer on ESP32 (future)**

- Add 5V piezo to GPIO 32
- Firmware generates tones directly for simple beeps
- Good for quick feedback; limited expressiveness

### 5.3 Audio Design Recommendations

- **Response time:** Sound should play within 200ms of trigger (no lag)
- **Level:** Mix at -18dB so speech/music clarity is maintained
- **Variety:** 5–8 distinct sounds; avoid repetition fatigue
- **Loop length:** Keep ambient loops <10s to prevent tediousness

## 6. Calibration & Setup

### 6.1 Scanning RFID Tags (First Time)

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

### 6.2 Proximity Threshold Tuning

1. **Mount HC-SR04** on table edge or overhead rig (facing user)
2. **Upload firmware** with **Serial logging enabled**
3. **Open Serial Monitor** to see real-time distance values
4. **Stand at table** and note distance at:
   - Arm's length (normal viewing) → ~100–150cm
   - Standing upright at table → ~60–80cm
   - Leaning in (face close to table) → ~20–40cm
   - User entering trigger zone → <30cm
5. **Set `PROXIMITY_THRESHOLD_CM`** to 30cm (triggers ONBOARDING)
6. **Set `USER_ABSENCE_TIMEOUT_MS`** to 30000 (30 seconds)
7. **Test a few times** to confirm detection is smooth (not flickering on/off)

### 6.3 User Absence Timeout Tuning

1. **Demo the workflow** with 2+ people taking turns
2. **Observe:** How long does a user typically spend at the table per interaction?
3. **If timeout too aggressive** (resets mid-workflow): increase `USER_ABSENCE_TIMEOUT_MS`
4. **If timeout too lenient** (doesn't reset when user leaves): decrease timeout
5. **Recommended:** 30–45 seconds for hands-on model placement

### 6.4 WiFi Connection Check

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

### 6.5 Full Integration Test

1. **Start TouchDesigner** with OSC In CHOP listening on port 9000
2. **Power up ESP32** (USB or battery)
3. **Verify heartbeat messages** arrive every 5 seconds
4. **Approach sensor** with no object → `/proximity/presence` should toggle to 1
5. **Verify `/esp32/state_trigger "user_entered"`** appears in TouchDesigner
6. **Present RFID tag** → `/rfid/model` message should appear in OSC In CHOP
7. **Walk away** from sensor for 30+ seconds → `/proximity/presence` should toggle to 0
8. **Check Serial Monitor** for any error messages

---

## 7. PlatformIO Configuration

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

## 8. Troubleshooting & Common Issues

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

## 9. Assembly, Mounting & Cable Management

### 9.1 Table Integration

- **Pedestal location:** Underneath or beside the main table (out of sight of camera)
- **Proximity sensor:** Mounted horizontally on table edge, ~20cm from where user stands
- **RFID reader:** Mounted vertically under the table surface (reads tags on model bases from below)
- **ESP32 + antenna:** Inside 3D-printed enclosure near reader to keep SPI cable short

### 9.2 Cable Routing

1. **RFID wires (SPI):** ~20cm from reader to ESP32; use shielded cable if available
2. **HC-SR04 wires:** ~30cm from sensor to ESP32; keep ECHO and TRIG twisted
3. **USB power:** Routed along table leg; tape down to prevent tripping
4. **WiFi:** No cable; ensure antenna is vertical for best signal

### 9.3 Enclosure (Optional 3D Print)

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

## 10. QA Checklist & Demo Preparation

Before final presentation, run through these checks systematically.

### 10.1 Hardware & Wiring QA

- [ ] **RFID reader** powers up; antenna LED (if present) blinks
- [ ] **HC-SR04** powers up; no flashing lights (indicates initialization)
- [ ] **ESP32** powers up; Serial Monitor shows "Setup complete"
- [ ] **SPI wiring:** All 6 MFRC522 pins connected correctly (check with multimeter)
- [ ] **GPIO wiring:** HC-SR04 TRIG & ECHO on correct pins (GPIO 4 & 2)
- [ ] **Decoupling caps:** 100nF caps soldered near MFRC522 and ESP32 power pins
- [ ] **No cold solder joints** on any connections

### 10.2 Firmware & Software QA

- [ ] **RFID:** All 3 tags read correctly; UIDs match `models[]` array
- [ ] **RFID:** Correct model ID sent for each tag (`/rfid/model` = 1, 2, or 3)
- [ ] **Proximity:** Distance values update smoothly (no jumps >10cm between reads)
- [ ] **Proximity:** `/proximity/presence` toggles correctly at ~30cm threshold
- [ ] **WiFi:** Connects on startup within 10 seconds
- [ ] **WiFi:** Heartbeat messages arrive every 5 seconds (no gaps >10s)
- [ ] **WiFi:** No disconnects during 10-minute continuous operation
- [ ] **OSC:** All messages reach TouchDesigner (verify in OSC In CHOP)
- [ ] **Serial logging:** No crash messages; CPU load stays <80%

### 10.3 Integration QA

- [ ] **TouchDesigner FSM** state changes when RFID tag detected
- [ ] **Proximity presence** transitions trigger expected visual/audio cues
- [ ] **User absence timeout** resets system after 30s with no proximity
- [ ] **State transitions** are smooth (no lag >500ms)
- [ ] **Error recovery:** If WiFi drops, system reconnects and resumes

### 10.4 Physical Assembly QA

- [ ] **Power cable:** Routed safely; secured with tape/velcro
- [ ] **Sensor cables:** All crimped/soldered connections solid; no loose wires
- [ ] **Enclosure:** Mounted securely; no vibration when table is tapped
- [ ] **Proximity sensor aim:** Points directly at user standing zone (no obstructions)
- [ ] **RFID reader:** Mounted under table, flush with surface for easy tag detection
- [ ] **Antenna:** Vertical orientation for best WiFi range

### 10.5 Backup & Documentation QA

- [ ] **Firmware backup:** `.hex` file saved to external drive
- [ ] **secrets.h:** Credentials saved in secure location (not in git)
- [ ] **RFID UIDs:** Written in `firmware/docs/UIDs.txt` (tag mapping)
- [ ] **Calibration values:** Logged in `firmware/docs/CALIBRATION.md`
- [ ] **Wiring diagram:** Photo or high-res image saved
- [ ] **Known issues:** Any workarounds documented

---

## 11. Demo Operation Runbook

This is your **step-by-step setup, run, and shutdown checklist** for demo day.

### 11.1 Pre-Demo Setup (30 minutes before)

1. **Power sequence:**
   - Connect ESP32 USB power cable to laptop
   - Wait 5s for Serial Monitor to show "Setup complete"
   - Verify WiFi connection message in Serial Monitor
   - Confirm heartbeat messages in TouchDesigner OSC In CHOP (should see `/esp32/heartbeat` every 5s)

2. **Hardware checks:**
   - Press each RFID tag to reader; verify `/rfid/model` arrives in OSC
   - Slowly walk toward proximity sensor; verify `/proximity/presence` transitions from 0 → 1
   - Walk away; verify presence transitions back to 0 after 30s

3. **TouchDesigner startup:**
   - Open TD project
   - Verify OSC In CHOP is listening on port 9000
   - Trigger a manual state change (e.g., keystroke) to confirm FSM is responsive
   - Test audio cues (if applicable)

4. **Projection setup:**
   - Projector powers on; brightness at 70–80%
   - Calibrate homography if needed (should persist from last session)
   - Run 1-minute warmup loop to ensure no overheating

### 11.2 During Demo (hands-off)

- **Monitor Serial Monitor** for errors (window on side of screen)
- **Watch OSC In CHOP** for heartbeat continuity (if heartbeat stops → WiFi dropped)
- **Listen for audio cues** that match expected state transitions
- **Have a phone nearby** with a note of your laptop IP (in case USB cable fails; can switch to battery + pre-configured IP)

### 11.3 Demo Fallback Plan

**If WiFi drops mid-demo:**
- Firmware auto-reconnects within 10s; system should resume
- If >20s without heartbeat: unplug USB, wait 3s, replug (hard reset)

**If RFID tag not detected:**
- Tag may be too far from reader; ensure tag is within 2cm and flush against table
- Try presenting a different tag to verify reader is working
- If all tags fail: restart ESP32 (unplug/replug USB)

**If proximity sensor not responding:**
- User may be outside detection zone; adjust walking distance
- If manual test shows no distance readings: check GPIO wiring (ECHO pin especially)
- Quick fix: reload firmware via Arduino IDE

**If audio cues not playing:**
- Not critical; system continues with visual feedback
- Check TouchDesigner audio output device is active

### 11.4 Post-Demo Shutdown (5 minutes after)

1. **Save logs:**
   - Copy Serial Monitor output to a text file
   - Note any errors, WiFi drops, or sensor glitches
   - Timestamp the log (helps with post-demo analysis)

2. **Power down:**
   - Stop TouchDesigner (Ctrl+Q)
   - Unplug ESP32 USB power
   - Power down projector
   - Close all applications

3. **Post-demo review:**
   - Did all RFID tags read correctly?
   - Did proximity sensor trigger expected state transitions?
   - Did WiFi remain stable for entire demo?
   - Any audio/visual mismatches?
   - Document any issues in `.planning/REVIEW-S1.md` or similar

---

## 12. Post-Demo Analysis & Logging

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

## 13. Future Enhancements

- **Multi-sensor:** Add temperature, humidity, or capacitive touch to model bases
- **BLE beacon:** Alternative to OSC for lower-power operation
- **MQTT:** Replace OSC with MQTT for better reliability (requires broker)
- **Onboard SD card:** Log all sensor data to SD for detailed analysis
- **LED feedback:** RGB LED on enclosure to show WiFi/RFID status
- **Audio cue:** Piezo buzzer to confirm tag read or proximity event
- **Gesture recognition:** Add accelerometer to detect "lean in" gestures beyond distance
- **Multi-model support:** Handle >3 construction methods via additional RFID tags

---

## 14. Repository Structure

Final firmware directory structure:

```
firmware/
├── README.md                                  # General overview
├── esp32-integration/
│   ├── ESP32-SENSOR-SYSTEM.md                # This file (comprehensive spec)
│   ├── platformio.ini                        # PlatformIO build config
│   ├── src/
│   │   ├── main.cpp                          # Main loop + setup
│   │   ├── rfid_handler.cpp
│   │   ├── rfid_handler.h
│   │   ├── proximity_handler.cpp
│   │   ├── proximity_handler.h
│   │   ├── osc_sender.cpp
│   │   ├── osc_sender.h
│   │   ├── config.h                          # Pin definitions, constants
│   │   └── secrets.h.example                 # WiFi credentials template
│   ├── test/
│   │   └── test_rfid_scan.ino                # Utility: scan tag UIDs
│   └── docs/
│       ├── CALIBRATION.md                    # Detailed tuning steps (post-calibration)
│       ├── UIDs.txt                          # Scanned RFID tag mapping
│       ├── WIRING.md                         # Full wiring schematic + photos
│       └── AUDIO_CUE_LIST.md                 # Sound events + file references
├── [legacy/ or old/]                         # Previous iterations (if any)
└── .gitignore                                # Exclude: secrets.h, *.hex, build/
```

---

**Author:** ESP32 / Sensor + Sound + QA / Ops  
**Reviewed by:** System Architecture Lead (integration sign-off)  
**Last Updated:** 2026-05-04  
**Status:** Comprehensive spec with demo runbook & QA checklist — Ready for firmware implementation & demo day operation

