# `social/` — Social-Media Visualization Module

Turns the championships data into **share-ready visuals** sized to platform specs, plus
the research-backed playbook for posting them. Same integrity standard as the rest of the
repo: factual data only, sources on every graphic, **no team logos or photos** (school
colors + facts — the trademark/copyright-safe path).

## Contents
```
social/
├── SOCIAL_VIZ_PLAYBOOK.md        # what performs + platform specs + posting tactics (sourced, 2025-26)
├── scripts/make_social_assets.py  # deterministic generator (exact pixels = figsize x dpi)
└── out/                          # generated assets (a 6-slide carousel + square hero + GIF)
```

## What it generates (`out/`)
A **6-slide carousel** (the highest-engagement format for data content) + extras:

| File | Size | Role |
|---|---|---|
| `01_hero.png` / `01b_hero_square.png` | 1080×1350 / 1080×1080 | cover — "47" hero stat |
| `02_olympic_split.png` | 1080×1350 | the surprising "79% Olympic" stat |
| `03_title_wall.png` | 1080×1350 | every title, sport × year |
| `04_by_decade.png` | 1080×1080 | titles by decade (2010s = 12 peak) |
| `05_coaches.png` | 1080×1350 | 3 coaches won 25 of 47 |
| `06_cta.png` | 1080×1350 | close / call-to-action |
| `title_race.gif` | 720×720 | animated cumulative title count 1936→2026 |

Design once at three canvases — **1080×1350 (4:5)**, **1080×1080 (1:1)**, **1080×1920 (9:16)** —
covers all 10 platforms (see playbook). Crop the 4:5 masters to 1:1 for X/LinkedIn/Reddit/Bluesky.

## Reproduce
```bash
python3 social/scripts/make_social_assets.py   # writes social/out/ (deterministic)
```
Pure Python (matplotlib + Pillow for the GIF). Exact pixels via `figsize × dpi` (dpi=100).
The GIF uses `PillowWriter` (no ffmpeg dependency); if Pillow's writer is missing it is skipped
with a notice rather than failing the build.

## Posting (short version — full tactics in the playbook)
Carousels (IG/LinkedIn) + Reels/Shorts for reach; 3–5 specific hashtags; lead the caption with
the hook and tell people to **save it**; post around OU games / the June CWS window; communities
(public) r/Sooners, r/CFB, r/collegebaseball, r/CWS, X "CFB Twitter," Threads. Export clean (no
watermark), re-caption per platform, follow Reddit's 9:1 rule, and never use team logos/photos.
