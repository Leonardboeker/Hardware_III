# FSM — Interactive Assembly Installation
## 5 states, draw this on paper for Session 2

```
                         ┌─────────────────────────────────┐
                         │                                 │
                         ▼                                 │
                ┌──────────────┐                           │
                │     IDLE     │  Ambient light pattern    │
                │              │  "approach to begin"      │
                └──────┬───────┘                           │
                       │                                   │
            user approaches table                          │
            (webcam detects presence)                      │
                       │                                   │
                       ▼                                   │
                ┌──────────────┐                           │
                │    READY     │  First target projected   │
                │              │  "place piece here"       │
                └──────┬───────┘                           │
                       │                                   │
              user places a piece                          │
              (ArUco marker detected)                      │
                       │                                   │
                       ▼                                   │
                ┌──────────────┐                           │
           ┌───►│   CHECKING   │  Brief blink (≤0.3s)     │
           │    │              │  validating position      │
           │    └──────┬───────┘                           │
           │           │                                   │
           │     ┌─────┴─────┐                             │
           │     │           │                             │
           │  INVALID     VALID                            │
           │     │           │                             │
           │     ▼           ▼                             │
           │ ┌────────┐ ┌──────────────┐                   │
           │ │ ERROR  │ │  CONFIRMED   │  Green pulse      │
           │ │        │ │              │  LCA data overlay  │
           │ │ Red    │ │  CO₂, labor, │  projected onto    │
           │ │ outline│ │  origin map  │  the piece itself  │
           │ └───┬────┘ └──────┬───────┘                   │
           │     │             │                           │
           │  user corrects   is this the                  │
           │  placement       last piece?                  │
           │     │             │                           │
           └─────┘        ┌────┴────┐                      │
                          │         │                      │
                         NO        YES                     │
                          │         │                      │
                          ▼         ▼                      │
                    back to    ┌──────────┐                │
                    READY      │ COMPLETE │  Final comparison│
                    (next      │          │  dashboard       │
                     piece)    └────┬─────┘                │
                                   │                       │
                              no presence                  │
                              for 60s                      │
                                   │                       │
                                   └───────────────────────┘
```

## States summary (for your paper sketch)

| State | Projection shows | Enters when | Exits when |
|-------|-----------------|-------------|------------|
| **IDLE** | Ambient pattern, "approach to begin" | System startup / 60s no presence | User approaches table |
| **READY** | Target outline for next piece | User detected / previous piece confirmed | User places a piece |
| **CHECKING** | Brief blink/pulse (≤0.3s) | Marker detected in placement zone | Position validated (→ CONFIRMED or ERROR) |
| **ERROR** | Red outline + ghost of correct position | Placement outside tolerance | User corrects placement → back to CHECKING |
| **CONFIRMED** | Green pulse + LCA data on piece (CO₂, hours, origin map) | Valid placement | User reaches for next piece → READY / Last piece → COMPLETE |
| **COMPLETE** | Side-by-side comparison of all methods | Last piece placed | Timeout 60s → IDLE |

## Transitions to label on your arrows

1. `user detected` → IDLE to READY
2. `piece placed` → READY to CHECKING
3. `position valid` → CHECKING to CONFIRMED
4. `position invalid` → CHECKING to ERROR
5. `user corrects` → ERROR to CHECKING
6. `next piece` → CONFIRMED to READY
7. `last piece valid` → CONFIRMED to COMPLETE
8. `timeout 60s` → COMPLETE to IDLE

## Edge cases (mention if tutor asks)

- User walks away mid-build → 30s timeout → IDLE (preserves progress)
- Two pieces placed simultaneously → process first detected, queue second
- Projector light interferes with camera → ArUco markers solve this (high contrast binary pattern)
