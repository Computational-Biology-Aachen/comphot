---
name: ComPhot
description: Interactive photosynthesis learning platform, composed entirely from the shared CPBL design system
---

# Design System: ComPhot

## Overview

**This file does not define ComPhot's visual system — it does not have one.** Per `PRODUCT.md`, ComPhot's colors, typography, spacing, radii, shadows, and component library are entirely inherited from `@computational-biology-aachen/design` (this meta-repo's `pkg-js/design`). That package's own `DESIGN.md`, `PRODUCT.md`, and `.impeccable/design.json` sidecar are the binding visual authority for every token and primitive component ComPhot uses — load and extend those for any color, typography, elevation, or shape decision. Nothing in this file overrides or duplicates them, and it carries no token frontmatter for that reason.

What this file documents instead is **ComPhot-specific composition**: how this site arranges the shared primitives into its own recurring page structure and the small number of genuinely local patterns (raw HTML sliders, chart phase-region conventions) that the shared library doesn't ship and ComPhot had to build itself. Re-run `/impeccable document` here if these composition patterns drift; re-run it in `pkg-js/design` (or read its `DESIGN.md` directly) for anything about color, type, or the ~100 shared components.

**Key Characteristics:**

- Every lesson page follows the same skeleton: objectives → prerequisites → navigation → content → simulation → literature → navigation.
- Content is audience-forked (4Bio / 4Math) at the block level throughout, not just in a sidebar note.
- The only non-inherited interactive primitive is the raw `<input type="range">` parameter slider, styled to match the shared token palette but not sourced from the design package.
- Simulation charts use a fixed dark-phase-blue / light-phase-orange convention to mark experimental phases, independent of and layered on top of the shared chart component.

## Layout

- Every content page wraps its content in the shared `Main` (aliased `SectionMain as Main`) at `width="90ch"`, `align="start"` — a single centered reading column, not a multi-column dashboard layout. This is consistent across `photosynthesis`, `method`, `model`, `experiments`, `plant-memory`, `conclusion`.
- Canonical page skeleton, in order: `H1` (page title, from a translated headline key, rendered via `marked.parseInline`) → `InfoBox header="Learning objectives"` → `InfoBox header="What you need to know" variant="warning"` (prerequisites) → `PageNav` (prev/next to adjacent lesson pages) → body content (`H2` sections, `Text`, `Figure`, `Accordion`, `Math`) → simulation block (sliders + results) → `Accordion` for literature/citations → a second `PageNav` at the page bottom, mirroring the top one.
- `PageNav` appears exactly twice per lesson page (top, right after prerequisites, and bottom, after literature) — it is a page-boundary marker, not a floating/sticky element.
- The interactive slider panel (`.slider-row`) breaks the single-column rule deliberately: it is a card that goes to a 4-column grid at `768px` and up (`display: grid; grid-template-columns: 1fr 1fr 1fr 1fr`), collapsing to a stacked column below that breakpoint. This is the one place ComPhot defines its own responsive grid rather than delegating to a shared layout primitive.
- Simulation results (`PamResults`) render as a `charts-grid`: one column by default, three equal columns (`.three-cols`) only in the 4Bio audience, where NPQ and Φ(PSII) charts join the fluorescence chart; 4Math shows only the fluorescence chart.

## Components

### Audience-forked content block (signature pattern)

Not a component but the dominant compositional idiom on every page: any block whose meaning differs by audience is written as `{#if audienceStore.audience === "4math"} ... {:else} ... {/if}`, duplicating the surrounding shared component (`InfoBox`, `Ul`/`Li`, `H2`) rather than branching inside a single shared instance. Simple string-only differences use the `ta(bioValue, mathValue)` helper (`src/lib/i18n.ts`) inline instead of duplicating markup. Rule of thumb reflected in the code: fork the block when structure or item count differs (e.g. 4Bio's 5 learning objectives vs 4Math's fewer/different ones); use `ta()` when only a label or sentence differs.

### Parameter Slider (signature component — not in the shared library)

- **Markup:** native `<input type="range">` inside a `<label class="slider-label">` showing the live value inline (`{@html m.slider_x()}: <strong>{value}</strong>`), not the design package's `InputChoice`/`Tabs` controls (those are used elsewhere for discrete choices, not continuous parameters).
- **Style:** `accent-color: var(--color-primary)` — the one place a native form control is hand-styled to match the shared petrol primary rather than using a shared component's built-in styling. (Established/confirmed recently: see the "brand-color the parameter sliders" fix — this is a settled convention, not a one-off.)
- **Container:** sliders are grouped in a `.slider-row` card — `background-color: var(--color-surface)`, `border-radius: var(--radius-lg)`, `padding: 1.5rem` — using shared tokens for color/radius/spacing even though the slider itself is unstyled HTML.
- **Audience gating:** the first 3 sliders (light intensity, duration, pulse interval) are always shown; 4Bio-only pages add more sliders (activation/deactivation rate, dark length, saturating pulse) inside an `{#if audienceStore.audience === "4bio"}` block, directly extending the same `.slider-row` grid rather than opening a second panel.

### Simulation phase overlay (signature convention)

Every simulation chart (`LineChart`'s `phases` prop, type `PhaseRegion[]`) marks the dark-adaptation phase and the actinic-light phase with a fixed, repeated color pair:

- **Dark phase:** `rgba(28, 91, 199, 0.18–0.25)` — a blue overlay.
- **Light phase:** `rgba(207, 109, 12, 0.18–0.25)` — an orange overlay.

**The Dark-Blue, Light-Orange Rule.** Any new simulation that has a dark/light (or off/on) phase structure reuses exactly these two `rgba` values (opacity may vary 0.18–0.25 by chart density) rather than inventing a new phase palette — it is already load-bearing across `experiments` and `plant-memory` and reads as "the ComPhot phase convention," distinct from the shared design system's own chart-color tokens (`--chart-violet`, `--chart-blue`, `--chart-magenta`), which mark data series, not time regions.

### InfoBox usage convention

`InfoBox` (default variant) is reserved for "Learning objectives"; `InfoBox variant="warning"` is reserved for "What you need to know" prerequisites. No other `InfoBox` headers or variants are currently used — this is a strict two-slot convention, not a general-purpose callout.

### Math & code walkthroughs (4Math-only)

`Math` (KaTeX, `display` mode for block equations) and `Code`/`Pre` (for Python snippets) appear only inside `{#if audienceStore.audience === "4math"}` blocks, usually nested inside an `Accordion` (e.g. "reaction rates", "model code") rather than inline in the main flow — keeping the default (4Bio) reading path free of implementation detail while still letting the 4Math track expand into full derivations and code on demand.

## Do's and Don'ts

### Do:

- **Do** reuse the exact `H1 → objectives InfoBox → prerequisites InfoBox (warning) → PageNav → content → PageNav` skeleton for any new lesson page; it's already the pattern on all six lesson routes.
- **Do** fork audience-dependent structure as a duplicated block (`{#if 4math}...{:else}...{/if}`) and reserve `ta()` for single-string swaps.
- **Do** reuse the dark-blue/light-orange `rgba` pair for any new simulation's phase regions, so charts read consistently across pages.
- **Do** style any new native form control (if the shared library has no equivalent) with `accent-color: var(--color-primary)` and place it inside a `--color-surface` / `--radius-lg` card, matching the slider panel.

### Don't:

- **Don't** add colors, fonts, spacing values, or new component variants here — that's `pkg-js/design`'s job; a value needed here that doesn't exist there is a request to extend the shared package, not a local override.
- **Don't** use `InfoBox` for anything other than the two established slots (objectives / prerequisites-warning) without a clear new reason — it isn't a general callout box in this codebase's usage.
- **Don't** invent a second phase-color pair for a new simulation; extend the existing dark/light convention instead of introducing a third region color.
- **Don't** break the single `Main width="90ch"` reading column for ordinary content — the slider panel's grid is the one deliberate, narrow exception, not a precedent for general multi-column layout.
