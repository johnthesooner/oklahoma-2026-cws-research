#!/usr/bin/env python3
"""
validate_football.py — schema/provenance validation for the football module's
datasets (football/data/). Self-contained; mirrors the softball/championships validators.

Checks each CSV: exact columns, min rows, non-empty key columns, recognized confidence
tag on every row (CONFIRMED/REPORTED/ESTIMATED/NOT_FOUND/NOT_AVAILABLE/CONFLICTING/
PENDING, incl. compound tags), non-empty source. Module-specific cross-foots:
  * games_football.csv W/L/PF/PA per season == seasons_football.csv
  * result == (ou_pts > opp_pts) on every game; no duplicate (season,date,opponent)
  * conference record from games' conf_game flag == seasons_football conf_W/conf_L
  * seasons 1999-2025 exactly once; no 2026 rows in games (2026 lives in the tracker)
  * derived columns recomputed: games.margin == ou_pts-opp_pts, games.one_score == |margin|<=8,
    seasons.G == W+L, seasons.win_pct == W/G, seasons.margin_pg == (PF-PA)/G
  * ratings: season unique and a subset of the seasons table, every rating/rank numeric, ranks in 1-136
  * tracker: PENDING rows carry no score; FINAL rows carry a score
  * anchors: 2000 13-0, 2024 6-7, 2025 10-3, Stoops era 190-48
Exit 0 = all valid.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
ALLOWED = {"CONFIRMED", "REPORTED", "ESTIMATED", "NOT_FOUND", "NOT_AVAILABLE", "CONFLICTING", "PENDING"}

REGISTRY = {
    "games_football.csv": {
        "columns": ["season", "date", "opponent", "opp_rank", "ou_rank", "site", "result", "ou_pts",
                    "opp_pts", "margin", "one_score", "conf_game", "game_type", "overtime", "era",
                    "conference", "confidence", "source", "note"],
        "min_rows": 356, "key": ["season", "date", "opponent", "result"]},
    "seasons_football.csv": {
        "columns": ["season", "era", "coach", "conference", "G", "W", "L", "win_pct", "conf_W", "conf_L",
                    "conf_finish", "conf_title", "PF", "PA", "margin_pg", "postseason", "ap_final",
                    "coaches_final", "confidence", "source", "note"],
        "min_rows": 27, "key": ["season", "era", "coach"]},
    "ratings_football.csv": {
        "columns": ["season", "fpi", "fpi_rank", "sos_rank", "sor_rank", "game_control_rank", "avg_wp_rank",
                    "eff_total", "eff_total_rank", "eff_off", "eff_off_rank", "eff_def", "eff_def_rank",
                    "eff_st_rank", "sp_rating", "sp_rank", "sp_off", "sp_off_rank", "sp_def", "sp_def_rank",
                    "sp_sos_rank", "confidence", "source", "note"],
        "min_rows": 21, "key": ["season"]},
    "recruiting_football.csv": {
        "columns": ["class_year", "rank_247_composite", "rank_rivals", "rank_espn", "rank_scout", "num_signees",
                    "notable_signees", "confidence", "source", "note"],
        "min_rows": 25, "key": ["class_year"]},
    "rivalry_football.csv": {
        "columns": ["season", "date", "rivalry", "opponent", "site", "result", "ou_pts", "opp_pts", "margin",
                    "ou_rank", "opp_rank", "game_type", "overtime", "confidence", "source", "note"],
        "min_rows": 52, "key": ["season", "rivalry", "result"]},
    "coaches_football.csv": {
        "columns": ["coach", "tenure_start", "tenure_end", "ou_wins", "ou_losses", "conf_titles",
                    "cfp_appearances", "bcs_or_cfp_title_games", "national_titles", "confidence", "source", "note"],
        "min_rows": 3, "key": ["coach"]},
    "season_2026_tracker.csv": {
        "columns": ["season", "date", "opponent", "site", "status", "result", "ou_pts", "opp_pts",
                    "confidence", "source", "note"],
        "min_rows": 12, "key": ["date", "opponent", "status"]},
}


def conf_ok(v: str) -> bool:
    u = str(v).upper()
    return any(tok in u for tok in ALLOWED)


def main() -> int:
    errors, info = [], []
    print("=" * 66)
    print("FOOTBALL MODULE — DATA VALIDATION")
    print("=" * 66)
    for f in sorted(p.name for p in DATA.glob("*.csv")):
        if f not in REGISTRY:
            errors.append(f"[{f}] not registered")
    frames = {}
    for name, spec in REGISTRY.items():
        p = DATA / name
        if not p.exists():
            errors.append(f"[{name}] MISSING"); continue
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        frames[name] = df
        if list(df.columns) != spec["columns"]:
            errors.append(f"[{name}] SCHEMA: missing={[c for c in spec['columns'] if c not in df.columns]} "
                          f"extra={[c for c in df.columns if c not in spec['columns']]}")
            continue
        if len(df) < spec["min_rows"]:
            errors.append(f"[{name}] ROWS {len(df)} < {spec['min_rows']}")
        for kc in spec["key"]:
            if (df[kc].str.strip() == "").sum():
                errors.append(f"[{name}] empty key cells in '{kc}'")
        bad = sorted({v for v in df["confidence"] if not conf_ok(v)})
        if bad:
            errors.append(f"[{name}] bad confidence tags: {bad}")
        dist = df["confidence"].str.upper().str.split("-").str[0].str.split("/").str[0].value_counts().to_dict()
        info.append(f"[{name}] {len(df)} rows; confidence: {dist}")
        if (df["source"].str.strip() == "").sum():
            errors.append(f"[{name}] empty source cells")

    # ---- cross-foots -------------------------------------------------------
    g, s = frames.get("games_football.csv"), frames.get("seasons_football.csv")
    if g is not None and s is not None and not errors:
        gi = g.assign(season=g.season.astype(int), ou=g.ou_pts.astype(int), op=g.opp_pts.astype(int))
        if gi.season.min() != 1999 or gi.season.max() != 2025:
            errors.append(f"[games] season span {gi.season.min()}-{gi.season.max()} != 1999-2025")
        wrong = gi[(gi.ou > gi.op) != (gi.result == "W")]
        if len(wrong):
            errors.append(f"[games] {len(wrong)} rows where result disagrees with score")
        dups = gi.duplicated(subset=["season", "date", "opponent"]).sum()
        if dups:
            errors.append(f"[games] {dups} duplicate game rows")
        si = s.assign(season=s.season.astype(int)).set_index("season")
        if sorted(si.index) != list(range(1999, 2026)):
            errors.append("[seasons] must contain 1999-2025 exactly once")
        for yr, grp in gi.groupby("season"):
            w, l = (grp.result == "W").sum(), (grp.result == "L").sum()
            pf, pa = grp.ou.sum(), grp.op.sum()
            row = si.loc[yr]
            if (w, l, pf, pa) != (int(row.W), int(row.L), int(row.PF), int(row.PA)):
                errors.append(f"[crossfoot] {yr}: games {w}-{l} {pf}/{pa} vs seasons {row.W}-{row.L} {row.PF}/{row.PA}")
            cg = grp[grp.conf_game == "Y"]
            cw, cl = (cg.result == "W").sum(), (cg.result == "L").sum()
            if (cw, cl) != (int(row.conf_W), int(row.conf_L)):
                errors.append(f"[crossfoot] {yr}: conf record from games {cw}-{cl} vs seasons {row.conf_W}-{row.conf_L}")
        # Derived game columns must agree with the scores they are derived from. Without this
        # every margin in the report could be shifted without the validator noticing.
        if not (gi.margin.astype(int) == gi.ou - gi.op).all():
            bad = gi[gi.margin.astype(int) != gi.ou - gi.op]
            errors.append(f"[games] {len(bad)} rows where margin != ou_pts - opp_pts "
                          f"(first: {bad.iloc[0].season} {bad.iloc[0].date} {bad.iloc[0].opponent})")
        one = gi.margin.astype(int).abs() <= 8
        if not (one == (gi.one_score == "Y")).all():
            bad = gi[one != (gi.one_score == "Y")]
            errors.append(f"[games] {len(bad)} rows where one_score disagrees with |margin| <= 8 "
                          f"(first: {bad.iloc[0].season} {bad.iloc[0].date} {bad.iloc[0].opponent})")
        # Derived season columns must agree with W/L/PF/PA.
        sd = si.astype({"G": int, "W": int, "L": int, "PF": int, "PA": int,
                        "win_pct": float, "margin_pg": float, "conf_W": int, "conf_L": int})
        for yr, row in sd.iterrows():
            if row.G != row.W + row.L:
                errors.append(f"[seasons] {yr}: G {row.G} != W+L {row.W + row.L}")
            if abs(row.win_pct - row.W / row.G) > 0.001:
                errors.append(f"[seasons] {yr}: win_pct {row.win_pct} != W/G {row.W / row.G:.3f}")
            if abs(row.margin_pg - (row.PF - row.PA) / row.G) > 0.01:
                errors.append(f"[seasons] {yr}: margin_pg {row.margin_pg} != (PF-PA)/G")
            if row.conf_W + row.conf_L > row.G:
                errors.append(f"[seasons] {yr}: conference games exceed total games")
        info.append("[crossfoot] derived columns (margin, one_score, G, win_pct, margin_pg) recomputed and agree")
        anchors = {2000: (13, 0), 2024: (6, 7), 2025: (10, 3), 2020: (9, 2)}
        for yr, (w, l) in anchors.items():
            if (int(si.loc[yr].W), int(si.loc[yr].L)) != (w, l):
                errors.append(f"[anchor] {yr} expected {w}-{l}")
        st = si[si.era == "Stoops"]
        if (st.W.astype(int).sum(), st.L.astype(int).sum()) != (190, 48):
            errors.append("[anchor] Stoops era seasons must sum to 190-48")
        info.append(f"[crossfoot] games↔seasons W/L/PF/PA + conference records reconcile for {len(si)} seasons")

    rt = frames.get("ratings_football.csv")
    if rt is not None and s is not None and not errors:
        rr = rt.assign(season=rt.season.astype(int))
        if not rr.season.is_unique:
            errors.append("[ratings] duplicate season rows")
        if not set(rr.season) <= set(s.season.astype(int)):
            errors.append("[ratings] contains seasons absent from the seasons table")
        rank_cols = [c for c in rr.columns if c.endswith("_rank")]
        for c in rank_cols + ["fpi", "sp_rating", "sp_off", "sp_def"]:
            vals = pd.to_numeric(rr[c], errors="coerce")
            populated = rr[c].astype(str).str.strip() != ""
            if (populated & vals.isna()).any():
                errors.append(f"[ratings] non-numeric value in '{c}'")
            if c.endswith("_rank"):
                bad = vals[(vals < 1) | (vals > 136)]
                if len(bad):
                    errors.append(f"[ratings] '{c}' has {len(bad)} rank(s) outside 1-136")
        info.append(f"[ratings] {len(rank_cols)} rank columns numeric and within 1-136; seasons unique")

    t = frames.get("season_2026_tracker.csv")
    if t is not None and not errors:
        pend = t[t.status == "PENDING"]
        if (pend.ou_pts.str.strip() != "").any() or (pend.result.str.strip() != "").any():
            errors.append("[tracker] PENDING rows must not carry a score/result")
        fin = t[t.status == "FINAL"]
        if (fin.ou_pts.str.strip() == "").any():
            errors.append("[tracker] FINAL rows must carry a score")
        info.append(f"[tracker] 2026: {len(fin)} final, {len(pend)} pending")

    c = frames.get("coaches_football.csv")
    if c is not None and s is not None and not errors:
        titles_seasons = int((s.conf_title == "Y").sum())
        titles_coaches = int(c.conf_titles.astype(int).sum())
        if titles_seasons != titles_coaches:
            errors.append(f"[crossfoot] conference titles: seasons table {titles_seasons} vs coaches table {titles_coaches}")
        else:
            info.append(f"[crossfoot] conference titles reconcile: {titles_seasons} (seasons) == {titles_coaches} (coaches)")
        stoops_w = int(c[c.coach == "Bob Stoops"].ou_wins.iloc[0]); riley_w = int(c[c.coach == "Lincoln Riley"].ou_wins.iloc[0])
        era_w = {e: int(s[s.era == e].W.astype(int).sum()) for e in ("Stoops", "Riley", "Venables")}
        # Riley-era seasons include the interim-coached 2021 Alamo Bowl win (+1)
        if era_w["Stoops"] != stoops_w or era_w["Riley"] != riley_w + 1:
            errors.append(f"[crossfoot] era wins {era_w} vs coaches Stoops {stoops_w}, Riley {riley_w}+1 interim")

    r = frames.get("rivalry_football.csv")
    if r is not None and g is not None and not errors:
        gg = g[g.opponent.isin(["Texas", "Oklahoma State"])]
        if len(gg) != len(r):
            errors.append(f"[rivalry] {len(r)} rows vs {len(gg)} Texas/Oklahoma State games in the game log")
        else:
            merged = r.merge(g[["season", "date", "opponent", "ou_pts", "opp_pts"]], on=["season", "date", "opponent"], suffixes=("", "_g"))
            if len(merged) != len(r) or (merged.ou_pts != merged.ou_pts_g).any() or (merged.opp_pts != merged.opp_pts_g).any():
                errors.append("[rivalry] scores do not match the game log")
    if r is not None and not errors:
        n = r.rivalry.value_counts().to_dict()
        if n.get("Red River", 0) != 28 or n.get("Bedlam", 0) != 25:
            errors.append(f"[rivalry] expected 28 Red River (27 + 2018 CCG) and 25 Bedlam rows, got {n}")

    print("\n--- INFO ---")
    for m in info:
        print("  •", m)
    print("\n" + "=" * 66)
    if errors:
        print(f"RESULT: ❌ FAIL — {len(errors)} error(s)")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"RESULT: ✅ PASS — {len(REGISTRY)} football datasets valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
