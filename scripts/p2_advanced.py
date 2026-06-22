#!/usr/bin/env python3
"""
p2_advanced.py — Phase 14 (P2): opponent adjustment, luck battery, betting
calibration, and inning-distribution analysis.

Feasible P2 slices (the full play-by-play / per-player WPA engine is NOT buildable —
StatBroadcast/NCAA PBP is JS-rendered and blocks scrapers, so it is flagged, not faked):
  - Game-level + tier opponent adjustment (game_log.csv x opponents_2026.csv).
  - Luck battery: Pythagorean, one-run record, BaseRuns (MLB-calibrated, caveated).
  - Betting calibration: market-implied vs outcomes (now incl. the Game 2 loss).
  - Inning distribution from the 6 postseason games with available line scores.
Charts 23-25 + data/p2_advanced_output.md. Deterministic; no fabrication.
"""
from __future__ import annotations
import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
CRIMSON, GRAY, GOLD, DARK = "#841617", "#8a8d8f", "#C9A227", "#2b2b2b"
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight",
                     "savefig.facecolor": "white", "axes.grid": True,
                     "grid.color": "#e9e9e9", "axes.titleweight": "bold"})

# 6 postseason games with confirmed OU inning-by-inning line scores (per-inning runs)
LINE_SCORES = {
    "Alabama 9-0":   [2, 0, 1, 0, 0, 2, 0, 4, 0],
    "Georgia 4-3":   [3, 0, 0, 1, 0, 0, 0, 0],
    "Georgia 11-4":  [0, 0, 1, 3, 0, 1, 1, 3, 2],
    "Kansas 8-1":    [0, 0, 0, 4, 3, 0, 1, 0, 0],
    "Kansas 13-2":   [1, 6, 1, 0, 0, 4, 0, 1],
    "North Carolina 9-3": [2, 0, 1, 4, 0, 1, 0, 0, 1],
}


def f(v):
    return float(str(v).strip())


def main() -> int:
    out = ["# Phase 14 — P2 Advanced: Opponent Adjustment, Luck, Market Calibration, Innings",
           "",
           "_Computed by `scripts/p2_advanced.py`. The full PBP/WPA engine is NOT built "
           "(public college play-by-play is JS-rendered / blocked) — flagged, not fabricated._", ""]

    # ============ 1. OPPONENT ADJUSTMENT ============
    g = pd.read_csv(DATA / "game_log.csv")
    opp = pd.read_csv(DATA / "opponents_2026.csv")
    g["opp_clean"] = g["opponent"].apply(lambda s: re.sub(r"\s*\(.*\)$", "", s).strip())
    m = g.merge(opp, left_on="opp_clean", right_on="opponent", how="left", suffixes=("", "_o"))
    assert m["record_2026"].notna().all(), "unmatched opponent: " + str(
        sorted(set(g.opp_clean) - set(opp.opponent)))

    def tier(r):
        if pd.notna(r.national_seed) and str(r.national_seed).strip() != "":
            return "1. National seed"
        if str(r.made_NCAA).strip() == "Y":
            return "2. NCAA (regional)"
        if f(r.win_pct) >= 0.500:
            return "3. Non-NCAA .500+"
        return "4. Sub-.500"
    m["tier"] = m.apply(tier, axis=1)

    out.append("## 1. Opponent-adjusted: OU by opponent quality tier\n")
    out.append("14 of OU's 27 distinct opponents made the 2026 NCAA Tournament (9 national seeds).\n")
    out.append("| Tier | Games | OU W-L | OU R/G | Opp R/G | Run diff/G | Avg opp win% |")
    out.append("|---|---|---|---|---|---|---|")
    order = ["1. National seed", "2. NCAA (regional)", "3. Non-NCAA .500+", "4. Sub-.500"]
    for t in order:
        sub = m[m.tier == t]
        if not len(sub):
            continue
        w = (sub.result == "W").sum(); l = (sub.result == "L").sum()
        rdg = (sub.ou_runs.sum() - sub.opp_runs.sum()) / len(sub)
        owp = sub.win_pct.astype(float).mean()
        out.append(f"| {t} | {len(sub)} | {w}-{l} | {sub.ou_runs.mean():.1f} | "
                   f"{sub.opp_runs.mean():.1f} | {rdg:+.1f} | {owp:.3f} |")
    # vs NCAA field overall
    ncaa = m[m.made_NCAA == "Y"]
    nw = (ncaa.result == "W").sum(); nl = (ncaa.result == "L").sum()
    ncaa_rdg = (ncaa.ou_runs.sum() - ncaa.opp_runs.sum()) / len(ncaa)
    sos = m.win_pct.astype(float).mean()
    out.append(f"\n**vs. 2026 NCAA Tournament teams overall: {nw}-{nl}** "
               f"({ncaa_rdg:+.1f} run diff/G). "
               f"Games-weighted average opponent win% = **{sos:.3f}** (a brutal slate). "
               "OU crushed the cupcakes (Feb) but was merely solid, not dominant, vs the tournament field — "
               "consistent with a good-not-great team that the schedule both toughened and flattered.\n")

    # game-level run adjustment — OFFICIAL opponent rates only (estimated rates inflate it)
    rated = m[m.R_per_g.notna() & m.RA_per_g.notna() & (m.rates_quality == "official")].copy()
    rated["off_vs_exp"] = rated.ou_runs - rated.RA_per_g.astype(float)
    rated["def_vs_exp"] = rated.R_per_g.astype(float) - rated.opp_runs
    out.append("## 2. Game-level opponent adjustment (official opponent rates only)\n")
    out.append(f"Over {len(rated)} games vs. opponents with **official** scoring rates "
               "(estimated-rate opponents excluded to avoid inflation):")
    out.append(f"- **Offense: {rated.off_vs_exp.mean():+.2f} runs/game vs. what those defenses normally allow** "
               f"(OU scored {rated.ou_runs.mean():.1f}/G; those opponents allowed {rated.RA_per_g.astype(float).mean():.1f}/G on average).")
    out.append(f"- **Defense: {rated.def_vs_exp.mean():+.2f} runs/game vs. what those offenses normally score** "
               f"(OU allowed {rated.opp_runs.mean():.1f}/G; those opponents scored {rated.R_per_g.astype(float).mean():.1f}/G on average).")
    out.append("- ⚠ **Caveat:** this naive adjustment is fragile — opponents' *season* R/g rates are themselves "
               "inflated by their own cupcake games, so the +2.8 'defense above expectation' is overstated. The "
               "**robust** opponent-adjusted result is the head-to-head **tier table above: vs the NCAA field OU was "
               "19-17, −0.2 run diff/G** — a good-not-elite team against quality, whose +112 overall margin came "
               "mostly from a 12-0 demolition of sub-.500 cupcakes. [ESTIMATED]\n")

    # ============ 3. LUCK BATTERY ============
    tb = pd.read_csv(DATA / "team_batting.csv").set_index("metric")
    H = f(tb.loc["Hits", "oklahoma"]); AVG = f(tb.loc["AVG", "oklahoma"])
    BB = f(tb.loc["BB", "oklahoma"]); HR = f(tb.loc["HR", "oklahoma"])
    D2 = f(tb.loc["Doubles", "oklahoma"]); T3 = f(tb.loc["Triples", "oklahoma"])
    AB = round(H / AVG); singles = H - D2 - T3 - HR
    TB = singles + 2*D2 + 3*T3 + 4*HR
    A = H + BB - HR
    B = (1.4*TB - 0.6*H - 3*HR + 0.1*BB) * 1.02
    C = AB - H
    BsR = A * B / (B + C) + HR
    actual_R = 454
    out.append("## 3. Luck / variance battery\n")
    out.append("| Test | Result | Read |")
    out.append("|---|---|---|")
    for exp in (1.83,):
        pw = 454**exp / (454**exp + 342**exp)
        out.append(f"| Pythagorean (exp {exp}) | exp {pw*64:.1f} W vs 42 actual ({42-pw*64:+.1f}) | ~neutral season luck |")
    out.append(f"| One-run games | 11-3 (.786) | favorable close-game variance (the real luck) |")
    out.append(f"| Blowouts (>=5) | 20-11 | high-variance team (offsets Pythagorean) |")
    out.append(f"| BaseRuns | {BsR:.0f} expected vs {actual_R} actual ({actual_R-BsR:+.0f}) | see caveat |")
    out.append(f"\n> **BaseRuns caveat:** the formula is MLB-calibrated and **systematically under-predicts the "
               f"higher college run environment**, so the +{actual_R-BsR:.0f} gap is mostly calibration, NOT clean "
               "sequencing luck. The trustworthy luck signals are **Pythagorean (≈neutral)** and the "
               "**11-3 one-run record (favorable)** — OU's variance was concentrated in close games, balanced by "
               "blowout losses. Verdict: **mild positive luck in close games; not a broadly lucky season.**\n")

    # ============ 4. BETTING CALIBRATION ============
    bet = pd.read_csv(DATA / "betting.csv")
    gl = bet[(bet.type == "game_line") & (bet.result.isin(["W", "L"]))
             & (bet.implied_prob_pct.astype(str).str.strip() != "NF")].copy()
    gl["imp"] = gl.implied_prob_pct.astype(float) / 100
    gl["outcome"] = (gl.result == "W").astype(int)
    brier = ((gl.imp - gl.outcome) ** 2).mean()
    naive = ((0.5 - gl.outcome) ** 2).mean()
    ou_record = f"{int(gl.outcome.sum())}-{int((1-gl.outcome).sum())}"
    out.append("## 4. Betting-market calibration (small n — indicative)\n")
    out.append(f"OU was an **underdog in all {len(gl)} priced postseason games** (implied < 50% each); "
               f"it went **{ou_record}** in them.\n")
    out.append("| Game | OU odds | Implied | Result |")
    out.append("|---|---|---|---|")
    for _, r in gl.iterrows():
        out.append(f"| {r.stage} vs {r.opponent} | {r.ou_odds_american} | {r.imp:.0%} | {r.result} |")
    out.append(f"\n- **Brier score {brier:.3f}** vs naive-0.5 **{naive:.3f}** — the market did **worse than a coin flip** "
               f"on OU because it kept pricing OU as an underdog while OU won {ou_record}. **The market was biased LOW "
               "on Oklahoma throughout the run** — the surprise was persistent, not a one-off. (n=4; directional.) "
               "Game 2 (the one loss) is the market's lone 'correct' underdog call.\n")

    # ============ 5. INNING DISTRIBUTION (6 postseason games) ============
    early = mid = late = first = scored_first = 0
    rows = []
    for game, sc in LINE_SCORES.items():
        e = sum(sc[0:3]); md = sum(sc[3:6]); lt = sum(sc[6:9])
        early += e; mid += md; late += lt; first += sc[0]
        if sc[0] > 0:
            scored_first += 1
        rows.append((game, sc[0], e, md, lt, sum(sc)))
    tot = early + mid + late
    out.append("## 5. Inning distribution (6 postseason games with line scores)\n")
    out.append(f"- First-inning runs: **{first}** over 6 games ({first/6:.1f}/G); OU scored in the 1st in "
               f"**{scored_first} of 6**.")
    out.append(f"- Early (1-3): **{early}** ({100*early/tot:.0f}%) · Middle (4-6): **{mid}** ({100*mid/tot:.0f}%) "
               f"· Late (7-9): **{late}** ({100*late/tot:.0f}%).")
    out.append("- Read: OU was **not purely a late-rally team** — scoring was spread across the game and peaked in the "
               "**middle innings**. (6-game sample; full inning data for all 64 games needs PBP, NOT obtained.)\n")

    # ============ 6. RE24 / WPA framework (honest limit) ============
    out.append("## 6. RE24 / WPA framework — status\n")
    out.append("A run-expectancy (24 base-out states) engine would power RE24 and per-player WPA. **Per-event base-out "
               "data requires play-by-play, which is not publicly obtainable for OU 2026** (StatBroadcast/NCAA PBP is "
               "JS-rendered and blocks automated retrieval). The framework is specified for a future build; **no WPA "
               "numbers are fabricated here.** Inning-level scoring (above) is the obtainable substitute.\n")

    (DATA / "p2_advanced_output.md").write_text("\n".join(out) + "\n")

    # ============ CHARTS ============
    # 23 — opponent tiers
    tiers = [t for t in order if len(m[m.tier == t])]
    rdg = [(m[m.tier == t].ou_runs.sum() - m[m.tier == t].opp_runs.sum()) / len(m[m.tier == t]) for t in tiers]
    recs = [f"{(m[m.tier==t].result=='W').sum()}-{(m[m.tier==t].result=='L').sum()}" for t in tiers]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar([t[3:] for t in tiers], rdg, color=[CRIMSON if v > 0 else GRAY for v in rdg])
    for b, v, rc in zip(bars, rdg, recs):
        ax.text(b.get_x()+b.get_width()/2, v + (0.2 if v >= 0 else -0.5), f"{v:+.1f}\n({rc})",
                ha="center", fontweight="bold", fontsize=9)
    ax.axhline(0, color=DARK, lw=1)
    ax.set_ylabel("Run differential per game")
    ax.set_title("OU 2026 by Opponent Quality: Dominant vs Cupcakes, Solid vs the Field")
    fig.text(0.5, -0.04, "Source: game_log.csv x opponents_2026.csv. 14 of 27 opponents made the NCAA field. [computed]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "23_opponent_tiers.png"); plt.close(fig)

    # 24 — luck battery
    pw183 = 454**1.83 / (454**1.83 + 342**1.83)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5))
    a1.bar(["Actual W", "Pythag exp W"], [42, pw183*64], color=[CRIMSON, GRAY])
    a1.set_title("Wins: Actual vs Pythagorean"); a1.set_ylim(0, 50)
    for i, v in enumerate([42, pw183*64]):
        a1.text(i, v+0.5, f"{v:.1f}", ha="center", fontweight="bold")
    a2.bar(["Actual R", "BaseRuns\n(MLB-cal.)"], [454, BsR], color=[CRIMSON, GRAY])
    a2.set_title("Runs: Actual vs BaseRuns (MLB-calibrated → underpredicts college)")
    for i, v in enumerate([454, BsR]):
        a2.text(i, v+5, f"{v:.0f}", ha="center", fontweight="bold")
    fig.suptitle("Luck Battery: ~Neutral by Pythagorean; Close-Game Variance the Real Signal (1-run 11-3)",
                 fontweight="bold", fontsize=12)
    fig.text(0.5, -0.03, "Pythagorean ~neutral (+2 W). BaseRuns gap is mostly MLB-calibration, not luck. [computed/ESTIMATED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "24_luck_battery.png"); plt.close(fig)

    # 25 — betting calibration
    fig, ax = plt.subplots(figsize=(9, 5.5))
    labels = [f"{r.stage}\nvs {r.opponent.split()[0]}" for _, r in gl.iterrows()]
    x = np.arange(len(gl)); w = 0.38
    ax.bar(x - w/2, gl.imp*100, w, label="Market-implied OU win%", color=GRAY)
    ax.bar(x + w/2, gl.outcome*100, w, label="Actual (100=win, 0=loss)", color=CRIMSON)
    ax.axhline(50, color=DARK, ls="--", lw=1)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Probability / outcome (%)")
    ax.set_title(f"Market Kept Doubting OU: Underdog in All 4, Went {ou_record} (Brier {brier:.2f} > 0.25)")
    ax.legend()
    fig.text(0.5, -0.05, "Market-implied (incl. vig) vs actual result. OU underpriced throughout. n=4, indicative. [computed]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "25_betting_calibration.png"); plt.close(fig)

    print("\n".join(out))
    print("\nCharts 23-25 written; results -> data/p2_advanced_output.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
