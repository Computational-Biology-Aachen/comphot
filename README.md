# ComPhot

Educational photosynthesis site. SvelteKit 5, adapter-static, i18n via paraglide-js (en/de/fr). Python simulations run client-side via Pyodide. Deployed at `/comphot`.

## Dev

```bash
bun install
bun run dev          # dev server on :5173
```

## Commands

```bash
bun run build        # static build → build/
bun run preview      # preview the build
bun run check        # TypeScript + Svelte type checking
bun run lint         # Prettier + ESLint check
bun run format       # auto-format with Prettier
```

## i18n

Message files: `messages/{en,de,fr}.json`. Locale-prefixed URLs (`/en/`, `/de/`, `/fr/`) handled client-side via reroute; static build suppresses 404s for these paths.
