import adapter from "@sveltejs/adapter-static";
import { existsSync } from "fs";
import { mdsvex } from "mdsvex";

// In the meta-repo, resolve the workspace packages from source for live edits;
// standalone installs fall back to the published package via its exports map.
const designSrc = new URL("../design/src/lib", import.meta.url).pathname;
const coreSrc = new URL("../../pkg/mxlweb-core/src", import.meta.url).pathname;
const workspaceAlias = {
  ...(existsSync(designSrc)
    ? { "@computational-biology-aachen/design": designSrc }
    : {}),
  ...(existsSync(coreSrc)
    ? { "@computational-biology-aachen/mxlweb-core": coreSrc }
    : {}),
};

/** @type {import('@sveltejs/kit').Config} */
const config = {
  compilerOptions: {
    // Force runes mode for the project, except for libraries. Can be removed in svelte 6.
    runes: ({ filename }) =>
      filename.split(/[/\\]/).includes("node_modules") ? undefined : true,
  },
  kit: {
    alias: workspaceAlias,
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
  },
  preprocess: [mdsvex({ extensions: [".svx", ".md"] })],
  extensions: [".svelte", ".svx", ".md"],
};

export default config;
