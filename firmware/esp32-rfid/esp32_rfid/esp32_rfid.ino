// Hardware III — RFID method selector
//
// ESP32 + MFRC522 RFID reader + MIFARE Classic 1K (S50) tags.
// Reads tag UID, prints "RFID:<HEX>" over USB serial @ 115200 baud.
// TouchDesigner Serial DAT (rfid_in) parses these lines.
//
// Hardware:
//   RC522 SDA  -> GPIO 5   (SS)
//   RC522 SCK  -> GPIO 18
//   RC522 MOSI -> GPIO 23
//   RC522 MISO -> GPIO 19
//   RC522 RST  -> GPIO 27
//   RC522 3.3V -> 3V3      (NOT 5V — RC522 is 3.3V only)
//   RC522 GND  -> GND
//
// Library: install "MFRC522" by GithubCommunity from Library Manager.

#include <SPI.h>
#include <MFRC522.h>
#include <algorithm>

constexpr uint8_t SS_PIN  = 5;
constexpr uint8_t RST_PIN = 27;

// ---- Slider (DollaTek 10K linear-slide potentiometer) ----
// GPIO34 is input-only on ESP32, ADC1_CH6, WiFi-safe.
constexpr uint8_t  SLIDER_PIN          = 34;
constexpr uint8_t  MAX_FLOORS          = 5;        // upper bound; per-method caps live TD-side
constexpr uint8_t  MEDIAN_WINDOW       = 8;        // ring buffer size (CONTEXT.md: median FIRST)
constexpr float    EMA_ALPHA           = 0.2f;     // tune in jitter test (CONTEXT.md starting point)
constexpr float    HYST_EPSILON        = 0.02f;    // CONTEXT.md hysteresis nudge
constexpr unsigned long SLIDER_POLL_MS = 50;       // ADC sample cadence
constexpr unsigned long SLIDER_EMIT_MS = 200;      // SLIDER:0.xxx periodic emit
constexpr float    SLIDER_MV_MAX       = 3300.0f;  // ADC_11db: full range ~0..3300 mV

// ---- Slider B (second DollaTek 10K, BUILDING_PHASE switch, Manual-Override-Only) ----
// GPIO35 is input-only on ESP32, ADC1_CH7, WiFi-safe.
constexpr uint8_t  SLIDER_B_PIN          = 35;
// No MAX_PHASES here — phase count is per-method, quantized TD-side (see CONTEXT.md Slider B amendment).
constexpr unsigned long SLIDER_B_POLL_MS = 50;     // ADC sample cadence (same as Slider A)
constexpr unsigned long SLIDER_B_EMIT_MS = 200;    // PSLIDER:0.xxx periodic emit

MFRC522 rfid(SS_PIN, RST_PIN);

// Debounce: ignore re-reads of the same tag for this many ms.
constexpr unsigned long REREAD_MS = 1500;

String   lastUid     = "";
unsigned long lastReadMs = 0;

// ---- Slider state ----
uint16_t sliderBuf[MEDIAN_WINDOW] = {0};
uint8_t  sliderBufCount           = 0;          // grows to MEDIAN_WINDOW then stays
uint8_t  sliderBufHead            = 0;          // circular write index
float    sliderEma                = 0.0f;       // last smoothed normalized value [0, 1]
uint8_t  lastFloor                = 1;          // 1..MAX_FLOORS
float    lastFloorCenter          = 0.0f;       // normalized centre of lastFloor (for hysteresis)
unsigned long lastSliderPollMs    = 0;
unsigned long lastSliderEmitMs    = 0;

// ---- Slider B state ----
uint16_t sliderBBuf[MEDIAN_WINDOW]   = {0};
uint8_t  sliderBBufCount             = 0;
uint8_t  sliderBBufHead              = 0;
float    sliderBEma                  = 0.0f;
unsigned long lastSliderBPollMs      = 0;
unsigned long lastSliderBEmitMs      = 0;

// Floor centre for a given 1..MAX_FLOORS index, in normalized [0, 1] space.
static inline float floorCenter(uint8_t f) {
  if (MAX_FLOORS <= 1) return 0.0f;
  return (float)(f - 1) / (float)(MAX_FLOORS - 1);
}

// Quantize a normalized [0, 1] value to a floor 1..MAX_FLOORS.
static inline uint8_t quantizeFloor(float norm) {
  if (norm < 0.0f) norm = 0.0f;
  if (norm > 1.0f) norm = 1.0f;
  float f = 1.0f + norm * (float)(MAX_FLOORS - 1);
  long  r = lroundf(f);
  if (r < 1) r = 1;
  if (r > (long)MAX_FLOORS) r = MAX_FLOORS;
  return (uint8_t)r;
}

// Median of the live samples in sliderBuf (only the first sliderBufCount entries are valid).
static inline uint16_t sliderMedian() {
  uint16_t copy[MEDIAN_WINDOW];
  uint8_t  n = sliderBufCount;
  if (n == 0) return 0;
  for (uint8_t i = 0; i < n; i++) copy[i] = sliderBuf[i];
  std::nth_element(copy, copy + n / 2, copy + n);
  return copy[n / 2];
}

void setup() {
  Serial.begin(115200);
  while (!Serial && millis() < 2000) {}  // wait briefly for USB CDC
  // Slider ADC: 0..3.3 V full range
  analogSetPinAttenuation(SLIDER_PIN, ADC_11db);
  analogReadResolution(12);              // 0..4095 raw if we ever need raw; we use millivolts API
  lastSliderPollMs = millis();
  lastSliderEmitMs = millis();
  // Slider B ADC: 0..3.3 V full range
  analogSetPinAttenuation(SLIDER_B_PIN, ADC_11db);
  lastSliderBPollMs = millis();
  lastSliderBEmitMs = millis();
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("BOOT:rfid_reader_ready");
}

void loop() {
  // Heartbeat every second so TD can see we're alive even with no tag.
  static unsigned long lastHb = 0;
  unsigned long now = millis();
  if (now - lastHb >= 1000) {
    lastHb = now;
    Serial.print("HB:");
    Serial.println(now / 1000);
  }

  // ---- Slider poll (every SLIDER_POLL_MS ms) ----
  if (now - lastSliderPollMs >= SLIDER_POLL_MS) {
    lastSliderPollMs = now;

    // 1) Sample ADC in millivolts (calibrated by ESP32 core).
    uint32_t mv = analogReadMilliVolts(SLIDER_PIN);
    if (mv > (uint32_t)SLIDER_MV_MAX) mv = (uint32_t)SLIDER_MV_MAX;

    // 2) Push into ring buffer.
    sliderBuf[sliderBufHead] = (uint16_t)mv;
    sliderBufHead = (sliderBufHead + 1) % MEDIAN_WINDOW;
    if (sliderBufCount < MEDIAN_WINDOW) sliderBufCount++;

    // 3) Median FIRST (kills single-tick spikes).
    uint16_t med_mv = sliderMedian();
    float    med_norm = (float)med_mv / SLIDER_MV_MAX;
    if (med_norm < 0.0f) med_norm = 0.0f;
    if (med_norm > 1.0f) med_norm = 1.0f;

    // 4) EMA SECOND (smooths the post-median signal).
    //    On the very first valid sample, seed EMA to med_norm so we don't ramp from 0.
    static bool emaSeeded = false;
    if (!emaSeeded) {
      sliderEma = med_norm;
      lastFloor = quantizeFloor(sliderEma);
      lastFloorCenter = floorCenter(lastFloor);
      emaSeeded = true;
    } else {
      sliderEma = (EMA_ALPHA * med_norm) + ((1.0f - EMA_ALPHA) * sliderEma);
    }

    // 5) Hysteresis-gated quantization. Floor only changes when the smoothed value has
    //    moved more than half a floor-step away from the current floor's centre, plus EPSILON.
    const float halfStep = (MAX_FLOORS > 1)
      ? (1.0f / (2.0f * (float)(MAX_FLOORS - 1)))
      : 0.5f;
    if (fabsf(sliderEma - lastFloorCenter) > (halfStep + HYST_EPSILON)) {
      uint8_t newFloor = quantizeFloor(sliderEma);
      if (newFloor != lastFloor) {
        lastFloor = newFloor;
        lastFloorCenter = floorCenter(lastFloor);
        Serial.printf("FLOOR:%u\n", (unsigned)lastFloor);
      }
    }
  }

  // ---- Slider periodic emit (every SLIDER_EMIT_MS ms) ----
  if (now - lastSliderEmitMs >= SLIDER_EMIT_MS) {
    lastSliderEmitMs = now;
    Serial.printf("SLIDER:%.3f\n", sliderEma);
  }

  // ---- Slider B poll (every SLIDER_B_POLL_MS ms) — NO quantization/hysteresis in firmware ----
  if (now - lastSliderBPollMs >= SLIDER_B_POLL_MS) {
    lastSliderBPollMs = now;

    // 1) Sample ADC in millivolts.
    uint32_t mvB = analogReadMilliVolts(SLIDER_B_PIN);
    if (mvB > (uint32_t)SLIDER_MV_MAX) mvB = (uint32_t)SLIDER_MV_MAX;

    // 2) Push into ring buffer.
    sliderBBuf[sliderBBufHead] = (uint16_t)mvB;
    sliderBBufHead = (sliderBBufHead + 1) % MEDIAN_WINDOW;
    if (sliderBBufCount < MEDIAN_WINDOW) sliderBBufCount++;

    // 3) Median FIRST — inline (own buffer, can't reuse sliderMedian()).
    uint8_t nB = sliderBBufCount;
    if (nB > 0) {
      uint16_t copyB[MEDIAN_WINDOW];
      for (uint8_t i = 0; i < nB; i++) copyB[i] = sliderBBuf[i];
      std::nth_element(copyB, copyB + nB / 2, copyB + nB);
      uint16_t medB_mv = copyB[nB / 2];
      float    medB_norm = (float)medB_mv / SLIDER_MV_MAX;
      if (medB_norm < 0.0f) medB_norm = 0.0f;
      if (medB_norm > 1.0f) medB_norm = 1.0f;

      // 4) EMA SECOND.
      static bool emaBSeeded = false;
      if (!emaBSeeded) {
        sliderBEma = medB_norm;
        emaBSeeded = true;
      } else {
        sliderBEma = (EMA_ALPHA * medB_norm) + ((1.0f - EMA_ALPHA) * sliderBEma);
      }
    }
  }

  // ---- Slider B periodic emit (every SLIDER_B_EMIT_MS ms) ----
  if (now - lastSliderBEmitMs >= SLIDER_B_EMIT_MS) {
    lastSliderBEmitMs = now;
    Serial.printf("PSLIDER:%.3f\n", sliderBEma);
  }

  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial())   return;

  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();

  if (uid != lastUid || (now - lastReadMs) > REREAD_MS) {
    Serial.print("RFID:");
    Serial.println(uid);
    lastUid     = uid;
    lastReadMs  = now;
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}
