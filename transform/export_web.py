#!/usr/bin/env python3
"""
export_web.py — export the dbt marts to a small JSON bundle for the static explorer.

Why not Evidence.dev: as of 2026-09 Evidence ships as a separately-installed binary that
requires an account and `evidence login`. This project's differentiator is that anyone can
rebuild every artifact from source with no server, no credentials and no vendor account, and a
login-gated build tool would break exactly that. The explorer is therefore a static page over
this bundle, which keeps the guarantee intact.

Reads transform/oklahoma.duckdb (built by `make dbt`) and writes site/data/explorer.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "transform" / "oklahoma.duckdb"
OUT = ROOT / "site" / "data" / "explorer.json"

QUERIES = {
    "eras": "select * from main_marts.mart_era_summary",
    "seasons": "select * from main_marts.mart_season_performance order by season",
    "units": "select * from main_marts.mart_unit_swap order by season",
    "games": """select season, cast(game_date as varchar) as game_date, opponent,
                       opponent_ap_rank, site, result, points_for, points_against, margin,
                       is_one_score, is_conference_game, game_type, went_overtime, era
                from main_staging.stg_games order by season, game_date""",
}


def main() -> int:
    if not DB.exists():
        print(f"error: {DB} not found — run `make dbt` first", file=sys.stderr)
        return 1
    con = duckdb.connect(str(DB), read_only=True)
    bundle = {}
    for name, sql in QUERIES.items():
        df = con.sql(sql).df()
        bundle[name] = json.loads(df.to_json(orient="records"))
        print(f"  {name}: {len(bundle[name])} rows")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # sort_keys + fixed separators so the bundle is byte-stable across runs
    OUT.write_text(json.dumps(bundle, sort_keys=True, separators=(",", ":")))
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
