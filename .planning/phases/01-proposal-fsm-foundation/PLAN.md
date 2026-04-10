# Phase 1 Plan: Proposal & FSM Foundation

**Goal:** Submit all S1 deliverables before Session 2. Concept fully defined: guided comparative assembly + projection + data + sound.
**Deadline:** April 17, 2026
**Requirements:** S1-01, S1-02, S1-03, S1-04

---

## Tasks

### 01-01: Lock Core Decisions (construction methods + building type)

**Deliverable:** Written decision record — which 2–4 methods and which building/object type

**Owner:** Full team (15-minute working session)

**Steps:**
1. Choose construction methods from: traditional masonry, 3D-printed concrete, modular prefab/CLT, adobe/vernacular
   - Recommendation: start with 3 methods — traditional masonry, 3D-printed concrete, modular prefab/CLT
   - Adobe is a strong 4th if time allows fabricating a 4th model set
2. Choose building type — must be simple enough to model at 1:50 scale in ~5–8 discrete pieces
   - Recommendation: a single-bay structural wall section (3m x 3m) — simple geometry, identical form across methods, lets data differences speak
   - Alternatives: small pavilion (~8 pieces), column with base (~4 pieces)
3. Define piece count per model (aim for 5–8 pieces — enough to feel sequential, not so many it becomes tedious)
4. Write decisions down in one sentence each: "We are comparing X, Y, Z construction methods. The object is a [type]. Each model has approximately N pieces."

**Done when:** Team has a written 4-sentence decision record and everyone agrees. No further debate on these choices.

---

### 01-02: Write Project Proposal (S1-01)

**Deliverable:** 1-page PDF or 3-slide deck submitted to instructors

**Owner:** Team — one person drafts, all review

**Steps:**
1. Open a slide deck or A4 document
2. Write/place these four sections (one per slide or per paragraph):
   - **Module type:** What are the physical pieces — describe geometry, material (cardboard, 3D-print, laser cut wood), scale, and how they differ per construction method
   - **Connection logic:** How pieces are placed — no physical connection between pieces, placement validated by overhead camera against projected target outline; pieces are color-coded or ArUco-marker-tagged per construction method
   - **Input method:** Overhead USB webcam (position detection via Firefly → Grasshopper) + ESP32 proximity sensor (user reaches toward table → data layer zooms)
   - **Feedback method:** Projector on table surface — step 1: placement outline projected; step 2: on confirmation, CO₂ + labor hours + method text appear on/around the placed piece; sound layer reinforces each step (method-specific audio: concrete mixer, robotic arm hum, timber stacking)
3. Add one image or diagram showing the top-down table layout (projector, webcam, models)
4. Export as PDF or save slide link
5. Submit to course platform / email instructors

**Done when:** Proposal document exists, covers all four required sections, submitted before April 17.

---

### 01-03: Create Project Management Schedule (S1-02)

**Deliverable:** Gantt chart or equivalent covering S1–S7 with team roles and per-session deliverables

**Owner:** PM lead (whoever takes that role)

**Steps:**
1. Open a spreadsheet (Excel, Google Sheets) or a tool like Notion, Trello, or a paper Gantt
2. Create a row per session/week:
   - S1 (April 10–17): Proposal, FSM paper diagram, embodied interaction observation
   - S2 (April 17): Module definition locked, connection logic spec, data research started
   - S3 (May 4): FSM in Grasshopper (Anemone), sensor pipeline live (webcam → Firefly → GH)
   - S4 (May 11): Full assembly loop for 2 methods, sound layer, ESP32 wired
   - S5 (May 18): Projection mapping calibrated, comparison view, all visual layers
   - S6 (May 22 Finals): End-to-end demo working, physical models fabricated, PM updated
3. Add a column for team role responsible per task
4. Define team roles — suggested split:
   - Tech lead: Grasshopper / Anemone / FSM logic
   - Sensing lead: Webcam / Firefly / ESP32 / Arduino
   - Projection lead: TouchDesigner or HeavyM calibration, visual layers
   - Content lead: Data research (CO₂, labor hours), physical model design + fabrication
   - PM: Schedule updates each session, submission tracking
   - (Roles can overlap for a small team — assign primary owner per task)
5. Export or screenshot the Gantt
6. Submit to course platform

**Done when:** Schedule exists as a shareable document, all sessions S1–S7 have at least one deliverable listed, each task has an owner name.

---

### 01-04: Draw FSM Diagram on Paper (S1-04)

**Deliverable:** Hand-drawn or sketched FSM diagram, photographed and submitted

**Owner:** Any team member, verified by all

**Steps:**
1. Take a blank sheet of A3 or A4
2. Draw 8 labeled state boxes:
   - IDLE
   - GUIDING
   - CHECKING
   - CONFIRMED
   - NEXT_PIECE
   - MODEL_COMPLETE
   - NEXT_MODEL
   - COMPARISON
3. Draw directed arrows between states with labeled transitions:
   - IDLE → GUIDING: "object / hand detected in zone (proximity sensor)"
   - GUIDING → CHECKING: "piece placed in target zone (webcam detects marker)"
   - CHECKING → CONFIRMED: "position valid (0.3s validation passes)"
   - CHECKING → GUIDING: "position invalid (ghost outline shown, retry)"
   - CONFIRMED → NEXT_PIECE: "data shown, timer expires or hand lifts (not last piece)"
   - CONFIRMED → MODEL_COMPLETE: "data shown, last piece of this model"
   - NEXT_PIECE → GUIDING: "next piece target highlighted"
   - MODEL_COMPLETE → NEXT_MODEL: "model summary shown, user picks up next kit"
   - NEXT_MODEL → GUIDING: "reset projection for new method"
   - COMPARISON → IDLE: "all models done, full stats projected, timeout resets"
   - Note: CONFIRMED → COMPARISON only when all models complete (annotate this)
4. Add a small legend: boxes = states, arrows = transitions, labels = trigger events
5. Photograph the diagram with good lighting (flat lay, no shadows)
6. Submit photo

**Done when:** Diagram photo shows all 8 states, all transitions have labeled triggers, submitted before April 17.

---

### 01-05: Capture Embodied Interaction Observation (S1-03)

**Deliverable:** One photo or sketch with a 2–3 sentence written observation, submitted

**Owner:** Any team member

**Steps:**
1. Find one non-touchscreen interaction in daily life that involves body position, gesture, or spatial awareness — examples:
   - Turning a door handle (rotational gesture, body weight transfer)
   - Operating a manual espresso machine (pressure feedback through the tamper)
   - Using stairs (proprioception without looking, rhythm)
   - Opening a lock with a physical key (tactile resistance, angular precision)
   - Pulling a drawer (resistance curve, sound of latch)
2. Photograph it in action (not a stock photo — your own hand/body) OR sketch it as a diagram showing body parts and directions of force/movement
3. Write 2–3 sentences describing:
   - What the body is doing (physical movement, contact points)
   - What feedback the body receives (resistance, sound, temperature, spatial position)
   - Why this is relevant to the project (connection to guided assembly / non-screen feedback)
4. Combine photo/sketch + text into one document or slide
5. Submit

**Done when:** Submission contains a photo or sketch + 2–3 sentences with explicit connection to the project concept. Must show a real non-digital interaction.

---

### 01-06: Submit All Deliverables + Commit Files to Git

**Deliverable:** All 4 S1 deliverables submitted to course + files committed to repository

**Owner:** Team (PM lead coordinates)

**Steps:**
1. Collect all deliverable files:
   - `S1-01_proposal.[pdf/slides link]`
   - `S1-02_gantt.[xlsx/pdf/screenshot]`
   - `S1-03_embodied_interaction.[jpg/png/pdf]`
   - `S1-04_fsm_diagram.[jpg/png]`
2. Place files in `D:\IAAC\Hardware_III\Project\S1_Deliverables\` (create folder if needed)
3. Submit to instructors (course platform or email — use whichever channel instructors specified)
4. Stage and commit to git:
   ```
   git add Project/S1_Deliverables/
   git commit -m "feat(S1): submit all S1 deliverables — proposal, Gantt, FSM diagram, embodied interaction"
   git push origin master
   ```
5. Verify push succeeded at: https://github.com/Leonardboeker/Hardware_III

**Done when:** All 4 files are committed and pushed to GitHub AND submitted to instructors. GitHub shows the S1_Deliverables folder in the latest commit.

---

## Timeline (April 10–17)

| Day | Task |
|-----|------|
| April 10 (today) | 01-01: Lock decisions (30 min team call) |
| April 11–12 | 01-02: Draft proposal; 01-04: Draw FSM diagram |
| April 12–13 | 01-03: Create Gantt; 01-05: Capture embodied interaction |
| April 14–15 | Review all materials as a team, revise |
| April 16 | Final review, compile, submit + commit |
| April 17 | Hard deadline — Session 2 |

---

## Success Criteria

All of the following must be TRUE before April 17:

- [ ] Written record of chosen construction methods (2–4) and building type exists
- [ ] Proposal document covers module type, connection logic, input method, feedback method — submitted
- [ ] Gantt/schedule covers S1–S7, lists deliverables per session, has team role assignments — submitted
- [ ] FSM diagram shows all 8 states with labeled transitions — photographed and submitted
- [ ] Embodied interaction: photo or sketch + 2–3 sentences connecting it to the project — submitted
- [ ] All files committed to GitHub master branch under `Project/S1_Deliverables/`
