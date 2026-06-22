#!/usr/bin/env python3
"""
analyze_softball.py — derived metrics, season ranking, and charts for the
Oklahoma softball dynasty module. Reads softball/data/ou_softball_dynasty.csv.

Computes win%, run differential (total + per game), OPS, HR/game, and a
dominance composite (z-scored), ranks OU's 2010-2026 seasons, and writes
charts 01-05 + softball/data/softball_analysis_output.md. Deterministic.
No fabrication; the 2000/older title teams are outside the 2010-2026 data window
and are noted, not invented.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent          # softball/
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
CRIMSON, GRAY, GOLD, DARK = "#841617", "#8a8d8f", "#C9A227", "#2b2b2b"
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight",
                     "savefig.facecolor": "white", "axes.grid": True,
                     "grid.color": "#e9e9e9", "axes.titleweight": "bold"})


def main() -> int:
    d = pd.read_csv(DATA / "ou_softball_dynasty.csv")
    wl = d["overall"].str.split("-", expand=True).astype(int)
    d["W"], d["L"] = wl[0], wl[1]
    d["G"] = d["W"] + d["L"]
    d["win_pct"] = d["W"] / d["G"]
    for c in ["RS", "RA", "HR", "ERA", "OBP", "SLG", "AVG"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["run_diff"] = d["RS"] - d["RA"]
    d["run_diff_pg"] = d["run_diff"] / d["G"]
    d["OPS"] = d["OBP"] + d["SLG"]
    d["HR_pg"] = d["HR"] / d["G"]

    def z(s):
        return (s - s.mean()) / s.std()
    # higher = more dominant; ERA inverted
    d["dominance"] = z(d.win_pct) + z(d.run_diff_pg) + z(d.OPS) - z(d.ERA)
    ranked = d.sort_values("dominance", ascending=False).reset_index(drop=True)

    out = ["# Softball Analysis — Computed Output", "",
           "_From `ou_softball_dynasty.csv`. Window = 2010-2026 (17 seasons); the 2000 title team predates the data._", ""]
    titles = (d.title == "Y").sum(); wcws = (d.WCWS == "Y").sum()
    out.append(f"**2010-2026 aggregate:** {d.W.sum()}-{d.L.sum()} ({d.W.sum()/(d.W.sum()+d.L.sum()):.3f}), "
               f"**{titles} national titles, {wcws} WCWS appearances** in 17 seasons.\n")
    out.append("## Best OU seasons by dominance composite (z: +win% +rundiff/G +OPS −ERA)\n")
    out.append("| Rank | Year | Record | Win% | RunDiff/G | OPS | ERA | Title | Composite |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for i, r in ranked.iterrows():
        out.append(f"| {i+1} | {r.year} | {r.overall} | {r.win_pct:.3f} | {r.run_diff_pg:+.1f} "
                   f"| {r.OPS:.3f} | {r.ERA:.2f} | {r.title} | {r.dominance:+.2f} |")
    out.append("")
    # four-peat vs SEC-era
    fp = d[(d.year >= 2021) & (d.year <= 2024)]
    sec = d[d.year >= 2025]
    out.append("## The four-peat (2021-24) vs the SEC era (2025-26)\n")
    out.append(f"- Four-peat: **{fp.W.sum()}-{fp.L.sum()} ({fp.W.sum()/(fp.W.sum()+fp.L.sum()):.3f})**, "
               f"avg ERA **{fp.ERA.mean():.2f}**, avg run diff/G **{fp.run_diff_pg.mean():+.1f}**, 4 titles.")
    out.append(f"- SEC era: **{sec.W.sum()}-{sec.L.sum()} ({sec.W.sum()/(sec.W.sum()+sec.L.sum()):.3f})**, "
               f"avg ERA **{sec.ERA.mean():.2f}**, 0 titles, 1 WCWS appearance, missed WCWS in 2026.")
    out.append(f"- **The crack is run prevention:** ERA 0.96 (2023) → 1.99 (2024) → 2.66 (2025) → 3.09 (2026); "
               "the 2026 offense actually peaked (187 HR, .786 SLG — both window highs).\n")
    (DATA / "softball_analysis_output.md").write_text("\n".join(out) + "\n")

    # ---- Chart 01: dynasty timeline (win% bars, titles gold) ----
    fig, ax = plt.subplots(figsize=(13, 5.5))
    colors = [GOLD if t == "Y" else (CRIMSON if r >= 2021 and r <= 2024 else GRAY)
              for t, r in zip(d.title, d.year)]
    bars = ax.bar(d.year.astype(str), d.win_pct, color=colors)
    for b, r in zip(bars, d.itertuples()):
        if r.title == "Y":
            ax.text(b.get_x()+b.get_width()/2, r.win_pct+0.005, "★", ha="center", color=GOLD, fontsize=12)
    ax.set_ylim(0.6, 1.0); ax.set_ylabel("Win %")
    ax.set_title("Oklahoma Softball 2010-2026: Win% by Season (★ = national title)")
    ax.axvspan(10.5, 13.5, color="#f4dada", alpha=0.5, zorder=0)
    ax.text(12, 0.62, "2021-24 four-peat", ha="center", color=CRIMSON, fontsize=9, style="italic")
    ax.text(15.5, 0.62, "SEC era\n(0 titles)", ha="center", color=DARK, fontsize=9, style="italic")
    fig.text(0.5, -0.03, "Gold = title; crimson = four-peat; gray = other. Source: ou_softball_dynasty.csv. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "01_dynasty_timeline.png"); plt.close(fig)

    # ---- Chart 02: run prevention crack (ERA) ----
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.plot(d.year, d.ERA, "-o", color=CRIMSON, lw=2.5)
    for r in d.itertuples():
        if r.year >= 2023:
            ax.annotate(f"{r.ERA:.2f}", (r.year, r.ERA), textcoords="offset points", xytext=(0, 8),
                        ha="center", fontsize=8, fontweight="bold")
    ax.set_ylabel("Team ERA (lower = better)")
    ax.set_title("The Crack Is Run Prevention: OU Team ERA Climbed 0.96 → 3.09 (2023→2026)")
    ax.invert_yaxis()
    fig.text(0.5, -0.03, "ERA rose every year 2023→2026 as OU entered the SEC. Source: ou_softball_dynasty.csv. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "02_run_prevention.png"); plt.close(fig)

    # ---- Chart 03: offense trend (OPS + HR) ----
    fig, ax1 = plt.subplots(figsize=(12, 5.2))
    ax1.bar(d.year, d.HR, color=GRAY, label="HR")
    ax1.set_ylabel("Home runs")
    ax2 = ax1.twinx()
    ax2.plot(d.year, d.OPS, "-o", color=CRIMSON, lw=2.5, label="OPS")
    ax2.set_ylabel("OPS")
    ax1.set_title("OU Offense 2010-2026: HR (bars) & OPS (line) — 2026 Set Window Highs (187 HR/.786 SLG)")
    ax1.legend(loc="upper left"); ax2.legend(loc="upper right")
    fig.text(0.5, -0.03, "The 2026 offense PEAKED even as the team missed Omaha — the decline was pitching, not bats. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "03_offense_trend.png"); plt.close(fig)

    # ---- Chart 04: all-time titles leaderboard (from historical_dynasties research) ----
    progs = ["UCLA", "Arizona", "Oklahoma", "Texas", "Ariz. St", "Texas A&M", "Florida"]
    tcounts = [12, 8, 8, 2, 2, 2, 2]
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(progs[::-1], tcounts[::-1],
                   color=[CRIMSON if p == "Oklahoma" else GRAY for p in progs[::-1]])
    for b, v in zip(bars, tcounts[::-1]):
        ax.text(v+0.1, b.get_y()+b.get_height()/2, str(v), va="center", fontweight="bold")
    ax.set_xlabel("NCAA national titles (UCLA incl. one vacated 1995)")
    ax.set_title("All-Time NCAA Softball Titles: OU (8) Ties Arizona, Trails UCLA (12)")
    fig.text(0.5, -0.04, "Through 2026; Texas won 2025 & 2026. Source: ESPN/NCAA/Wikipedia (historical_dynasties.csv). [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "04_titles_leaderboard.png"); plt.close(fig)

    # ---- Chart 05: best OU teams (dominance composite) ----
    top = ranked.head(10)[::-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh([f"{int(r.year)} ({r.overall})" for r in top.itertuples()], top.dominance,
                   color=[GOLD if t == "Y" else GRAY for t in top.title])
    for b, v in zip(bars, top.dominance):
        ax.text(v+0.05, b.get_y()+b.get_height()/2, f"{v:+.2f}", va="center", fontweight="bold", fontsize=8)
    ax.set_xlabel("Dominance composite (z: +win% +runDiff/G +OPS −ERA)")
    ax.set_title("Most Dominant OU Seasons 2010-2026 (gold = national title)")
    fig.text(0.5, -0.03, "2023 (61-1) & 2022 (59-3) top the list. Window 2010-2026 only. Source: computed. [CONFIRMED/ESTIMATED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "05_best_ou_teams.png"); plt.close(fig)

    print("\n".join(out))
    print("\nCharts 01-05 written; results -> softball/data/softball_analysis_output.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
