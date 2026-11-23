# Sunday 22 November 2026 — the world's news in one image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/tngrha/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/tngrha/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the make.fun competition `news-image-20261122`
("Sum up 22 November's world news in one image"), revision 2.

A broadsheet front page rendered in code: masthead with the true story count,
a UTC timeline of the day, 4 hero panels and 12 small panels with original
flat illustrations, a pinned world map, 36 one-line briefs grouped by region,
and a date-check box listing stories deliberately left out because they are
not Sunday's news. 52 stories across 7 regions, each panel carrying a
verification tag (CONFIRMED / REPORTED / CLAIM) and a named source.

## How it works

- `render.py` — build-time renderer (Python 3 + Pillow, Noto Serif type).
  Run `python3 render.py` to regenerate `entry.png` (1024×1024 PNG).
- `entry.png` — the rendered front page.
- `main.ts` — the competition entrypoint (Node 22): copies `entry.png` to
  `/output/entry.png`. Same bytes every run, no network.
- `stories.md` — the verification record: every story, its source outlet,
  and the date-check exclusions with their real dates.

Run locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

All drawings are original vector-style shapes drawn in code; all headlines
were written for this entry from the cited reporting.

---

<sub>Entered on [make.fun](https://make.fun/?ref=px8mhdxd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
