# `championships/` — Oklahoma's National Championships (All Sports)

An evidence-first accounting of **every national championship the University of Oklahoma
claims, across every sport** — built inside the OU 2026 research repo, same integrity
standard (every figure `CONFIRMED / REPORTED / ESTIMATED / NOT_FOUND / CONFLICTING`;
nothing fabricated; conflicts surfaced).

## Headline (one line)
**47 national championships = 40 NCAA team titles + 7 football selector titles, across 7 sports —
and 79% are in Olympic/non-revenue sports (gymnastics, softball, wrestling, golf), not football.**
(47th: the 2026 baseball CWS title.)

## Structure
```
championships/
├── report/OKLAHOMA_NATIONAL_CHAMPIONSHIPS.md   # full report (8 sections)
├── data/        # 6 datasets (all confidence + source tagged)
├── charts/      # 4 charts (by sport, timeline, by decade, cumulative)
├── scripts/     # analyze_championships.py + validate_championships.py (with cross-foot checks)
└── audit/       # conflicts, resolutions, gaps
```

## Datasets (`championships/data/`)
- `ou_all_championships.csv` — the master: all 47 titles (year, sport, coach, basis, result, NCAA-vs-selector, shared flag)
- `titles_by_sport.csv` — per-sport counts, windows, coaches
- `titles_by_decade.csv` — distribution by decade (peak: 2010s = 12)
- `championship_coaches.csv` — 16 title-winning coaches and their years
- `football_unclaimed_titles.csv` — ~10 minor-selector years OU does NOT claim (REPORTED/CONFLICTING)
- `near_misses.csv` — recent runner-ups / deep runs that fell short (e.g., 2019 football CFP, 2022 baseball, 2025/26 softball)

## Reproduce
```bash
python3 championships/scripts/validate_championships.py   # 6/6 datasets + cross-foot to 47
python3 championships/scripts/analyze_championships.py     # aggregates + charts 01-04 (deterministic)
```

## Interactive
`viz/index.html` — a self-contained (dependency-free) interactive "championship wall":
every title as a point on a sport × year grid, hover for the story, click a sport to
isolate its dynasty run, plus a by-decade bar strip. Open it directly in a browser, or
`python3 -m http.server --directory championships/viz` and visit the printed URL. Deployable
as-is to any static host (Vercel / GitHub Pages).

## Key facts
- **By sport:** Men's Gymnastics 12 · Softball 8 · Women's Gymnastics 8 · Football 7 (selector) · Wrestling 7 · Baseball 3 · Men's Golf 2.
- **28 of 47 (60%) since 2000;** the 2010s produced a record 12.
- **Top coaches:** Mark Williams (9, men's gym), K.J. Kindler (8, women's gym), Patty Gasso (8, softball).
- **Football nuance:** 7 claimed, only **2000** fully undisputed (BCS+AP+Coaches); 1974 was AP-only (probation).
- **Shared titles:** 1977 men's gym and 2014 women's gym (tied Florida) — counted, but flagged.
- **2026 titles:** baseball (CWS, the 47th — first since 1994) and women's gymnastics (8th); softball missed the WCWS; men's gym was runner-up.

See [`audit/CHAMPIONSHIPS_AUDIT.md`](audit/CHAMPIONSHIPS_AUDIT.md) for conflicts and how each was resolved.
