---
target: site-wide (homepage + 6 lesson pages)
total_score: 24
max_score: 40
na_heuristics:
p0_count: 2
p1_count: 3
target_identity: "file:/home/marvin/git/0-admin/pages/comphot/site-wide (homepage + 6 lesson pages)"
timestamp: 2026-09-17T20-15-43Z
slug: site-wide-homepage-6-lesson-pages
closed: true
---

Method: dual-agent (A: design-review agent · B: detector-evidence agent)

## Design Health Score

| #         | Heuristic                       | Score     | Key Issue                                                                                                                                                  |
| --------- | ------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1         | Visibility of System Status     | 2         | No loading affordance for simulations; charts flash a garbled transitional layout before settling; locale switch gives no feedback that it silently failed |
| 2         | Match System / Real World       | 3         | Domain terms (NPQ, ΦPSII, PAM, Fm) correct and progressively explained                                                                                     |
| 3         | User Control and Freedom        | 3         | Sliders freely reversible, PageNav lets you roam; no "reset to defaults"                                                                                   |
| 4         | Consistency and Standards       | 1         | Navbar page names diverge from PageNav names on 5 of 8 pages; InfoBox header text reused out of context                                                    |
| 5         | Error Prevention                | 3         | Range inputs structurally prevent invalid values                                                                                                           |
| 6         | Recognition Rather Than Recall  | 2         | Audience/locale state hidden behind icon-only menus with no visible current-state label                                                                    |
| 7         | Flexibility and Efficiency      | 2         | No shareable/bookmarkable slider state, no shortcuts — acceptable for a Read-mode tool but not free                                                        |
| 8         | Aesthetic and Minimalist Design | 3         | Clean via the shared design system; chart-render jank and an uneven slider-grid layout                                                                     |
| 9         | Error Recovery                  | 2         | Solver-failure errors surface (`PamResults.svelte`) but with generic wording and no next-step guidance                                                     |
| 10        | Help and Documentation          | 3         | Nested Accordions with guiding questions + literature citations are strong in-flow help                                                                    |
| **Total** |                                 | **24/40** | **Acceptable — significant improvements needed before users are happy**                                                                                    |

## Design Specificity Verdict

**Mostly specific, with a rough, unfinished-feeling shell.**

**LLM assessment**: The audience fork is genuinely authored at the block level, not surface relabeling — `/model`'s 4Math track gets full LaTeX ODE systems plus runnable-style Python for the same SIR toy model that 4Bio gets as an "aliens on Planet-X" cartoon narrative. The phase-shaded "compare with last simulation" pattern in `PamResults.svelte` is bespoke to this simulation domain. That's real, product-specific design work. What drags the verdict down is the page skeleton itself: the "Learning objectives" InfoBox is reused verbatim as a generic mid-article callout on `/photosynthesis` with unrelated content, navbar and PageNav disagree on page names, and the homepage's own onboarding copy describes UI (a left sidebar, a "video transcripts" toggle) that doesn't exist in the current SvelteKit build. These read as an unproofed shell around carefully-authored content, not generic taste.

**Deterministic scan**: Static source scan (`npx impeccable detect` over `src/routes`, `src/lib`) came back **completely clean — 0 findings** — comphot's own code never hardcodes colors/fonts/shadows, everything routes through the shared design system's tokens/components. All 196 rendered-page findings came from browser (Puppeteer URL) scans across all 8 routes, desktop + mobile:

| Rule                                    | Count            | Verdict                                                                                                                                                                                                                                                                           |
| --------------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| line-length                             | 131              | False positive — the deliberate `Main width="90ch"` reading column, already tracked separately                                                                                                                                                                                    |
| side-tab                                | 18               | False positive — `InfoBox`'s documented 4px accent border (see `DESIGN.md` "InfoBox usage convention"); it carries an inline `impeccable-disable` comment that suppresses it for source scans but doesn't reach Puppeteer's rendered-page scans                                   |
| text-occlusion                          | 24 (mobile only) | Likely false positive — the detector force-opens the mobile burger `<details>` dropdown and flags its own intentional overlay-over-content behavior; worth a quick manual click-through to be 100% sure                                                                           |
| low-contrast                            | 17               | **Genuine** — `#727682` text on `#f6f6f8` background, 4.2:1 (needs 4.5:1), on 5 of 8 pages both viewports. Traces to muted chart axis/legend text in the shared `LineChart.svelte` component                                                                                      |
| body-text-viewport-edge / text-overflow | 6 (mobile only)  | **Genuine responsive bug** — long citation/literature links bleed off the right edge at 390px width, root-caused in the shared design package: `Ul.svelte`'s `grid-template-columns: 1fr` (needs `minmax(0, 1fr)`) and `Text.svelte`'s `<p>` missing `overflow-wrap`/`word-break` |

**Visual overlays**: No interactive browser tab was available to either assessment in this environment, so no live `[Human]`-tab overlay was injected. Assessment A instead captured static screenshots (desktop 1440×900 and mobile 390×844, across both audiences, saved to its scratchpad) and Assessment B relied on the detector's own headless Puppeteer URL scans rather than the injected-overlay flow.

## Overall Impression

The content and pedagogy are the strongest part of this site — real per-audience authoring, not a toggle bolted onto one text. But the skeleton around that content has drifted from what the copy claims it does: the homepage's own instructions for picking a learning track point at UI that no longer exists, and the navbar's advertised German/French locales don't actually translate anything. For a public teaching tool whose entire premise is "pick your track, in your language," those two gaps hit the product's core promise directly, not a peripheral feature.

## What's Working

1. **Real block-level pedagogy fork** — `/model`'s SIR section (cartoon vs. LaTeX+code tabs) and `/plant-memory`'s bio-only sliders vs. math-only derivations are genuinely different lessons, not relabeled text.
2. **"Compare with last simulation"** (`PamResults.svelte`) gives the sliders real formative-assessment value: a learner can see whether a parameter change helped or hurt, on the same axes.
3. **Self-quizzing accordions** (e.g. `/experiments`' guiding questions with a reveal-answers checkbox) are a well-crafted, low-friction check-your-understanding pattern.

## Priority Issues

**[P0] Broken instructions for the site's core personalization mechanism**

- **Why it matters**: The homepage tells first-time visitors to pick a track via "the left side panel... drop-down menu (you can also click on the highlighted text)." There is no left panel — the toggle lives in a top-right icon menu — and the inline `id="4Math"`/`id="4Bio"` links have no click handlers at all (verified live: `hasClickListeners: false`). A confused first-timer's very first instructed action is a dead click.
- **Fix**: Wire the anchors to `audienceStore.setAudience(...)`, or rewrite the onboarding copy to match the real top-right icon-menu UI.
- **Suggested command**: `/impeccable clarify`

**[P0] Locale switching doesn't translate the page**

- **Why it matters**: Verified live and via `curl`: navigating to `/de/photosynthesis` keeps `<html lang="en">` and English body text, even though the German translation already exists in `messages/de.json`. This is a skeleton-level failure across every page, not a per-page gap — for a site built specifically for RWTH Aachen and advertising de/fr as first-class locales, it's the most credibility-damaging failure mode available.
- **Fix**: Diagnose why locale resolution (`paraglideMiddleware`/`m.*()`) isn't reflected for this route; likely a reroute or hooks.server misconfiguration.
- **Suggested command**: `/impeccable harden`

**[P1] Navbar and PageNav disagree on page names**

- **Why it matters**: `+layout.svelte`'s hardcoded nav labels ("Method", "Model", "Experiments"...) differ from the `sde_pagenames_*` messages the in-page `PageNav` uses for the same destinations ("Measuring Method", "Computational Models", "Experiments in silico"...) on 5 of 8 pages. A user following a PageNav link and then checking the navbar to orient sees a different name for where they just went.
- **Fix**: Have both components read from the same `sde_pagenames_*` message source; this also fixes the navbar's own hardcoded, non-localized strings.
- **Suggested command**: `/impeccable clarify`

**[P1] InfoBox skeleton labels bypass i18n entirely**

- **Why it matters**: `header="Learning objectives"` and `header="What you need to know"` are literal English strings (12 occurrences across 6 pages) — unlike every other string on the same pages, which routes through `m.*()`. Even after the locale bug above is fixed, the most prominent box on every lesson page will never translate.
- **Fix**: Replace with proper message keys — translated equivalents already exist (e.g. a German "Lernziele" heading).
- **Suggested command**: `/impeccable harden`

**[P1] Long citation text overflows the viewport edge on mobile**

- **Why it matters**: At 390px width, literature/citation list items bleed off the right edge by up to 96px. Root cause lives in the shared design package, not comphot: `Ul.svelte`'s `grid-template-columns: 1fr` (should be `minmax(0, 1fr)`) and `Text.svelte`'s `<p>` sets `hyphens: auto` but no `overflow-wrap`/`word-break`, so a long inline citation link has no break opportunity.
- **Fix**: Fix in `pkg-js/design` (`Ul.svelte`, `Text.svelte`) since every consuming site shares this bug, not just comphot.
- **Suggested command**: `/impeccable adapt`

**[P2] Chart axis/legend text fails WCAG AA contrast**

- **Why it matters**: `#727682` text on `#f6f6f8` background measures 4.2:1 against a 4.5:1 AA requirement, on 17 occurrences across 5 lesson pages (both viewports). Likely the muted axis/legend text color in the shared `LineChart.svelte` component. Borderline, but a stated WCAG AA baseline is a specific commitment for this exact site (its public, multi-language, teaching-tool status is the named reason for that baseline).
- **Fix**: Darken the muted-text token slightly, or verify the exact rendered color against `--color-text-muted`.
- **Suggested command**: `/impeccable audit`

**[P2] Audience and language controls are unlabeled, equally-weighted icon menus**

- **Why it matters**: Both render as bare Material icons with no visible text and no current-state indicator until opened. Since the audience fork is the entire product's premise, giving it the same visual treatment as the purely cosmetic language switcher undersells the site's core mechanism — and low-vision users at higher zoom lose icon meaning entirely without a text label.
- **Fix**: Promote the audience toggle to an always-visible labeled control; reserve the icon-menu pattern for language.
- **Suggested command**: `/impeccable clarify`

## Persona Red Flags

**Jordan (Confused First-Timer)**: Reads the homepage's explicit instructions, looks left for a panel that isn't there, clicks the one thing that looks clickable ("4Math"), and nothing happens. Reasonable next thought: "this feature is broken," not "let me check the top-right corner."

**Sam (Accessibility-Dependent User)**: The audience/language triggers are icon-only menus with no visible text — worth confirming they carry proper `aria-label`s, since a Material-Symbols glyph is not reliably an accessible name on its own; low-vision users at higher zoom lose the icon's meaning entirely.

**A German/French RWTH student** (project-specific — the site is built specifically for RWTH Aachen and ships de/fr as first-class locales): opens the globe icon, picks "de," and gets a page indistinguishable from English except the URL. For a locale built specifically for this institution's own students, that's the single most credibility-damaging failure the site can produce.

## Minor Observations

- Source-level static scan came back 100% clean (0 findings) — comphot's own code has good discipline; every rendered-page problem traces to either an intentional shared-system pattern or the shared design package's own components.
- `side-tab` (18) and `text-occlusion` (24, mobile) detector findings are false positives from the scan methodology itself (InfoBox's documented accent border; the detector force-opening the mobile burger menu) — no action needed beyond confirming the burger-menu click-through once.
- `PamResults.svelte` charts show a visibly garbled, overlapping-label transitional layout before settling, with no spinner to cover it — a slow render could look broken rather than loading.
- The `.slider-row` 4-column grid produces uneven row heights on pages with many sliders (`plant-memory` has 9, `experiments` has 8) — a slightly uneven "bento box" look.
- `/contact`'s H1 carries a 📬 emoji — the only emoji across all eight pages, a small inconsistency.
- The homepage copy references a "Show video transcripts" option "on the left" that doesn't exist anywhere in the current UI — a second stale-copy artifact alongside the broken audience-picker instructions, suggesting the copy hasn't been reread since a pre-SvelteKit layout was replaced.
- On `/photosynthesis`, a second "Learning objectives" `InfoBox` mid-page wraps unrelated NPQ content — reads as a templating shortcut rather than intentional emphasis.

## Questions to Consider

1. If the homepage's own "how to use this site" text describes UI that hasn't existed since some earlier version (sidebar, transcript toggle, functional inline links), how much of the rest of the copy across eight pages is similarly stale?
2. The audience fork is the entire pedagogical premise of the product — why does it get the same UI treatment (a hidden icon dropdown) as the purely cosmetic language switcher?
3. Are `/de` and `/fr` a known work-in-progress, or a silent regression nobody has checked since the paraglide-js integration landed — given they're advertised in a live, always-visible navbar control?
