#!/usr/bin/env python3
"""
make_social_assets.py — generate social-ready visualizations of OU's national-title
data, sized to platform specs, from championships/data/ou_all_championships.csv.

Implements the SOCIAL_VIZ_PLAYBOOK: one-number hero cards, a surprising-stat split,
the title wall, a decade chart, a coaches chart, a CTA slide (a 6-slide carousel),
plus an animated cumulative-title GIF. Exact pixels = figsize(in) x dpi (dpi=100):
  portrait 1080x1350 (4:5) · square 1080x1080 (1:1) · video-safe handled in playbook.
Deterministic, no fabrication, no team logos/photos (school colors + factual data only).
Outputs -> social/out/.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parent.parent          # social/
OUT = ROOT / "out"
MASTER = ROOT.parent / "championships" / "data" / "ou_all_championships.csv"
DPI = 100
CHAR, CREAM, MUTE = "#141414", "#f4efe3", "#9a948a"
CRIMSON, CRIMSON_BG, GOLD = "#b1232f", "#841617", "#d4a72c"
FOOTER = "Data: NCAA / Sports Reference, cross-verified (≥2 sources) · OU 2026 research project"
plt.rcParams.update({"font.family": "DejaVu Sans"})

OLYMPIC = ["Men's Gymnastics", "Women's Gymnastics", "Softball", "Wrestling", "Men's Golf"]


def load():
    d = pd.read_csv(MASTER, dtype=str, keep_default_na=False)
    d["year"] = d["year"].astype(int)
    d["is_ncaa"] = d["ncaa_team_title"].str.lower() == "yes"
    d["is_shared"] = d["shared_title"].str.lower() == "yes"
    return d


def textcanvas(w, h):
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    fig.patch.set_facecolor(CHAR)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_facecolor(CHAR)
    return fig, ax


def save(fig, name, bg=CHAR):
    fig.savefig(OUT / name, dpi=DPI, facecolor=bg)
    plt.close(fig)


def hero(name, w, h, big_fs):
    fig = plt.figure(figsize=(w, h), dpi=DPI); fig.patch.set_facecolor(CRIMSON_BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_facecolor(CRIMSON_BG)
    ax.text(0.5, 0.90, "Oklahoma Sooners", fontsize=30, color=CREAM, ha="center", va="center")
    ax.text(0.5, 0.605, "46", fontsize=big_fs, color=GOLD, ha="center", va="center", fontweight="bold")
    ax.text(0.5, 0.45, "national championships", fontsize=37, color=CREAM, ha="center", va="center", fontweight="bold")
    ax.text(0.5, 0.395, "across 7 sports · 1936–2026", fontsize=21, color="#e7c9cd", ha="center", va="center")
    ax.plot([0.26, 0.74], [0.345, 0.345], color=GOLD, lw=2.5)
    ax.text(0.5, 0.295, "39 NCAA team titles  +  7 football poll titles", fontsize=21, color=CREAM, ha="center", va="center")
    ax.text(0.5, 0.205, "80% are in Olympic sports — not football", fontsize=24, color=GOLD, ha="center", va="center", fontweight="bold")
    ax.text(0.5, 0.06, FOOTER, fontsize=13, color="#e7c9cd", ha="center", va="center")
    save(fig, name, bg=CRIMSON_BG)


def olympic_split(d):
    fig, ax = textcanvas(10.8, 13.5)
    oly = int(d["sport"].isin(OLYMPIC).sum()); rev = len(d) - oly
    ax.text(0.5, 0.90, "Where Oklahoma actually wins titles", fontsize=28, color=CREAM, ha="center", fontweight="bold")
    ax.text(0.5, 0.66, "80%", fontsize=170, color=GOLD, ha="center", va="center", fontweight="bold")
    ax.text(0.5, 0.50, "of OU's 46 national titles are in", fontsize=23, color=CREAM, ha="center")
    ax.text(0.5, 0.455, "Olympic / non-revenue sports", fontsize=27, color=GOLD, ha="center", fontweight="bold")
    x0, w = 0.12, 0.76
    share = oly / len(d)
    ax.add_patch(Rectangle((x0, 0.30), w * share, 0.055, color=CRIMSON))
    ax.add_patch(Rectangle((x0 + w * share, 0.30), w * (1 - share), 0.055, color=GOLD))
    ax.text(x0, 0.265, f"Gymnastics · softball · wrestling · golf — {oly}", fontsize=16, color=CREAM, ha="left")
    ax.text(x0 + w, 0.265, f"Football + baseball — {rev}", fontsize=16, color=MUTE, ha="right")
    ax.text(0.5, 0.14, "Football is the brand. The trophies are everywhere else.", fontsize=18, color=CREAM, ha="center")
    ax.text(0.5, 0.055, FOOTER, fontsize=13, color=MUTE, ha="center")
    save(fig, "02_olympic_split.png")


def title_wall(d):
    fig = plt.figure(figsize=(10.8, 13.5), dpi=DPI); fig.patch.set_facecolor(CHAR)
    fig.text(0.5, 0.945, "Every Oklahoma national title, 1936–2026", fontsize=25, color=CREAM, ha="center", fontweight="bold")
    fig.text(0.5, 0.915, "crimson = NCAA team title    ·    gold = football poll title", fontsize=15, color=MUTE, ha="center")
    ax = fig.add_axes([0.30, 0.085, 0.66, 0.80]); ax.set_facecolor(CHAR)
    order = list(d.groupby("sport").size().sort_values(ascending=False).index)
    yidx = {s: i for i, s in enumerate(order[::-1])}
    ax.axvspan(2013, 2026, color=CRIMSON, alpha=0.13, zorder=0)
    for _, r in d.iterrows():
        col = CRIMSON if r.is_ncaa else GOLD
        if r.is_shared:
            ax.scatter(r.year, yidx[r.sport], s=300, facecolors="none", edgecolors=GOLD, linewidths=2, zorder=2)
        ax.scatter(r.year, yidx[r.sport], s=150, color=col, edgecolors=CHAR, linewidths=1.2, zorder=3)
    ax.set_xlim(1932, 2028); ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_yticks(range(len(order))); ax.set_yticklabels(order[::-1], color=CREAM, fontsize=15)
    ax.set_xticks([1936, 1950, 1970, 1990, 2010, 2026])
    ax.tick_params(colors=MUTE, labelsize=13)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.grid(axis="x", color="#2a2a2a", lw=0.6)
    fig.text(0.5, 0.03, FOOTER, fontsize=12, color=MUTE, ha="center")
    save(fig, "03_title_wall.png")


def by_decade(d):
    fig = plt.figure(figsize=(10.8, 10.8), dpi=DPI); fig.patch.set_facecolor(CHAR)
    fig.text(0.5, 0.93, "Oklahoma titles by decade", fontsize=26, color=CREAM, ha="center", fontweight="bold")
    fig.text(0.5, 0.885, "the 2010s were the peak — 12 national titles", fontsize=16, color=GOLD, ha="center")
    ax = fig.add_axes([0.09, 0.12, 0.86, 0.71]); ax.set_facecolor(CHAR)
    decs = list(range(1930, 2030, 10))
    counts = [int(((d.year // 10 * 10) == dec).sum()) for dec in decs]
    labels = [f"{x}s" for x in decs]
    cols = [GOLD if c == max(counts) else CRIMSON for c in counts]
    bars = ax.bar(labels, counts, color=cols)
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, c + 0.2, str(c), ha="center", color=CREAM, fontsize=15, fontweight="bold")
    ax.set_ylim(0, max(counts) + 2)
    ax.tick_params(colors=MUTE, labelsize=13); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.5, 0.04, FOOTER, fontsize=12, color=MUTE, ha="center")
    save(fig, "04_by_decade.png")


def coaches():
    fig = plt.figure(figsize=(10.8, 13.5), dpi=DPI); fig.patch.set_facecolor(CHAR)
    fig.text(0.5, 0.93, "Three coaches won 25 of the 46", fontsize=27, color=CREAM, ha="center", fontweight="bold")
    fig.text(0.5, 0.895, "Oklahoma's modern dynasty is built on a few benches", fontsize=16, color=MUTE, ha="center")
    ax = fig.add_axes([0.34, 0.10, 0.60, 0.76]); ax.set_facecolor(CHAR)
    data = [("Mark Williams", 9, "men's gym"), ("K.J. Kindler", 8, "women's gym"), ("Patty Gasso", 8, "softball"),
            ("Barry Switzer", 3, "football"), ("Bud Wilkinson", 3, "football"), ("Port Robertson", 3, "wrestling")]
    names = [f"{n}\n{s}" for n, _, s in data][::-1]
    vals = [v for _, v, _ in data][::-1]
    cols = [GOLD if v >= 8 else CRIMSON for v in vals]
    bars = ax.barh(names, vals, color=cols)
    for b, v in zip(bars, vals):
        ax.text(v + 0.15, b.get_y() + b.get_height() / 2, str(v), va="center", color=CREAM, fontsize=16, fontweight="bold")
    ax.set_xlim(0, 10); ax.tick_params(colors=CREAM, labelsize=14); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.5, 0.04, FOOTER, fontsize=12, color=MUTE, ha="center")
    save(fig, "05_coaches.png")


def cta():
    fig = plt.figure(figsize=(10.8, 13.5), dpi=DPI); fig.patch.set_facecolor(CRIMSON_BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.5, 0.78, "Every title. Every coach.", fontsize=34, color=CREAM, ha="center", fontweight="bold")
    ax.text(0.5, 0.71, "The receipts.", fontsize=34, color=GOLD, ha="center", fontweight="bold")
    ax.text(0.5, 0.55, "Full dataset + an interactive", fontsize=22, color=CREAM, ha="center")
    ax.text(0.5, 0.505, "championship wall in the repo", fontsize=22, color=CREAM, ha="center")
    ax.plot([0.3, 0.7], [0.44, 0.44], color=GOLD, lw=2)
    ax.text(0.5, 0.37, "Every figure cross-verified against", fontsize=18, color="#e7c9cd", ha="center")
    ax.text(0.5, 0.335, "≥2 independent sources.", fontsize=18, color="#e7c9cd", ha="center")
    ax.text(0.5, 0.20, "Built with Python · reproducible · no logos, just data", fontsize=16, color=GOLD, ha="center")
    ax.text(0.5, 0.06, FOOTER, fontsize=13, color="#e7c9cd", ha="center")
    save(fig, "06_cta.png", bg=CRIMSON_BG)


def race_gif(d):
    years = list(range(1936, 2027))
    cum = [int((d.year <= y).sum()) for y in years]
    fig, ax = plt.subplots(figsize=(7.2, 7.2), dpi=DPI); fig.patch.set_facecolor(CHAR)

    def upd(i):
        ax.clear(); ax.set_facecolor(CHAR)
        ax.plot(years[:i + 1], cum[:i + 1], color=CRIMSON, lw=3)
        ax.fill_between(years[:i + 1], cum[:i + 1], color=CRIMSON, alpha=0.18)
        ax.scatter([years[i]], [cum[i]], color=GOLD, s=70, zorder=3)
        ax.set_xlim(1936, 2026); ax.set_ylim(0, 50)
        ax.text(0.04, 0.90, f"{years[i]}", transform=ax.transAxes, fontsize=44, color=CREAM, fontweight="bold")
        noun = "title" if cum[i] == 1 else "titles"
        ax.text(0.04, 0.80, f"{cum[i]} national {noun}", transform=ax.transAxes, fontsize=20, color=GOLD)
        ax.tick_params(colors=MUTE, labelsize=12); ax.set_yticks([0, 10, 20, 30, 40])
        ax.set_xticks([1936, 1960, 1980, 2000, 2026])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.grid(color="#2a2a2a", lw=0.5)
        ax.set_title("Oklahoma's national titles add up", color=CREAM, fontsize=18, fontweight="bold")

    frames = list(range(len(years))) + [len(years) - 1] * 14
    ani = FuncAnimation(fig, upd, frames=frames, interval=80)
    try:
        ani.save(OUT / "title_race.gif", writer=PillowWriter(fps=12), dpi=DPI)
        plt.close(fig)
        return True
    except Exception as e:  # noqa: BLE001
        plt.close(fig)
        print(f"  [skip] title_race.gif NOT built (Pillow writer unavailable): {e}")
        return False


def main():
    OUT.mkdir(exist_ok=True)
    d = load()
    assert len(d) == 46, f"expected 46 titles, got {len(d)}"
    hero("01_hero_46.png", 10.8, 13.5, 215)
    hero("01b_hero_46_square.png", 10.8, 10.8, 200)
    olympic_split(d)
    title_wall(d)
    by_decade(d)
    coaches()
    cta()
    gif = race_gif(d)
    pngs = sorted(p.name for p in OUT.glob("*.png"))
    print("Social assets written to social/out/:")
    for p in pngs:
        print("  •", p)
    print("  •", "title_race.gif" if gif else "(gif skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
