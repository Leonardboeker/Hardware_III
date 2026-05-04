# Technical Specification: Hardware III Installation

**Stack:** TouchDesigner + ESP32 (WiFi/OSC) + RFID + ArUco + Projector
**Last updated:** 2026-04-17

---

## 1. Hardware List

| Component | Spec | Quantity |
|-----------|------|----------|
| Laptop | Windows/Mac, dedicated GPU preferred | 1 |
| Video projector | Short-throw, min 3000 lumen | 1 |
| USB webcam | Wide angle, min 1080p, fixed focus | 1 |
| ESP32 dev board | ESP32-WROOM-32 | 1 |
| RFID reader | MFRC522 (13.56MHz) | 1 |
| RFID tags | MIFARE Classic 1K, coin type | 3 |
| Overhead mount | Camera arm or ceiling rig | 1 |
| USB cable | ESP32 → laptop (power only, comms via WiFi) | 1 |

**Estimated extra cost: ~25–40€**

---

## 2. ArUco Markers

### What is ArUco
ArUco is a library of square fiducial markers. Each has a unique binary pattern. OpenCV detects them in a camera feed and returns: which marker ID, where on the image (4 corners), and orientation.

### The 12 markers

| Marker | IDs | Count | Purpose |
|--------|-----|-------|---------|
| Floor plan tiles | 0–9 | 10 | User arranges to define building footprint |
| Story level selector | 10 | 1 | User places to set number of floors |
| Material selector | 11 | 1 | User places to select material variant |

### Generating the markers

Install: `pip install opencv-contrib-python`

```python
import cv2
import cv2.aruco as aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

for marker_id in range(12):
    marker_image = aruco.generateImageMarker(dictionary, marker_id, 300)
    cv2.imwrite(f"marker_{marker_id:02d}.png", marker_image)
    print(f"Saved marker_{marker_id:02d}.png")
```

Run: `python generate_markers.py` → outputs 12 PNG files.

### Printing ArUco with the Bambu X1C (in-place multi-color)

1. Design piece in Rhino — add a flat recessed square on top surface (depth: 0.4mm, size: 40×40mm)
2. Import STL into **Bambu Studio**
3. Right-click model → **Add Decal** → select your marker PNG
4. Align decal to top face, scale to fit recessed area
5. Assign: base filament = white PLA, decal layer = black PLA (via AMS)
6. Print — X1C pauses and swaps filament automatically for the marker layer

**Result:** Permanent, flush ArUco marker embedded in the print. No paper, no glue.

**Print settings:**
- Layer height: 0.2mm
- Recess depth: 0.4mm (2 layers)
- Use **matte** filament — glossy reflects projector light and breaks detection

---

## 3. RFID + ESP32

### Wiring: MFRC522 → ESP32

| MFRC522 pin | ESP32 pin |
|-------------|-----------|
| SDA (SS) | GPIO 5 |
| SCK | GPIO 18 |
| MOSI | GPIO 23 |
| MISO | GPIO 19 |
| GND | GND |
| RST | GPIO 27 |
| 3.3V | 3.3V |

### Embedding RFID tag in 3D model
- Design a pocket (25×25×2mm) in the base of each model
- Drop in RFID coin tag, seal with thin printed lid or resin
- Keep tag within 3cm of reader — MFRC522 read range is ~3cm

---

## 4. WiFi Communication: ESP32 → TouchDesigner via OSC

### Why OSC over WiFi
- No USB cable between ESP32 and laptop
- TouchDesigner has native OSC In CHOP — no extra setup
- Lightweight messages: `/rfid/model 2`

### Arduino Libraries (install via Arduino Library Manager)
- `MFRC522` by GithubCommunity
- `ArduinoOSC` by hideakitai
- `WiFi` — built into ESP32 board package

### ESP32 Firmware

```cpp
#include <WiFi.h>
#include <ArduinoOSC.h>
#include <MFRC522.h>
#include <SPI.h>

const char* ssid     = "YOUR_NETWORK";
const char* password = "YOUR_PASSWORD";
const char* TD_IP    = "192.168.1.100";  // your laptop IP
const int   TD_PORT  = 9000;

#define SS_PIN  5
#define RST_PIN 27
MFRC522 rfid(SS_PIN, RST_PIN);

// Fill UIDs after scanning each tag with a test sketch
struct RFIDModel {
  byte uid[4];
  int  model_id;
  const char* name;
};

RFIDModel models[] = {
  {{0xA1, 0xB2, 0xC3, 0xD4}, 1, "masonry"},
  {{0xE5, 0xF6, 0x07, 0x18}, 2, "3d_print"},
  {{0x29, 0x3A, 0x4B, 0x5C}, 3, "prefab"}
};

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
}

void loop() {
  OscWiFi.update();

  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) return;

  for (auto& m : models) {
    if (memcmp(rfid.uid.uidByte, m.uid, 4) == 0) {
      Serial.printf("Model: %s (ID %d)\n", m.name, m.model_id);
      OscWiFi.send(TD_IP, TD_PORT, "/rfid/model", m.model_id);
      OscWiFi.send(TD_IP, TD_PORT, "/rfid/name",  m.name);
      break;
    }
  }

  rfid.PICC_HaltA();
  delay(1000);  // debounce
}
```

> **First run:** Use a UID scan sketch to read the actual UIDs of your 3 tags via Serial Monitor, then fill in the `models[]` array above.

---

## 5. TouchDesigner Pipeline

### Node network overview

```
[Video Device In TOP]   ← webcam
        ↓
[Script DAT]            ← OpenCV ArUco detection (Python, runs every frame)
        ↓
[Table DAT: aruco_data] ← detected marker IDs + normalized positions
        ↓
[CHOP Execute DAT]      ← FSM logic
        ↑
[OSC In CHOP]           ← receives /rfid/model from ESP32
        ↓
[Select CHOP]           ← active model ID
        ↓
[Render / Composite TOP] ← builds projection content per state
        ↓
[Homography TOP]         ← warps content to match table surface
        ↓
[Window COMP]            ← fullscreen output to projector
```

### A. Camera input
```
Video Device In TOP
  Device: your webcam
  Resolution: 1920×1080
  Flip horizontal if needed
```

### B. ArUco detection (Script DAT — Frame Start callback)

```python
import cv2
import cv2.aruco as aruco
import numpy as np

def onFrameStart(dat):
    cam_top = op('videodevicein1')
    frame = cam_top.numpyArray()[:, :, :3]
    frame = (frame * 255).astype(np.uint8)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    params = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, params)
    corners, ids, _ = detector.detectMarkers(frame_bgr)

    table = op('aruco_data')
    table.clear()
    table.appendRow(['id', 'cx', 'cy'])

    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            c = corners[i][0]
            cx = float(np.mean(c[:, 0])) / frame_bgr.shape[1]
            cy = float(np.mean(c[:, 1])) / frame_bgr.shape[0]
            table.appendRow([int(marker_id), round(cx, 4), round(cy, 4)])
```

### C. OSC receiver (RFID input)
```
OSC In CHOP
  Network Port: 9000
  Active: On
→ Select CHOP filtering "/rfid/model"
→ value (1, 2, or 3) feeds into FSM
```

### D. Projection mapping (Homography calibration)
```
Homography TOP
  Input: your rendered content TOP
  Do this once:
    1. Project a white square fullscreen
    2. Physically measure the 4 table corners
    3. Drag Homography TOP corner pins until square aligns with table edges
  Save corner values — they persist between sessions
```

### E. FSM state machine (CHOP Execute DAT)

States: `IDLE` → `PRESENTING` → `DETAIL` → `COMPARISON`

```python
def onValueChange(channel, sampleIndex, val, prev):
    state_table = op('fsm_state')
    model_id = int(val)

    if model_id == 0:
        state_table['state', 1] = 'IDLE'
    else:
        rfid_count = int(op('active_models')['count', 1])
        if rfid_count >= 2:
            state_table['state', 1] = 'COMPARISON'
        else:
            state_table['state', 1] = 'PRESENTING'
            state_table['active_model', 1] = model_id
```

---

## 6. Software & Libraries

| Tool | Version | Purpose |
|------|---------|---------|
| **TouchDesigner** | 2023.11+ (free non-commercial) | Runtime: CV, projection mapping, FSM, output |
| **OpenCV** (Python) | `opencv-contrib-python 4.8+` | ArUco detection inside TD |
| **Arduino IDE** | 2.x | ESP32 firmware |
| **MFRC522 library** | Arduino Library Manager | RFID read |
| **ArduinoOSC** by hideakitai | Arduino Library Manager | WiFi OSC send from ESP32 |
| **ESP32 board package** | Arduino Board Manager | ESP32 support |
| **Python 3.11** | System | TD scripting + marker generation |
| **Rhino + Grasshopper** | Course version | LCA math, geometry design |

---

## 7. Setup Order (day of installation)

1. Mount webcam overhead, fixed — no wobble
2. Power ESP32 via USB or battery pack
3. Connect both laptop and ESP32 to same WiFi network
4. Open TouchDesigner → confirm OSC messages arriving (`/rfid/model`)
5. Run ArUco detection → confirm all 12 markers detected correctly
6. Homography calibration → align projection to table (~10 min, one time)
7. Test full flow: place model → RFID read → correct content projected

---

## 8. Known Issues & Mitigations

| Issue | Mitigation |
|-------|-----------|
| Projector light washes out ArUco detection | Use matte filament; tune camera exposure down |
| ESP32 WiFi drops | Add reconnect loop in firmware; use 2.4GHz not 5GHz |
| Homography drifts if projector moves | Re-run calibration; mark projector position with tape |
| RFID read range too short | Keep reader flush with pedestal surface; coin tags work at 0–3cm |

---
*Created: 2026-04-17*
