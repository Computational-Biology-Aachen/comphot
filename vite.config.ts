import { cpSync, existsSync, readdirSync, readFileSync } from "fs";
import { createRequire } from "module";
import { dirname, extname, join } from "path";
import { paraglideVitePlugin } from "@inlang/paraglide-js";
import adapter from "@sveltejs/adapter-static";
import { sveltekit } from "@sveltejs/kit/vite";
import { mdsvex } from "mdsvex";
import { defineConfig, type Plugin } from "vite";

const require = createRequire(import.meta.url);
const coreStatic = join(
  dirname(
    require.resolve("@computational-biology-aachen/mxlweb-core/package.json"),
  ),
  "static",
);

// In the meta-repo, workspaceAlias below points the design package at its
// source under ../../pkg-js/design/src/lib for live edits. That makes imports resolve relative to ../../pkg-js/design, so a
// package it depends on (e.g. katex, for its fonts) can resolve to
// ../../pkg-js/design's own nested node_modules rather than this project's —
// which SvelteKit's dev server doesn't allow serving from by default. Allow
// it explicitly when present.
const designNodeModules = new URL(
  "../../pkg-js/design/node_modules",
  import.meta.url,
).pathname;
const designSrc = new URL("../../pkg-js/design/src/lib", import.meta.url)
  .pathname;
const coreSrc = new URL("../../pkg-js/mxlweb-core/src", import.meta.url)
  .pathname;

// In the meta-repo, resolve the workspace packages from source for live edits;
// standalone installs fall back to the published package via its exports map.
const workspaceAlias: Record<string, string> = {
  ...(existsSync(designSrc)
    ? { "@computational-biology-aachen/design": designSrc }
    : {}),
  ...(existsSync(coreSrc)
    ? { "@computational-biology-aachen/mxlweb-core": coreSrc }
    : {}),
};

const MIME: Record<string, string> = {
  ".js": "application/javascript",
  ".wasm": "application/wasm",
};

function serveAndCopyCoreStatic(): Plugin {
  return {
    name: "mxlweb-core-static",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split("?")[0] ?? "";
        const filePath = join(coreStatic, url);
        try {
          const content = readFileSync(filePath);
          res.setHeader(
            "Content-Type",
            MIME[extname(filePath)] ?? "application/octet-stream",
          );
          res.end(content);
        } catch {
          next();
        }
      });
    },
    closeBundle() {
      if (this.environment?.name !== "client") return;
      const wasmSrc = join(coreStatic, "wasm");
      // Copy into the client output dir so adapter-static picks them up
      const wasmDest = join(".svelte-kit", "output", "client", "wasm");
      const files = readdirSync(wasmSrc).filter((f) => f !== ".gitkeep");
      cpSync(wasmSrc, wasmDest, {
        recursive: true,
        filter: (f) => !f.endsWith(".gitkeep"),
      });
      this.warn?.(`copied ${files.length} wasm files → ${wasmDest}`);
    },
  };
}

export default defineConfig({
  resolve: { alias: workspaceAlias },
  plugins: [
    sveltekit({
      compilerOptions: {
        // Force runes mode for the project, except for libraries. Can be removed in svelte 6.
        runes: ({ filename }) =>
          filename.split(/[/\\]/).includes("node_modules") ? undefined : true,
      },
      adapter: adapter(),
      prerender: {
        handleHttpError: ({ path, message }) => {
          // Paraglide locale-prefixed URLs are handled client-side via reroute;
          // suppress 404s for these paths in the static build.
          if (/\/(en|de|fr|es|pl)(\/|$)/.test(path)) {
            return;
          }
          throw new Error(message);
        },
      },
      paths: {
        base: process.argv.includes("dev") ? "" : "/comphot",
      },
      version: {
        // Poll for new deploys so long-lived tabs upgrade proactively instead of
        // only recovering reactively after a failed navigation.
        pollInterval: 300_000,
      },
      preprocess: [mdsvex({ extensions: [".svx", ".md"] })],
      extensions: [".svelte", ".svx", ".md"],
    }),
    paraglideVitePlugin({
      project: "./project.inlang",
      outdir: "./src/lib/paraglide",
      // This site is locale-prefixed (/de/, /fr/) and statically prerendered
      // for GitHub Pages — there's no server to read a cookie after deploy,
      // so the URL must be the source of truth for locale resolution. The
      // plugin's own default strategy omits "url" entirely, which is why
      // locale-prefixed routes were silently rendering baseLocale (English).
      strategy: ["url", "baseLocale"],
    }),
    serveAndCopyCoreStatic(),
  ],
  server: {
    port: 5176,
    strictPort: true,
    fs: {
      allow: existsSync(designSrc) ? [designNodeModules] : undefined,
    },
  },
});
