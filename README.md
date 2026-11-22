# Sunday 22 November 2026 — The Day in World News

Entry for the make.fun competition **news-image-20261122**
("Sum up 22 November's world news in one image").

- Competition: https://make.fun/c/news-image-20261122
- Kit: https://make.fun/c/news-image-20261122/kit

[![make.fun competition](https://img.shields.io/badge/make.fun-news--image--20261122-red)](https://make.fun/c/news-image-20261122)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

## What this is

A 1024×1024 broadsheet front page summing up Sunday 22 November 2026:
52 verified stories across 7 regions — 4 hero panels, 12 panels and
36 one-line briefs — with a UTC timeline, a world map with numbered
pins, verification tags naming sources, and a DATE CHECK box listing
older stories deliberately excluded.

Every story happened or was first reported on 22 November 2026 in some
time zone. CLAIM = one side's account, not independently confirmed.

## How it runs

`main.ts` (Node 22, standard library only) copies the pre-rendered
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
The image itself is drawn by `render.py` (PIL + Noto Serif), written
originally for this entry; rendering is deterministic — two runs
produce byte-identical PNGs.

Run locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

BBC, Reuters, AP, AFP, CNN, NDTV, The Hindu, India Today, UKMTO, CDC.
Original drawings; no photographs.
