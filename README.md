# ComPhot

Educational photosynthesis site. SvelteKit 5, adapter-static, i18n via paraglide-js (en/de/fr). Python simulations run client-side via Pyodide. Deployed at `/comphot`.

Model building and the compute backends come from the shared [`@computational-biology-aachen/mxlweb-core`](https://github.com/Computational-Biology-Aachen/mxlweb-core) package (the PAM fluorescence model is consumed from its `./pam` export).

## Dev

```bash
npm install
npm run dev          # dev server on :5173
```

## Commands

```bash
npm run build        # static build → build/
npm run preview      # preview the build
npm run check        # TypeScript + Svelte type checking
npm run lint         # Prettier + ESLint check
npm run format       # auto-format with Prettier
```

## i18n

Message files: `messages/{en,de,fr}.json`. Locale-prefixed URLs (`/en/`, `/de/`, `/fr/`) handled client-side via reroute; static build suppresses 404s for these paths.

## Tool family 🏠

`ComPhot` is part of a larger ecosystem:

- [mxlweb-core](https://github.com/Computational-Biology-Aachen/mxlweb-core) — shared model-building and compute engine powering this site
- [MxlWeb](https://github.com/Computational-Biology-Aachen/mxl-web) — browser-side ODE model explorer
- [MxlPy](https://github.com/Computational-Biology-Aachen/MxlPy) — Python package for mechanistic learning
- [MxlBricks](https://github.com/Computational-Biology-Aachen/mxl-bricks) — pre-defined reaction bricks on top of MxlPy
- [MxlModels](https://github.com/Computational-Biology-Aachen/mxl-models) — flat single-file model versions for easy inspection
- [pysbml](https://github.com/Computational-Biology-Aachen/pysbml) — SBML import/export for MxlPy
- [Parameteriser](https://gitlab.com/marvin.vanaalst/parameteriser) — kinetic parameter lookup from BRENDA and other databases
