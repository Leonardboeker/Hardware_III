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

constexpr uint8_t SS_PIN  = 5;
constexpr uint8_t RST_PIN = 27;

MFRC522 rfid(SS_PIN, RST_PIN);

// Debounce: ignore re-reads of the same tag for this many ms.
constexpr unsigned long REREAD_MS = 1500;

String   lastUid     = "";
unsigned long lastReadMs = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial && millis() < 2000) {}  // wait briefly for USB CDC
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
