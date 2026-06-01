# DESIGN.md — Hardware III deck

High-contrast monolithic. Reads like a museum-wall caption set on a workshop wall, with diagrams that read like a circuit schematic. Tinted off-white surface, near-black ink, three saturated method colours pulled directly from the TouchDesigner runtime (`footprint_viz_v5.py`).

## Scene sentence

An IAAC juror reviewing slide 7 of 18 at 16:40 in a sunlit Barcelona studio, projected on a mid-grey wall behind the presenter. Needs to read at the back of the room. Needs to survive being skimmed in the post-crit PDF on a 13" laptop at midnight. Sunlit room forces light theme, not dark.

## Color tokens (OKLCH)

```css
:root {
  /* Surface — warm off-white, faint terracotta tint */
  --paper:        oklch(0.972 0.006 60);
  --paper-edge:   oklch(0.945 0.008 60);
  --rule:         oklch(0.83  0.010 60);

  /* Ink — near-black, faint warm undertone */
  --ink:          oklch(0.18  0.012 60);
  --ink-soft:     oklch(0.42  0.010 60);
  --ink-faint:    oklch(0.62  0.008 60);

  /* Method colours — pulled from touchdesigner/scripts/footprint_viz_v5.py:67-70 */
  --masonry:      oklch(0.66  0.155 45);   /* terracotta */
  --printed:      oklch(0.66  0.145 235);  /* steel blue */
  --prefab:       oklch(0.71  0.140 145);  /* green */

  /* States */
  --live:         oklch(0.70  0.150 145);  /* heartbeat green, == prefab */
  --pending:      oklch(0.78  0.110 80);   /* amber */
  --invalid:      oklch(0.62  0.180 25);   /* alarm red */
  --offline:      oklch(0.55  0.020 60);   /* warm grey */
}
```

Strategy: **Restrained-with-committed-accents**. Paper + ink carry 90% of pixels. Method colours appear only where they refer to an actual method (the data-layer table, the method-selection panel mock, the FSM chip). Never decorative.

Tinted-warm neutral; never pure `#fff` or `#000`.

## Typography

Pair, intentional:

- **Display + body**: `Funnel Display` (variable, 300–800) and `Funnel Sans` (variable, 300–800) — both via Google Fonts. Same family. Wide, monolithic counterforms. Reads architectural, not editorial-magazine. Not on the reflex-reject list.
- **Mono**: `JetBrains Mono` (variable, 300–800) — for technical labels, code, RFID UIDs, OSC channel paths, ArUco IDs, BOM. Carries weight contrast inside the same family. Not on the reflex-reject list.

Falls back to: `Funnel Display, "Funnel Display Fallback", system-ui, sans-serif`.

### Scale (slide-scale, 1280 × 720 native, scaled)

```css
:root {
  --t-mono-xs:   clamp(0.62rem, 0.55rem + 0.3vw, 0.78rem);   /* 10-12.5px */
  --t-mono-sm:   clamp(0.72rem, 0.65rem + 0.35vw, 0.92rem);  /* 11.5-15px */
  --t-body:      clamp(0.95rem, 0.85rem + 0.6vw, 1.25rem);   /* 15-20px */
  --t-lede:      clamp(1.20rem, 1.00rem + 1.2vw, 1.75rem);   /* 19-28px */
  --t-h3:        clamp(1.50rem, 1.20rem + 1.6vw, 2.30rem);   /* 24-37px */
  --t-h2:        clamp(2.20rem, 1.60rem + 3.2vw, 4.00rem);   /* 35-64px */
  --t-h1:        clamp(3.20rem, 2.20rem + 5.5vw, 6.80rem);   /* 51-109px */
}
```

Ratio 1.5 between steps. Strong contrast. Variable axis weight contrast for emphasis inside paragraphs (`font-variation-settings: 'wght' 650`).

### Voice

- Headings: lowercase or all-caps in JetBrains Mono micro-labels only; never SentenceCase display. Lowercase reads architectural, not corporate.
- No em dashes, no `--`. Use comma, colon, period, parens.
- Mono is for *things from the system* (file paths, channel names, IDs, values). Never decorative monospace.

## Layout

Strict left-aligned 12-column grid with a 1-column gutter for slide numbers and section labels. Asymmetric within. No centered title stacks.

```css
.slide {
  display: grid;
  grid-template-columns: clamp(72px, 8vw, 132px) repeat(11, 1fr);
  grid-template-rows: clamp(48px, 6vh, 80px) 1fr clamp(48px, 6vh, 80px);
  gap: clamp(16px, 1.4vw, 32px);
  padding: clamp(28px, 3vw, 56px);
}
```

Slides use the grid; diagrams use SVG inside it. No nested cards. No icon-heading-paragraph card grids.

Spacing rhythm: tight groupings (`--s-tight: 0.5rem`), comfortable bodies (`--s-body: 1.25rem`), generous section breaks (`--s-section: 4rem`).

## Components

### Slide kicker (mono, top-left)

```
SECTION 04 / 18    ·    ARCHITECTURE
```

Sits in column 2, row 1. JetBrains Mono, `var(--t-mono-sm)`, `var(--ink-faint)`.

### Display heading (one per slide)

`Funnel Display`, weight 700, `var(--t-h1)` or `var(--t-h2)`, lowercase. Sits in columns 2-9. Pulled tight (line-height 0.95).

### Diagram rule

1px `var(--rule)` horizontal divider above and below significant diagrams. Architectural drafting convention.

### Mono spec block

```html
<dl class="spec">
  <dt>protocol</dt><dd>OSC over UDP</dd>
  <dt>port</dt><dd>7000</dd>
  <dt>rate</dt><dd>every frame, ~30 Hz</dd>
</dl>
```

`dt` in mono uppercase faint-ink, `dd` in body weight 500. Two-column grid, tight gap.

### Method chip

Small filled square + method name in mono. Background uses the method colour at 0.16 mix with paper for the chip face; full saturation only for the leading swatch.

### Status pill (in-progress / shipped / blocked)

Three states, three colours: `--live` shipped, `--pending` in flight, `--invalid` blocked. Mono micro-label inside. Never the only signal — paired with text.

## Diagrams

All rebuilt as inline SVG so they scale, theme, and stay editable. Existing PNG / PDF diagrams are reference, not assets to embed. SVG uses `currentColor` for stroke so ink toggles cleanly.

Stroke widths: 1.5 for primary, 1 for secondary, 0.5 for grid. No drop shadows. No gradients.

## Motion

- Page-load reveals only. Fade + 12px translate-y, staggered 60ms.
- Easing: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quart).
- Reveal between slides: instant. No transitions between fragments unless the fragment is content.
- Respect `prefers-reduced-motion`.

```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

## Absolute bans (from shared design laws)

Reaffirmed:

- No side-stripe borders on callouts.
- No `background-clip: text` gradient text.
- No glassmorphism.
- No hero-metric template.
- No identical-card grids of icon + heading + text.
- No modal-first thinking — slide deck is single-window anyway.
- No em dashes in copy.
- No #000 or #fff anywhere.
- No Inter, no IBM Plex, no Space Grotesk, no Fraunces.

## Reveal.js posture

Use Reveal.js 5.x as transport, override nearly everything. Linear progression only (no nested vertical decks). Custom theme CSS at `assets/css/theme.css`. Native PDF print mode supported (`?print-pdf`).
