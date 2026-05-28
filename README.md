# ComPhot

Educational photosynthesis site. SvelteKit 5, adapter-static, i18n via paraglide-js (en/de/fr). Python simulations run client-side via Pyodide. Deployed at `/comphot`.

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
