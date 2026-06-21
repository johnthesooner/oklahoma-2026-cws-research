#!/usr/bin/env python3
"""
gamelog_market_analysis.py — P0 audit-driven additions.

From data/game_log.csv, ratings.csv, betting.csv (+ existing team CSVs) computes:
  - Monthly W-L and run-differential splits (the May collapse -> June surge, quantified).
  - One-run, extra-inning, and blowout records (luck/variance signals).
  - Pythagorean expectation + luck delta.
  - K% / BB% and a bullpen-vs-starter ERA split (previously "NOT FOUND").
  - An opponent-adjusted "how good was OU really" read from ratings.csv (ELO/SOS).
Writes charts 16-18 and data/gamelog_market_output.md. No network; nothing fabricated.
Extra-inning flags can't be derived from final scores, so the recap-verified list is
declared explicitly and labeled [REPORTED].
"""
from __future__ import annotations
from pathlib import Path
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

MONTHS = {"02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun"}
# Extra-inning games can't be detected from final scores; recap-verified list:
EXTRA_INNINGS = {"W": ["Texas A&M 12-11 (3/15)", "Vanderbilt 13-11 (4/10)", "Georgia Tech 8-7 (6/1, 10)"],
                 "L": ["Texas 3-4 (3/27, 10)"]}


def f(v):
    return float(str(v).strip())


def main() -> int:
    out = ["# P0 Audit Additions — Game Log, Luck Tests, Ratings & Market",
           "",
           "_Computed by `scripts/gamelog_market_analysis.py`. Totals reconcile to 42-22._", ""]

    g = pd.read_csv(DATA / "game_log.csv")
    g["month"] = g["date"].str.slice(5, 7).map(MONTHS)
    g["margin"] = g["ou_runs"] - g["opp_runs"]
    W = (g.result == "W").sum(); L = (g.result == "L").sum()

    # ---- reconciliation gate ----
    rf, ra = g.ou_runs.sum(), g.opp_runs.sum()
    assert (W, L) == (42, 22), f"record mismatch {(W, L)}"
    assert (rf, ra) == (454, 342), f"runs mismatch {(rf, ra)}"
    out.append(f"**Reconciliation:** {W}-{L}, {rf} RF / {ra} RA — matches official totals. ✓\n")

    # ---- monthly splits ----
    out.append("## Monthly splits — the collapse → surge, quantified\n")
    out.append("| Month | W-L | RF | RA | Run diff | RA/G |")
    out.append("|---|---|---|---|---|---|")
    order = ["Feb", "Mar", "Apr", "May", "Jun"]
    monthly = []
    for m in order:
        sub = g[g.month == m]
        w = (sub.result == "W").sum(); l = (sub.result == "L").sum()
        mrf, mra = sub.ou_runs.sum(), sub.opp_runs.sum()
        monthly.append((m, w, l, mrf, mra, mra / len(sub)))
        out.append(f"| {m} | {w}-{l} | {mrf} | {mra} | {mrf-mra:+d} | {mra/len(sub):.1f} |")
    out.append("\n**Read:** Feb 10-1 hot start → Mar/Apr ~.500 → **May collapse (6-8, RA/G 8.4)** → "
               "**June surge (7-0, RA/G 2.9)**. The June turnaround is as much a *run-prevention* story "
               "(8.4 → 2.9 RA/G) as an offensive one — a correction to the 'offense-only transformation' framing.\n")

    # ---- one-run / extra-inning / blowout ----
    one = g[g.margin.abs() == 1]
    ow = (one.result == "W").sum(); ol = (one.result == "L").sum()
    blow = g[g.margin.abs() >= 5]
    bw = (blow.result == "W").sum(); bl = (blow.result == "L").sum()
    out.append("## Luck / variance signals\n")
    out.append(f"- **One-run games: {ow}-{ol}** (.{round(1000*ow/(ow+ol))}). A .786 one-run record IS a "
               "variance/clutch marker — one-run records are largely non-predictive in baseball. "
               "**This corrects the audit's earlier 6-4 (that was a subset).**")
    out.append(f"- **Extra-inning: {len(EXTRA_INNINGS['W'])}-{len(EXTRA_INNINGS['L'])}** [REPORTED, recap-verified]: "
               f"W {', '.join(EXTRA_INNINGS['W'])}; L {', '.join(EXTRA_INNINGS['L'])}.")
    out.append(f"- **Blowouts (margin ≥5): {bw}-{bl}.** OU was a high-variance team — many lopsided games both ways, "
               "which is why the strong one-run record coexists with only a small Pythagorean overperformance.\n")

    # ---- Pythagorean ----
    out.append("## Pythagorean expectation (luck test)\n")
    out.append("| Exponent | Pyth win% | Expected W | Actual W | Luck (W − exp) |")
    out.append("|---|---|---|---|---|")
    for exp in (2.0, 1.83):
        pw = rf**exp / (rf**exp + ra**exp)
        out.append(f"| {exp} | {pw:.3f} | {pw*64:.1f} | 42 | {42-pw*64:+.1f} |")
    out.append("\n**Read:** by total run differential OU was **essentially NOT lucky** (+1–2 wins). The variance "
               "lived in *close games* (11-3 one-run), offset by blowout losses — net Pythagorean luck is small.\n")

    # ---- K% / BB% ----
    tb = pd.read_csv(DATA / "team_batting.csv").set_index("metric")
    H = f(tb.loc["Hits", "oklahoma"]); AVG = f(tb.loc["AVG", "oklahoma"])
    BB = f(tb.loc["BB", "oklahoma"]); SO = f(tb.loc["SO", "oklahoma"]); HBP = f(tb.loc["HBP", "oklahoma"])
    AB = round(H / AVG); PA = AB + BB + HBP
    out.append("## Plate-discipline rates (were missing)\n")
    out.append(f"- Approx PA = {PA} (AB {AB} + BB {int(BB)} + HBP {int(HBP)}; SF/SH omitted). "
               f"**K% ≈ {100*SO/PA:.1f}%, BB% ≈ {100*BB/PA:.1f}%, BB/K = {BB/SO:.2f}.** [ESTIMATED]\n")

    # ---- bullpen vs starter ----
    p = pd.read_csv(DATA / "pitchers.csv")
    def ipr(v):
        w = int(f(v)); fr = round((f(v) - w) * 10); return w + fr / 3
    p["ipr"] = p["IP"].apply(ipr); p["er"] = p["ERA"].apply(f) * p["ipr"] / 9
    p["bucket"] = p["role"].apply(lambda r: "Starter" if "Starter" in r else "Reliever")
    out.append("## Bullpen vs. starter split (was 'NOT FOUND' — calculable)\n")
    out.append("| Bucket | IP | ERA | K/9 | BB/9 | n |")
    out.append("|---|---|---|---|---|---|")
    for b, sub in p.groupby("bucket"):
        ip = sub.ipr.sum(); er = sub.er.sum()
        k = sub.SO.apply(f).sum(); bb = sub.BB.apply(f).sum()
        out.append(f"| {b} | {ip:.1f} | {er*9/ip:.2f} | {k*9/ip:.1f} | {bb*9/ip:.1f} | {len(sub)} |")
    out.append("\n**Read:** the **bullpen (4.76 ERA) was slightly BETTER than the rotation (5.04)** — refutes any "
               "'shaky bullpen' assumption. (Rough role-bucketing; swing arms split by primary role.) [ESTIMATED]\n")

    # ---- opponent-adjusted read ----
    r = pd.read_csv(DATA / "ratings.csv")
    out.append("## How good was OU *really*? (opponent-adjusted)\n")
    out.append("Raw record (.656) and NCAA RPI (#24) understate OU because they don't fully reward the **#2 "
               "strength of schedule**. Opponent-adjusted systems disagree sharply with the seed:\n")
    out.append("| System | OU rank | Note |")
    out.append("|---|---|---|")
    for _, row in r.iterrows():
        out.append(f"| {row.system} | {row['rank']} | {row.note} |")
    out.append("\n**Read:** the postseason-updated, opponent-adjusted **ELO ranks OU #4 nationally** — a far cry "
               "from its #24 selection RPI — but **still behind finals opponent UNC (#2)**. So opponent adjustment "
               "*raises* OU materially, yet does NOT make it the favorite. Honest synthesis: a top-5-caliber team "
               "that the seed badly underrated, not a dominant #1.\n")

    (DATA / "gamelog_market_output.md").write_text("\n".join(out) + "\n")

    # ===== CHARTS =====
    # 16 — monthly W/L + run differential
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ms = [m[0] for m in monthly]; ws = [m[1] for m in monthly]; ls = [m[2] for m in monthly]
    rd = [m[3]-m[4] for m in monthly]
    x = range(len(ms)); wbar = 0.38
    ax1.bar([i-wbar/2 for i in x], ws, wbar, label="Wins", color=CRIMSON)
    ax1.bar([i+wbar/2 for i in x], ls, wbar, label="Losses", color=GRAY)
    ax1.set_xticks(list(x)); ax1.set_xticklabels(ms); ax1.set_ylabel("Games")
    ax2 = ax1.twinx()
    ax2.plot(list(x), rd, "-o", color=GOLD, lw=2.5, label="Run diff")
    ax2.axhline(0, color=DARK, lw=0.8); ax2.set_ylabel("Run differential")
    ax1.set_title("OU 2026 by Month: Hot Start → May Collapse → June Surge")
    ax1.legend(loc="upper left"); ax2.legend(loc="upper right")
    fig.text(0.5, -0.03, "Source: game_log.csv (reconciles 42-22). May RA/G 8.4 → June 2.9. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "16_monthly_splits.png"); plt.close(fig)

    # 17 — ratings rank comparison
    rr = r[r["rank"].apply(lambda v: str(v).strip().isdigit())].copy()
    rr["rank"] = rr["rank"].astype(int); rr = rr.sort_values("rank")
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(rr.system, rr["rank"], color=[CRIMSON if v <= 9 else GRAY for v in rr["rank"]])
    for b, v in zip(bars, rr["rank"]):
        ax.text(v+0.3, b.get_y()+b.get_height()/2, f"#{v}", va="center", fontweight="bold")
    ax.invert_yaxis(); ax.set_xlabel("OU national rank (lower = better)")
    ax.set_title("How Good Was OU? Depends on the System (#24 RPI → #4 ELO)")
    fig.text(0.5, -0.04, "Opponent-adjusted ELO (#4) vs selection-day RPI (#24). Source: ratings.csv. [CONFIRMED/REPORTED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "17_ratings_comparison.png"); plt.close(fig)

    # 18 — betting futures progression
    b = pd.read_csv(DATA / "betting.csv")
    bf = b[b.type == "futures"].copy()
    bf["implied"] = bf["implied_prob_pct"].astype(float)
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(range(len(bf)), bf["implied"], "-o", color=CRIMSON, lw=2.5, ms=8)
    for i, (_, row) in enumerate(bf.iterrows()):
        ax.annotate(f"{row.ou_odds_american}\n{row.implied:.1f}%", (i, row.implied),
                    textcoords="offset points", xytext=(0, 10), ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(range(len(bf)))
    ax.set_xticklabels([s.replace(" ", "\n") for s in bf.stage], fontsize=8)
    ax.set_ylabel("Market-implied title probability (%)")
    ax.set_title("The Market Never Believed: OU Title Odds, ~150/1 → Finals Underdog")
    ax.set_ylim(0, max(bf["implied"])*1.25)
    fig.text(0.5, -0.05, "American odds + raw implied prob (incl. bookmaker vig). Source: betting.csv. [CONFIRMED/REPORTED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "18_betting_futures.png"); plt.close(fig)

    print("\n".join(out))
    print("\nCharts 16-18 written; results -> data/gamelog_market_output.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
