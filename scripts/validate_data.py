#!/usr/bin/env python3
"""
validate_data.py — schema, integrity, and provenance validation for the
2026 Oklahoma Sooners CWS research datasets.

Checks every CSV in data/ for:
  1. Schema        — exact expected column set.
  2. Row counts    — at least the expected number of data rows.
  3. Missing values— no empty cells in identity ("key") columns.
  4. Confidence    — every confidence label is from the allowed vocabulary.
  5. Source fields — every row has a non-empty source/provenance value.
  6. Numeric sanity— rate/counting columns parse and fall in plausible ranges
                     (explicit NA / NOT_FOUND / NOT_AVAILABLE markers are allowed).

Exit code 0 = all datasets valid; 1 = one or more hard failures.
No network, no fabrication: this only inspects local files.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

# Allowed confidence vocabulary (a value may carry a "-suffix", e.g. CONFIRMED-score).
ALLOWED_CONFIDENCE = {"CONFIRMED", "REPORTED", "ESTIMATED", "NOT_FOUND", "NOT_AVAILABLE"}
# Markers that legitimately stand in for "no public data" — never treated as errors.
MISSING_MARKERS = {"", "NA", "NOT_FOUND", "NOT_AVAILABLE", "none", "RV"}

# Per-dataset schema registry. min_rows is a floor, not an exact count.
REGISTRY = {
    "team_batting.csv": {
        "columns": ["metric", "oklahoma", "opponents", "confidence", "note", "source"],
        "min_rows": 18, "key": ["metric"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "team_pitching_fielding.csv": {
        "columns": ["metric", "oklahoma", "opponents", "confidence", "note", "source"],
        "min_rows": 28, "key": ["metric"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "hitters.csv": {
        "columns": ["player", "pos", "class", "GP", "GS", "AVG", "OBP", "SLG", "OPS",
                    "HR", "RBI", "BB", "SO", "SB", "SB_att", "confidence", "source"],
        "min_rows": 12, "key": ["player", "pos", "class"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_rate": ["AVG", "OBP", "SLG", "OPS"],
        "numeric_count": ["GP", "GS", "HR", "RBI", "BB", "SO", "SB", "SB_att"],
    },
    "pitchers.csv": {
        "columns": ["pitcher", "class", "role", "ERA", "W", "L", "SV", "IP",
                    "H", "BB", "SO", "opp_AVG", "confidence", "source"],
        "min_rows": 14, "key": ["pitcher", "class", "role"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_rate": ["opp_AVG"],
        "numeric_count": ["W", "L", "SV", "H", "BB", "SO"],
    },
    "postseason_games.csv": {
        "columns": ["game", "date", "round", "opponent", "opp_seed", "result",
                    "ou_runs", "opp_runs", "ou_hr", "key_performers",
                    "ou_starter_line", "confidence", "source"],
        "min_rows": 12, "key": ["game", "date", "round", "opponent"],
        "confidence_col": "confidence", "source_col": "source",
        "result_col": "result", "allowed_results": {"W", "L", "PENDING", "CONDITIONAL"},
    },
    "cws_opponents.csv": {
        "columns": ["team", "record", "national_seed", "final_rank_d1b", "team_AVG",
                    "team_ERA", "team_HR", "confidence", "source", "note"],
        "min_rows": 6, "key": ["team", "national_seed"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "record_and_rankings.csv": {
        "columns": ["item", "value", "confidence", "source"],
        "min_rows": 20, "key": ["item", "value"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "champions.csv": {
        "columns": ["year", "team", "status", "W", "L", "T", "conf_record",
                    "national_seed", "rpi", "G", "R", "RA", "AVG", "OBP", "SLG",
                    "HR", "ERA", "IP", "H_allowed", "BB_allowed", "K_pitch",
                    "opp_AVG", "FLD_pct", "E", "DP", "confidence", "source"],
        "min_rows": 22, "key": ["year", "team", "status"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_rate": ["AVG", "OBP", "SLG", "opp_AVG", "FLD_pct"],
        "numeric_count": ["W", "L", "G", "HR"],
    },
    "game_log.csv": {
        "columns": ["game", "date", "opponent", "site", "ou_runs", "opp_runs",
                    "result", "conf_game", "confidence", "source"],
        "min_rows": 64, "key": ["game", "date", "opponent"],
        "confidence_col": "confidence", "source_col": "source",
        "result_col": "result", "allowed_results": {"W", "L"},
        "numeric_count": ["ou_runs", "opp_runs"],
    },
    "ratings.csv": {
        "columns": ["system", "scope", "ou_value", "ou_rank",
                    "unc_value", "unc_rank", "as_of",
                    "opponent_adjusted", "confidence", "source", "note"],
        "min_rows": 7, "key": ["system", "scope"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "historical_cws_context.csv": {
        "columns": ["topic", "subject", "finding", "value",
                    "confidence", "source", "note"],
        "min_rows": 18, "key": ["topic", "subject"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "betting.csv": {
        "columns": ["type", "stage", "opponent", "ou_odds_american",
                    "implied_prob_pct", "result", "confidence", "source", "note"],
        "min_rows": 12, "key": ["type", "stage"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "cws_field.csv": {
        "columns": ["year", "team", "cws_result", "national_seed", "W", "L", "G",
                    "R", "RA", "AVG", "OBP", "SLG", "HR", "ERA", "IP", "H_allowed",
                    "BB_allowed", "K_pitch", "opp_AVG", "FLD_pct", "E",
                    "is_champion", "confidence", "source"],
        "min_rows": 41, "key": ["year", "team", "cws_result"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_rate": ["AVG", "OBP", "SLG", "opp_AVG", "FLD_pct"],
        "numeric_count": ["W", "L", "G", "HR"],
    },
    "opponents_2026.csv": {
        "columns": ["opponent", "record_2026", "win_pct", "made_NCAA",
                    "national_seed", "R_per_g", "RA_per_g", "rates_quality",
                    "confidence", "source"],
        "min_rows": 27, "key": ["opponent", "record_2026"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_rate": ["win_pct"],
    },
    # Meta-tables (predictions / contradictions): schema + rows + keys only.
    "predictions_ledger.csv": {
        "columns": ["id", "date_made", "prediction", "basis", "confidence",
                    "status", "resolution"],
        "min_rows": 6, "key": ["id", "prediction"],
    },
    "contradictions_log.csv": {
        "columns": ["id", "item", "conflict", "resolution", "status"],
        "min_rows": 14, "key": ["id", "item"],
    },
    # --- Pre-Game-3 data sprint (ingested from box scores / live research) ---
    "game_log_enriched.csv": {
        "columns": ["game", "date", "round", "opponent", "result", "ou_score",
                    "opp_score", "ou_by_inning", "opp_by_inning", "attendance",
                    "ou_hr", "confidence", "source"],
        "min_rows": 13, "key": ["game", "date", "opponent"],
        "confidence_col": "confidence", "source_col": "source",
        "result_col": "result", "allowed_results": {"W", "L"},
        "numeric_count": ["ou_score", "opp_score"],
    },
    "lineups_postseason.csv": {
        "columns": ["game", "date", "opponent", "b1", "b2", "b3", "b4", "b5",
                    "b6", "b7", "b8", "b9", "catcher", "dh", "notes",
                    "confidence", "source"],
        "min_rows": 6, "key": ["game", "date", "opponent"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "player_postseason_splits.csv": {
        "columns": ["player", "game", "date", "opponent", "AB", "H", "HR", "RBI",
                    "confidence", "source"],
        "min_rows": 40, "key": ["player", "game", "date"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_count": ["AB", "H", "HR", "RBI"],
    },
    "pitching_usage.csv": {
        "columns": ["game", "date", "pitcher", "role", "IP", "H", "R", "ER",
                    "BB", "K", "decision", "pitch_count", "source", "confidence"],
        "min_rows": 40, "key": ["game", "date", "pitcher"],
        "confidence_col": "confidence", "source_col": "source",
        "numeric_count": ["H", "R", "ER", "BB", "K"],
    },
    "game3_preview.csv": {
        "columns": ["factor", "detail", "confidence", "source"],
        "min_rows": 15, "key": ["factor", "detail"],
        "confidence_col": "confidence", "source_col": "source",
    },
    # --- Future-outlook module (forward-looking; heavy ESTIMATED/NOT_FOUND) ---
    "roster_future_outlook.csv": {
        "columns": ["player", "pos", "class_2026", "eligibility_remaining",
                    "role_2026", "production_2026", "draft_eligible_2026",
                    "draft_risk", "return_likelihood_2027", "development_upside",
                    "confidence", "source"],
        "min_rows": 26, "key": ["player", "pos"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "mlb_draft_risk.csv": {
        "columns": ["player", "pos", "class", "draft_ranking", "projected_round",
                    "signability_return", "replacement_difficulty", "confidence", "source"],
        "min_rows": 21, "key": ["player", "pos"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "transfer_portal_watch.csv": {
        "columns": ["direction", "cohort", "player", "pos", "from_or_to",
                    "note", "confidence", "source"],
        "min_rows": 20, "key": ["direction", "player"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "recruiting_pipeline.csv": {
        "columns": ["cohort", "player", "pos", "bats_throws", "hs_state",
                    "ranking", "draft_risk", "expected_impact", "confidence", "source"],
        "min_rows": 13, "key": ["cohort", "player"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "sec_competitive_landscape.csv": {
        "columns": ["team", "record_2026", "sec_record", "postseason_2026",
                    "coaching_2027", "tier_2027", "ou_obstacle_level",
                    "confidence", "source"],
        "min_rows": 16, "key": ["team"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "returning_production.csv": {
        "columns": ["scenario", "metric", "total_2026_documented", "returning",
                    "returning_pct", "confidence", "source"],
        "min_rows": 21, "key": ["scenario", "metric"],
        "confidence_col": "confidence", "source_col": "source",
    },
    "future_scenarios.csv": {
        "columns": ["scenario", "assumptions", "key_returners", "needed_additions",
                    "record_range_2027", "sec_finish_range", "ncaa_tourney_prob",
                    "cws_prob", "confidence", "source"],
        "min_rows": 3, "key": ["scenario"],
        "confidence_col": "confidence", "source_col": "source",
    },
}


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def err(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)
    def note(self, m): self.info.append(m)


def base_conf(v: str) -> str:
    return v.split("-", 1)[0].strip()


def validate_file(name: str, spec: dict, r: Report) -> None:
    path = DATA / name
    if not path.exists():
        r.err(f"[{name}] FILE MISSING")
        return
    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    # 1. Schema
    cols = list(df.columns)
    if cols != spec["columns"]:
        missing = [c for c in spec["columns"] if c not in cols]
        extra = [c for c in cols if c not in spec["columns"]]
        r.err(f"[{name}] SCHEMA mismatch. missing={missing} extra={extra} order_ok={cols == spec['columns']}")
    # 2. Row count
    n = len(df)
    if n < spec["min_rows"]:
        r.err(f"[{name}] ROW COUNT {n} < expected min {spec['min_rows']}")
    else:
        r.note(f"[{name}] {n} rows (>= {spec['min_rows']})")

    # 3. Missing values in key columns
    for kc in spec.get("key", []):
        if kc in df.columns:
            blanks = (df[kc].str.strip() == "").sum()
            if blanks:
                r.err(f"[{name}] {blanks} empty value(s) in key column '{kc}'")

    # 4. Confidence vocabulary
    cc = spec.get("confidence_col")
    if cc and cc in df.columns:
        bad = sorted({v for v in df[cc] if base_conf(v) not in ALLOWED_CONFIDENCE})
        if bad:
            r.err(f"[{name}] invalid confidence label(s): {bad}")
        dist = df[cc].map(base_conf).value_counts().to_dict()
        r.note(f"[{name}] confidence dist: {dist}")

    # 5. Source field present on every row
    sc = spec.get("source_col")
    if sc and sc in df.columns:
        blanks = (df[sc].str.strip() == "").sum()
        if blanks:
            r.err(f"[{name}] {blanks} row(s) with EMPTY source field")

    # 6a. Allowed results (games table)
    rc = spec.get("result_col")
    if rc and rc in df.columns:
        bad = sorted({v for v in df[rc] if v not in spec["allowed_results"]})
        if bad:
            r.err(f"[{name}] invalid result value(s): {bad}")
        pend = df[rc].isin({"PENDING", "CONDITIONAL"}).sum()
        if pend:
            r.note(f"[{name}] {pend} live-series placeholder row(s) (PENDING/CONDITIONAL) — expected mid-Finals")

    # 6b. Numeric sanity (skip explicit missing markers)
    def check_numeric(colset, lo, hi, kind):
        for col in colset:
            if col not in df.columns:
                continue
            for i, raw in enumerate(df[col]):
                v = raw.strip()
                if v in MISSING_MARKERS:
                    continue
                try:
                    x = float(v)
                except ValueError:
                    r.warn(f"[{name}] row {i+2} col '{col}': non-numeric '{v}'")
                    continue
                if not (lo <= x <= hi):
                    r.warn(f"[{name}] row {i+2} col '{col}': {kind} value {x} outside [{lo},{hi}]")

    check_numeric(spec.get("numeric_rate", []), 0.0, 2.0, "rate")
    check_numeric(spec.get("numeric_count", []), 0.0, 1000.0, "count")

    # Informational: count explicit unavailability markers
    na_cells = int((df.apply(lambda s: s.str.strip().isin({"NA", "NOT_FOUND", "NOT_AVAILABLE"}))).to_numpy().sum())
    if na_cells:
        r.note(f"[{name}] {na_cells} explicit unavailable-data marker cell(s) (documented, not errors)")


def main() -> int:
    r = Report()
    print("=" * 70)
    print("DATA VALIDATION — 2026 Oklahoma Sooners CWS research package")
    print("=" * 70)

    found = sorted(p.name for p in DATA.glob("*.csv"))
    expected = sorted(REGISTRY)
    unregistered = [f for f in found if f not in REGISTRY]
    if unregistered:
        r.warn(f"Unregistered CSV(s) present (no schema spec): {unregistered}")
    for name in expected:
        validate_file(name, REGISTRY[name], r)

    print("\n--- INFO ---")
    for m in r.info:
        print("  •", m)
    if r.warnings:
        print("\n--- WARNINGS (non-blocking) ---")
        for m in r.warnings:
            print("  ⚠", m)
    print("\n" + "=" * 70)
    if r.errors:
        print(f"RESULT: ❌ FAIL — {len(r.errors)} error(s)")
        for m in r.errors:
            print("  ✗", m)
        print("=" * 70)
        return 1
    print(f"RESULT: ✅ PASS — {len(expected)} datasets valid, "
          f"{len(r.warnings)} warning(s)")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
