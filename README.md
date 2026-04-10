# Hardware III — Guided Comparative Assembly Installation

**Course:** Hardware III — Human-in-the-Loop: Interactive Systems
**Institute:** IAAC, MRAC + MAAI 2025/2026
**Instructors:** Hamid Peiro, Aleksandra Kraeva
**Schedule:** April 10 – May 22, 2026
**Team:** Leo, Elais, Rafik, Seid, Onur, Nithik

---

## Mission

> "We compare different statistics of the housing construction industry and display them through an interactive exhibit."

## Concept

An interactive table installation where the user physically assembles 2–3 scale models of the same object — each built using a different construction method (e.g. traditional masonry, 3D-printed concrete, modular prefabrication).

A projector guides every assembly step. As each piece is placed, production data is mapped directly onto the object: CO₂ consumption, labor hours, material origin. Once all models are complete, a full comparison is projected across the table.

**The point:** Instead of reading abstract statistics, you build the comparison yourself — piece by piece. The data becomes physical.

---

## How It Works

1. Projector highlights where to place the next piece
2. User places the physical piece on the table
3. Camera confirms correct placement
4. Data is projected onto the piece: CO₂, labor hours, production method
5. Next piece is highlighted → repeat until model complete
6. Move to next construction method → build again
7. All models complete → full comparison projected side by side

---

## FSM States

```
IDLE → GUIDING → CHECKING → CONFIRMED → NEXT_PIECE
                     ↓
                   ERROR (wrong placement → ghost guide shown)

CONFIRMED (last piece) → MODEL_COMPLETE → NEXT_MODEL → GUIDING
NEXT_MODEL (last model) → COMPARISON → IDLE
```

---

## Tech Stack

| Tool | Role |
|------|------|
| Rhino + Grasshopper | Main logic environment |
| Anemone (GH plugin) | FSM loop logic |
| Firefly (GH plugin) | Webcam/sensor → Grasshopper data stream |
| TouchDesigner / HeavyM | Projection mapping + visual output |
| Arduino / ESP32 | Proximity sensor (user leans in → data zoom) |
| USB webcam (overhead) | Piece placement detection |
| Video projector (top-down) | Guided projection on table + model surfaces |

---

## Project Structure

```
.planning/
  PROJECT.md              — Full project context and concept
  REQUIREMENTS.md         — All requirements (S1–Finals)
  ROADMAP.md              — Phase breakdown with goals and success criteria
  STATE.md                — Current phase and progress
  phases/
    01-proposal-fsm-foundation/
      PLAN.md             — Phase 1 tasks (due April 17)
```

---

## Phases

| Phase | Goal | Deadline |
|-------|------|----------|
| 1 — Proposal & FSM Foundation | Submit S1 deliverables, lock concept | April 17 |
| 2 — Data Research & Physical Model Design | Source CO₂/labor data, fabricate model parts | May 4 |
| 3 — FSM Implementation & Assembly Logic | Full FSM in Anemone, piece detection pipeline | May 4 |
| 4 — Human-in-the-Loop Assembly & Sound | Guided loop for 2+ methods, sound layer | May 11 |
| 5 — Projection Mapping & Comparison View | Projector calibrated, comparison statistics | May 18 |
| 6 — Integration, Testing & Finals | Reliable end-to-end demo | May 22 |

---

## Key Reference

Stefana Parascho — *Cooperative Robotic Assembly* (ETH Diss. 25839)
Assembly sequence as FSM: each intermediate state must be structurally valid before the next step is permitted. Directly maps to guided piece-by-piece placement in this installation.
