#!/usr/bin/env python3
"""
build_site.py — copy a curated set of existing chart outputs into site/assets/,
optimized for web. Deterministic; does NOT move or alter source data/charts.

PNGs wider than MAXW are downscaled (LANCZOS) and re-saved with optimize=True;
the GIF is copied as-is. The curated list is the gallery + case-study imagery for
the public landing page. Re-run with `make site` after `make all` regenerates charts.
"""
from __future__ import annotations
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path(__file__).resolve().parent / "assets"
MAXW = 1100

# (source relative to repo root, destination filename in site/assets/)
PNGS = [
    ("charts/01_ranking_trajectory.png", "bb_ranking.png"),
    ("charts/02_postseason_scores.png", "bb_postseason.png"),
    ("charts/03_power_surge.png", "bb_power.png"),
    ("charts/22_monte_carlo_finals.png", "bb_montecarlo.png"),
    ("charts/20_champ_separation.png", "bb_pca.png"),
    ("charts/17_ratings_comparison.png", "bb_ratings.png"),
    ("softball/charts/01_dynasty_timeline.png", "sb_timeline.png"),
    ("softball/charts/02_run_prevention.png", "sb_runprev.png"),
    ("softball/charts/04_titles_leaderboard.png", "sb_leaderboard.png"),
    ("softball/charts/05_best_ou_teams.png", "sb_bestteams.png"),
    ("football/charts/01_winpct_margin_by_era.png", "fb_eras.png"),
    ("football/charts/03_unit_ranks_over_time.png", "fb_units.png"),
    ("football/charts/04_sos_big12_vs_sec.png", "fb_sos.png"),
    ("football/charts/05_actual_vs_pythagorean.png", "fb_luck.png"),
    ("championships/charts/01_titles_by_sport.png", "champ_bysport.png"),
    ("championships/charts/02_title_timeline.png", "champ_timeline.png"),
    ("championships/charts/04_cumulative_titles.png", "champ_cumulative.png"),
    ("social/out/01_hero.png", "social_hero.png"),
    ("social/out/02_olympic_split.png", "social_split.png"),
]
COPIES = [("social/out/title_race.gif", "title_race.gif")]


def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    total = 0
    for src, dst in PNGS:
        p = ROOT / src
        if not p.exists():
            print(f"  [missing] {src}"); continue
        im = Image.open(p)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        if im.width > MAXW:
            h = round(im.height * MAXW / im.width)
            im = im.resize((MAXW, h), Image.LANCZOS)
        out = ASSETS / dst
        im.save(out, optimize=True)
        kb = out.stat().st_size // 1024
        total += kb
        print(f"  {dst:24s} {im.width}x{im.height}  {kb} KB")
    for src, dst in COPIES:
        p = ROOT / src
        if p.exists():
            shutil.copy2(p, ASSETS / dst)
            kb = (ASSETS / dst).stat().st_size // 1024
            total += kb
            print(f"  {dst:24s} (copied)  {kb} KB")
    print(f"\nsite/assets/ built — {len(PNGS) + len(COPIES)} files, ~{total} KB total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
