#!/usr/bin/env python3
"""
validate_championships.py — schema/provenance validation for the all-sports
championships module (championships/data/). Self-contained; mirrors the main
project's validator.

Checks each CSV: exact columns, min rows, non-empty key columns, every row has a
recognized confidence tag (CONFIRMED/REPORTED/ESTIMATED/NOT_FOUND/NOT_AVAILABLE/
CONFLICTING, including compound tags), and a non-empty source. Also runs two
cross-foot checks specific to this module: the master file's confirmed-title count
must equal 46 (39 NCAA + 7 football selector), and the by-sport / by-decade /
coaches tables must each sum to 46. Exit 0 = all valid.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
ALLOWED = {"CONFIRMED", "REPORTED", "ESTIMATED", "NOT_FOUND", "NOT_AVAILABLE", "CONFLICTING"}
TOTAL_TITLES = 46  # 39 NCAA team titles + 7 football selector titles (officially claimed)

REGISTRY = {
    "ou_all_championships.csv": {
        "columns": ["year", "sport", "head_coach", "title_basis", "opponent_or_result",
                    "ncaa_team_title", "shared_title", "confidence", "source"],
        "min_rows": 46, "key": ["year", "sport"]},
    "titles_by_sport.csv": {
        "columns": ["sport", "ncaa_team_titles", "football_selector_titles", "total_titles",
                    "first_title", "last_title", "head_coaches", "confidence", "source"],
        "min_rows": 7, "key": ["sport"]},
    "titles_by_decade.csv": {
        "columns": ["decade", "total_titles", "sports", "confidence", "source"],
        "min_rows": 9, "key": ["decade"]},
    "championship_coaches.csv": {
        "columns": ["coach", "sport", "titles", "years", "confidence", "source"],
        "min_rows": 16, "key": ["coach"]},
    "football_unclaimed_titles.csv": {
        "columns": ["year", "head_coach", "note", "confidence", "source"],
        "min_rows": 10, "key": ["year"]},
    "near_misses.csv": {
        "columns": ["year", "sport", "result", "head_coach", "note", "confidence", "source"],
        "min_rows": 6, "key": ["year", "sport"]},
}


def conf_ok(v: str) -> bool:
    u = str(v).upper()
    return any(tok in u for tok in ALLOWED)


def main() -> int:
    errors, info = [], []
    print("=" * 66)
    print("CHAMPIONSHIPS MODULE — DATA VALIDATION")
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

    # ---- cross-foot checks (this module's internal consistency) ----
    try:
        master = pd.read_csv(DATA / "ou_all_championships.csv", dtype=str, keep_default_na=False)
        n_master = len(master)
        if n_master != TOTAL_TITLES:
            errors.append(f"[cross-foot] master has {n_master} titles, expected {TOTAL_TITLES}")
        ncaa = (master["ncaa_team_title"].str.lower() == "yes").sum()
        fb = (master["ncaa_team_title"].str.lower() == "no").sum()
        info.append(f"[cross-foot] master: {ncaa} NCAA team titles + {fb} football selector = {n_master}")
        if ncaa != 39 or fb != 7:
            errors.append(f"[cross-foot] split {ncaa}+{fb} != expected 39+7")
        # uniqueness of (year, sport)
        dupes = master.duplicated(subset=["year", "sport"]).sum()
        if dupes:
            errors.append(f"[cross-foot] {dupes} duplicate (year, sport) rows in master")

        bysport = pd.read_csv(DATA / "titles_by_sport.csv", dtype=str, keep_default_na=False)
        s_total = bysport["total_titles"].astype(int).sum()
        if s_total != TOTAL_TITLES:
            errors.append(f"[cross-foot] titles_by_sport sums to {s_total}, expected {TOTAL_TITLES}")

        bydec = pd.read_csv(DATA / "titles_by_decade.csv", dtype=str, keep_default_na=False)
        d_total = bydec["total_titles"].astype(int).sum()
        if d_total != TOTAL_TITLES:
            errors.append(f"[cross-foot] titles_by_decade sums to {d_total}, expected {TOTAL_TITLES}")

        coaches = pd.read_csv(DATA / "championship_coaches.csv", dtype=str, keep_default_na=False)
        c_total = coaches["titles"].astype(int).sum()
        if c_total != TOTAL_TITLES:
            errors.append(f"[cross-foot] championship_coaches sums to {c_total}, expected {TOTAL_TITLES}")
    except Exception as e:  # noqa: BLE001
        errors.append(f"[cross-foot] check failed to run: {e}")

    print("\n--- INFO ---")
    for m in info:
        print("  •", m)
    print("\n" + "=" * 66)
    if errors:
        print(f"RESULT: ❌ FAIL — {len(errors)} error(s)")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"RESULT: ✅ PASS — {len(REGISTRY)} championships datasets valid; all cross-foot checks = {TOTAL_TITLES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
