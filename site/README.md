# `site/` — public landing page

A lightweight, dependency-free static site that tells the project's story in under three
minutes and lets readers explore deeper. No backend, no framework, no external requests —
it runs from the filesystem and deploys as-is to GitHub Pages.

```
site/
├── index.html        # the landing page (8 sections + embedded interactive title wall)
├── styles.css        # all styling (responsive, mobile-first breakpoints)
├── build_site.py     # copies + optimizes curated charts into assets/ (deterministic)
└── assets/           # web-optimized images used by the page (generated)
```

## Sections
1. Hero story — "Oklahoma is not just a football school" (47 titles, 79% Olympic).
2. Interactive championship wall — every title by sport × year, with sport / decade / NCAA-vs-selector filters, hover cards, and dynasty-streak connectors.
3. Baseball case study — the 2026 title (incl. the honestly-logged Game-3 model miss).
4. Softball case study — greatest peak, contested future.
5. What the project demonstrates — for a data/analytics audience.
6. Selected-charts gallery.
7. Portfolio case-study summary.
8. Launch copy (GitHub, LinkedIn, X, Reddit, email pitch) with copy buttons.

## Preview locally
```bash
# regenerate the web-optimized assets from the source charts (after `make all`)
make site                          # or: python3 site/build_site.py

# serve it (any static server works)
python3 -m http.server --directory site 8000
# then open http://localhost:8000
```
You can also just open `site/index.html` directly in a browser.

## Deploy (GitHub Pages)
All paths are relative, so point Pages at either the repo root (visit `/site/`) or the
`/site` folder. No build step is required on the host — `assets/` is committed.

## Notes
- Images are downscaled to ≤1100px wide and re-saved optimized (`build_site.py`); the
  animated title-race GIF is copied as-is. Source charts are never moved or altered.
- The embedded title wall reuses the same 47-title dataset as `championships/`; it is
  self-contained (no fetch), so it works offline.
