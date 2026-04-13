# Proposal Review — Session 1
**Source:** Group member critique (April 2026)
**Status:** Open for team discussion

---

## Critique Points (6)

1. **Three full builds is a UX trap** — ~15 min per build × 3 = visitor fatigue. Alternative: physically build ONE method end-to-end, play the other two as projected animations on adjacent table zones. Same comparison, fraction of the attention cost.

2. **The proposal flattens what isn't flat** — a 3D-printed concrete wall and a brick wall are not "the same wall" (structural, thermal, acoustic, aesthetic differences). Reducing all methods to CO₂/hours/cost reproduces the LCA tunnel vision we should be critiquing.

3. **The numbers are contested** — EPDs for cement and brick vary massively by source. Single figures can be dismantled in 30 seconds. Fix: project ranges with sources visible on the piece.

4. **"You feel it because you built it" is marketing, not embodiment** — the visitor feels the time to follow projector arrows, not a mason's labor. The labor-hours mapping is symbolic. Either own that explicitly (it's a metaphor) or it collapses under serious critique.

5. **The three methods are suspiciously canonical** — masonry/3DP/prefab is the lecture-slide trio. Swap one for reclaimed/reused brick: near-zero embodied carbon, outperforms 3DP on every metric, flips the story from tech showcase to political question.

6. **No politics** — silent on who loses jobs: 3DP eliminates skilled mason work, prefab moves jobs from local sites to factories. For architecture school this is the hot button.

---

## Additions — Ranked by Impact/Effort

### Top picks
1. **Material-origin map projected ON each piece** — when a brick is placed, a world map projects onto its surface: clay from X, fired in Y, shipped via Z. Strongest "data becomes physical" moment.
2. **Context dial** — physical knob changes climate zone or grid carbon (Beirut vs Zurich vs Lagos). Same pieces, comparison flips. Kills "which one wins?" → replaces with "wins for whom, where?"
3. **Carbon-budget clock** — continuously projected counter showing construction industry's remaining 1.5°C budget. Each piece placed ticks it down. Cheap, makes stakes visceral.
4. **Reused-brick as 4th method** — salvaged brick, near-zero embodied carbon. Single biggest narrative upgrade.
5. **Failure states** — misplace a brick → projector animates collapse. Misalign 3DP layer → whole layer wasted (cost ticks up). Visitors feel the failure cost of each method.

### Optional / nice-to-have
- **Disassembly mode** — build it, then deconstruct and project recyclability/landfill fate. Circular economy story.
- **Soundscape per method** — trowel scraping vs pump motor vs factory clang. Zero extra hardware.
- **End-of-experience vote** — physical button. Running tally projected: "47 visitors picked masonry, 12 picked 3DP."

---

## Reference Projects

### Guided assembly — direct precedents
- **Augmented Bricklaying** — Gramazio Kohler Research, ETH Zurich (2018–20). AR-guided masons placing bricks for complex facades. Direct ancestor of this idea.
- **Steampunk Pavilion** — Fologram + Gwyllim Jahn, Tallinn Architecture Biennale 2019. Untrained builders assembling a curved timber pavilion from AR instructions. Proved guided assembly works with the public.
- **Fologram** — Grasshopper-native AR toolkit. Commercial product of the above research line.
- **RoMA (Robotic Modeling Assistant)** — Huaishu Peng, Cornell/Autodesk, CHI 2018. Robot + AR guide user assembling a physical model in real time.

### Tangible / physical data visualization
- **inFORM** — Hiroshi Ishii / MIT Tangible Media Group, 2013. Canonical "data you can touch" reference.
- **Domestic Data Streamers** — Barcelona. Participatory physical dataviz where visitors aggregate into sculptural data.

### LCA / embodied carbon
- **Material Cultures** — London, 2021–. Bio-based comparison demonstrators. Same comparison logic, full-scale, not interactive.
- **EPFL Structural Xploration Lab** — Corentin Fivet. Pavilions from reclaimed components, embodied carbon as design driver. Cite if taking the reused-brick suggestion.
- **Striatus Bridge** — Zaha Hadid Computation + Block Research Group + ETH, 2021. What 3D-printed concrete actually looks like — use image in slides.
- **TECLA** — WASP + Mario Cucinella, 2021. Earth-based 3DP housing, explicitly framed around embodied carbon.

### Key gap (our opportunity)
No precedent exists for a **tabletop interactive LCA comparison installation**. Guided assembly exists. Tangible dataviz exists. LCA comparison demonstrators exist. Nobody has combined all three at table scale. This is our white space — state it explicitly in the proposal.

---

## Technical Feasibility Verdict

**Rhino + Grasshopper + Anemone + webcam + projector is a fragile stack for a public installation:**
- Grasshopper is single-threaded; Anemone stalls the canvas while looping → bad for real-time response
- Webcam piece-tracking inside GH (Firefly/Quokka) is slow and light-sensitive — projector light contaminates camera feed (known problem)
- Projection-mapping calibration onto small pieces drifts constantly — GH gives no help here
- Typical outcome: final week spent fighting canvas freezes instead of finishing the experience

**Recommended alternative: TouchDesigner**
- Native projection mapping + computer vision (OpenCV TOPs)
- Gallery-stable for long runs
- Use Rhino/GH only for geometry design + LCA math offline
- OSC bridge if runtime needs to talk back to GH
- Second choice: Unity + MadMapper

**If staying in Grasshopper:**
- Use Firefly (not Anemone) for camera input
- Put ArUco fiducial markers on every piece — detection independent of color/light
- Run projector from a separate machine to avoid blocking the canvas

---
*Review received: 2026-04-13*
