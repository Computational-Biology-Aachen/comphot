import { cpSync, readdirSync, readFileSync } from "fs";
import { createRequire } from "module";
import { dirname, extname, join } from "path";
import { paraglideVitePlugin } from "@inlang/paraglide-js";
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, type Plugin } from "vite";

const require = createRequire(import.meta.url);
const coreStatic = join(
  dirname(
    require.resolve("@computational-biology-aachen/mxlweb-core/package.json"),
  ),
  "static",
);

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
  plugins: [
    sveltekit(),
    paraglideVitePlugin({
      project: "./project.inlang",
      outdir: "./src/lib/paraglide",
    }),
    serveAndCopyCoreStatic(),
  ],
  server: { port: 5176, strictPort: true },
});
