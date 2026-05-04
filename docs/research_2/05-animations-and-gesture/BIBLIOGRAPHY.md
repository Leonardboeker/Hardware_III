# 05 — Animations + Gesture: Annotated Bibliography (APA 7.0)

**Strand:** 05-animations-and-gesture
**Date:** 2026-05-04
**Tier convention:** Tier 1 = peer-reviewed journal / foundational research blog from primary lab; Tier 2 = institutional / vendor primary documentation; Tier 3 = vendor marketing or third-party summary (used only as corroborative).
**Sub-strand tags:** A = hand tracking; B = AI animation; C = uncertainty viz; D = projection-animation precedents.

---

## A — Hand / fingertip tracking

**Bazarevsky, V., & Zhang, F. (2019, August 19). *On-device, real-time hand tracking with MediaPipe* [Blog post]. Google Research. https://research.google/blog/on-device-real-time-hand-tracking-with-mediapipe/**
*[A — Tier 1]* The original MediaPipe Hands announcement from the authoring team. Establishes the two-stage architecture (BlazePalm detector + 21-keypoint landmark regressor), the synthetic + real training-data mix (~30 K real-world images), and the headline regression-error numbers (13.4 % mixed vs. 25.7 % synthetic-only vs. 16.1 % real-only). Used as the primary architectural citation for sub-strand A.

**Zhang, F., Bazarevsky, V., Vakunov, A., Tkachenka, A., Sung, G., Chang, C.-L., & Grundmann, M. (2020). *MediaPipe Hands: On-device real-time hand tracking* (arXiv:2006.10214). arXiv. https://arxiv.org/abs/2006.10214**
*[A — Tier 1]* The CVPR 2020 4th Workshop on CV for AR/VR paper that backs up the blog post with the full architecture, training methodology, and ablation studies. Confirms that the 21-keypoint landmarker is trained primarily on hands at near-natural lighting; no published evaluation under saturated projected color.

**Cao, Z., Hidalgo Martinez, G., Simon, T., Wei, S., & Sheikh, Y. A. (2019). OpenPose: Realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 43(1), 172–186. https://doi.org/10.1109/TPAMI.2019.2929257**
*[A — Tier 1]* The extended TPAMI version of the original CVPR 2017 paper (Cao, Simon, Wei & Sheikh). Defines Part Affinity Fields, the architecture's non-parametric body-part association, and the open-source CMU implementation. Used to characterise OpenPose's heavier-but-multi-person profile relative to MediaPipe's single-hand-optimised pipeline.

**Kaltenbrunner, M., & Bencina, R. (2007). reacTIVision: A computer-vision framework for table-based tangible interaction. In *Proceedings of the 1st International Conference on Tangible and Embedded Interaction (TEI '07)* (pp. 69–74). ACM. https://doi.org/10.1145/1226969.1226983**
*[A, D — Tier 1]* The reacTIVision paper underlying the reacTable. Local-Barcelona MTG/UPF lineage. Important because reacTIVision since v1.6 also tracks untagged finger blobs via TUIO, providing a precedent for non-fiducial tabletop gesture recognition long before MediaPipe.

**Jordà, S., Geiger, G., Alonso, M., & Kaltenbrunner, M. (2007). The reacTable: Exploring the synergy between live music performance and tabletop tangible interfaces. In *Proceedings of TEI '07* (pp. 139–146). ACM. https://doi.org/10.1145/1226969.1226998**
*[A, D — Tier 1]* The reacTable paper. Establishes the gesture vocabulary (rotate, slide, connect) for tabletop manipulation that downstream installations — including this one — implicitly reference.

**Kreylos, O., Bawden, G., Bernardin, T., Billen, M. I., Cowgill, E. S., Gold, R. D., Hamann, B., Jadamec, M., Kellogg, L. H., Staadt, O. G., & Sumner, D. Y. (2006–present). *Augmented Reality Sandbox* [Software / project page]. UC Davis. https://web.cs.ucdavis.edu/~okreylos/ResDev/SARndbox/**
*[A, D — Tier 2]* Project documentation for the AR Sandbox. Describes the Kinect overhead-camera / overhead-projector / hand-occluder loop, the depth-statistic hand filter, and the open-source software stack. Closest functional precedent to this installation's overhead-camera tabletop geometry.

**Mitterberger, D., Dörfler, K., Sandy, T., Salveridou, F., Hutter, M., Gramazio, F., & Kohler, M. (2020). Augmented bricklaying: Human–machine interaction for in situ assembly of complex brickwork using object-aware augmented reality. *Construction Robotics*, 4(3–4), 151–161. https://doi.org/10.1007/s41693-020-00035-8**
*[A, D — Tier 1]* Peer-reviewed account of the Kitrvs Winery façade (13 596 bricks, 225 m², three months on-site). Documents the visual-inertial object tracking + dynamic optical guidance system. The error-feedback animation grammar (translucent target, on-target color change) is the reference idiom for this installation's "you traced the footprint, here is how it would be built" sequence.

**Leithinger, D., Follmer, S., Olwal, A., & Ishii, H. (2014). Physical telepresence: Shape capture and display for embodied, computer-mediated remote collaboration. In *Proceedings of UIST '14* (pp. 461–470). ACM. https://doi.org/10.1145/2642918.2647377**
*[A, D — Tier 1]* The follow-up UIST paper to inFORM (2013). Establishes the design language for "your hand is the controller and the surface responds in real time" with a 30 × 30 actuated pin display and Kinect input.

**Ultraleap. (2023). *Leap Motion Controller 2 datasheet (UL-006511-SP-17)*. Ultraleap Ltd. https://leap-2.ultraleap.com/**
*[A — Tier 2]* Vendor primary documentation for the second-generation Leap Motion device: stereo near-IR cameras, 160° × 160° FoV, 10–110 cm tracking range, 27 hand joints, USB-C connector. Cited as the IR-camera fallback for the projector-light-interference failure mode.

**Blankensmith, T. (2024–25). *MediaPipe TouchDesigner plugin* [Software, v1.x]. GitHub. https://github.com/torinmb/mediapipe-touchdesigner**
*[A, D — Tier 2]* The de facto production path for MediaPipe in TouchDesigner. Describes WebAssembly + embedded Chromium + WebSocket architecture; documents `detectTime`, `realTimeRatio`, and "at least 3 frames" `totalInToOutDelay`. Tested up to TD 2025.31500. Cited for the implementation specifics in `RECOMMENDATIONS.md`.

---

## B — AI-generated phase animations

**Runway Research. (2025). *Introducing Runway Gen-4* [Research note]. Runway. https://runwayml.com/research/introducing-runway-gen-4**
*[B — Tier 2]* Vendor primary documentation for Gen-4. Describes the diffusion-transformer architecture and "cinematic conditioning" training. Useful for the architectural-prompt-fidelity claim; treated as Tier 2 because it is the primary source for the model's design but is also marketing.

**OpenAI. (2026). *What to know about the Sora discontinuation* [Help Center article]. OpenAI. https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation**
*[B — Tier 2]* Primary OpenAI documentation of Sora's discontinuation. Establishes the consumer web/app shutdown date (2026-04-26) and API shutdown date (2026-09-24). The single citation that removes Sora from the installation's candidate set.

**Stability AI. (2023–24). *stable-video-diffusion-img2vid-xt* [Model card]. Hugging Face. https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt**
*[B — Tier 2]* Primary model card for SVD-XT: 25 frames at 576 × 1024 from a conditioning image. The reference for the open-source local-control path.

**Luma AI. (2025–26). *Architectural visualization with Dream Machine Ray 3*. Luma Labs. https://lumalabs.ai/use-case/architectural-visualization-with-dream-machine-ray-3**
*[B — Tier 2]* Vendor documentation describing the diffusion-transformer + NeRF-derived 3D-consistency hybrid; the relevant technique for image-to-video transitions between authored stills.

**Pika Labs. (2024–26). *Pika 2.0: Scene Ingredients*. Pika Art. https://pika.art/**
*[B — Tier 2]* Vendor documentation of the "Ingredients" mechanism for cross-shot subject consistency. The reference for the texture-consistency-across-five-phases use case.

**Kuaishou Technology / Kling AI. (2026, February 4). *Kling 3.0 release notes*. Kling. https://kling3.io/**
*[B — Tier 2]* Vendor announcement for Kling 3.0, advertising 3D Spacetime Joint Attention and chain-of-thought reasoning. Cited for the physics-simulation claim and dated to the model's actual release.

---

## C — Uncertainty visualization

**Hullman, J., Resnick, P., & Adar, E. (2015). Hypothetical outcome plots outperform error bars and violin plots for inferences about reliability of variable ordering. *PLOS ONE*, 10(11), e0142444. https://doi.org/10.1371/journal.pone.0142444**
*[C — Tier 1]* The foundational HOPs paper. Establishes that animated frames each drawn from the distribution support better untrained-observer judgments than static error bars or violin plots. The empirical backing for the installation's flickering-value idiom.

**Kale, A., Nguyen, F., Kay, M., & Hullman, J. (2019). Hypothetical outcome plots help untrained observers judge trends in ambiguous data. *IEEE Transactions on Visualization and Computer Graphics*, 25(1), 892–902. https://doi.org/10.1109/TVCG.2018.2864909**
*[C — Tier 1]* The IEEE TVCG follow-up. Demonstrates that with HOPs, untrained observers reach ~75 % accuracy on noisy time-series trends with less evidence than error-bar viewers need. Strengthens the case for animated uncertainty over static idioms in a public-facing tabletop installation.

**van der Bles, A. M., van der Linden, S., Freeman, A. L. J., Mitchell, J., Galvao, A. B., Zaval, L., & Spiegelhalter, D. J. (2019). Communicating uncertainty about facts, numbers and science. *Royal Society Open Science*, 6(5), 181870. https://doi.org/10.1098/rsos.181870**
*[C — Tier 1]* The framework for uncertainty communication: three objects (facts/numbers/hypotheses) × two levels (direct/indirect), nine-rung expression scale. Directly informs the recommendation that the installation use a rung-3 (rounded range) plus rung-2 (summary distribution) combination, supplemented by named-assumption text.

**Smith, A. (Financial Times Visual Journalism Team). (2018–present). *Visual vocabulary*. Financial Times / GitHub. https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary**
*[C — Tier 2]* Open-source FT chart-selection guide. Establishes the fan chart as the journalism-mainstream idiom for forecast uncertainty. Reference for the gradient-band comparison view.

**Lupi, G., & Posavec, S. (2016). *Dear data*. Princeton Architectural Press.**
*[C — Tier 2]* The 52-week hand-drawn data postcard project. Reference for the legend-as-companion idiom — every visualization is paired with a hand-written note that can include uncertainty annotations. Borrowed pattern for the installation's named-assumption sentence.

---

## D — Tabletop projection animation

**Parascho, S. (2019). *Cooperative robotic assembly: Computational design and robotic fabrication of spatial metal structures* [Doctoral dissertation, ETH Zürich]. ETH Research Collection. https://doi.org/10.3929/ethz-b-000364322**
*[D — Tier 1]* Peer-examined ETH dissertation. Establishes the cooperative-assembly FSM pattern (each robot's role, handoff conditions, dependency graph) that translates into the installation's five-phase progression as a state machine.

**Parascho, S., Han, I. X., Walker, S., Beghini, A., Bruun, E. P. G., & Adriaenssens, S. (2020). Robotic vault: A cooperative robotic assembly method for brick vault construction. *Construction Robotics*, 4(3–4), 117–126. https://doi.org/10.1007/s41693-020-00041-w**
*[D — Tier 1]* Peer-reviewed paper applying the cooperative-assembly framework to brick-vault construction. Reference for any animation that visualises element-by-element assembly with explicit dependency and stability conditions.

**Block Research Group, Zaha Hadid Architects Computation and Design Group, incremental3D, & Holcim. (2021). *Striatus 3DCP arched bridge* [Project documentation]. Block Research Group, ETH Zürich. https://block.arch.ethz.ch/brg/project/striatus**
*[D — Tier 2]* Project documentation for the Striatus bridge: 53 unreinforced 3DCP blocks, ~500 layers each, six-axis robot, ~84 h total print time, dry assembly. Reference for the 3D-printed-method phase animation: layer-by-layer accretion and compression-only block geometry. (Reassembled in 2024 as Phoenix in Lyon.)

**Derivative. (2024–25). *TouchDesigner documentation: Palette:kantanMapper, CHOP Execute DAT, Script CHOP, Working with CHOPs in Python, Engine COMP*. https://docs.derivative.ca/**
*[D — Tier 2]* Primary product documentation for the TouchDesigner operators relevant to this installation's projection mapping (Kantan Mapper), gesture-event handling (CHOP Execute DAT, Script CHOP), and subsystem isolation (Engine COMP). Treated as Tier 2 because it is vendor primary, not peer-reviewed.

**Lieberman, Z., Watson, T., & Castro, A. (2005–present). *openFrameworks* [Software framework]. https://openframeworks.cc/ ; Bell, A., et al. (2010–present). *Cinder* [Software framework]. https://libcinder.org/**
*[D — Tier 2]* The pre-TouchDesigner creative-coding lineage. Many tabletop and projection installations of 2008–2018 were built in openFrameworks; the example library is the cheapest place to read the canonical idioms (computer-vision blob detection, projection-mapping warps, particle-system animation) before transferring them to TouchDesigner.

---

## Cross-strand reference

**Finlayson, G. (2018). Colour and illumination in computer vision. *Interface Focus*, 8(4), 20180008. https://doi.org/10.1098/rsfs.2018.0008**
*[A — Tier 1]* Royal Society review of illumination's effect on computer-vision performance. Cited in support of the claim that illumination variation often dominates appearance variation between subjects — the underlying reason projector light is a hard problem for RGB hand tracking.
