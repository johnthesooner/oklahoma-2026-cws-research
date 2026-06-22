#!/usr/bin/env python3
"""
validate_softball.py — schema/provenance validation for the softball module's
datasets (softball/data/). Self-contained; mirrors the main project's validator.

Checks each CSV: exact columns, min rows, non-empty key columns, every row has a
recognized confidence tag (CONFIRMED/REPORTED/ESTIMATED/NOT_FOUND/NOT_AVAILABLE/
CONFLICTING, including compound tags), and a non-empty source. Exit 0 = all valid.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
ALLOWED = {"CONFIRMED", "REPORTED", "ESTIMATED", "NOT_FOUND", "NOT_AVAILABLE", "CONFLICTING"}

REGISTRY = {
    "ou_softball_dynasty.csv": {
        "columns": ["year", "overall", "conf_record", "conference", "final_rank",
                    "WCWS", "title", "RS", "RA", "AVG", "OBP", "SLG", "HR", "ERA",
                    "WHIP", "K", "FLD_pct", "confidence", "source", "notes"],
        "min_rows": 17, "key": ["year"]},
    "historical_dynasties.csv": {
        "columns": ["topic", "subject", "finding", "value", "confidence", "source", "note"],
        "min_rows": 30, "key": ["topic", "subject"]},
    "gasso_profile_softball.csv": {
        "columns": ["fact", "value", "confidence", "source", "note"],
        "min_rows": 25, "key": ["fact"]},
    "recruiting_pipeline_softball.csv": {
        "columns": ["class_year", "rank", "ranking_service", "notable_signees",
                    "geography", "role_in_dynasty", "confidence", "source", "note"],
        "min_rows": 10, "key": ["class_year"]},
    "portal_analysis_softball.csv": {
        "columns": ["section", "player_or_program", "direction", "pos", "from_or_to",
                    "ou_season", "detail", "confidence", "source"],
        "min_rows": 25, "key": ["section", "player_or_program"]},
    "player_development_softball.csv": {
        "columns": ["player", "position", "ou_years", "recruit_tag", "hs_ranking",
                    "freshman_production", "peak_production", "peak_year",
                    "pro_post_college", "confidence", "source", "note"],
        "min_rows": 10, "key": ["player"]},
    "sec_transition_softball.csv": {
        "columns": ["section", "subject", "season_or_metric", "value", "detail",
                    "confidence", "source", "note"],
        "min_rows": 28, "key": ["section", "subject"]},
    "future_outlook_softball.csv": {
        "columns": ["section", "item", "value", "detail", "confidence", "source", "note"],
        "min_rows": 24, "key": ["section", "item"]},
    "cross_sport_oklahoma.csv": {
        "columns": ["program", "era", "achievement", "classification",
                    "confidence", "source", "notes"],
        "min_rows": 6, "key": ["program"]},
}


def conf_ok(v: str) -> bool:
    u = str(v).upper()
    return any(tok in u for tok in ALLOWED)


def main() -> int:
    errors, info = [], []
    print("=" * 66)
    print("SOFTBALL MODULE — DATA VALIDATION")
    print("=" * 66)
    found = sorted(p.name for p in DATA.glob("*.csv"))
    for f in found:
        if f not in REGISTRY:
            errors.append(f"[{f}] not registered")
    for name, spec in REGISTRY.items():
        p = DATA / name
        if not p.exists():
            errors.append(f"[{name}] MISSING"); continue
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        if list(df.columns) != spec["columns"]:
            errors.append(f"[{name}] SCHEMA: missing={[c for c in spec['columns'] if c not in df.columns]} "
                          f"extra={[c for c in df.columns if c not in spec['columns']]}")
            continue
        if len(df) < spec["min_rows"]:
            errors.append(f"[{name}] ROWS {len(df)} < {spec['min_rows']}")
        for kc in spec["key"]:
            if (df[kc].str.strip() == "").sum():
                errors.append(f"[{name}] empty key cells in '{kc}'")
        if "confidence" in df.columns:
            bad = sorted({v for v in df["confidence"] if not conf_ok(v)})
            if bad:
                errors.append(f"[{name}] bad confidence tags: {bad}")
            dist = df["confidence"].str.upper().str.split("-").str[0].str.split("/").str[0].value_counts().to_dict()
            info.append(f"[{name}] {len(df)} rows; confidence: {dist}")
        if "source" in df.columns:
            if (df["source"].str.strip() == "").sum():
                errors.append(f"[{name}] empty source cells")
    print("\n--- INFO ---")
    for m in info:
        print("  •", m)
    print("\n" + "=" * 66)
    if errors:
        print(f"RESULT: ❌ FAIL — {len(errors)} error(s)")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"RESULT: ✅ PASS — {len(REGISTRY)} softball datasets valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
