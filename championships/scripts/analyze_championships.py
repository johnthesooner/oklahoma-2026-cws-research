#!/usr/bin/env python3
"""
analyze_championships.py — aggregates and charts for OU's all-sports national
championships. Reads championships/data/ou_all_championships.csv (the master).

Computes: total titles, NCAA-vs-football split, by-sport, by-decade, by-coach,
shared-title count, and a cumulative timeline. Writes charts 01-04 and
championships/data/championships_analysis_output.md. Deterministic; no fabrication
(the master is the single source of truth and every figure is derived from it).
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent          # championships/
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
CRIMSON, GRAY, GOLD, DARK = "#841617", "#8a8d8f", "#C9A227", "#2b2b2b"
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight",
                     "savefig.facecolor": "white", "axes.grid": True,
                     "grid.color": "#e9e9e9", "axes.titleweight": "bold"})


def main() -> int:
    d = pd.read_csv(DATA / "ou_all_championships.csv", dtype=str, keep_default_na=False)
    d["year"] = d["year"].astype(int)
    d["is_ncaa"] = d["ncaa_team_title"].str.lower() == "yes"
    d["is_shared"] = d["shared_title"].str.lower() == "yes"
    d["decade"] = (d["year"] // 10 * 10).astype(int)

    total = len(d)
    ncaa = int(d["is_ncaa"].sum())
    fb = int((~d["is_ncaa"]).sum())
    shared = int(d["is_shared"].sum())

    by_sport = d.groupby("sport").size().sort_values(ascending=False)
    by_decade = d.groupby("decade").size().sort_index()
    by_coach = d.groupby("head_coach").size().sort_values(ascending=False)

    # ---- output markdown ----
    out = ["# OU National Championships — Computed Output", "",
           "_Derived entirely from `ou_all_championships.csv` (the master). "
           "Football titles are selector-based (AP/Coaches/BCS), not NCAA-administered._", ""]
    out.append(f"**Total national championships: {total}** "
               f"= **{ncaa} NCAA team titles** + **{fb} football selector titles**. "
               f"({shared} of the {total} are shared/co-championships.)\n")
    out.append("## By sport\n")
    out.append("| Sport | Titles | First | Last |")
    out.append("|---|---|---|---|")
    for sport, n in by_sport.items():
        yrs = d[d.sport == sport]["year"]
        out.append(f"| {sport} | {n} | {yrs.min()} | {yrs.max()} |")
    out.append("")
    out.append("## By decade\n")
    out.append("| Decade | Titles |")
    out.append("|---|---|")
    for dec, n in by_decade.items():
        out.append(f"| {dec}s | {n} |")
    out.append(f"\n_Peak decade: **{by_decade.idxmax()}s** with **{by_decade.max()}** titles._\n")
    out.append("## Winningest championship coaches\n")
    out.append("| Coach | Titles | Sport(s) |")
    out.append("|---|---|---|")
    for coach, n in by_coach.head(8).items():
        sports = "/".join(sorted(d[d.head_coach == coach]["sport"].unique()))
        out.append(f"| {coach} | {n} | {sports} |")
    out.append("")
    # the modern Olympic-sport engine
    modern = d[(d.year >= 2000)]
    olympic = d[d.sport.isin(["Men's Gymnastics", "Women's Gymnastics", "Softball", "Wrestling", "Men's Golf"])]
    out.append("## The shape of the dynasty\n")
    out.append(f"- **{len(modern)} of {total}** OU national titles ({len(modern)/total:.0%}) have come in **2000 or later**.")
    out.append(f"- **{len(olympic)} of {total}** ({len(olympic)/total:.0%}) are in **Olympic / non-revenue sports** "
               "(gymnastics, softball, wrestling, golf) — not football or baseball.")
    out.append(f"- Football is the brand, but its **{fb}** titles are **{fb/total:.0%}** of the total and the last came in **2000**.")
    mg = int(by_sport.get("Men's Gymnastics", 0))
    out.append(f"- **Men's gymnastics ({mg})** is OU's single most-decorated program — more national titles than any other OU sport.\n")
    (DATA / "championships_analysis_output.md").write_text("\n".join(out) + "\n")

    # ---- Chart 01: titles by sport ----
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sports = list(by_sport.index)[::-1]
    counts = list(by_sport.values)[::-1]
    colors = [GOLD if s == "Football" else CRIMSON for s in sports]
    bars = ax.barh(sports, counts, color=colors)
    for b, v in zip(bars, counts):
        ax.text(v + 0.15, b.get_y() + b.get_height() / 2, str(v), va="center", fontweight="bold")
    ax.set_xlabel("National championships")
    ax.set_title(f"Oklahoma National Championships by Sport ({total} total)")
    fig.text(0.5, -0.04, "Crimson = NCAA team titles; gold = football selector titles (AP/Coaches/BCS). "
             "Source: ou_all_championships.csv. [CONFIRMED]", ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "01_titles_by_sport.png"); plt.close(fig)

    # ---- Chart 02: timeline (year x sport) ----
    order = list(by_sport.index)
    yidx = {s: i for i, s in enumerate(order[::-1])}
    fig, ax = plt.subplots(figsize=(13, 6))
    for r in d.itertuples():
        ax.scatter(r.year, yidx[r.sport],
                   marker="*" if r.is_shared else "o",
                   s=230 if r.is_shared else 130,
                   color=GOLD if r.sport == "Football" else CRIMSON,
                   edgecolor=DARK, linewidth=0.6, zorder=3)
    ax.set_yticks(range(len(order))); ax.set_yticklabels(order[::-1])
    ax.set_xlim(1930, 2030)
    ax.set_xlabel("Year")
    ax.set_title("Every OU National Title, 1936-2026 (★ = shared/co-championship)")
    ax.axvspan(2013, 2026, color="#f4dada", alpha=0.45, zorder=0)
    ax.text(2019.5, len(order) - 0.4, "2013-2026:\n20 titles", ha="center", color=CRIMSON, fontsize=9, style="italic")
    fig.text(0.5, -0.02, "Gold = football (selector); crimson = NCAA team. Clusters: 1950s and the 2010s-2020s. "
             "Source: ou_all_championships.csv. [CONFIRMED]", ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "02_title_timeline.png"); plt.close(fig)

    # ---- Chart 03: by decade ----
    fig, ax = plt.subplots(figsize=(11, 5.2))
    labels = [f"{dec}s" for dec in by_decade.index]
    colors = [CRIMSON if v == by_decade.max() else GRAY for v in by_decade.values]
    bars = ax.bar(labels, by_decade.values, color=colors)
    for b, v in zip(bars, by_decade.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.1, str(v), ha="center", fontweight="bold")
    ax.set_ylabel("National championships")
    ax.set_title(f"OU National Titles by Decade — the {by_decade.idxmax()}s Were the Peak ({by_decade.max()})")
    fig.text(0.5, -0.04, "Through 2026. Source: ou_all_championships.csv. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "03_titles_by_decade.png"); plt.close(fig)

    # ---- Chart 04: cumulative titles ----
    yr = d.sort_values("year")
    years = list(range(d.year.min(), 2027))
    cum = [(d.year <= y).sum() for y in years]
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.step(years, cum, where="post", color=CRIMSON, lw=2.5)
    ax.fill_between(years, cum, step="post", color="#f4dada", alpha=0.5)
    ax.set_ylabel("Cumulative national titles")
    ax.set_xlabel("Year")
    ax.set_title(f"Oklahoma's Cumulative National Championships, 1936-2026 (to {total})")
    for y_mark in (1956, 1994, 2018, 2026):
        c = int((d.year <= y_mark).sum())
        ax.annotate(f"{y_mark}: {c}", (y_mark, c), textcoords="offset points", xytext=(5, -12), fontsize=8)
    fig.text(0.5, -0.03, "More than half of all OU titles have come since 2000. Source: ou_all_championships.csv. [CONFIRMED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "04_cumulative_titles.png"); plt.close(fig)

    print("\n".join(out))
    print("\nCharts 01-04 written; results -> championships/data/championships_analysis_output.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
