# Work Plan & Task Division
**Team:** Leo, Elais, Rafik, Onur, Nithik, Seid
**Last updated:** 2026-04-17

---

## Role Areas

| Role | Owns |
|------|------|
| **Tech / TouchDesigner** | TD project, ArUco detection, projection mapping, FSM logic |
| **Hardware / Electronics** | ESP32 firmware, RFID wiring, WiFi/OSC pipeline |
| **3D Modeling / Fabrication** | Physical models, ArUco pucks, RFID embedding |
| **Data / Research** | Building phases, CO2 data, company outreach, cost data |
| **Visuals / Animation** | Phase animations, GUI design, projection content |
| **PM / Documentation** | GitHub, Notion, Gantt, session reports |

> Assign names below — each person takes a primary role + one support role

| Name | Primary | Support |
|------|---------|---------|
| Leo | | |
| Elais | | |
| Rafik | | |
| Onur | | |
| Nithik | | |
| Seid | | |

---

## Sprint 1 — Before Session 2 (April 17)

### Deliverables due
- [ ] S1-01: Project proposal (3 slides)
- [ ] S1-02: Gantt chart covering S1–S7
- [ ] S1-03: Embodied interaction photo/sketch
- [ ] S1-04: FSM diagram on paper

### Task breakdown

| Task | Owner | Due |
|------|-------|-----|
| Write proposal slides (concept, system arch, methods) | | Apr 17 |
| Create Gantt chart | | Apr 17 |
| FSM diagram on paper (8 states, labeled transitions) | | Apr 17 |
| Embodied interaction photo/sketch | | Apr 17 |
| 3D print 12 ArUco pucks (circular, matte, X1C) | | Apr 17 |
| TouchDesigner: camera in + ArUco detection working | | Apr 17 |
| Install + test YOLO plugin in TouchDesigner | | Apr 17 |

---

## Sprint 2 — Session 2 → Session 3 (April 17 – May 4)

| Task | Owner | Due |
|------|-------|-----|
| **Research: building phases** — 5 phases per method (masonry, 3DP, prefab) | | May 4 |
| **Research: data** — CO2, labor hours, cost per phase, Catalonia focus | | May 4 |
| **Company outreach** — contact 10+ companies per method for reference data | | May 4 |
| **TD: floor plan logic** — ArUco positions → building footprint + m² calculation | | May 4 |
| **TD: floor selector** — ArUco marker 10 → stories + feasibility check | | May 4 |
| **TD: material selector** — ArUco marker 11 → material choice + constraints | | May 4 |
| **TD: projection calibration** — homography setup on table | | May 4 |
| **ESP32 + RFID** — wire, flash firmware, test WiFi OSC to TouchDesigner | | May 4 |
| **3D models** — design and print 3 completed construction method models with RFID pockets | | May 4 |

---

## Sprint 3 — Session 3 → Session 4 (May 4 – May 11)

| Task | Owner | Due |
|------|-------|-----|
| **Building phase animations** — 5 phases × 3 methods = 15 animations (AI-generated) | | May 11 |
| **TD: phase display** — walk user through phases with animation + info per phase | | May 11 |
| **TD: feasibility feedback** — red state if parameters not possible | | May 11 |
| **TD: user input per phase** — accept/continue input between phases | | May 11 |
| **Data integration** — CO2, labor, cost data wired into TD per phase | | May 11 |

---

## Sprint 4 — Session 4 → Session 5 (May 11 – May 18)

| Task | Owner | Due |
|------|-------|-----|
| **TD: save dataset** — store building config + data after completion | | May 18 |
| **TD: comparison view** — project side-by-side stats for 2 completed builds | | May 18 |
| **TD: final output** — total cost, CO2, material use, logistics breakdown | | May 18 |
| **Projection mapping on models** — project construction progress onto physical model surfaces | | May 18 |

---

## Sprint 5 — Finals (May 18 – May 22)

| Task | Owner | Due |
|------|-------|-----|
| Full system test — end-to-end demo run | | May 22 |
| Fix bugs from test | | May 22 |
| Update PM schedule for submission | | May 22 |
| Prepare presentation flow | | May 22 |

---

## Open Research Questions

1. What are the exact 5 construction phases for masonry / 3D printed / prefab?
2. Does CO2 data correlate exactly to user's chosen parameters or is it general educational data?
3. Which AI animation tool is fastest for generating phase visualizations?
4. Does YOLO plugin work reliably in TouchDesigner, or do we use OpenCV?
5. Can we get real company data in time, or do we use published EPD averages?

---
*Created: 2026-04-17*
