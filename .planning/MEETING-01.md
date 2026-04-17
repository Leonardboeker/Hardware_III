# Meeting Notes — Session 1 Team Discussion
**Date:** April 2026
**Present:** Leo, Rafik, Onur, Nithik, Seid (Elais absent)
**Source:** Notion AI transcript

---

## Decisions Made

- Construction methods locked: **Masonry**, **3D Printed**, **Prefab/Modular**
- Platform: **TouchDesigner** (YOLO plugin needed, OpenCV may not work for object recognition)
- 12 ArUco markers: 10 floor plan pucks + 1 stories selector + 1 material selector
- RFID chip in each 3D printed model → ESP32 pedestal reader
- Project framing: **interactive installation / teaching exhibit** (not a pure research or software tool)
- Target audiences: children, young architects, decision makers
- Regional data focus: **Catalonia** (local suppliers for logistics costs)
- Material constraints: earth 3D print = max 1 story; masonry = brick or stone; prefab = all modular

## Development Phases (team priority order)

| Priority | Phase | What it delivers |
|----------|-------|-----------------|
| 1 — Most important for course | ArUco floor plan + floor selector + projector + camera + GUI | Basic working installation loop |
| 2 | RFID + ESP32 + building method selection | Physical model triggers content |
| 3 | Building phase animations + info display per phase | Educational layer |
| 4 | Cost tracking + CO2 tracking + comparison across builds | Full data output |

---

## Action Plan

### Immediate (before Session 2 — April 17)

- [ ] 3D print the 12 ArUco marker pucks (circular, matte filament)
- [ ] Install YOLO plugin in TouchDesigner + test if it works (alternative: OpenCV)
- [ ] Define all parameters and data points needed per construction method
- [ ] Start TouchDesigner project: camera in → ArUco detection → table projection

### Research sprint (parallel, this week)

- [ ] **Building phases per method** — what are the 5 phases for masonry / 3D print / prefab?
- [ ] **Contact 10+ companies per method** — request reference data (CO2, labor hours, costs)
- [ ] **AI animation tools** — research how to generate building phase animations easily
- [ ] **Material costs + CO2 per unit** — Catalonia region focus, local suppliers

### Phase 2 tasks (after Session 2)

- [ ] Wire RFID reader + ESP32, test read range
- [ ] Firmware: WiFi OSC → TouchDesigner
- [ ] Map RFID UIDs to construction methods

---
*Notes saved: 2026-04-17*
