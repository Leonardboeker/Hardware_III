# Hardware III — Guided Comparative Assembly

**Subtitle:** An interactive construction kitchen — configure, build, compare.
**Proposal submitted:** April 17, 2026 (`Group_3_Hardware_III_Proposal.pdf`)

## What This Is

A hands-on exhibit for children, young architects, and decision makers.
The user configures a building (footprint, height, material) using physical ArUco pucks and dials on a table. A projector guides them through 5 construction phases — each with CO₂, cost, labor, and logistics data. Three construction methods can be compared: Masonry, 3D Printed, Prefab. No screens. No buttons.

## Core Value

Turn abstract construction data into embodied knowledge:
you *build* the comparison yourself, piece by piece — the statistics emerge from your own hands.

## Concept

**Flow per model:**
1. Piece highlight projected → where to place next element
2. User places physical piece → camera/Kinect confirms position
3. Data appears projected on/around the piece: CO₂, labor hours, material origin, method explanation
4. Sound layer reinforces the data (industrial noise, time-lapse audio, factory vs. site sounds)
5. Next piece highlighted → repeat until model complete
6. Model summary shown → move to next construction method model

**After all models complete:**
- Full comparison statistics projected across all models simultaneously
- CO₂ totals, labor hours, time, cost — side by side
- Sound transitions to a final ambient layer

**Construction methods to compare (TBD, 2–4 models):**
- Traditional masonry / site-built
- 3D-printed concrete / robotic extrusion
- Modular prefabrication / CLT
- (Strong candidate) Reclaimed / reused brick — near-zero embodied carbon, outperforms 3DP on every metric, sharpens the political argument

## FSM States (locked in proposal)

```
IDLE → METHOD → FOOTPRINT → HEIGHT → MATERIALS → VALIDATED → 5 PHASES → COMPARISON
```

- **IDLE**: No model on pedestal
- **METHOD**: RFID read → construction method selected (Masonry / 3D Printed / Prefab)
- **FOOTPRINT**: User arranges 10 ArUco pucks → footprint + m² calculated
- **HEIGHT**: User rotates ArUco dial (ID 10) → floors selected
- **MATERIALS**: User rotates ArUco dial (ID 11) → material variant selected
- **VALIDATED**: System checks feasibility (e.g. earth 3DP max 1 story) → green/red feedback
- **5 PHASES**: Foundation → Structure → Roof → Openings → Finishing (animated, data per phase)
- **COMPARISON**: All data saved, side-by-side dashboard projected

## Building Phases (locked)

| Phase | Name |
|-------|------|
| 1 | Foundation |
| 2 | Structure / Walls |
| 3 | Roof |
| 4 | Openings (windows/doors) |
| 5 | Finishing |

## Input / Sensing

- **USB Webcam overhead**: detects piece placement position on table surface
- **Kinect** (optional): depth sensing for better 3D object recognition, height
- **ESP32 + proximity sensor**: detects when user leans in / reaches for piece → triggers data layer zoom
- **Physical pieces**: color-coded or marker-tagged parts per construction method

## Output

- **Projection on table surface + model surfaces**: placement guides, data overlays, statistics
- **Sound**: construction method audio per step (concrete mixer, robotic printer hum, timber assembly)
- **Statistics view**: final comparison projected as graphic across full table

## Toolkit

- Rhino + Grasshopper (main logic environment)
- Firefly (GH plugin): webcam/Kinect → Grasshopper data stream
- Anemone (GH plugin): FSM loop logic
- TouchDesigner or HeavyM: projection mapping calibration + visual output
- Arduino / ESP32: proximity sensor integration
- USB webcam overhead + video projector (top-down or angled)

## Context

**Course:** Hardware III seminar, MRAC + MAAI 2025/2026
**Instructors:** Hamid Peiro, Aleksandra (Sasha) Kraeva
**Schedule:** 5 course days + Finals (April 10 – May 22, 2026)
**User background:** Ausstellungsbau (exhibition design) — content must be critical and substantive, not just visually reactive

**Key theoretical reference:** Stefana Parascho, "Cooperative Robotic Assembly" (ETH Diss. 25839)
— assembly sequence as FSM, each intermediate state must be valid → directly maps to guided piece placement

**Reference projects (from S1 review):**
- Gramazio Kohler, Augmented Bricklaying, ETH 2018–20 — direct precedent for AR-guided assembly
- Fologram, Steampunk Pavilion, Tallinn 2019 — guided assembly proven with public
- MIT Tangible Media, inFORM, 2013 — canonical tangible dataviz reference
- EPFL SXL, Corentin Fivet — reuse + embodied carbon as design driver
- Striatus Bridge (ZHA + BRG + ETH, 2021) — 3DP concrete visual reference
- Domestic Data Streamers — participatory physical dataviz

**White space:** No precedent exists for a tabletop interactive LCA comparison installation combining guided assembly + tangible dataviz + LCA at table scale.

## Constraints

- **Timeline:** S1 proposal due April 17 — concept locked, execution starts
- **Tech Stack:** Rhino + Grasshopper mandatory (course toolkit)
- **Output:** Projection on physical surface — no screens
- **Team:** Group project — PM schedule required from S1
- **Data:** CO₂ and labor hour data must be sourced/researched for each construction method
- **Models:** Physical replica parts must be fabricated (3D print or laser cut) before Session 4

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Comparative structure (2–4 models) | Makes data tangible through contrast | — Pending |
| Guided assembly (not free exploration) | Matches course requirement: FSM + human-in-the-loop | — Pending |
| Table projection (top-down) | Easier calibration, direct piece-to-data feedback | — Pending |
| ArUco fiducial markers on pieces | Color detection unreliable under projector light | — Pending (recommended over color) |
| Sound as equal layer to visuals | Ausstellungsbau background — content depth matters | — Pending |
| Runtime: TouchDesigner vs GH/Anemone | GH is single-threaded; Anemone stalls canvas; webcam under projector light is fragile — TD does projection mapping + CV natively | — **Open — needs team decision** |
| Build all 3 methods physically vs. 1 physical + 2 animated | 3 full builds = visitor fatigue risk | — **Open — needs team decision** |
| LCA data as ranges (with sources) vs. single figures | Single EPD figures vary wildly and collapse under expert questioning | — **Open** |

## Open Critiques (from S1 peer review — address in proposal)

1. Three full builds may exhaust visitors — consider 1 physical + 2 projected animations
2. LCA numbers must be ranges with cited sources, not single figures
3. Labor-hours mapping is symbolic, not embodied — own that framing explicitly
4. Missing political dimension: who loses jobs in each method?
5. Reused/reclaimed brick as a 4th method is the strongest narrative upgrade available

See `.planning/REVIEW-S1.md` for full critique, additions, and references.

---
*Last updated: 2026-04-17 — proposal submitted, FSM + phases locked*
