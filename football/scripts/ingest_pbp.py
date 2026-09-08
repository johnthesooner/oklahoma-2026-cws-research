#!/usr/bin/env python3
"""
ingest_pbp.py — play-by-play EPA and success rate for Oklahoma, from a key-free source.

WHY THIS EXISTS. Earlier versions of this module marked EPA, success rate and every other
play-level metric `NOT_AVAILABLE`, with the stated blocker being the lack of a
CollegeFootballData API key. **That was wrong.** The sportsdataverse project publishes
pre-built, ESPN-derived college-football play-by-play as GitHub Release assets — the same
assets cfbfastR's `load_espn_cfb_pbp()` consumes — with no key, no account and no
authentication. The mislabel is logged in `data/contradictions_log.csv` and in
`football/audit/FOOTBALL_DATA_AUDIT.md`; a `NOT_AVAILABLE` that turns out to be available is
the most damaging kind of error a confidence-graded project can make, so it is recorded rather
than quietly corrected.

WHAT IT COMPUTES. For each season, Oklahoma's offensive and defensive EPA per play and success
rate, plus its national rank on each, both raw and with garbage time removed.

GARBAGE TIME. The field expects an explicit, published threshold rather than a silent filter.
This uses Connelly's widely republished thresholds — a play is garbage time when the offense
leads by more than 43 in Q1, 37 in Q2, 27 in Q3, or 21 in Q4/OT.

WHAT IT IS NOT. These figures are **not opponent-adjusted**. That matters enormously here:
Oklahoma played a top-15 schedule in both SEC seasons, so its raw EPA rank understates it
relative to opponent-adjusted systems like SP+. The gap between the two is itself informative
and is reported in the module rather than hidden.

Default window is 2021-2025 — the exact spans the report's SEC-transition question compares
(Big 12 2021-23 vs SEC 2024-25). Pass --seasons to widen it; the upstream covers 2004+.

Raw parquet is cached under football/sources/raw/pbp/ (gitignored, ~55 MB per season) and is
NOT redistributed; only derived aggregates are committed, with attribution.

Usage:  python3 football/scripts/ingest_pbp.py [--seasons 2021-2025] [--refresh]
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = ROOT / "sources" / "raw" / "pbp"
ASSET = ("https://github.com/sportsdataverse/sportsdataverse-data/releases/download/"
         "espn_cfb_pbp/play_by_play_{season}.parquet")
OU = "Oklahoma Sooners"
UA = "OUFootballResearch/1.0 (portfolio research; github.com/johnthesooner)"
# Connelly garbage-time thresholds: lead greater than N in that quarter.
GARBAGE = {1: 43, 2: 37, 3: 27, 4: 21}
MIN_PLAYS = 300          # teams below this are excluded from national ranking


def fetch(season: int, refresh: bool) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"play_by_play_{season}.parquet"
    if p.exists() and not refresh and p.stat().st_size > 1_000_000:
        return p
    url = ASSET.format(season=season)
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r, p.open("wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            print(f"  {season}: downloaded {p.stat().st_size / 1e6:.0f} MB")
            time.sleep(1)
            return p
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"{season}: download failed after 3 attempts ({last})")


def is_garbage(df: pd.DataFrame) -> pd.Series:
    """True where the play is garbage time by the Connelly thresholds."""
    lead = pd.to_numeric(df["pos_team_score"], errors="coerce") - pd.to_numeric(
        df["def_pos_team_score"], errors="coerce")
    period = pd.to_numeric(df["period"], errors="coerce").fillna(4).clip(1, 4)
    thresh = period.map(GARBAGE).astype(float)
    return lead > thresh


def side_summary(df: pd.DataFrame, team_col: str, label: str) -> dict:
    """Mean EPA/play and success rate for OU, plus national rank, on one side of the ball."""
    epa = pd.to_numeric(df["EPA"], errors="coerce")
    suc = pd.to_numeric(df["EPA_success"], errors="coerce")
    g = df.assign(_epa=epa, _suc=suc).groupby(team_col)
    agg = g.agg(epa=("_epa", "mean"), success=("_suc", "mean"), plays=("_epa", "size"))
    agg = agg[agg.plays >= MIN_PLAYS]
    if OU not in agg.index:
        return {}
    # offense: higher EPA better. defense: lower EPA allowed better.
    asc = label == "def"
    epa_rank = int(agg.epa.rank(ascending=asc, method="min").loc[OU])
    suc_rank = int(agg.success.rank(ascending=asc, method="min").loc[OU])
    r = agg.loc[OU]
    return {f"{label}_plays": int(r.plays), f"{label}_epa_play": round(float(r.epa), 4),
            f"{label}_epa_rank": epa_rank, f"{label}_success": round(float(r.success), 4),
            f"{label}_success_rank": suc_rank, "n_teams": int(len(agg))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", default="2021-2025", help="inclusive range, e.g. 2014-2025")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.seasons.split("-"))

    rows = []
    for season in range(lo, hi + 1):
        d = pd.read_parquet(fetch(season, args.refresh),
                            columns=["season", "pos_team", "def_pos_team", "EPA", "EPA_success",
                                     "pos_team_score", "def_pos_team_score", "period"])
        d = d[pd.to_numeric(d["EPA"], errors="coerce").notna()]
        clean = d[~is_garbage(d)]
        row = {"season": season}
        for frame, suffix in ((d, ""), (clean, "_cg")):
            off = side_summary(frame, "pos_team", "off")
            dfn = side_summary(frame, "def_pos_team", "def")
            if not off or not dfn:
                raise RuntimeError(f"{season}: Oklahoma missing or below the play floor")
            for k, v in {**off, **dfn}.items():
                row[f"{k}{suffix}" if k != "n_teams" else ("n_teams" + suffix)] = v
        row["confidence"] = "REPORTED"
        row["source"] = (f"{ASSET.format(season=season)} (sportsdataverse-data ESPN play-by-play "
                         "release asset, the same data cfbfastR's load_espn_cfb_pbp() reads; no API key)")
        row["note"] = ("EPA and success rate are NOT opponent-adjusted — OU played a top-15 schedule in "
                       "2024 and 2025, so these ranks understate it against adjusted systems like SP+. "
                       "'_cg' columns remove garbage time by the Connelly thresholds (lead > 43/37/27/21 "
                       f"by quarter). Teams below {MIN_PLAYS} plays are excluded from ranking.")
        rows.append(row)
        print(f"  {season}: OU offense {row['off_epa_play']:+.4f} EPA/play (#{row['off_epa_rank']} of "
              f"{row['n_teams']}), defense {row['def_epa_play']:+.4f} allowed (#{row['def_epa_rank']})")

    out = DATA / "epa_football.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"wrote {out} ({len(rows)} seasons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
