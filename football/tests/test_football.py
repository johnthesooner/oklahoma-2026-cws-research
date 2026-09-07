"""Offline unit tests for the football module's pure helpers and for the
committed datasets' internal consistency. Runs with no network access.

    python3 -m pytest football/tests -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]          # football/
sys.path.insert(0, str(ROOT / "scripts"))

import football_lib as fl  # noqa: E402

FIX = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------- pure functions
@pytest.mark.parametrize("season,era", [
    (1999, "Stoops"), (2016, "Stoops"), (2017, "Riley"), (2021, "Riley"),
    (2022, "Venables"), (2025, "Venables"), (2026, "Venables"),
])
def test_era_boundaries(season, era):
    assert fl.era_for_season(season) == era


def test_era_before_1999_raises():
    with pytest.raises(ValueError):
        fl.era_for_season(1998)


def test_pythagorean_symmetric_and_bounded():
    assert fl.pythagorean_wins(300, 300, 12) == pytest.approx(6.0)
    assert 0 <= fl.pythagorean_wins(500, 100, 13) <= 13
    assert fl.pythagorean_wins(500, 100, 13) > fl.pythagorean_wins(300, 300, 13)
    assert fl.pythagorean_wins(0, 0, 12) == 0.0


def test_pythagorean_known_value():
    # 2000 OU: 481 PF, 194 PA over 13 games (fixture-independent sanity value)
    exp = fl.pythagorean_wins(481, 194, 13)
    assert 11.5 < exp < 13.0


@pytest.mark.parametrize("margin,expected", [(8, True), (-8, True), (3, True), (9, False), (-20, False), (0, True)])
def test_one_score(margin, expected):
    assert fl.is_one_score(margin) is expected


def test_conference_switch():
    assert fl.conference_for_season(2023) == "Big 12"
    assert fl.conference_for_season(2024) == "SEC"


def test_aggregate_seasons_from_fixture():
    g = pd.read_csv(FIX / "games_sample.csv")
    agg = fl.aggregate_seasons(g).set_index("season")
    # fixture: 2020 has 3 rows (2 W, 1 L); 2024 has 2 rows (1 W, 1 L)
    assert agg.loc[2020, "W"] == 2 and agg.loc[2020, "L"] == 1
    assert agg.loc[2020, "PF"] == 48 + 35 + 53
    assert agg.loc[2020, "PA"] == 0 + 38 + 45
    assert agg.loc[2024, "G"] == 2
    assert agg.loc[2024, "margin_pg"] == pytest.approx(((20 + 24) - (21 + 3)) / 2)


def test_aggregate_ignores_pending_rows():
    g = pd.DataFrame({
        "season": [2026, 2026], "result": ["W", ""], "ou_pts": [51, ""],
        "opp_pts": [0, ""], "status": ["FINAL", "PENDING"],
    })
    agg = fl.aggregate_seasons(g)
    assert agg.loc[0, "G"] == 1 and agg.loc[0, "W"] == 1


def test_dedupe_games():
    g = pd.read_csv(FIX / "games_sample.csv")
    doubled = pd.concat([g, g.iloc[[0]]])
    assert len(fl.dedupe_games(doubled)) == len(g)


def test_lag_join_alignment():
    seasons = pd.DataFrame({"season": [2014, 2015, 2016]})
    rec = pd.DataFrame({"class_year": [2012, 2013], "rank_247_composite": [11, 16]})
    out = fl.lag_join(seasons, rec, lag=3).set_index("season")
    assert out.loc[2015, "rank_247_composite_lag3"] == 11
    assert out.loc[2016, "rank_247_composite_lag3"] == 16
    assert pd.isna(out.loc[2014, "rank_247_composite_lag3"])


# ---------------------------------------------------------- committed datasets
DATA = ROOT / "data"
HAS_DATA = (DATA / "games_football.csv").exists() and (DATA / "seasons_football.csv").exists()


@pytest.mark.skipif(not HAS_DATA, reason="datasets not built yet")
def test_games_crossfoot_to_seasons():
    games = pd.read_csv(DATA / "games_football.csv")
    seasons = pd.read_csv(DATA / "seasons_football.csv").set_index("season")
    agg = fl.aggregate_seasons(games).set_index("season")
    for s, row in agg.iterrows():
        assert row["W"] == seasons.loc[s, "W"], f"{s} wins mismatch"
        assert row["L"] == seasons.loc[s, "L"], f"{s} losses mismatch"
        assert row["PF"] == seasons.loc[s, "PF"], f"{s} PF mismatch"
        assert row["PA"] == seasons.loc[s, "PA"], f"{s} PA mismatch"


@pytest.mark.skipif(not HAS_DATA, reason="datasets not built yet")
def test_games_no_2026_and_result_matches_score():
    games = pd.read_csv(DATA / "games_football.csv")
    assert games["season"].max() == 2025
    assert games["season"].min() == 1999
    won = games["ou_pts"] > games["opp_pts"]
    assert (won == (games["result"] == "W")).all()
    assert games.duplicated(subset=["season", "date", "opponent"]).sum() == 0


@pytest.mark.skipif(not HAS_DATA, reason="datasets not built yet")
def test_2020_covid_season_short():
    games = pd.read_csv(DATA / "games_football.csv")
    assert len(games[games.season == 2020]) == 11


@pytest.mark.skipif(not HAS_DATA, reason="datasets not built yet")
def test_anchor_records():
    seasons = pd.read_csv(DATA / "seasons_football.csv").set_index("season")
    assert (seasons.loc[2000, "W"], seasons.loc[2000, "L"]) == (13, 0)
    assert (seasons.loc[2024, "W"], seasons.loc[2024, "L"]) == (6, 7)
    assert (seasons.loc[2025, "W"], seasons.loc[2025, "L"]) == (10, 3)
    stoops = seasons[seasons.era == "Stoops"]
    assert (stoops.W.sum(), stoops.L.sum()) == (190, 48)
    riley = seasons[seasons.era == "Riley"]
    # Riley-era seasons sum to 56-10 because the 2021 Alamo Bowl (W) was coached
    # by interim Bob Stoops; Riley's personal record is 55-10.
    assert (riley.W.sum(), riley.L.sum()) == (56, 10)
