# Hardware III — Human-in-the-Loop Interactive Systems

## What This Is

A semester-long interactive installation project at IAAC (MRAC + MAAI, 2025/2026).
A physical scale replica (building or object) is placed on a table. A projector maps
directly onto the 3D surface of the model, revealing layered content: CO₂ emissions,
material provenance, and critical historical facts — accompanied by spatial sound.
Camera/Kinect detects object placement and orientation; the human interaction (placing,
rotating, approaching) drives the FSM that controls what information layer is shown.

## Core Value

A physical replica becomes a data interface: place the model, and the building/object
tells its own critical story through light and sound projected directly onto it.

## Requirements

### Validated

(None yet — in progress)

### Active

- [ ] Session 1 deliverable: Project proposal (1 page/3 slides) submitted before April 17
- [ ] Session 1 deliverable: Project management schedule submitted before April 17
- [ ] Session 1 deliverable: FSM sketch on paper (3–5 states, labeled transitions)
- [ ] Define module type, connection logic, and intended human input method
- [ ] FSM implemented in Grasshopper (Anemone) with at least 4 states: IDLE → READY → CHECKING → CONFIRMED/ERROR → COMPLETE
- [ ] Input pipeline: sensor/webcam → Firefly → Grasshopper data stream working
- [ ] Human-in-the-loop: system cannot proceed without human action at key decision points
- [ ] Projection mapping: light guides placement, validates position, signals state changes
- [ ] Final working prototype demonstrated May 22

### Out of Scope

- Touchscreen interfaces — explicitly excluded by course philosophy
- Pre-recorded/static projection — must respond in real time to human action
- Full automation — human judgment must be part of the loop

## Context

**Course:** Hardware III seminar, MRAC + MAAI 2025/2026
**Instructors:** Hamid Peiro, Aleksandra (Sasha) Kraeva
**Schedule:** 5 course days + Finals (April 10 – May 22, 2026)
**Toolkit:** Rhino + Grasshopper (main), Firefly (sensor input), Anemone (FSM/loops),
TouchDesigner/HeavyM (projection), Arduino/ESP32 (physical sensors), USB webcam overhead

**Three paradigms of making (course framing):**
- Traditional Craft → Human decides in real time, not scalable
- Digital Fabrication → Front-loaded, deterministic, no feedback
- **Human-in-the-Loop** ← THIS PROJECT — decisions distributed, system responds in real time

**Key theoretical reference:** Stefana Parascho, "Cooperative Robotic Assembly" (ETH Diss. 25839)
— assembly sequence as FSM, each intermediate state must be structurally valid

**Project concept (confirmed April 10):**
- Physisches Replica (Gebäude oder Objekt als Maßstabsmodell) wird auf Tisch platziert
- Projektor mappt direkt auf die 3D-Oberfläche des Modells (kein flacher Screen)
- Inhalt-Schichten: CO₂-Emissionen, Materialherkunft, kritische historische Fakten
- Ton/Sound als Ebene: industrielle Geräusche, historische Audio-Fragmente, Umgebungsklang
- Kamera (overhead) + ggf. Kinect erkennt Platzierung und Orientierung des Modells
- ESP32 + Sensor für zusätzliche Interaktion (Proximity, Rotation, Touch)
- FSM-Logik: jeder State = eine Informationsschicht (IDLE → PLACED → CO2 → HISTORY → ORIGIN → COMPLETE)
- Hintergrund: Ausstellungsbau — Installation vermittelt kritischen Inhalt, nicht nur visuelle Aktivität

## Constraints

- **Timeline:** S1 proposal due April 17 — sets the direction for the entire course
- **Tech Stack:** Rhino + Grasshopper mandatory (course environment)
- **Output:** Projection-mapped interactive system — no screens
- **Team:** Group project — project management schedule required from S1
- **Budget:** Video projector available (€200 rental if needed)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| No touchscreens | Course philosophy: body language, not screen conventions | — Pending |
| FSM-first design approach | Draw diagram before code — course requirement | — Pending |
| Physical object as input method | Placing module triggers system validation | — Pending |
| Grasshopper as main logic environment | Course toolkit, Anemone for state loops | — Pending |

---
*Last updated: 2026-04-10 — initial project setup from Session 1 slides*
