import adapter from "@sveltejs/adapter-static";
import { mdsvex } from "mdsvex";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  compilerOptions: {
    // Force runes mode for the project, except for libraries. Can be removed in svelte 6.
    runes: ({ filename }) =>
      filename.split(/[/\\]/).includes("node_modules") ? undefined : true,
  },
  kit: {
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
