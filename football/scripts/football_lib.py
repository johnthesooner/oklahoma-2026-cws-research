#!/usr/bin/env python3
"""
football_lib.py — pure, dependency-light helpers shared by the football module's
analysis script and its offline tests. No I/O in here.

Era boundaries, Pythagorean expectation, one-score classification, per-season
aggregation from a game log, and lagged joins for recruiting. Everything here is
deterministic and unit-tested (football/tests/test_football.py).
"""
from __future__ import annotations

from typing import Iterable

import pandas as pd

# Head-coach eras by SEASON. The 2021 Alamo Bowl was coached by Bob Stoops on an
# interim basis after Riley left; the season is still labelled Riley (documented
# in football/data/README.md). Venables runs 2022-present.
ERAS: list[tuple[str, int, int]] = [
    ("Stoops", 1999, 2016),
    ("Riley", 2017, 2021),
    ("Venables", 2022, 9999),
]
ERA_ORDER = ["Stoops", "Riley", "Venables"]
ERA_BOUNDARIES = [2017, 2022]          # first season of each new era (chart vlines)
PYTHAG_EXP = 2.37                      # standard college/NFL football exponent
ONE_SCORE_MARGIN = 8                   # |margin| <= 8 == one possession


def era_for_season(season: int) -> str:
    """Map a season year to its head-coach era label."""
    for name, start, end in ERAS:
        if start <= season <= end:
            return name
    raise ValueError(f"season {season} predates the Stoops era (1999)")


def pythagorean_wins(pf: float, pa: float, games: int, exp: float = PYTHAG_EXP) -> float:
    """Expected wins from points for/against (Pythagorean expectation)."""
    if pf <= 0 and pa <= 0:
        return 0.0
    pct = pf ** exp / (pf ** exp + pa ** exp)
    return pct * games


def is_one_score(margin: int) -> bool:
    """True if the final margin was one possession (8 points or fewer)."""
    return abs(int(margin)) <= ONE_SCORE_MARGIN


def conference_for_season(season: int) -> str:
    """OU's conference by season: Big 12 through 2023, SEC from 2024."""
    return "SEC" if season >= 2024 else "Big 12"


def aggregate_seasons(games: pd.DataFrame) -> pd.DataFrame:
    """Per-season W, L, PF, PA, games, margin/G from a game log.

    Expects columns: season, result (W/L), ou_pts, opp_pts. Ignores any rows
    whose `status` column (if present) is not FINAL, so an in-progress tracker
    can share the function.
    """
    g = games.copy()
    if "status" in g.columns:
        g = g[g["status"].astype(str).str.upper() == "FINAL"]
    g["ou_pts"] = pd.to_numeric(g["ou_pts"])
    g["opp_pts"] = pd.to_numeric(g["opp_pts"])
    g["w"] = (g["result"].astype(str).str.upper() == "W").astype(int)
    g["l"] = (g["result"].astype(str).str.upper() == "L").astype(int)
    agg = (g.groupby("season")
             .agg(G=("result", "size"), W=("w", "sum"), L=("l", "sum"),
                  PF=("ou_pts", "sum"), PA=("opp_pts", "sum"))
             .reset_index())
    agg["margin_pg"] = (agg["PF"] - agg["PA"]) / agg["G"]
    agg["win_pct"] = agg["W"] / agg["G"]
    return agg


def dedupe_games(games: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate game rows (same season, date, opponent)."""
    return games.drop_duplicates(subset=["season", "date", "opponent"]).reset_index(drop=True)


def lag_join(seasons: pd.DataFrame, recruiting: pd.DataFrame, lag: int,
             value_col: str = "rank_247_composite") -> pd.DataFrame:
    """Attach the recruiting rank from `lag` years earlier to each season.

    A class signed in February of year Y is at its (Y + lag) season. E.g. lag=3:
    the 2015 season is joined to the 2012 class.
    """
    r = recruiting[["class_year", value_col]].copy()
    r["season"] = r["class_year"].astype(int) + lag
    r = r.rename(columns={value_col: f"{value_col}_lag{lag}"}).drop(columns=["class_year"])
    return seasons.merge(r, on="season", how="left")


def record_str(w: int, l: int) -> str:
    return f"{int(w)}-{int(l)}"


def mean_or_nan(values: Iterable[float]) -> float:
    vals = [v for v in values if pd.notna(v)]
    return sum(vals) / len(vals) if vals else float("nan")
