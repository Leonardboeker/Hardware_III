# Hardware III — Comparative Construction: Guided Assembly Installation

## What This Is

An interactive table installation at IAAC (MRAC + MAAI, 2025/2026).
The user assembles 2–4 physical scale models of the same building/object,
each representing a different construction method (traditional, 3D-printed, modular prefab, etc.).
A projector guides each placement step and reveals real data at every piece:
CO₂ consumption, labor hours, construction time, and method explanation.
After all models are complete, a comparative statistics view is projected — making
the environmental and economic differences tangible and visceral.

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
- (Optional) Adobe / earthen / vernacular

## FSM States

```
IDLE
  → Object detected in zone → GUIDING

GUIDING
  → Piece placed correctly → CHECKING

CHECKING (0.3s validation)
  → Valid → CONFIRMED
  → Invalid → ERROR (show ghost of correct position)

CONFIRMED
  → Show data layer (CO₂, hours, method)
  → Timer / user lifts hand → NEXT_PIECE
  → If last piece → MODEL_COMPLETE

NEXT_PIECE
  → Highlight next piece → GUIDING

MODEL_COMPLETE
  → Show model summary
  → User picks up next model set → NEXT_MODEL

NEXT_MODEL
  → Reset projection for new method → GUIDING

COMPARISON (all models complete)
  → Full statistics projected
  → Loop / reset after timeout → IDLE
```

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
| Color/marker-tagged pieces | Reliable detection without complex CV | — Pending |
| Sound as equal layer to visuals | Ausstellungsbau background — content depth matters | — Pending |

---
*Last updated: 2026-04-10 — concept finalized in conversation*
