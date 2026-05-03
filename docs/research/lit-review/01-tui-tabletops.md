# 01 — TUI and Fiducial-Tracked Tabletops

> Slice of the lit review covering the TUI lineage that the team's interaction model — pucks + overhead camera + top-down projector — descends from.

## Scope

This slice covers the canonical works in tangible user interfaces (TUIs) and fiducial-tracked tabletops that defined the interaction grammar the "Guided Comparative Assembly" installation will use: physical tokens placed on a flat surface, recognized by a camera (visible-light or IR), with computational state projected back onto/around the tokens. **In scope:** Ishii's MIT Tangible Media Group lineage, the reacTable / reacTIVision toolchain, the ArUco / ARToolKit / ARTag fiducial marker lineage, multi-user tabletop hardware (DiamondTouch, Microsoft Surface/PixelSense), Sifteo, and recent (2018–2025) academic work using fiducial-tracked tabletops for education and decision support. **Out of scope (covered by other slices):** projection-mapping pipelines, LCA tools and data sources, and physical fabrication of the table itself.

## Search strategy

- **Databases:** ACM Digital Library (DOI lookup), IEEE Xplore (fiducial tracking papers), Semantic Scholar (citation traces), Google Scholar (snowball from canonical works), tangible.media.mit.edu and modin.yuri.at (Tangible Media Group and Kaltenbrunner project pages).
- **Date range:** 1997 (Ishii & Ullmer "Tangible Bits") through 2025.
- **Keyword sets:** "tangible bits", "tangible user interface", "fiducial marker", "reacTIVision", "reacTable", "ArUco", "ARToolKit", "ARTag", "DiamondTouch", "PixelSense", "Sifteo / Siftables", "TUIO protocol", and modifier terms ("urban planning", "education", "decision support", "configurator", "LCA tabletop").
- **Excluded:** AR HMD literature, capacitive multi-touch without object tracking, and shape-display/actuated TUI work beyond a single canonical reference (Radical Atoms, inFORM) since the team's project is a passive-token + projection setup.

## Key works (annotated, in chronological order)

### Ishii & Ullmer, 1997 — "Tangible Bits: Towards Seamless Interfaces between People, Bits and Atoms"

- **Tier:** peer-reviewed conference (CHI '97)
- **Citation:** Ishii, H., & Ullmer, B. (1997). Tangible bits: towards seamless interfaces between people, bits and atoms. In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '97)*, 234–241. ACM. https://doi.org/10.1145/258549.258715
- **What it is:** The vision paper that named and framed Tangible User Interfaces — coupling physical artifacts to digital state so the body and the room become part of the interface.
- **Why it matters for the team:** This is the canonical citation that legitimizes the entire interaction premise of the installation. Cite it once in any project text as the lineage origin.
- **What to reuse:** The conceptual framing of "graspable representation + ambient display." The team's pucks-as-handles-for-construction-methods is exactly this pattern.
- **Limitations:** It is a vision paper, not a how-to. No technical detail transfers; everything operational is in later work.

### Underkoffler & Ishii, 1999 — "Urp: A Luminous-Tangible Workbench for Urban Planning and Design"

- **Tier:** peer-reviewed conference (CHI '99)
- **Citation:** Underkoffler, J., & Ishii, H. (1999). Urp: a luminous-tangible workbench for urban planning and design. In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '99)*, 386–393. ACM. https://doi.org/10.1145/302979.303114
- **What it is:** Top-down projection onto physical building models on a workbench — shadows, wind simulation, reflectivity all rendered in real time as users move models.
- **Why it matters for the team:** This is the closest direct ancestor of "Guided Comparative Assembly." Same I/O loop (physical objects → overhead sensing → projected feedback), same domain (architecture/urbanism), same audience scenario (small group around a table).
- **What to reuse:** The "tool token" pattern (a wand object that *changes mode* — wind, time-of-day, material). The team can use a special puck to swap which LCA dimension is foregrounded (CO₂ vs cost vs labor vs time).
- **Limitations:** Used custom IR-sensed pucks, not vision-detected fiducials; their hardware stack does not transfer.

### Piper, Ratti & Ishii, 2002 — Illuminating Clay / SandScape

- **Tier:** peer-reviewed conference (CHI '02 for Illuminating Clay) + project page
- **Citation:** Piper, B., Ratti, C., & Ishii, H. (2002). Illuminating clay: a 3-D tangible interface for landscape analysis. In *Proceedings of CHI '02*, 355–362. ACM. https://doi.org/10.1145/503376.503439. SandScape project page: https://tangible.media.mit.edu/project/sandscape/
- **What it is:** Continuous-form TUIs where a deformable substrate (clay, glass beads) is sensed and overlaid with GIS analysis (slope, drainage, shadow).
- **Why it matters for the team:** Demonstrates that the projected analytical layer is the persuasive part — the physical substrate is just an interface. Reinforces "let the projection carry the cognitive payload."
- **What to reuse:** Visual idiom for projected analytic overlays (heatmaps, flow lines, contour shading) on a tabletop substrate.
- **Limitations:** Not fiducial-based; not directly transferable to a discrete-token interaction model.

### Kato & Billinghurst, 1999 — ARToolKit (the fiducial ancestor)

- **Tier:** peer-reviewed workshop (IWAR '99)
- **Citation:** Kato, H., & Billinghurst, M. (1999). Marker tracking and HMD calibration for a video-based augmented reality conferencing system. In *Proceedings of the 2nd IEEE and ACM International Workshop on Augmented Reality (IWAR '99)*, 85–94. https://doi.org/10.1109/IWAR.1999.803809
- **What it is:** First widely adopted square-fiducial AR marker library. Defined the visual format (black border, ID inside) that ArUco still uses.
- **Why it matters for the team:** Historical context only — the team will use ArUco. Cite as "lineage."
- **What to reuse:** Nothing operational. Use ArUco directly.
- **Limitations:** Older detector, less robust to lighting, no formal dictionary distance guarantees.

### Bencina, Kaltenbrunner & Jordà, 2005 — reacTIVision + the reacTable line

- **Tier:** peer-reviewed conference (IEEE CVPR Workshops '05; later TEI '07; CACM 2010)
- **Citations:**
  - Bencina, R., Kaltenbrunner, M., & Jordà, S. (2005). Improved topological fiducial tracking in the reacTIVision system. In *2005 IEEE CVPR Workshops*, vol. 3, 99. https://doi.org/10.1109/CVPR.2005.475
  - Jordà, S., Geiger, G., Alonso, M., & Kaltenbrunner, M. (2007). The reacTable: exploring the synergy between live music performance and tabletop tangible interfaces. In *Proceedings of TEI '07*, 139–146. ACM. https://doi.org/10.1145/1226969.1226998
  - Project: https://reactivision.sourceforge.net/ ; https://www.upf.edu/web/mtg/reactable
- **What it is:** reacTIVision is the open-source CV framework that tracks "amoeba" topological fiducials on a translucent table from below; reacTable is the modular synthesizer that famously sits on top of it (Björk, *Volta* tour, 2007).
- **Why it matters for the team:** This is the *most direct precedent* for an installation that uses fiducial-tracked pucks on a table to drive a real-time visualization. It is also almost certainly the lineage of the "Swiss museum DJ table" the team cites. The reacTable is on permanent display at multiple European science museums (e.g. ZKM Karlsruhe, Game Science Center Berlin) — see "Sources requiring verification" below.
- **What to reuse:** The interaction grammar (proximity = connection, rotation = parameter, finger gestures alongside tokens). Also TUIO (see below) as a clean abstraction layer if the team wants to decouple sensing from rendering.
- **Limitations:** reacTable uses *rear* projection through a translucent surface with a camera underneath. The team is doing *top-down* projection with an overhead camera, which is mechanically simpler but introduces hand-occlusion issues that reacTable avoids.

### Kaltenbrunner et al., TUIO protocol (2005, 2018)

- **Tier:** peer-reviewed conference + journal (GW '05; ACM EICS / PACMHCI 2018)
- **Citations:**
  - Kaltenbrunner, M., Bovermann, T., Bencina, R., & Costanza, E. (2005). TUIO: a protocol for table-top tangible user interfaces. In *Proceedings of the 6th International Workshop on Gesture in Human-Computer Interaction and Simulation*. https://modin.yuri.at/publications/tuio_gw2005.pdf
  - Kaltenbrunner, M., & Echtler, F. (2018). The TUIO 2.0 Protocol: An Abstraction Framework for Tangible Interactive Surfaces. *Proceedings of the ACM on Human-Computer Interaction*, 2 (EICS), Article 8. https://doi.org/10.1145/3229090
- **What it is:** Open OSC-based protocol that decouples object/touch sensing from application logic — a de-facto standard in TUI work.
- **Why it matters for the team:** If the team builds even a small abstraction between OpenCV/ArUco detection and the projection app, TUIO is the right shape. Lots of clients exist (Processing, openFrameworks, Unity, p5).
- **What to reuse:** Either TUIO directly, or its message vocabulary as inspiration for the team's own JSON event stream.
- **Limitations:** Adds a layer; for a 3-week build with a single application, sending Python dicts straight into the renderer is fine.

### Dietz & Leigh, 2001 — DiamondTouch

- **Tier:** peer-reviewed conference (UIST '01) — UIST Lasting Impact Award
- **Citation:** Dietz, P., & Leigh, D. (2001). DiamondTouch: a multi-user touch technology. In *Proceedings of UIST '01*, 219–226. ACM. https://doi.org/10.1145/502348.502389
- **What it is:** Capacitive multi-user table that distinguished *which user* was touching where via per-user receivers.
- **Why it matters for the team:** Establishes that multi-user co-located interaction needs an answer to "whose action is this?" The team's pucks have unique IDs but no per-user identity — worth thinking about whether assigning pucks to participants matters.
- **What to reuse:** Conceptual: think about turn-taking and ownership in a small-group installation.
- **Limitations:** Hardware is obsolete and was never about tokens.

### Microsoft Surface / PixelSense, 2007–2012

- **Tier:** product / industry — supplement with Wikipedia and contemporary press
- **Citation:** Microsoft Surface 1.0 announced 30 May 2007 (D5 conference); later rebranded PixelSense in 2012. Reference: https://en.wikipedia.org/wiki/Microsoft_PixelSense
- **What it is:** Commercial tabletop with rear-projection + IR-camera object recognition (byte-tag stickers on object undersides).
- **Why it matters for the team:** Proves the consumer-grade viability of fiducial-on-puck tabletops; useful for design references (UX patterns for placing/removing objects, contextual menus around objects).
- **What to reuse:** Object-attached menu/halo affordances — projecting a UI ring around each puck is a well-validated pattern.
- **Limitations:** Closed platform, discontinued. No code reuse.

### Merrill, Kalanithi & Maes, 2007 — Siftables (later Sifteo Cubes)

- **Tier:** peer-reviewed conference (TEI '07)
- **Citation:** Merrill, D., Kalanithi, J., & Maes, P. (2007). Siftables: towards sensor network user interfaces. In *Proceedings of TEI '07*, 75–78. ACM. https://doi.org/10.1145/1226969.1226984
- **What it is:** Small wireless cubes with screens and accelerometers — the tokens themselves are smart.
- **Why it matters for the team:** Counter-example. Siftables put the display *in* the token; the team is putting it *around* the token via projection. Useful comparison when articulating why projection beats embedded screens for a 3-week budget (cheaper, fewer batteries, single rendering surface).
- **Limitations:** Not directly applicable to a vision-tracked passive-token system.

### Weiss et al., 2009 — SLAP Widgets

- **Tier:** peer-reviewed conference (CHI '09)
- **Citation:** Weiss, M., Wagner, J., Jansen, Y., Jennings, R., Khoshabeh, R., Hollan, J. D., & Borchers, J. (2009). SLAP widgets: bridging the gap between virtual and physical controls on tabletops. In *Proceedings of CHI '09*, 481–490. ACM. https://doi.org/10.1145/1518701.1518779
- **What it is:** Translucent silicone/acrylic sliders, knobs, and keyboards placed on a multi-touch table; relabeled dynamically by rear projection through the widget body.
- **Why it matters for the team:** Direct precedent for "passive physical control whose label/affordance is reprojected at runtime." If the team wants any continuous control (e.g., a knob to scrub through assembly time), SLAP shows how.
- **What to reuse:** The pattern of physical affordance + projected label. For the team, this could mean: a puck *could* have an arrow notch on top, and the projection labels which option that arrow currently points at.
- **Limitations:** Requires translucent widgets; doesn't fit the team's described opaque pucks.

### Hilliges et al., 2007 — PhotoHelix

- **Tier:** peer-reviewed conference (IEEE Tabletop / ITS-precursor 2007)
- **Citation:** Hilliges, O., Baur, D., & Butz, A. (2007). Photohelix: Browsing, sorting and sharing digital photo collections. In *Second IEEE Tabletop Workshop on Tabletop Computing Systems*, 87–94. IEEE. https://doi.org/10.1109/TABLETOP.2007.18
- **What it is:** A spiral time-based browser for photo collections, controlled by a hacked physical knob (an IKEA timer with a wireless mouse inside).
- **Why it matters for the team:** Excellent low-budget pattern for a single-purpose physical control built from off-the-shelf parts in days. The team is operating under similar time pressure.
- **What to reuse:** The "hack a cheap mechanical input device with whatever sensor we already own" mindset. Worth mentally bookmarking if any LCA dimension needs continuous adjustment.
- **Limitations:** Not vision-tracked; one-off hardware.

### Garrido-Jurado et al., 2014 — ArUco

- **Tier:** peer-reviewed journal (Pattern Recognition)
- **Citation:** Garrido-Jurado, S., Muñoz-Salinas, R., Madrid-Cuevas, F. J., & Marín-Jiménez, M. J. (2014). Automatic generation and detection of highly reliable fiducial markers under occlusion. *Pattern Recognition*, 47(6), 2280–2292. https://doi.org/10.1016/j.patcog.2014.01.005
- **What it is:** The paper behind the ArUco library the team is using. Provides configurable marker dictionaries with provable inter-marker Hamming distance and an occlusion-robust detection pipeline.
- **Why it matters for the team:** This *is* the team's tracking layer. Cite this when the project doc says "we use ArUco markers."
- **What to reuse:** Use OpenCV's `cv2.aruco` module (which ships this algorithm). Pick a small dictionary (`DICT_4X4_50` or `DICT_5X5_50`) so the markers stay readable at the team's expected camera resolution and puck size. Generate markers at https://chev.me/arucogen/.
- **Limitations:** Marker design is functional, not pretty — for an installation aimed at the public, the team will probably want to laminate or recess markers under the puck base so they don't dominate the visual.

### Ishii et al., 2012 — Radical Atoms (and Follmer/Leithinger 2013 — inFORM)

- **Tier:** magazine article (ACM Interactions) + peer-reviewed conference (UIST '13)
- **Citations:**
  - Ishii, H., Lakatos, D., Bonanni, L., & Labrune, J.-B. (2012). Radical atoms: beyond tangible bits, toward transformable materials. *Interactions*, 19(1), 38–51. https://doi.org/10.1145/2065327.2065337
  - Follmer, S., Leithinger, D., Olwal, A., Hogge, A., & Ishii, H. (2013). inFORM: dynamic physical affordances and constraints through shape and object actuation. In *Proceedings of UIST '13*, 417–426. ACM. https://doi.org/10.1145/2501988.2502032
- **What it is:** The forward edge of the lineage — surfaces that physically actuate under software control.
- **Why it matters for the team:** Useful as a "where the field is going" footnote and as honest framing of the team's own work as "passive-token + projection," i.e. a deliberately constrained, achievable slice of the larger TUI vision.
- **Limitations:** Wildly out of scope for a 3-week build.

### Recent (2018–2025) work — fiducial-tracked tabletops for education / decision support

- **ArUcoTUI toolkit (TEI '25):** A software toolkit for prototyping tangible interactions on flat-panel displays using ArUco + OpenCV, with an evaluation in a university classroom. Citation/URL: https://dl.acm.org/doi/10.1145/3731459.3779317. **Why it matters:** Most directly comparable contemporary toolkit to what the team is building. The team should look at what ArUcoTUI exposes as its event API and copy what works.
- **Maquil et al., 2018 — Geospatial TUIs in collaborative urban planning:** Maquil, V., Tobias, E., De Sousa, L., Schwartz, L., & Zephir, O. (2018). Towards a framework for geospatial tangible user interfaces in collaborative urban planning. *Journal of Geographical Systems*, 20(2), 185–206. https://doi.org/10.1007/s10109-018-0265-6. **Why it matters:** Same domain pattern (tokens-on-table for spatial decisions), uses reacTIVision + TUIO + a GIS backend. Confirms that this interaction style maps cleanly onto multi-criteria decision tasks — which is exactly LCA.
- **COPSE (PACMHCI 2017):** Tissoires, B. et al. — software framework for instantiating problem-solving "microworlds" on tangible tabletops. https://doi.org/10.1145/3095808. **Why it matters:** Relevant as a precedent for *educational* tangible tabletops, which is the team's framing.

## Cross-cutting themes

1. **Two stable hardware archetypes.** Every system in this lineage is either (a) rear-projection through a translucent table with a camera underneath (reacTable, Microsoft Surface, SLAP) or (b) top-down projection with an overhead camera (Urp, most recent ArUco-based work). The team is choosing (b), which is mechanically and budgetarily easier but trades robustness — hand occlusion of both the camera and the projector matters.
2. **Tokens carry identity and pose; projection carries information.** Across 25 years, the consistent division of labor is: the physical object encodes *what* and *where*, the projected layer encodes *meaning, state, and feedback*. The team should resist any temptation to put labels on the pucks themselves; let the projection do that work so you can change it.
3. **Open toolchain has consolidated.** From custom IR sensing (Urp), to Anoto pens, to ARToolKit/ARTag, to reacTIVision amoebas, to ArUco — the field has converged on ArUco + OpenCV as the default. The team is on the well-trodden path.
4. **The interaction is social.** Every successful tabletop in this lineage works because multiple people stand around it. The team's installation should be designed for 2–4 simultaneous users, not one-at-a-time interaction.

## What's missing in this literature

- **LCA / construction-method comparison as a domain is essentially absent from the TUI tabletop literature.** Urban-planning TUIs exist; landscape-analysis TUIs exist; educational TUIs exist; but tangible interfaces specifically for comparing the embodied carbon, cost, and labor of building methods do not appear in the searches conducted. This is the team's defensible novelty claim.
- **Project-process visualization on a TUI is also rare.** Most tabletops show *state* (the city now, the landscape now). Showing a *time-evolving construction process* (assembly steps unfolding) on a tabletop is uncommon and is a second novelty hook.
- **Public-installation ergonomics for a top-down ArUco rig** are barely documented in published work — most academic ArUco-tabletop papers are lab prototypes. The team will probably learn things worth writing up.

## Direct recommendations for the team

1. **Use OpenCV's `cv2.aruco` directly** with `DICT_4X4_50` or `DICT_5X5_50`. Generate markers at https://chev.me/arucogen/ . Cite Garrido-Jurado et al. 2014.
2. **Position your work explicitly downstream of Urp (1999) and reacTable (2005/2007).** These two citations alone justify almost every interaction choice. Add ArUcoTUI (2025) as the contemporary reference point.
3. **Decide top-down vs rear-projection now and don't waver.** You said top-down. Then plan for hand-occlusion: place the overhead camera and projector at slight offsets so a hand blocking one rarely blocks the other; consider an IR camera + IR-reflective markers if visible-light detection turns out to be too fragile under stage lighting. (This is *unverified for your specific room*; test early.)
4. **Use a tool-token, à la Urp's wand.** Reserve one puck whose role is "switch the projected overlay between CO₂ / cost / labor / time." This pattern is well-validated and saves you from inventing a separate menu UI.
5. **Don't print labels on the pucks; project them.** Per the cross-cutting theme above. Keeps you free to repurpose pucks late in the build.
6. **Skip TUIO for v1.** A direct OpenCV → renderer pipeline is faster to build in 3 weeks. Adopt TUIO only if you split sensing and rendering across machines or want to use an existing TUIO client framework (Processing, openFrameworks).

## Sources requiring verification

- **The "Swiss museum DJ table" the team cites — I could not pin it to a specific Swiss venue.** The Reactable is on permanent display at ZKM (Karlsruhe, Germany) and the Game Science Center (Berlin), per https://reactable.com/experience/museum-exhibitions/ . No web evidence surfaced of a permanent Reactable installation in Zurich, Bern, Basel, or Lausanne. Possibilities the team should check directly:
  - Was it actually at ZKM (often confused with Switzerland by non-Europeans)?
  - Was it a temporary exhibition at Museum für Gestaltung Zürich, Vitra Design Museum (just over the German border), or Swiss Science Center Technorama in Winterthur?
  - Was it a different installation entirely (e.g. a *Skoog*, or a custom student/festival piece) that the team is mentally filing under "reacTable-like"?
  - Recommend: ask the team member who saw it for the museum name and approximate year; search that museum's exhibition archive directly.
- **Maquil et al. 2018 DOI** (10.1007/s10109-018-0265-6) — verified via Springer link in search results, but I did not fetch the full PDF. Treat the abstract summary as paraphrased from the abstract page.
- **ArUcoTUI (TEI '25)** — DOI 10.1145/3731459.3779317 surfaced in search but I did not open the full paper. Authors and exact contributions unverified beyond the ACM landing page snippet.
- **COPSE (PACMHCI 2017)** — author list cited from search snippet; should be re-checked against the ACM record before being cited in a paper.
