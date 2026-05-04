# Proposal — 3 Slides
## Interactive Assembly Installation: Building Methods Compared Through Touch

---

### SLIDE 1 — Concept & Modules

**Title:** Comparative Assembly: How Construction Methods Shape What We Build

**What are the modules?**
Small-scale physical blocks representing three construction methods:
- Masonry: individual brick units (≈4×2×1.5 cm), stacked with alignment logic
- 3D-Printed Concrete: curved layer strips (≈8×2×0.5 cm), deposited sequentially
- Modular Prefab: larger panel units (≈8×4×1 cm), snapped into position

All modules are laser-cut or 3D-printed at tabletop scale. Each has a fiducial marker (ArUco) on its underside for camera tracking.

**What is the final assembled thing?**
A small wall section (≈25×20 cm), built three different ways. Same final form, completely different assembly process, completely different environmental cost.

---

### SLIDE 2 — Interaction & Feedback

**What human action drives the system?**
Physical object placement, detected by an overhead USB webcam reading ArUco markers on each piece. No touch, no gesture — the act of building IS the input.

**What does the projection feedback do?**
1. GUIDE: Projects the outline of where the next piece goes (placement target)
2. CONFIRM: Green pulse when piece is correctly placed
3. INFORM: After confirmation, LCA data projects directly onto the placed piece — CO₂ (kg), labor (hours), material origin (mini supply-chain map)
4. ERROR: Red outline + ghost of correct position if placement is wrong
5. COMPARE: After all three methods are built, side-by-side dashboard projected on the table

**What is the connection logic?**
- Masonry: gravity stack + horizontal alignment (piece must be within ±5mm of target)
- 3DP layers: sequential vertical stack (layer N only valid after layer N-1)
- Prefab panels: slot alignment (rotation must match within ±10°)

A piece is "valid" when its ArUco marker position/rotation matches the target within tolerance.

---

### SLIDE 3 — System Architecture & Timeline

**System diagram:**

```
[Physical pieces w/ ArUco markers]
        ↓ placed on table
[Overhead webcam] → detects marker ID + position + rotation
        ↓
[Processing: Grasshopper/TouchDesigner]
  - Compare detected vs. target position
  - Determine current FSM state
  - Look up LCA data for this piece
        ↓
[Projector overhead] → projects guidance, data, and feedback onto table + pieces
        ↓
[User sees feedback] → places next piece → loop continues
```

**Tech stack:**
- Rhino/Grasshopper: geometry definition, LCA data, assembly sequence design
- TouchDesigner (or Grasshopper+Firefly): runtime — camera input, projection output, FSM logic
- ArUco markers on pieces for reliable detection under projector light
- HD projector + USB webcam, both mounted overhead

**Key reference (white space):**
No existing project combines interactive tabletop assembly + projection-mapped LCA data + method comparison. Closest precedents: Gramazio Kohler Augmented Bricklaying (ETH), Fologram Steampunk Pavilion (Tallinn 2019).
