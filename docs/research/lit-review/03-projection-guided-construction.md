# 03 — Projection-Guided Construction & Cooperative Robotic Assembly

## Scope

This review covers three overlapping bodies of work that the IAAC tabletop installation draws on, even where the team's borrowing is conceptual rather than technical:

1. **Cooperative robotic assembly**, anchored on Stefana Parascho's ETH dissertation, which the team explicitly cites as the lineage for treating an assembly process as a sequence of valid intermediate states (i.e. an FSM).
2. **Projection-mapped construction guidance**, from the foundational Spatial Augmented Reality literature (Bimber & Raskar) through recent in-situ AR systems for masonry, carpentry, and shell formwork (Gramazio Kohler's Augmented Bricklaying, EPFL IBOIS Augmented Carpentry, Block Research Group).
3. **Projector–camera calibration and FSM-based runtime architectures** for human-in-the-loop interactive installations, including practitioner literature around TouchDesigner, MadMapper, Resolume and HeavyM.

Out of scope here (covered in sibling reviews): ArUco/fiducial tracking specifics, LCA data sources, Gramazio Kohler's robot-only pipelines.

## Search strategy

Searches were run via WebSearch across: ETH Research Collection, Springer/Construction Robotics, ScienceDirect, arXiv, ACM Digital Library, Brown's structured-light course materials, derivative.ca, project sites (parascho, dfab, block.arch.ethz.ch, achimmenges.net, ibois-epfl). Where ETH Research Collection returned a 500 error on direct fetch, citation details were cross-checked against the Gramazio Kohler dissertations index, Princeton SoA bio, and AAG/Construction Robotics publications by the same author. Items I could not personally verify the full text of are marked **[unverified]**.

## Key works (annotated, in chronological order)

### Bimber & Raskar, 2005 — *Spatial Augmented Reality: Merging Real and Virtual Worlds*
- **Tier:** Book (foundational textbook).
- **Citation:** Bimber, O., & Raskar, R. (2005). *Spatial Augmented Reality: Merging Real and Virtual Worlds*. A K Peters/CRC Press, 392 pp. ISBN 978-1-56881-230-4. Open PDF copy: https://pages.cs.wisc.edu/~dyer/cs534/papers/SAR.pdf
- **What it is:** The canonical reference defining "Spatial AR" — augmenting physical surfaces with projected light rather than head-worn displays. Chapters cover geometric projection concepts, projector-based illumination, multi-projector blending, and an appendix on calibration.
- **Why it matters for the team:** Their tabletop is *exactly* a SAR system: a fixed top-down projector painting information onto a passive surface (the puck footprint). Bimber & Raskar's vocabulary (registration, geometric correction, projector-based illumination) is the language a reviewer will expect.
- **What to reuse:** The calibration appendix; the framing of "projector as light source replacing physical paint" justifies why projecting LCA data over real pucks is more intelligible than a screen.
- **Limitations:** Pre-dates modern structured-light toolchains and consumer projectors; for actual implementation, prefer Moreno & Taubin (2012) below.

### Salvi, Pagès & Batlle, 2004 — Pattern codification strategies in structured light
- **Tier:** Peer-reviewed (Pattern Recognition).
- **Citation:** Salvi, J., Pagès, J., & Batlle, J. (2004). Pattern codification strategies in structured light systems. *Pattern Recognition*, 37(4), 827–849. **[unverified DOI; widely cited]**
- **What it is:** Survey of how to encode projector pixels so a camera can recover dense correspondences (binary, Gray-code, De Bruijn, phase-shift).
- **Why it matters:** If the team ever wants to detect *what's on the table* with the projector itself (as opposed to relying solely on overhead ArUco), this is the entry point.
- **What to reuse:** The taxonomy alone — picking Gray-code patterns is the safe default for a one-off calibration.
- **Limitations:** Theoretical survey, no implementation.

### Moreno & Taubin, 2012 — Simple, Accurate, and Robust Projector–Camera Calibration
- **Tier:** Peer-reviewed (3DIMPVT / 3DV).
- **Citation:** Moreno, D., & Taubin, G. (2012). Simple, Accurate, and Robust Projector-Camera Calibration. *Proc. 3DIMPVT 2012*. Code/data: http://mesh.brown.edu/calibration/ ; tutorial: http://mesh.brown.edu/desktop3dscan/ch3-calib.html
- **What it is:** The de-facto standard procedure for calibrating a projector–camera pair using a printed checkerboard plus projected Gray-code, recovering full pinhole intrinsics + extrinsics for both devices.
- **Why it matters for the team:** This is the single most useful paper in this review for actually building the rig. The IAAC setup has a fixed top-down projector and (presumably) a top-down camera doing ArUco detection; Moreno-Taubin gives them a well-validated way to express both in a common world frame so the projector can mark where a puck *is*.
- **What to reuse:** The reference implementation linked above (also re-implemented in `kamino410/procam-calibration` on GitHub) — both use OpenCV.
- **Limitations:** Assumes the projector behaves as a pinhole; short-throw / wide-angle projectors will need explicit distortion modelling.

### Parascho, 2019 — Cooperative Robotic Assembly (ETH Diss. 25839)
- **Tier:** Doctoral dissertation.
- **Citation:** Parascho, S. (2019). *Cooperative Robotic Assembly: Computational Design and Robotic Fabrication of Spatial Metal Structures*. Doctoral thesis, ETH Zurich, Diss. ETH No. 25839. DOI: 10.3929/ethz-b-000364322. Research Collection: https://www.research-collection.ethz.ch/handle/20.500.11850/364322 . Advisors: Prof. Fabio Gramazio & Prof. Matthias Kohler (Gramazio Kohler Research, ITA, ETH); co-examiner Prof. Stelian Coros **[unverified — inferred from co-authored publications]**.
- **What it is:** A computational design and fabrication framework where two cooperating industrial robots assemble bespoke spatial metal structures without scaffolding by holding members in place until structural stability is reached. The dissertation models the assembly as a sequence of structurally valid intermediate states.
- **Why it matters for the team:** This is the team's headline reference. See Deep-dive below.
- **What to reuse:** The framing that *valid* states (those the system permits transitioning into) form a small subset of the combinatorial state space, and that the planner's job is to discover a path through them. Map this directly onto the interaction FSM (e.g. you cannot reach `MATERIALS_CHOSEN` from `IDLE`).
- **Limitations:** Domain is robot fabrication, not interactive installations; the analogy is structural, not technical.

### Huang, Garrett & Mueller, 2018 — Choreo (Automated SAMP for spatial extrusion)
- **Tier:** Peer-reviewed (Construction Robotics) + arXiv preprint.
- **Citation:** Huang, Y., Garrett, C. R., & Mueller, C. T. (2018). Automated sequence and motion planning for robotic spatial extrusion of 3D trusses. *Construction Robotics*, 2, 15–39. https://doi.org/10.1007/s41693-018-0012-z ; arXiv:1810.00998. Code: https://github.com/yijiangh/Choreo
- **What it is:** A CSP-based planner that finds a feasible extrusion order plus collision-free robot motions for arbitrary spatial trusses. Each partial assembly is a state; pruned by stability + collision constraints.
- **Why it matters:** Companion citation to Parascho — it makes the "assembly = constrained state-space search" framing fully explicit and machine-readable.
- **What to reuse:** The CSP formulation as a vocabulary for explaining *why* invalid puck configurations should be rejected at the FSM transition (e.g. "no overlapping footprints" is a hard constraint).
- **Limitations:** Targets robot motion planning, not human-paced interaction — but the framing transfers.

### Mitterberger, Dörfler, Sandy et al., 2020 — Augmented Bricklaying
- **Tier:** Peer-reviewed (Construction Robotics).
- **Citation:** Mitterberger, D., Dörfler, K., Sandy, T., Salveridou, F., Hutter, M., Gramazio, F., & Kohler, M. (2020). Augmented bricklaying: human–machine interaction for in situ assembly of complex brickwork using object-aware augmented reality. *Construction Robotics*, 4, 151–161. https://doi.org/10.1007/s41693-020-00035-8
- **What it is:** A handheld AR system that overlays target brick positions onto the in-progress wall, lets the bricklayer place mortar manually, and tracks each placed brick to update the next instruction. Validated on a winery facade in Greece.
- **Why it matters:** Closest published precedent for the team's *interaction loop*: physical objects placed by humans, visually augmented with the next-step target. Their state machine implicitly is "current_brick_index → expected_pose → place → confirm → next."
- **What to reuse:** The "object-aware" framing — the system updates instructions based on what was actually placed, not what was planned. The team's puck FSM should similarly key off detected ArUco positions, not assumed positions.
- **Limitations:** Tablet-based AR, not projection — but the interaction structure is directly transferable.

### Mitterberger et al., 2022 — Interactive Robotic Plastering (CHI)
- **Tier:** Peer-reviewed (ACM CHI 2022).
- **Citation:** Mitterberger, D. et al. (2022). Interactive Robotic Plastering: Augmented Interactive Design and Fabrication for On-site Robotic Plastering. *Proc. CHI 2022*. https://doi.org/10.1145/3491102.3501842
- **What it is:** A CHI paper where a designer paints in AR while a robot plasters in real time, with the design state explicitly tracked.
- **Why it matters:** Shows how to publish this kind of human-in-the-loop fabrication system in an HCI venue — useful template if the team wants to write up the installation later.
- **What to reuse:** Argumentation pattern (system contribution + study).
- **Limitations:** Mobile robot context; not directly comparable hardware-wise.

### EPFL IBOIS — Augmented Carpentry, 2025
- **Tier:** Practitioner / project page (peer-reviewed write-ups in progress).
- **Citation:** Settimi, A. et al. (2025). Augmented Carpentry. EPFL IBOIS. Project page: https://actu.epfl.ch/news/augmented-reality-improves-carpentry-ease-and-prec/ ; code: https://github.com/ibois-epfl/augmented-carpentry. **[journal version unverified]**
- **What it is:** Open-source AR system that mounts a tablet on standard hand tools (saw, drill) and projects cutting/drilling targets aligned to scanned timber. Sub-millimetre accuracy claimed.
- **Why it matters:** Same pattern as Augmented Bricklaying but lower-tech, on-tool. Reinforces that "AR overlay → manual action → re-detect → next step" is becoming a standard digital-fabrication idiom.
- **What to reuse:** Open-source codebase as a reference for pose tracking under a moving viewpoint.

### Block Research Group, ETH — Unfold Form / discrete-element shells, ongoing
- **Tier:** Project pages + AAG papers.
- **Citation:** Block Research Group, ITA, ETH Zurich. Project portfolio: http://block.arch.ethz.ch/ ; Unfold Form (2025): https://www.designboom.com/architecture/eth-zurich-lightweight-reusable-formwork-system-reduces-concrete-steel-construction-02-19-2025/ . Also: Parascho, S. et al. (2020). LightVault. *AAG 2020 Proceedings*. https://thinkshell.fr/wp-content/uploads/2019/10/AAG2020_18_Parascho.pdf
- **What it is:** Discrete-element vault and shell systems whose assembly order is non-trivial — they explicitly model which intermediate configurations are statically valid.
- **Why it matters:** Real-world architectural confirmation that "what counts as a valid intermediate" is a first-class design concern, not an afterthought.
- **What to reuse:** As a citation to demonstrate that the FSM framing isn't just a software pattern but mirrors how serious structural designers think about assembly.

### Derivative — TouchDesigner Table-Driven FSM (community asset)
- **Tier:** Practitioner.
- **Citation:** Derivative (community contribution). Table-Driven Finite State Machine (FSM). https://derivative.ca/community-post/asset/table-driven-finite-state-machine-fsm-manage-interactive-logic-cleanly-free
- **What it is:** A free TouchDesigner component that implements an FSM via Table DATs with Python callbacks for transition validation against hardware/sensor state.
- **Why it matters:** If TouchDesigner is the runtime, this is the idiomatic pattern. Even if the team uses Python/openFrameworks instead, the table-driven approach (states × events → next state) is a clean implementation target.
- **Limitations:** Community asset, no formal publication.

### Matthew Ragan — Custom Parameters and Cues case study
- **Tier:** Practitioner blog.
- **Citation:** Ragan, M. (2019). TouchDesigner Case Study: Custom Parameters and Cues. https://matthewragan.com/2019/05/06/touchdesigner-case-study-custom-parameters-and-cues/
- **What it is:** Detailed walkthrough of show-control architecture for an MFA installation ("{ remnants } of a { ritual }"), including cue lists and runtime stability.
- **Why it matters:** A concrete published precedent for treating an installation as a cue-driven state machine. Useful if the team writes up their installation as a project case.

### MadMapper / Resolume / HeavyM — practitioner ecosystem
- **Tier:** Practitioner / vendor docs.
- **Citation:** Comparison overview: https://studio-z.ca/3-best-projection-mapping-tools-you-need-to-know/ ; HeavyM https://www.heavym.net/ ; MadMapper https://madmapper.com/ ; Resolume https://resolume.com/
- **What it is:** The three dominant turnkey projection-mapping engines outside TouchDesigner. HeavyM = beginner / templates; MadMapper = mid-level / architectural mapping; Resolume Arena = live VJ / show control.
- **Why it matters:** These define the baseline that a reviewer will compare a custom TouchDesigner runtime against ("why didn't you just use MadMapper?"). The honest answer is that none of them ship with an LCA-data-driven FSM; they are renderers, not interactive logic engines.

## Deep-dive: Parascho's assembly-as-FSM framing

Parascho's 2019 thesis develops a method where two industrial robots cooperate to assemble spatial metal node structures *without scaffolding*: at any point during assembly, one robot acts as a temporary structural support while the other places the next member, and they hand off as the structure becomes self-supporting. The central computational claim is that the space of possible assembly sequences is enormous and combinatorial, but only a small subset of partial assemblies is *physically valid* — meaning statically stable under gravity and reachable by the two robots without collision. Her algorithms explore this constrained graph and return an ordered sequence of state-to-state transitions where every node is a checked, valid intermediate. This is, in everything but name, a finite state machine over partial assemblies, where transitions are gated by structural and kinematic predicates.

For the IAAC team, the analogy is direct even though the domain is different. Their interaction FSM (`IDLE → METHOD_SELECTED → FOOTPRINT_DEFINED → HEIGHT_SET → MATERIALS_CHOSEN → VALIDATED → PHASE_DISPLAY ×5 → BUILDING_COMPLETE → COMPARISON`) is similarly an enumeration of *valid* points in a much larger possible space of user actions. Just as Parascho's planner refuses transitions that would topple the structure, the installation must refuse transitions that would produce nonsensical LCA data (e.g. computing materials before the footprint is known). The team should cite Parascho not for *technical* reuse — they aren't planning robot motions — but as the precedent for treating "assembly" (whether of steel members or of a meaningful LCA scenario) as a constrained state-space traversal where invalid configurations are rejected by design rather than handled as runtime exceptions. The Choreo paper (Huang et al., 2018) is a useful companion citation because it makes the CSP formulation explicit and is easier to read than the dissertation itself.

## Camera-projector calibration: practical guidance from the literature

Three operational recommendations emerge from Bimber & Raskar (2005), Moreno & Taubin (2012), and the Brown structured-light course (mesh.brown.edu/desktop3dscan/):

1. **Mount everything rigidly before calibrating, and never move it.** Both projector and camera must be fixed to the same physical frame as the table; any post-calibration nudge invalidates the model.
2. **Use Moreno–Taubin Gray-code calibration with a printed checkerboard.** Capture the board in 10–20 poses spanning the table, projecting Gray-code patterns each time. The reference implementation at http://mesh.brown.edu/calibration/ and the modern OpenCV port `kamino410/procam-calibration` will both produce projector intrinsics + projector–camera extrinsics.
3. **Express both ArUco poses and projector output in a common table-plane frame.** Once the camera is calibrated against the projector and both are calibrated against the table plane (one ArUco board lying flat will do), the projector can paint accurately on top of any ArUco-detected puck. This is the minimum competence bar; the rest is graphics.

For top-down setups specifically, the camera and projector's optical axes are roughly parallel and near-vertical, which is the easy case for calibration — there is little parallax and the table plane is close to a fronto-parallel target.

## Cross-cutting themes

- **Valid intermediate states as a first-class concept.** Across Parascho, Choreo, BRG shells, and Augmented Bricklaying, the recurring move is to define and enforce what counts as a legitimate partial state. This is the through-line that justifies the team's FSM choice.
- **Object-aware feedback loops.** Augmented Bricklaying and Augmented Carpentry both close the loop on what the human actually did, not what they were told to do. The team's ArUco tracking should drive transitions, not just visualisation.
- **Projection as a sense-making medium, not decoration.** SAR (Bimber & Raskar) and Augmented Bricklaying treat projected light as the primary information channel about *what to do next*, with the physical world as the substrate. The LCA overlay should be designed in this spirit — readable, registered, and tied to user state.
- **Practitioner runtimes are renderers; logic is yours.** TouchDesigner, MadMapper, Resolume and HeavyM all assume you bring the interaction model. The published TouchDesigner FSM asset and Ragan's cue-driven case study are the closest things to "best practice" for installation logic.

## What's missing in this literature

- **No published study of projection-mapped *interactive* tabletop installations driven by LCA data.** The team's project sits in a genuine gap between SAR research (technical), construction robotics (practical), and museum/exhibition design (under-published academically).
- **Almost no peer-reviewed evaluation of TouchDesigner-as-runtime.** Most TouchDesigner literature is community-contributed; CHI/UIST papers describing TD-based systems usually treat it as plumbing rather than as an object of study.
- **Camera-projector calibration literature largely ignores top-down tabletop geometries.** The published methods work, but the parameter sweeps are biased toward stereo / scanning configurations.
- **FSM design for interactive installations is folkloric.** There's no canonical paper on "how to design an FSM for a museum-scale interactive" — game-programming references (gameprogrammingpatterns.com/state.html) are the closest analog.

## Direct recommendations for the team

1. **Cite Parascho 2019 as the conceptual anchor**, with full DOI, and explicitly note the analogy: structural validity → interaction validity. Don't oversell it as a technical inheritance; sell it as a framing inheritance.
2. **Add Huang et al. 2018 (Choreo)** as a companion — it makes the CSP/state-space formulation explicit and is more readable than the dissertation chapter.
3. **Cite Bimber & Raskar 2005** in the projection / display section for vocabulary and legitimacy.
4. **Use Moreno & Taubin 2012 + the Brown software** for actual calibration. Budget half a day for it.
5. **Cite Augmented Bricklaying (Mitterberger et al. 2020)** as the closest published interaction precedent, and explain the difference: the IAAC piece is *conceptual* (data overlay) where Augmented Bricklaying is *operational* (placement instruction). That contrast is the contribution.
6. **Implement the FSM with a table-driven pattern** (per the Derivative TouchDesigner asset or the equivalent in whatever runtime you choose). Keep transitions pure functions of `(current_state, event, world_state)` and reject invalid events explicitly — never silently.
7. **Write up the installation as a CHI Late-Breaking Work or TEI work-in-progress.** Mitterberger et al. 2022 (Interactive Robotic Plastering, CHI) is the template.

## Sources requiring verification

- **Parascho dissertation co-examiner:** Stelian Coros is reported in summaries as co-advisor / co-examiner; advisors of record (Gramazio + Kohler) are confirmed. Verify by direct PDF inspection of the front matter at https://www.research-collection.ethz.ch/handle/20.500.11850/364322 (the live page returned a server error during this review and should be retried).
- **Salvi, Pagès & Batlle 2004 DOI:** Citation is widely reproduced but the DOI was not directly fetched.
- **Augmented Carpentry peer-reviewed venue:** Project pages and EPFL news coverage are confirmed; the corresponding journal publication should be verified before formal citation.
- **All practitioner blog posts and project pages:** Acceptable as practitioner references but should be cited as such (not as peer-reviewed sources) and accessed-on dates recorded.
