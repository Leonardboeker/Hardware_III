# Hardware III — Session Summary (2026-05-31)

End-to-end migration from TD-heavy to Python-heavy architecture, plus
demo-day stabilization. Single laptop hosts everything by the end of
the day.

---

## Story line

**Vor heute** (Phase 02.1 + Vision-Pipeline live, branch `origin/Onur`):
ESP32-Setup mit RFID + Slider A (FLOOR) + Slider B (PHASE) lief; TD's
`vision_in` OSC In CHOP empfing Vision-Stream vom externen Laptop;
Onurs `metrics_engine` CSV-Pipeline war seit Wochen wegen
`KeyError: 'method'` kaputt.

**Heute** drei Hauptphasen:

1. **Phase B — TD-Bridge** (vormittags): Onurs UI lebendig machen
   ohne sein metrics_engine. Python-Orchestrator (gestern fertig)
   pumpt `ui_state` via OSC nach TD; ein neuer `state_in` OSC In CHOP
   + chopexec DAT + `state_in_dat` für Strings spiegelt alles in
   `owner.store('ui_state', dict)`. Onurs `parent().fetch(me.name, "")`
   Pattern bleibt unverändert → seine 32 text TOPs werden automatisch
   reaktiv.

2. **Vision-Debugging** (mittags): externer Vision-Laptop kam nicht
   durch. Mehrere falsche Hypothesen (ICMP ≠ UDP, wrong subnet,
   firewall) — am Ende: sein `main.py` lief schlicht nicht. Pivot zu
   single-laptop: Vision-Repo lokal kloniert, Logitech BRIO an Leos
   Maschine, OSC nun via `127.0.0.1`.

3. **Demo-Polish** (nachmittags): per-method `max_floors`/`n_phases`
   Quantisierung, RFID-Priorität über Vision, Cost/CO2/Labor scaling
   pro `area × floors`, sketch render TOP mit cyan walls + yellow
   pucks + Meter-Labels along the wall, iterative Beamer-Kalibrierung,
   phase-reaktives `right_cost_chart`, lebendiges `current_state`
   panel.

---

## Probleme & Lösungen

### Hardware / Firmware

| Problem | Lösung |
|---|---|
| `'SLIDER:' in 'PSLIDER:0.5'` — substring collision | PSLIDER branch zuerst prüfen |
| ESP32 reset on Serial open (DTR pulse) → FLOOR not re-emitted | Slider kurz bewegen nach orchestrator start ODER firmware: emit FLOOR on boot |
| RFID UIDs hatten sich geändert nach Re-Pairing | Live ausgelesen via `rfid_listener.py` helper, in methods_db.json gepatcht |

### TouchDesigner

| Problem | Lösung |
|---|---|
| File-Sync auf `O:/...` (teammate's drive) — 4 DAT warnings | `syncfile=False` + `file=''` per DAT |
| Movie File In TOPs zeigten auf non-existente .gif assets | `play=False` + `loadondemand=True` |
| Serial DAT (`rfid_in`) blockierte COM4 für orchestrator | `active=False` |
| `project.performWindowPath = '/project1/window1'` existiert nicht | Auf `/project1/projector_out` (vorhandener Window COMP) umgebogen |
| OSC In CHOP **droppt string-args** silent | Zusätzliches `state_in_dat` (OSC In DAT) für strings, callback merged in selben ui_state dict |
| `chopexec` `onValueChange` feuert nur wenn TD-Network cookt — paused im Editor | OK in Perform Mode (F1). Manuell triggern für editor-tests via `ed.module.onValueChange(...)` |
| PIL nicht in TDs Python-Bundle → wall-length labels invisible | `cv2.putText` (cv2 4.11 ist da) |
| MCP-Webserver script in neuer .toe hatte SyntaxError + port 9982 statt 9981 | Disk-Version reingeladen + Port via `ws.par.port = 9981` korrigiert |
| Onurs `metrics_engine` CSV-Pipeline kaputt (KeyError) | Komplett umgangen — Cost/CO2/Labor jetzt im orchestrator berechnet |
| Bridge-Nodes nur in-memory, verloren beim .toe reload | `td.project.save()` nach jeder MCP-Mutation |

### Networking (Vision Laptop)

| Problem | Lösung |
|---|---|
| Sniffer empfing nichts trotz "main.py läuft" | Sein script lief nicht — eine `osc_test.py` (1-shot) kam an, der continuous nicht |
| `ping 192.168.10.22` von vision-laptop → timeout | ICMP wird oft separat geblockt, sagt nichts über UDP aus |
| 4 Subnetz-Hypothesen (Vision war auf .11.x, Leo auf .10.x) | Faktisch /23 subnet → war nie das Problem |
| Continuous heartbeat fehlte | Kollege hat eigenen heartbeat-thread @5Hz gebaut |
| Eskalation: zu viel cross-machine Koordination | **Pivot single-laptop**, vision repo lokal cloned, OSC → 127.0.0.1 |

### Orchestrator (Python)

| Problem | Lösung |
|---|---|
| `StateManager.snapshot()` kopiert Felder manuell — neue Felder fehlen | Beide Stellen updaten (dataclass + snapshot copy) |
| `/method/selected` von vision schickte `0` → überschrieb RFID | `HW3_RFID_PRIORITY=1` in run.bat |
| Firmware sendet FLOOR:1..5, aber PREFAB will 1..8, 3DP nur 1..2 | Re-Quantisierung in `ui_state.py` aus `slider_raw + active_method.max_floors` |
| Vision sendet `/puck/<i>` mit projector coords — orchestrator hatte sie aber nicht an TD geforwarded | `puck_<i>_x/y/active` in ui_state payload eingefügt |
| `hb_alive=0` "obwohl heartbeat ankommt" | False alarm: Test-Query lief 10s **nach** dem heartbeat → 3s timeout abgelaufen. Code war richtig |

### Calibration / UI

| Problem | Lösung |
|---|---|
| Sketch-render auf voller 1280×720 statt ArUco-Fläche | `BOUND_XMIN/MAX/YMIN/YMAX` parameters im Script TOP, manuell justiert |
| Y-Achse 1.5× zu gestreckt | Y-bounds compressed 0.7 → 0.46 basierend auf Top vs Bottom puck error (1cm vs 18cm) |
| Beamer mirrored projection → text reads backwards | `cv2.flip(text_img, 1)` (horizontal flip) bevor draw |
| Text saß auf der Wand-Linie | Perpendicular offset 22px (`-dy/seg_len, dx/seg_len`) |
| Text horizontal egal welche Wand-Richtung | `cv2.getRotationMatrix2D` + `warpAffine` mit angle aus `atan2(dy,dx)` |
| Real-world dimensions display | 1:100 scale → 1cm physical = 1m real, einfach Einheit getauscht |

---

## Architektur (final, single laptop)

```
ESP32 (COM4, USB Serial @115200) ──┐
                                    │
                                    ├──→ Orchestrator (Python, 30Hz)
                                    │       │
Vision (vision2/main.py, local) ────┘       │
  - Camera (Logitech BRIO)                   │
  - ArUco detect / sketch                    │
  - OSC → 127.0.0.1:7000                    │
                                              ↓
                                       state_in CHOP + DAT (TD)
                                              │
                                              ↓
                                       chopexec → owner.store('ui_state', dict)
                                              │
                                              ↓
                                       text TOPs + sketch_render Script TOP
                                              │
                                              ↓
                                       final_composite (Over TOP)
                                              │
                                              ↓
                                       projector_out (Window COMP) → Beamer
```

**Single command boot:** `.\start_all.bat` (worktree root).

---

## Lessons learned

1. **Move logic out of TD early.** Python ist 10× schneller zu
   entwickeln, testbar, versionierbar. TD = nur rendering.
2. **OSC In CHOP droppt strings silent.** Für mixed payloads braucht
   man parallel ein OSC In DAT.
3. **`chopexec` cooked nur wenn das TD-Network läuft** (Perform Mode
   oder Timeline play). Im Editor mit pausierter Timeline feuert er
   nicht — kein Bug, ein TD-Feature.
4. **PIL ist nicht garantiert in TDs Python**, cv2 schon (4.11). Für
   text rendering immer cv2 oder numpy.
5. **State + snapshot synchron halten.** Neue Felder müssen an beiden
   Stellen rein, sonst kriegt der main loop stale defaults.
6. **Test-Methodik überprüfen vor "Bug" deklarieren.** Heartbeat-Timeout
   ist 3s — wenn man 10s nach dem heartbeat misst, ist hb_alive
   natürlich 0.
7. **Cross-machine coordination ist Demo-Gift.** Single-laptop
   eliminiert 90% der Debug-Surface (firewall, subnet, IP, parallel
   processes).
8. **Logitech Options Show-Mode vs DSHOW zoom**: nur eine Quelle für
   camera-config wählen, sonst double-zoom.
9. **MCP für TD ist Gold.** Statt "paste this in textport, send me
   output" → ich kann direkt nodes lesen/erstellen/modifizieren +
   `.toe` saven. Einer der größten Productivity-Booster heute.
10. **Onurs panel UI ist clever**: `parent().fetch(me.name, "")` als
    Pattern macht text TOPs einfach reaktiv ohne pro-TOP wiring. Wir
    haben das ohne Code-Änderungen aus seinem .toe übernommen.

---

## Was am Ende live ist

- ✅ RFID → Method switch (MASONRY / 3D PRINTED / PREFAB)
- ✅ Slider A → Floor (1..n je nach Method)
- ✅ Slider B → Phase (1..n je nach Method) + manual-override mit 10s timer
- ✅ Vision → Pucks, Sketch area, perimeter, FSM state
- ✅ TD renders: cyan walls + yellow pucks + meter labels along walls
- ✅ Polygon schließt sich ab 3 Punkten
- ✅ Beamer mirror compensated (text + bounds)
- ✅ Method-spezifische cost/CO2/labor scaling per area × floors
- ✅ Phase-reactive right_cost_chart
- ✅ Reactive current_state panel (method + phase + floors + area)
- ✅ Single laptop, single launcher (`start_all.bat`)
- ✅ 37 unit tests grün

## What's NOT done

- Per-phase cost-weighting (aktuell gleicher Split, Foundation =
  Finishing). Realistisch wäre Foundation 30%, Structure 40%, Roof 15%,
  Openings 10%, Finishing 5% — würde nochmal 15 min.
- ArUco-Bounds Calibration via Homography statt manuelle Sliders.
- Color-coded chips für aktive Phase (aktuell `[Foundation]` brackets).

---

## Repo state

- Branch `feat/orchestrator-hybrid` ist auf GitHub (pushed).
- 13 Commits seit Phase A.
- `td_verify_final2.21_ON.toe` (Haupt-Repo) noch nicht gepusht, lebt im
  master Branch hinter 28 lokalen auto-commits.
- Vision repo (`C:\Users\leona\Downloads\vision2`) ist Kollegen-fork,
  lokale Änderungen (CAMERA_ZOOM=100, namedWindow resize) nicht
  upstream gepusht.
