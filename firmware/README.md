# firmware/

ESP microcontroller code — RFID pedestal, any sensor inputs, comms with TouchDesigner.

## Scope

- RFID reader on the pedestal (detects which 3D-printed method model is placed)
- ESP → host transport: OSC over WiFi recommended (TouchDesigner has a native OSC In CHOP)
- Any other physical sensors that come up (buttons, encoders)

## Suggested layout

```
firmware/
├── pedestal-rfid/
│   ├── platformio.ini   # or arduino .ino
│   └── src/
└── shared/
    └── osc-protocol.md   # message names + payloads agreed with the TD side
```

## Conventions

- PlatformIO if you can — easier than Arduino IDE for collaboration.
- Pin assignments and any wiring diagrams go in this folder, not buried in commit messages.
- Never hardcode WiFi credentials. Use a `secrets.h` (gitignored) or load from a config.
