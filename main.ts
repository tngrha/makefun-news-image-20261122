// main.ts — entrypoint for make.fun competition news-image-20261122 (revision 2).
// Copies the pre-rendered front-page image (entry.png, built by render.py)
// to /output/entry.png. Deterministic: same bytes on every run, no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
