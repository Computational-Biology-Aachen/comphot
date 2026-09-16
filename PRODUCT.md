# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two overlapping audiences, both self-selected via a persistent 4Bio/4Math toggle rather than separate products: curious newcomers and more advanced learners in biology, and learners more comfortable with mathematics/computational modelling. Framed by the site itself as a university-level teaching tool ("21st-century students"), built by RWTH Aachen's Computational Life Science Lab, but deployed as a public static site (GitHub Pages, no login) rather than gated behind a specific course roster.

## Product Purpose

ComPhot ("Computational Photosynthesis") teaches photosynthesis — specifically light-dependent reactions, non-photochemical quenching (NPQ)/the xanthophyll cycle, and the PAM (Pulse Amplitude Modulation) fluorescence measurement method — through simulation-based learning rather than static text. Learners run real computational models client-side (via Pyodide) and manipulate parameters (light intensity, experiment duration, mutant conversion rates) to see how the underlying biology responds, instead of only reading about it. Success is a learner completing the site's page sequence (photosynthesis → method → model → plant-memory → experiments → conclusion) with a working intuition for how light intensity, NPQ, and short-term plant light memory relate, at the depth appropriate to their chosen track.

## Positioning

The 4Bio/4Math dual-track mechanism is the core differentiator: the same content sequence is genuinely re-authored per audience (different learning objectives, different depth of mathematical/implementation detail, different parameter exposure in the simulations — e.g. the 4Bio track exposes more mutant parameters and more outputs), not a single text with an optional appendix. It is also simulation-first: models are real, runnable Python (via Pyodide) or the shared mxlweb-core PAM implementation, not illustrative diagrams, and learners can create and investigate their own "in silico mutants."

## Operating Context

- Static SvelteKit 5 (adapter-static) site, deployed at `/comphot` under `computational-biology-aachen.github.io`.
- i18n via paraglide-js across en/de/fr, locale-prefixed routes (`/en/`, `/de/`, `/fr/`), handled client-side via reroute.
- Route sequence: home → `photosynthesis` → `method` → `model` → `plant-memory` → `experiments` → `conclusion`, plus `contact`. Content lives in `messages/{en,de,fr}.json` translation keys, not hardcoded in Svelte markup.
- Persistent client-side state: audience choice (4Bio/4Math, `localStorage`) and locale.
- Simulations run in-browser: `src/lib/simulations/pam.ts` and Pyodide workers (`src/lib/workers/pyWorker.ts`) execute Python model code client-side — no backend/server component.
- The PAM fluorescence model itself is not owned by this repo — it's consumed from the shared `@computational-biology-aachen/mxlweb-core` package's `./pam` export, so changes to the model's behavior originate upstream, not here.
- Part of the CPBL/mxl tool family (see root `CLAUDE.md`): sibling sites/tools include the main lab site, mxl-web (ODE explorer), MxlPy, mxl-bricks, and others.

## Capabilities and Constraints

- Consumes `@computational-biology-aachen/design` (shared Svelte 5 component + token library) and `@computational-biology-aachen/mxlweb-core` (compute engine + PAM model) as GitHub git dependencies — both are shared across the whole CPBL/mxl-web family, so component or model API changes originate upstream and propagate via `sync.sh`'s lockfile re-pin, not local edits here.
- No custom backend; all computation (Python model runs) happens client-side via Pyodide, so anything requiring server-side state or heavy compute is out of scope for this site.
- Content strings are centralized in `messages/{en,de,fr}.json` — new or changed copy must stay translatable across all three locales, not just English.
- WCAG AA accessibility baseline applies (inherited as a stated commitment of the shared design system, which explicitly names ComPhot's public/teaching nature as a reason for that baseline).

## Brand Commitments

- Site name "ComPhot" (Computational Photosynthesis); favicon `cpbl-favicon.svg`; affiliated with RWTH Aachen's Computational Life Science Lab (CPBL).
- Visual identity is entirely inherited, not local: ComPhot has no independent visual world and is not meant to grow one. `@computational-biology-aachen/design` (this meta-repo's `pkg-js/design`) is the binding design-system authority for every visual decision on this site — its `DESIGN.md`, `PRODUCT.md`, and `.impeccable/design.json` are the reference to load and extend for any future Impeccable design work here, rather than authoring a competing DESIGN.md for ComPhot itself. Concretely: RWTH petrol primary / RWTH orange accent, Space Grotesk typeface, the shared spacing/radius/shadow token scale, and the ~100-component library are all sourced from that package, loaded via `tokens.css` + Google Fonts `<link>` tags per the design package's own consumption contract.

## Evidence on Hand

- Full existing bilingual/trilingual content set in `messages/{en,de,fr}.json` covering photosynthesis biology, the FvCB/Bellasio/e-photosynthesis/CAM models, PAM methodology, and plant light memory — extensive real content, not placeholder copy.
- Introduction video embedded on the homepage (YouTube).
- No user research, usage analytics, or learner outcome data exists or applies — this is a public teaching resource, not a product with a funnel.

## Product Principles

- Every explanation and every simulation exists in two genuinely different depths (4Bio / 4Math), not one text with a toggle-hidden appendix — new content should extend both tracks, not just one.
- Simulate, don't just illustrate: prefer a runnable, parameter-manipulable model over a static diagram or canned chart wherever the underlying science supports it.
- Visual identity, layout primitives, and interactive chrome come from the shared design package; ComPhot's own work is content, simulations, and page composition — not new tokens, colors, or component variants.
- The compute/model layer is borrowed, not owned: PAM and other shared models are mxlweb-core's responsibility; ComPhot's job is presenting and contextualizing them for learners.
- Content is translation-first: copy changes go through the message-key system so en/de/fr stay in sync, never through hardcoded strings in components.

## Accessibility & Inclusion

WCAG AA baseline (inherited from the shared design system, which names ComPhot's public-facing, multi-language teaching-site status as a specific reason for that standard). No additional ComPhot-specific accessibility requirements are currently recorded.
