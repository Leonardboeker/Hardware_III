# PRODUCT.md — Hardware III · Guided Comparative Assembly

## Surface

Final-critique presentation deck for IAAC MRAC + MAAI 2025–2026 course **Hardware III · Human in the Loop · Interactive Systems**. Delivered as an HTML slide deck (Reveal.js) for a fixed, time-boxed jury review on 2026-05-22.

## Register

**Brand.** The deck IS the deliverable. The artefact being judged is the argument, not a product the jury will operate. Visual confidence, typographic conviction, and diagrammatic precision are the work itself, not packaging around it.

## Users

Primary: **IAAC faculty + external jurors** at the MRAC + MAAI final critique. Architects, computational designers, and fabrication researchers. They sit through 12 to 20 decks in one session. They have seen every category-default presentation template. They reward clarity, evidence, and a defensible position; they punish hedging and decoration.

Secondary: **the team itself** (Leo, Elias, Rafik, Seid, Onur, Nithik) using the deck as a final-week handoff. Must read without narration.

Tertiary: **archive viewers** — IAAC researchers and prospective students who may open the file months later with zero verbal context.

## Project purpose

Argue that construction-method consequences (CO₂, labour, time, cost) can be made legible *during* the configuration moment — at a physical table, by non-experts, with the data shown as honest ranges and not as deceptively precise single figures.

The installation is a guided comparative-assembly table. Visitors place RFID method models on a pedestal, arrange ten ArUco pucks for a footprint, choose height and material, walk through five construction phases, and finally see a comparison view. TouchDesigner is the runtime. ESP32 + RC522 read RFID. Overhead webcam + OpenCV detect pucks. Short-throw projector returns visual feedback.

## Voice

Architectural, technical, honest. The jury knows the discipline. Talk to them like peers.

- Declarative sentences. No hedging adverbs.
- Numbers carry sources and ranges, never a single figure with no provenance.
- Diagrams say more than paragraphs. Captions are short, structural, lowercase.
- Where data is incomplete, say so explicitly. Methodological wobble is a first-class topic.

## Anti-references

Visual treatments to avoid even if they would be "safe":

- **SaaS-cream landing-page aesthetic.** Soft beige + display serif + italic kicker + drop cap. Editorial-magazine costume on a hardware-installation brief is wrong register.
- **Architecture-school greyscale template.** Helvetica Light over a blurred render. Reads as 2015 thesis-book default.
- **Hero-metric template.** A giant number with a small label and three supporting stats. SaaS cliché.
- **Photo backgrounds with white text overlay.** Stock photography crutch.
- **Side-stripe borders, gradient text, glassmorphism.** Banned by the design system.
- **Default Reveal.js theme.** Black background with centered white serif title. Recognisable on sight as "didn't customise."

## Strategic principles

- **Diagrams are content, not decoration.** Rebuild every diagram from the original deck in code (SVG / CSS Grid) so it scales cleanly and stays editable.
- **Whitespace beats density.** Jury fatigue is real. Give every slide room.
- **One idea per slide.** If two ideas show up, split the slide.
- **Type carries hierarchy.** Variable-weight contrast inside a single display family, not size-spam.
- **Three method colours are baked into the project.** Respect them: masonry terracotta, 3D-printed steel blue, prefab green. Everything else is neutral.
- **Honest gaps.** Where a slide claims a subsystem that is still in flight, label it with current state, not aspirational state.

## Register field

`register: brand`

## Locked decisions

- **Methods are three.** Reclaimed brick is dropped completely as of 2026-05-18. Remove from all slides.
- **Resolution.** Short-throw projector outputs 1280 × 720 per the architecture slide; deck must show this number, not aspirational 1920 × 1080.
- **HEIGHT input.** ArUco ID 10 dial is being replaced by a DollaTek 10K linear-slide potentiometer wired into the ESP32 (Phase 02.1). Deck must reflect the slider, not the retired dial.
- **Material logic input.** ArUco ID 11 is the marker. Pipeline planned, not yet shipped — label as in-progress.
- **Vision stack.** vision2/ (ArUco + MediaPipe gestures) is the canonical sketch pipeline. HSV puck path retired.
