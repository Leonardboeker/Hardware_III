# Concept (Extended) — Guided Comparative Assembly Installation

> **Note:** This is a more detailed concept document developed by Rafik based on the iterations after Session 2. It expands on the version in the root `README.md`. Treat the root README as the **canonical** concept until the team merges this in.

**Course:** Hardware III — Human-in-the-Loop: Interactive Systems
**Institute:** IAAC, MRAC + MAAI 2025/2026
**Instructors:** Hamid Peiro, Aleksandra Kraeva
**Schedule:** April 10 – May 22, 2026
**Team:** Leo, Elais, Rafik, Seid, Onur, Nithik

---

## Mission

We compare different statistics of the housing construction industry and display them through an interactive exhibit — a hands-on learning experience for children, young architects, and decision makers.

## Concept

An interactive table installation where users **configure** and compare buildings across three construction methods. Instead of reading abstract statistics, you define your building, watch it get constructed phase by phase, and see the real environmental and economic cost — all through physical interaction with projection-mapped surfaces.

Inspired by the Swiss Museum's interactive DJ table (ArUco markers + projection mapping).

---

## Construction Methods

| Method | Description | Materials |
|--------|-------------|-----------|
| **Classical / Masonry** | Traditional brickwork construction | Brick or Stone |
| **3D Printed** | Additive construction, layer by layer | Earth or Concrete |
| **Prefab / Modular** | Factory-built modules assembled on site | Grid / Modular panels |

### Material Constraints
- Earth-based 3D printing: max 1 story
- System enforces realistic limitations with visual feedback (red = not possible)

---

## User Interaction Flow

```
1. METHOD SELECTION
   Place one of three 3D-printed models on RFID pedestal
   → System identifies construction method

2. DEFINE BUILDING SIZE
   Arrange 10 ArUco marker pucks on table to create building footprint
   → Camera tracks distances between markers → calculates dimensions
   → Area within markers shown in green (valid) or red (invalid)

3. SET HEIGHT / FLOORS
   Use dedicated ArUco marker (physically distinct) to select number of stories
   → System validates feasibility per method + material

4. CHOOSE MATERIALS
   Use another distinct ArUco controller to select foundation type + main material
   → Masonry: brick or stone
   → 3DP: earth or concrete
   → Prefab: modular grid

5. GUIDED BUILDING PHASES (~5 per method)
   System walks through each construction phase with animations:
   → Foundation/excavation → Walls/structure → Roof → Windows → Finishing
   → Each phase shows: CO₂ per ton, energy usage, labor hours, time, cost
   → User accepts to continue to next phase

6. FINAL OUTPUT
   Complete breakdown: total cost, carbon emissions, material usage,
   logistics, labor — contextualized (e.g., "2000 tons of wood = X trees")

7. SAVE & COMPARE
   Save building as dataset → build another configuration → compare side by side
```

---

## Key Parameters & Data Points

- CO₂ emissions and carbon footprint
- Labor hours and worker health/safety
- Material usage (concrete, wood, cement) with real-world equivalents
- Total costs broken down by phase
- Logistics and transportation (focused on Catalonia region)
- Time required for construction

---

## System Architecture

### Physical Components

| Component | Role |
|-----------|------|
| **RFID Pedestal + ESP** | Recognizes which construction method model is placed |
| **3 Physical 3D-printed models** | Method selectors (classical, 3DP, prefab) — also projection targets |
| **10 Circular ArUco pucks** | Define building footprint on table |
| **Height ArUco marker** | Physically distinct — selects number of floors |
| **Material ArUco controller** | Selects foundation type and main material |
| **Top-down projector** | Projects onto table (construction site) |
| **Overhead camera** | Tracks ArUco positions, calculates distances |
| **ESP controllers** | Communication between physical inputs and system |
| **Display screens** | Information, cost estimates, comparisons |

### Software Stack

| Tool | Role |
|------|------|
| **TouchDesigner** | Primary development environment |
| **YOLO plugin (TD)** | Object recognition for markers |
| **Rhino + Grasshopper** | Geometry and parametric design |
| **ESP firmware** | RFID + sensor communication |

---

## FSM States

```
IDLE
  → model placed on RFID pedestal
METHOD_SELECTED
  → ArUco pucks placed on table
FOOTPRINT_DEFINED
  → camera validates distances, area calculated
  → height marker placed
HEIGHT_SET
  → material marker placed
MATERIALS_CHOSEN
  → system validates feasibility
  → VALID: proceed | INVALID: show error, adjust
VALIDATED
  → begin phase walkthrough
PHASE_DISPLAY (×5 per method)
  → animation plays, data shown
  → user accepts → next phase
BUILDING_COMPLETE
  → final output displayed
  → save dataset
COMPARISON
  → multiple builds compared side by side
  → timeout → IDLE
```

---

## Building Phases (per method, ~5 each)

| Phase | Example (Masonry) | Data Shown |
|-------|-------------------|------------|
| 1. Foundation / Excavation | Excavator, concrete pour | CO₂/ton cement, cost, time |
| 2. Structure / Walls | Brickwork rises | Labor hours, material qty |
| 3. Roof | Framing + covering | Material usage, safety |
| 4. Windows / Openings | Installation | Cost, energy |
| 5. Finishing | Plastering, painting, floors | Total finishing cost, time |

*Exact phases per method require research — 3DP and prefab have different sequences.*

---

## Development Priorities

| Priority | Phase | Scope |
|----------|-------|-------|
| **P1 (Course critical)** | Projector + Camera + ArUco | Square meter sizing, floor selection, GUI, top-down projection, camera tracking |
| **P2** | RFID + ESP | Pedestal integration, method selection, ESP communication |
| **P3** | Building phases | Phase animations (AI-generated), information display per phase |
| **P4** | Data + Comparison | Cost tracking, CO₂ tracking, dataset save, side-by-side comparison |

---

## Research Action Items

- [ ] Research building phases for classical/masonry, 3D printed, and prefab methods
- [ ] Contact 10+ companies per construction method for reference data
- [ ] Research AI-generated animation tools for building phase visualization
- [ ] Define all analytical parameters and data requirements
- [ ] 3D print ArUco marker pucks
- [ ] Install YOLO plugin for TouchDesigner
- [ ] Gather regional data (Catalonia focus) for logistics calculations

---

## Key Reference

**Swiss Museum DJ Table** — Interactive installation using ArUco markers on a large table with top-down projection. Users place physical objects to compose music. Direct precedent for our interaction model.

**Stefana Parascho** — *Cooperative Robotic Assembly* (ETH Diss. 25839). Assembly sequence as FSM.
