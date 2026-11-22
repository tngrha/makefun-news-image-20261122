// Entry program for news-image-20261122, written in-session 2026-11-22.
// Copies the pre-rendered front page (entry.png, drawn by render.py in this
// repo) to the grader output directory. No network, no dependencies.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(import.meta.dirname, "entry.png"), join(outDir, "entry.png"));
