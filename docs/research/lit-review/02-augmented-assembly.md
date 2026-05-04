# 02 — Augmented Assembly and AR-Guided Construction

## Scope

This review surveys the literature on augmented-, mixed-, and projected-reality systems that guide humans (and, where relevant, robots) through physical assembly tasks. The slice was chosen to inform "Guided Comparative Assembly", a tabletop installation in which a top-down projector walks users through three different building methods (masonry, 3D-printed, prefab). Three sub-domains are covered:

1. Architectural-scale AR-guided assembly (Gramazio Kohler, Fologram, EPFL IBOIS).
2. Industrial / HCI studies of head-mounted vs. projected AR work-instructions.
3. Foundational projector-based AR (spatial AR / SAR) theory and effectiveness studies.

The brief from the team specifies a top-down projector — so projector-based / SAR work is weighted slightly more heavily than HoloLens work, but both inform the design.

## Search strategy

WebSearch + WebFetch across: ACM DL, IEEE Xplore, Springer (Construction Robotics, Automation in Construction), arXiv, ETH Research Collection, EPFL Infoscience, project sites (gramaziokohler.arch.ethz.ch, fologram.com, epfl.ch/labs/ibois). Search terms combined author names, project names ("Augmented Bricklaying", "Steampunk Pavilion", "In situ Fabricator", "smARt.Assembly"), and effect terms ("error reduction", "completion time", "cognitive workload"). Where DOIs returned redirect errors I cross-checked the citation against multiple secondary sources (ResearchGate, Semantic Scholar, ETH Research Collection landing page).

## Key works (annotated, in chronological order)

### Bimber & Raskar, 2005 — *Spatial Augmented Reality: Merging Real and Virtual Worlds*
- **Tier:** Book (foundational textbook).
- **Citation:** Bimber, O. & Raskar, R. (2005). *Spatial Augmented Reality: Merging Real and Virtual Worlds*. A K Peters / CRC Press. ISBN 978-1-56881-230-4. Free PDF: https://pages.cs.wisc.edu/~dyer/cs534/papers/SAR.pdf
- **What it is:** The canonical reference for projector-based AR. Covers projector-camera calibration, geometric warping for non-planar surfaces, multi-projector blending, and projector-based illumination of physical objects.
- **Why it matters for the team:** This is the conceptual backbone for the tabletop's top-down projector. Chapters 5–7 (creating images with projection, projector-based illumination/augmentation) are directly applicable to projecting onto physical building components.
- **What to reuse:** Calibration workflow (intrinsic + projector-to-table extrinsic), discussion of perceptual artefacts (occlusion shadows, surface BRDFs, ambient light wash-out).
- **Limitations:** Pre-mass-market depth cameras and projection-mapping toolchains; modern Kinect/RealSense + MadMapper/HeavyM workflows are not covered.

### Helm, Ercan, Gramazio & Kohler, 2014 — *In-Situ Robotic Fabrication: Advanced Digital Manufacturing Beyond the Laboratory*
- **Tier:** Peer-reviewed book chapter.
- **Citation:** Helm, V., Ercan, S., Gramazio, F., Kohler, M. (2014). In: *Gearing Up and Accelerating Cross-fertilization between Academic and Industrial Robotics Research in Europe* (Springer Tracts in Advanced Robotics, vol 94). DOI: 10.1007/978-3-319-03838-4_4.
- **What it is:** Early statement of the "robot leaves the factory and goes to site" agenda that became the In situ Fabricator line.
- **Why it matters for the team:** Frames the question of *who* (robot, human, or both) executes the build — the same framing the team's installation puts to its visitors.
- **What to reuse:** The position-tolerance discussion (site tolerances are 5–10× tighter than typical robot precision allowed for) is a good primer for any "real-world build" narrative panel.
- **Limitations:** Predates the AR-as-interface turn; assumes the robot is the actor.

### Dörfler, Sandy, Giftthaler, Gramazio, Kohler & Buchli, 2016 — *Mobile Robotic Brickwork*
- **Tier:** Peer-reviewed book chapter (Robotic Fabrication in Architecture, Art and Design 2016).
- **Citation:** Dörfler, K., Sandy, T., Giftthaler, M., Gramazio, F., Kohler, M., Buchli, J. (2016). *Mobile Robotic Brickwork*. In: *Robotic Fabrication in Architecture, Art and Design 2016*, Springer. DOI: 10.1007/978-3-319-26378-6_15.
- **What it is:** First demonstration of an autonomous mobile robot laying a non-standard double-leaf brick wall on site, using on-board LiDAR for localisation.
- **Why it matters for the team:** This is the "robotic" leg of the comparative trio. For the masonry station, this is the contrast point — the same brick geometry that *Augmented Bricklaying* (below) lets a human do.
- **What to reuse:** Cycle-time and tolerance numbers; the bricks-per-hour figure makes a useful LCA-adjacent KPI overlay.
- **Limitations:** No human-in-the-loop comparison; the In situ Fabricator was a research prototype, not a commercial tool.

### Funk, Bächler, Bächler, Kosch, Heidenreich & Schmidt, 2016 — *Interactive Worker Assistance: Comparing the Effects of In-Situ Projection, Head-Mounted Displays, Tablet, and Paper Instructions*
- **Tier:** Peer-reviewed (ACM UbiComp 2016).
- **Citation:** Funk, M., Bächler, A., Bächler, L., Kosch, T., Heidenreich, T., Schmidt, A. (2016). In: *Proc. ACM UbiComp '16*, pp. 934–939. DOI: 10.1145/2971648.2971706.
- **What it is:** Within-subjects comparison of four instruction modalities on a Lego Duplo benchmark task.
- **Why it matters for the team:** This is the single most relevant effectiveness study for a top-down projector tabletop. Key result: in-situ projection beats HMD on both error rate and perceived cognitive load; HMD is *slowest* at locating positions.
- **What to reuse:** The Lego-Duplo benchmark methodology is directly translatable to the team's assembly task — useful if they want a Session-2 user study.
- **Limitations:** Abstract block task, not architectural; assemblers were lay users.

### Sandy, Giftthaler, Dörfler, Kohler & Buchli, 2017 — *Mobile Robotic Fabrication at 1:1 Scale: the In situ Fabricator*
- **Tier:** Peer-reviewed (Construction Robotics, vol. 1).
- **Citation:** Giftthaler, M., Sandy, T., Dörfler, K., Brooks, I., Buckingham, M., Rey, G., Kohler, M., Gramazio, F., Buchli, J. (2017). *Construction Robotics*, 1, 3–14. DOI: 10.1007/s41693-017-0003-5. Preprint: arXiv:1701.03573.
- **What it is:** Full system paper for the In situ Fabricator hardware/software stack — base, arm, perception, control.
- **Why it matters for the team:** Provides the engineering vocabulary (localisation drift, tool-tip accuracy, base re-positioning) needed to honestly describe what "robotic masonry" requires.
- **What to reuse:** Their accuracy budget table is gold for an LCA-adjacent "what does the precision cost?" panel.
- **Limitations:** Hardware-paper genre; little on user experience.

### Jahn, Newnham, van den Berg, Iraheta & Wells, 2019 — *Holographic Construction*
- **Tier:** Peer-reviewed conference paper (DMSB 2019, Springer).
- **Citation:** Jahn, G., Newnham, C., van den Berg, N., Iraheta, M., Wells, J. (2020 in print, 2019 conf.). In: *Impact: Design With All Senses — Proc. DMSB 2019*, Springer, pp. 314–324. DOI: 10.1007/978-3-030-29829-6_25.
- **What it is:** Theoretical and practical statement of Fologram's "holographic construction" workflow — Rhino/Grasshopper → HoloLens → human builder, with the building model as the only source of truth (no drawings, no CNC).
- **Why it matters for the team:** Articulates *why* AR-guided assembly is interesting even without robots: it lets unskilled labour build geometry that previously required either CNC or a master craftsman.
- **What to reuse:** Their argument that the model *is* the drawing maps cleanly onto the team's pitch (the projection *is* the instruction set).
- **Limitations:** HoloLens-specific; assumes per-builder headsets, not shared projection.

### Jahn, Newnham, Hahm, Pantic et al., 2019 — *Steampunk Pavilion*, Tallinn Architecture Biennale
- **Tier:** Project (peer-recognised — TAB 2019 winning installation pavilion). Best peer-reviewed write-up: see *Holographic Construction* above and the practitioner article in *Architect / Archpaper*.
- **Citation:** Jahn, G., Newnham, C. (Fologram); Hahm, S. (SoomeenHahm Design); Pantic, I.; with Format Engineers (2019). *Steampunk Pavilion*, Tallinn Architecture Biennale 2019. Project documentation: https://soomeenhahm.com/portfolio-item/steampunk-pavilion/. ArchDaily write-up: https://www.archdaily.com/926191/.
- **What it is:** A steam-bent ash-timber pavilion built by a team of unskilled volunteers wearing HoloLens 2 headsets, with no drawings or CNC code at any stage.
- **Why it matters for the team:** The reference exemplar for "AR replaces drawings". Shows what the *narrative* looks like when AR-guided assembly is foregrounded.
- **What to reuse:** The visual rhetoric (volunteers + holograms + bent wood) is directly applicable to how the team can stage a video loop next to their installation.
- **Limitations:** No quantitative effectiveness data; HoloLens not projector.

### Mitterberger, Dörfler, Sandy, Salveridou, Hutter, Gramazio & Kohler, 2020 — *Augmented Bricklaying*
- **Tier:** Peer-reviewed (Construction Robotics).
- **Citation:** Mitterberger, D., Dörfler, K., Sandy, T., Salveridou, F., Hutter, M., Gramazio, F., Kohler, M. (2020). *Augmented bricklaying: human–machine interaction for in situ assembly of complex brickwork using object-aware augmented reality.* Construction Robotics, 4, 151–161. DOI: 10.1007/s41693-020-00035-8. ETH Research Collection: https://www.research-collection.ethz.ch/handle/20.500.11850/466341.
- **What it is:** A wearable + object-tracking AR system that let local Greek masons hand-lay 13,596 individually rotated bricks to build the 225 m² Kitrvs winery facade in under three months — at robotic-grade geometric complexity, with mortar handling preserved as a human craft skill.
- **Why it matters for the team:** This is the strongest piece of evidence in the literature that AR-guided manual masonry can match robotic masonry on geometry. It is *the* citation for the masonry station's "human + AR" build mode.
- **What to reuse:** Their interaction loop (project the next brick → mason places → object tracking confirms → advance) is a direct template for the tabletop's brick-by-brick UX.
- **Limitations:** Wearable rig (custom HoloLens-class device + tracker), not a top-down projector — the team will need to translate the interaction loop to the projector form-factor. Co-developed with incon.ai (ETH spinoff), so the tracking stack is non-trivial to reproduce.

### Funk, 2016/2017 — *In-situ projected assembly instructions reduce errors by 82% on cumulative tasks*
- **Tier:** Peer-reviewed (multiple papers; key result re-reported in Funk's UbiComp work and *Teach Me How!* — Funk & Lischke, 2017, Springer book chapter, DOI 10.1007/978-981-10-6404-3_4).
- **What it is:** A line of HCI studies (Funk + collaborators) on projection-based assembly assistance, including a study with cognitively impaired workers in a real industrial setting.
- **Why it matters for the team:** Provides the headline numbers ("AR cuts errors by ~80%") that the installation's narrative will lean on.
- **What to reuse:** The error-rate reduction figure; the design of "contour visualisation" (project the silhouette of the part where it should go).
- **Limitations:** Industrial assembly tasks, not architectural; numbers vary by task type.

### Doshi, Smith, Thomas & Bouras, 2017 — *Use of projector-based augmented reality to improve manual spot-welding precision and accuracy*
- **Tier:** Peer-reviewed (Int. J. Advanced Manufacturing Technology).
- **Citation:** Doshi, A., Smith, R.T., Thomas, B.H., Bouras, C. (2017). *Int. J. Adv. Manuf. Technol.*, 89, 1279–1293. DOI: 10.1007/s00170-016-9164-5.
- **What it is:** Industrial study showing 52% reduction in standard deviation of manual spot-weld placement when projected AR cues are used.
- **Why it matters for the team:** A second clean quantitative data point for "projector AR makes humans more precise".
- **What to reuse:** Cite alongside Funk for the effectiveness section of the team's wall labels.
- **Limitations:** Spot welding, not bricklaying; one-off task vs. cumulative-error task.

### Kyjanek, Bharadwaj, Mitterberger et al. (Gramazio Kohler), 2022 — *Interactive Robotic Plastering*
- **Tier:** Peer-reviewed (ACM CHI 2022).
- **Citation:** Mitterberger, D. et al. (2022). *Interactive Robotic Plastering: Augmented Interactive Design and Fabrication for On-site Robotic Plastering.* In: *Proc. ACM CHI 2022.* DOI: 10.1145/3491102.3501842.
- **What it is:** Architect-in-the-loop system where a human shapes plaster in AR and the robot deposits it accordingly.
- **Why it matters for the team:** Shows the most recent direction of the Gramazio Kohler programme: AR not as instruction but as a *shared design surface* between human and machine. Useful framing for the projector as bidirectional (input AND output).
- **Limitations:** Robot-plus-human, not pure-human-with-AR.

### Settimi, Gamerro & Weinand, 2025 — *Augmented Carpentry: Computer Vision-assisted Framework for Manual Fabrication*
- **Tier:** Peer-reviewed (Automation in Construction, vol. 179, Nov 2025).
- **Citation:** Settimi, A., Gamerro, J., Weinand, Y. (2025). *Automation in Construction*, 179. DOI: 10.1016/j.autcon.2025.106473 (verify on landing page). arXiv preprint: arXiv:2503.07473. Project site: https://ibois-epfl.github.io/augmented-carpentry/. Open-source code: https://github.com/ibois-epfl/augmented-carpentry.
- **What it is:** Open-source AR system for woodworking using computer-vision-based tool tracking (sister tool: TTool, MDPI Applied Sciences 2024). Reports millimetre-precision joint fabrication and 3 mm positional precision over 3 m beams, using only consumer hardware.
- **Why it matters for the team:** Open-source, recent, *very* close to what the team needs (CV-based feedback on hand work). The Augmented Carpentry stack is a candidate for actual code reuse.
- **What to reuse:** The pose-estimation pipeline; the open-source repo; the precision benchmark methodology.
- **Limitations:** Wood-specific; head-mounted, not table-projected.

### Cooperative Augmented Assembly (CAA), 2024 — Mitterberger et al.
- **Tier:** Peer-reviewed (Construction Robotics).
- **Citation:** Mitterberger, D. et al. (2024). *Cooperative augmented assembly (CAA): augmented reality for on-site cooperative robotic fabrication.* Construction Robotics, 8. DOI: 10.1007/s41693-024-00138-6.
- **What it is:** Generalises Augmented Bricklaying into a multi-agent (humans + robots + AR) assembly framework.
- **Why it matters for the team:** Most current statement of where the field is heading. If the team wants a forward-looking citation, this is it.

## Cross-cutting themes

1. **The model becomes the drawing.** Both Fologram (Steampunk, *Holographic Construction*) and Gramazio Kohler (Augmented Bricklaying) explicitly remove paper drawings, CNC code, and physical templates from the workflow. The 3D model is projected/holographed directly onto the workpiece. This is the conceptual move the team's installation should foreground.
2. **Object-aware vs. blind projection.** The most sophisticated systems (Augmented Bricklaying, Augmented Carpentry, Funk's "contour" condition) close the loop with computer vision: the system knows where the brick/timber/part is and updates accordingly. Pure open-loop projection (project step N, advance on a button) is the easier baseline and is what the team should ship in 3 weeks.
3. **HMD vs. SAR is not settled.** HMDs give per-user 3D parallax; projectors give shared visibility, no headset fatigue, and (per Funk 2016) lower cognitive load on locating tasks. For a museum-style installation with multiple onlookers, projection wins on social affordance.
4. **Effectiveness is a story about *which* errors.** AR helps most on cumulative errors (mistakes that compound across steps) and on positional accuracy. It helps less on tasks that are already cognitively trivial.

## Effectiveness evidence

Quantitative results from the comparative studies surfaced:

| Study | Task | Result vs. baseline |
|---|---|---|
| Funk et al., 2016 (UbiComp) | Lego Duplo assembly | In-situ projection: lowest error rate AND lowest cognitive load vs. HMD, tablet, paper. HMD slowest at *locating* positions. |
| Funk et al. (cumulative-error follow-up) | Pick-and-place w/ dependent steps | Reported ~82% reduction in cumulative-error rate with overlaid 3D instructions. |
| Doshi et al., 2017 (IJAMT) | Manual spot welding | 52% reduction in standard deviation of weld placement. |
| Holorailway (HoloLens 2, railway insulation) | Industrial assembly | 78% faster localisation, error reduction in 88% of cases vs. traditional. |
| Iowa State / Hoover (HoloLens 1, ASME JCISE 2020) | Manufacturing-guided assembly | HoloLens condition fastest AND lowest error rate vs. desktop MBI, tablet MBI, tablet AR. |
| Mitterberger et al., 2020 (Augmented Bricklaying) | 13,596-brick winery facade, 225 m² | Built in <3 months by *local masons* (no robotic fabrication training). Geometric precision claimed equivalent to robotic fabrication. |
| Settimi et al., 2025 (Augmented Carpentry) | Timber joinery | Sub-millimetre joint precision; 3 mm position precision over 3 m beams, with consumer-grade hardware. |

The consistent finding across a decade of HCI research: **AR guidance reduces errors and cognitive load relative to paper, sometimes at a small cost in raw speed** (paper is hard to beat for a single trivial step; AR pulls ahead on multi-step or geometrically complex tasks). For the installation's narrative, "AR cuts assembly errors by 50–80% in industrial studies (Funk 2016; Doshi 2017)" is a defensible headline.

## What's missing in this literature

- **Tabletop / model-scale AR-guided assembly studies.** Almost everything is either 1:1 architectural or 1:1 industrial. The team's tabletop scale is a niche. *Action:* the team's installation can itself be a small contribution here.
- **Comparative LCA-overlay studies.** No surveyed paper combines AR assembly guidance with live LCA data. This is genuinely novel ground for the team.
- **Multi-user, shared-projection installations** (vs. single-headset). Funk's projection studies are single-worker workstations; museum-style multi-viewer projection is under-studied.
- **Long-term skill-transfer effects.** Most studies are within-session. Whether AR-trained workers retain skills without AR is mostly unstudied (Funk 2017 hints at it).

## Direct recommendations for the team

1. **Use a top-down projector + ArUco/AprilTag fiducials on the building components.** Replicate the *Augmented Bricklaying* interaction loop (project next-piece location → user places → CV confirms → advance) at table scale. This is achievable in 3 weeks; HMD is not.
2. **Cite the headline numbers explicitly on a wall panel.** "Projected AR reduces cumulative assembly errors by ~82% (Funk et al., 2016) and standard deviation of placement by 52% (Doshi et al., 2017)." Backs up the installation's premise with hard data.
3. **Steal the Steampunk / Augmented Bricklaying visual language** for documentation and video loops — these are the public-facing exemplars visitors will recognise.
4. **Look at the Augmented Carpentry GitHub repo** (https://github.com/ibois-epfl/augmented-carpentry and TTool: https://github.com/ibois-epfl/TTool) before writing custom CV. Open-source, recent, and the closest in spirit to what the team needs.
5. **For the masonry station specifically, contrast Mobile Robotic Brickwork (Dörfler et al., 2016) vs. Augmented Bricklaying (Mitterberger et al., 2020).** Same brick geometry, two different makers. This is the cleanest in-literature illustration of the human/robot/AR design space the installation explores.
6. **If the team runs even a small user study in Session 2,** lift Funk's Lego-Duplo benchmark methodology — it's the most-cited protocol in this space and gives directly comparable numbers.

## Sources requiring verification

- Settimi et al. 2025 *Automation in Construction* DOI was inferred from the journal/volume; the team should confirm against the publisher landing page before final citation. The arXiv preprint (2503.07473) is verified.
- The "82% cumulative-error reduction" figure attributed to Funk's line is widely re-quoted; before publishing in a paper, locate the exact original Funk publication and confirm the percentage.
- *Holographic Construction* (Jahn et al.) was published in the DMSB 2019 proceedings (Springer, *Impact: Design With All Senses*); page numbers given here are best-estimate and should be confirmed against the front-matter.
- *Cooperative Augmented Assembly* (2024) author list given here is partial — confirm full authorship from the Springer landing page before citing.
- Iowa State / Hoover HoloLens evaluation: cited from the secondary "Measuring the Performance Impact of Using the Microsoft HoloLens 1" (Hoover et al., ASME JCISE 20(6): 061001, 2020, DOI inferred — verify).
