# Hardware III — Reference Notes
*Course: Human-in-the-Loop Interactive Systems for Fabrication — IAAC Barcelona*

---

## 1. Computational Assemblies (EG Tutorial) — https://sutd-cgl.github.io/supp/Publication/projects/2022-EG-AssemblyTutorial/index.html

**Type:** Tutorial / Academic publication (Eurographics 2022)
**Relevance:** Establishes the four foundational pillars of computational assembly design — fabricability, joining, sequencing, and stability — directly mapping to the problem space of this course.

### Key Concepts
- Assemblies are objects composed of smaller discrete parts (puzzles, LEGO, furniture, architecture)
- Four core problems: parts fabricability, parts joining, assembly planning/sequencing, structural stability
- Addresses limitations of digital fabrication methods: 3D printing, CNC milling, laser cutting
- Designing assemblies is framed as "highly non-trivial" — individual part properties interact with whole-assembly behaviour

### Takeaways for the Course
- Provides a clean conceptual taxonomy for any assembly system design: use these four pillars to audit your own projects
- Assembly planning (sequencing) is explicitly named as a standalone design problem, not an afterthought — aligns with FSM-driven sequencing logic
- Structural stability must be considered alongside fabrication constraints, not separately
- The range from puzzles to architecture suggests the methods scale — relevant to modular assembly at any resolution

---

## 2. Cooperative Robotic Assembly of Spatial Metal Structures — https://www.research-collection.ethz.ch/entities/publication/727d44fb-f4fc-45e0-80b8-865d17f936ac

**Type:** Doctoral thesis (ETH Zurich, Stefana Parascho, 2019)
**Relevance:** Demonstrates how fabrication constraints and assembly sequencing can be embedded directly into the design process, not applied after the fact — a core principle for FSM-based fabrication logic.

### Key Concepts
- Two cooperative industrial robots swap roles during fabrication, supporting each other without temporary scaffolding
- Connection typology accommodates bars joining at individual angles — high geometric differentiation
- Assembly sequence-based design: sequence informs geometry, and geometry informs sequence (bidirectional)
- Integrates physical prototyping with digital design generation simultaneously
- Core thesis: controlling complexity of design, fabrication, and structure together expands the architectural design space

### Takeaways for the Course
- Role-switching between agents during assembly is a direct FSM pattern: each robot state transitions based on what the other is doing
- Fabrication constraints as design drivers — not limitations but generative parameters
- The bidirectional relationship between sequence and geometry is a key insight for human-in-the-loop systems: the human operator's choices at each step shape future options
- Cooperative (multi-agent) assembly without support structures is achievable when sequencing logic is rigorous

---

## 3. Robot Made 2024 — https://robotics.utoronto.ca/news/robot-made-2024-digital-fabrication-brings-engineering-and-architecture-students-together

**Type:** Educational project / course initiative (University of Toronto + UBC, 2024)
**Relevance:** Real-world example of students operating industrial robots for timber fabrication — shows how digital-to-physical workflows are structured in an interdisciplinary educational context.

### Key Concepts
- Engineering + architecture students collaborate on designing and fabricating timber structural systems
- Full workflow: parametric design → scripting → robotic fabrication → collaborative assembly
- Tools: COMPAS_FEA (structural analysis), Parametric Robot Control (PRC), KUKA robotic cells
- Students directly drive industrial robots — hands-on human-robot interaction
- Culminates in full-scale collaborative assembly of the fabricated structure

### Takeaways for the Course
- COMPAS framework (open-source) is production-proven for this type of cross-disciplinary fabrication work
- PRC (Parametric Robot Control) bridges Grasshopper/parametric design directly to robot execution — minimal translation layer
- The assembly phase is where interdisciplinary knowledge converges: engineering precision meets architectural intent
- Physical assembly from robotically fabricated parts requires sequencing logic even without a formal FSM — this project would benefit from one

---

## 4. ICD Stuttgart Research — https://www.icd.uni-stuttgart.de/research/

**Type:** Research institute overview (Institute for Computational Design and Construction, University of Stuttgart)
**Relevance:** ICD is the leading institution for computational fabrication research; their projects collectively define the state of the art in agent-based design, human-robot collaboration, and material-driven assembly.

### Key Concepts
- **Task and Motion Planning for Collaborative Robotic Construction with Irregular Materials** — planning strategies for non-uniform building materials with human involvement
- **Strategies for Human-Robot Collaboration in Building Prefabrication** — integrating human workers with robotic systems in modular construction
- **Towards Human-Robot Co-Agency** — shared decision-making frameworks beyond simple operator/tool relationships
- **Agent-based Methods for Fabrication-aware Design of Modular Precast Structures** — design and assembly sequencing co-evolved
- Material-driven design: self-forming components, material-responsive fabrication
- AI reasoning and knowledge graphs for multidisciplinary collaboration

### Takeaways for the Course
- "Task and motion planning" for irregular materials is exactly the FSM/sequencing problem applied to real-world variability
- Human-robot co-agency reframes the human not as supervisor but as co-decision-maker — relevant to interaction design
- Prefabrication + modular assembly is where sequencing logic pays off: each module placement affects structural and spatial options downstream
- ICD's open-source tools (ABxM, COMPAS integrations) are directly usable in course projects

---

## 5. CAP Uncertainty Workshop — EPFL — https://cap-uncertainty.epfl.ch/program

**Type:** Workshop / academic program (EPFL, 6-day intensive)
**Relevance:** Directly addresses how human-robot collaborative fabrication must accommodate uncertainty — material variability, model limitations, and social/collaborative factors — rather than assuming ideal conditions.

### Key Concepts
- Four axes of uncertainty: model uncertainty, material uncertainty, design-with-uncertainty, social uncertainty
- Morning roundtables with experts in collaborative design, robotic fabrication, and construction materials
- Afternoon sessions: hands-on fabrication of a timber pavilion using human-robot collaborative processes
- Uncertainty is reframed as a design variable, not a problem to eliminate

### Takeaways for the Course
- FSMs for assembly must account for uncertainty states: what happens when a component doesn't fit as expected?
- Material variability (stone, timber, irregular elements) requires adaptive decision logic — pure pre-scripted sequences fail
- Social uncertainty (human behaviour variability) is as real as material uncertainty — interaction design must absorb it
- Building a pavilion collaboratively with robots is the course's prototypical project type — this workshop is a direct template
- Embracing uncertainty through design is more robust than attempting to eliminate it through precision

---

## 6. Arkite — Operator Guidance Platform — https://arkite.com/

**Type:** Commercial tool / industrial AR platform
**Relevance:** Production-deployed human-in-the-loop assembly guidance system — shows what mature projection/AR-based operator assistance looks like at industrial scale.

### Key Concepts
- AR work instructions projected/displayed at manufacturing workstations: step-by-step, spatially registered
- Real-time validation via 3D sensors: confirms correct component placement and orientation
- Smart vision inspection: detects screws/bolts >0.5cm, validates correct orientation
- Immediate error feedback: operator is notified instantly when a step is incorrect
- Ecosystem integration with factory IT systems; converts manual operations into data
- Customizable operator experience interface

### Takeaways for the Course
- Arkite is a commercial implementation of the exact feedback loop this course builds toward: project → operator acts → sensor validates → feedback
- Step-by-step AR instruction = serialized FSM rendered spatially — each state maps to one instruction card
- Real-time validation closes the human-in-the-loop: the system doesn't just guide, it confirms
- Error states are first-class: the system explicitly handles incorrect actions rather than assuming correct execution
- Projection/AR as the output channel for FSM state is proven to reduce errors and training time in production

---

## 7. YouTube — https://www.youtube.com/watch?v=Vcd_vk3n-HY

**Type:** Video (content could not be fully retrieved — YouTube returns JavaScript infrastructure rather than page content)
**Relevance:** URL provided for course reference; likely demonstrates a projection-mapping or human-in-the-loop fabrication system based on context of surrounding sources.

### Key Concepts
- Video content could not be confirmed via automated fetch (YouTube page is JavaScript-rendered)
- Based on course context and adjacent IAAC resources found during research: likely covers projection-based assembly guidance, real-time feedback systems, or interactive fabrication workflows
- Related IAAC work on projection mapping (2019-2020, students Anna Batalle, Matt Gordon, Lorenzo Masini, Roberto Vargas) uses projectors as spatial instruction overlays during fabrication

### Takeaways for the Course
- Manually view this video to confirm its content
- If it covers projection mapping for assembly: the key design question is how projected information is synchronized with operator actions (i.e., what triggers the next projection state)
- Projection feedback as a low-cost alternative to full AR headsets: requires only a projector + depth camera, no wearable hardware

---

## 8. Timberstone — EPFL MANSLAB / IBOIS / EESD — https://epfl-enac.github.io/MANSLAB-IBOIS-EESD-timberstone/

**Type:** Research project (EPFL, multi-lab collaboration)
**Relevance:** Full implementation of a human-in-the-loop AR assembly system for vernacular dry-stone + timber construction — the closest existing example to a complete course-relevant system.

### Key Concepts
- Hybrid timber-stone construction: dry-stacked stone masonry interlaced with timber bands (vernacular technique with high seismic resistance)
- Experienced craftsmen build prototype walls; all gestures photographed and filmed to capture tacit knowledge
- **Cockroach**: open-source point cloud processing plugin (IBOIS) for Rhino — reconstructs as-built walls layer by layer from LiDAR scans
- **Stacking algorithm**: AI + mason's rules-of-thumb via nonlinear optimization — determines stone placement sequence and position without trimming stones
- **AR Assembly System**: 3D camera + projector provide real-time visual guidance — green contours for initial placement, three feedback points for orientation refinement
- Human operator retains decision authority; system provides suggestions, not commands
- System records as-built geometry dynamically as work progresses

### Takeaways for the Course
- This is a complete human-in-the-loop fabrication loop: compute → project → human acts → scan → update → repeat
- The stacking algorithm is an FSM-adjacent system: each stone placement creates a new state that constrains the next decision
- Green-contour + three-point feedback is a minimal, effective projection UI — practical to replicate in course projects
- Separating "suggestion" from "command" preserves human agency and handles edge cases the algorithm can't predict
- LiDAR-to-CAD pipeline (Cockroach) enables real-time as-built tracking — critical for any adaptive assembly system
- Tacit knowledge capture (photographing expert gestures) is a valid design research method before building computational systems

---

## 9. Introduction to Behavior Trees — https://robohub.org/introduction-to-behavior-trees/

**Type:** Technical article / tutorial (Robohub)
**Relevance:** Behavior Trees (BTs) are a direct alternative and complement to FSMs for encoding assembly logic — more modular, more composable, and better suited to complex multi-step tasks.

### Key Concepts
- BTs are hierarchical tree structures: root node → control nodes → leaf nodes (behaviors)
- Leaf nodes: Actions (multi-tick, do something) and Conditions (single-tick, check something)
- Control nodes: Sequence (run children until one fails), Fallback/Selector (run children until one succeeds), Parallel (run children concurrently)
- Decorators: modify single child behaviour (repeat, invert, etc.)
- Execution model: discrete **ticks** at a set rate — the tree is traversed and statuses bubble up
- **Blackboard**: shared data structure for reading/writing state across the tree
- BTs vs FSMs: BTs excel at modularity and composability; FSMs excel at reactive mode-switching and global state transitions
- Recommended hybrid: "FSMs for higher-level operating modes, BTs for complex sequences within those modes"
- Tools: py_trees (Python, ROS 2 compatible), BehaviorTree.CPP (C++, XML-based + Groot visualizer)

### Takeaways for the Course
- BTs solve the scalability problem of FSMs: adding a new assembly step doesn't require rewiring all existing transitions
- Sequence nodes directly model assembly steps — if step N fails, the sequence stops (no invalid state reached)
- Fallback nodes model recovery behaviour: try preferred method, fall back to alternative if it fails
- The Blackboard is the shared state in a human-in-the-loop system: human input writes to it, assembly logic reads from it
- The FSM + BT hybrid is the pragmatic architecture: top-level FSM manages major modes (idle / assembling / error / complete), BT handles step sequencing within each mode
- py_trees + ROS 2 is a practical course-level implementation stack

---

## 10. Shape Grammars — https://medium.com/@isohale/shape-grammars-1989ddcdeef7

**Type:** Article / explainer (Medium)
**Relevance:** Shape grammars are the formal foundation of rule-based design — directly relevant to generating assembly rules, modular part configurations, and design-space exploration within constraints.

### Key Concepts
- Invented by George Stiny and James Gips (1972): formal system for visual computation
- Rules operate spatially, not symbolically: primitives are shapes, relationships are spatial
- Basic structure: initial shape + transformation rules (A → B, applied recursively) + termination rule
- Operations: similarity, rotation, spatial relations — purely geometric
- "Purely visual computation": links process to product visibly and legibly
- Applications: urban design, architectural pattern generation, Thonet chair variations, Koch Snowflake, Peano curves
- Rules are human-readable and human-designable — not black-box algorithms

### Takeaways for the Course
- Shape grammars provide the formal language for encoding assembly rules: each rule = one valid next-step transformation
- In modular assembly, the grammar defines which module can connect to which, in which orientation — this IS the FSM transition table rendered geometrically
- Recursive application of rules generates complex assemblies from simple starting conditions — relevant to generative design of structures
- Rules are inspectable and editable by non-programmers — supports human-in-the-loop rule refinement during design
- Combining shape grammars (which rules apply) with FSMs (which state are we in) gives a powerful hybrid: grammar defines valid moves, FSM tracks which have been executed

---

## 11. ABxM Framework — https://www.icd.uni-stuttgart.de/research/research-tools/abxm-framework/

**Type:** Research tool / open-source software framework (ICD Stuttgart)
**Relevance:** ABxM provides a standardized, reproducible infrastructure for agent-based simulation — directly applicable to modelling assembly agents, swarm fabrication, and human-robot collaborative scenarios.

### Key Concepts
- Agent-based (individual-based) modelling framework for dynamic systems of locally interacting discrete entities
- Modular architecture: central abstract core + domain-specific add-ons; avoids reinventing foundational simulation infrastructure
- Supports both divergent (exploratory/generative) and convergent (optimization/goal-directed) use cases
- Multi-threading for complex simulations
- Synchronous update mechanism: all agents update simultaneously per tick — relevant for multi-robot or human+robot scenarios
- Development history: Holz R3, BUGA Wood, SFB 1244 projects — proven in architectural-scale fabrication research
- Grasshopper plugin available (Food4Rhino) for direct integration with parametric design workflows
- Open-source, hosted on DaRUS (DOI: 10.18419/darus-2994)

### Takeaways for the Course
- Agent-based modelling is the simulation layer beneath FSM logic: each agent (human, robot, module) has local rules; emergent assembly behaviour arises from interactions
- Synchronous tick-based updating mirrors BT execution and FSM ticking — consistent mental model across layers
- Grasshopper plugin means ABxM is usable directly in a Rhino/GH workflow — low integration friction for course projects
- For modular assembly design: model each module as an agent with connection rules; run the simulation to evaluate sequence feasibility before fabricating
- The divergent/convergent duality is pedagogically useful: use divergent mode to explore assembly options, convergent mode to optimize a chosen sequence

---

## Summary

### 5–8 Cross-Cutting Insights

1. **FSM + Behavior Tree hybrid is the practical architecture.** Multiple sources (Robohub BTs, ETH cooperative assembly, Arkite) converge on the same pattern: a top-level FSM manages major operating modes (idle / active / error / complete), while a Behavior Tree handles the step-by-step sequence within each mode. Neither alone is sufficient for complex, real-world assembly.

2. **Sequence IS design — not an afterthought.** The EG Assembly Tutorial, Parascho's ETH thesis, and Timberstone all demonstrate that assembly sequence cannot be decoupled from geometry and structure. In human-in-the-loop systems, each human action at step N constrains what is physically and structurally possible at step N+1. Designing the sequence is designing the system.

3. **Projection/AR as the output channel for FSM state.** Arkite (commercial), Timberstone (research), and IAAC's XR work all use projected or AR-overlaid instructions as the human-readable rendering of computational state. The implementation varies (industrial projector, HoloLens, depth-camera + projector) but the pattern is identical: FSM state → spatial instruction → human action → sensor validation → FSM transition.

4. **Uncertainty is a design input, not a failure condition.** The EPFL CAP Uncertainty workshop and Timberstone both explicitly embrace material and behavioural variability. Any assembly FSM that assumes perfect part placement will fail in practice. Robust systems include fallback states, sensor-driven re-evaluation, and human override as first-class design features — not edge cases.

5. **Shape grammars and agent-based models operate below FSMs, providing the rule vocabulary.** Shape grammars (Stiny & Gips) define which moves are structurally and geometrically valid; ABxM (ICD Stuttgart) simulates how agents following local rules produce global assembly behaviour. FSMs then sequence execution through the valid state space these lower layers define. The three form a coherent stack: grammar → agent simulation → FSM execution.

6. **Human agency must be preserved, not engineered away.** Across Timberstone, Arkite, XR for Assembly, and the EPFL workshop, the human operator is always the executor — the system guides and validates but does not override. Interaction design for fabrication must make it easy to follow the suggested path and safe to deviate from it. The system should detect deviations, not prevent them.

7. **Open-source, composable tooling is the norm.** COMPAS (Toronto/UBC), ABxM (ICD Stuttgart), Cockroach (IBOIS/EPFL), py_trees (ROS 2), BehaviorTree.CPP — all the research-grade tools in this space are open-source and built for composability with parametric design environments (Grasshopper, ROS). Course projects should plug into this ecosystem rather than build from scratch.

8. **Modular assembly and rule-based design are two sides of the same coin.** Shape grammars formalize what connections are valid; modular assembly systems enforce those rules physically. An FSM for modular assembly is essentially an interpreter for a shape grammar — it walks the valid rule applications in the sequence dictated by structural and fabrication constraints. Designing the module connector geometry IS writing the grammar.

---
*Notes compiled: April 2026 | Sources fetched and synthesised for Hardware III — IAAC Barcelona*
