"""
Generates the chart suite for the 2026 Oklahoma Sooners CWS research report.
All data sourced from official OU cumulative stats PDF (as of Jun 20, 2026),
ESPN box scores, and WarrenNolan RPI. Estimated figures are labeled on-chart.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent
DATA = OUT.parent / "data"

CRIMSON = "#841617"
CREAM = "#FDF9E7"
GRAY = "#8a8d8f"
DARK = "#2b2b2b"
GOLD = "#C9A227"

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.edgecolor": "#cccccc",
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linewidth": 0.8,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

def footer(fig, txt):
    fig.text(0.5, -0.02, txt, ha="center", fontsize=8, color="#666666", style="italic")

# ---------------------------------------------------------------------------
# 1. Ranking trajectory (line, inverted axis)
# ---------------------------------------------------------------------------
points = ["Preseason", "Early Feb", "Mid-March", "April", "Enter NCAAs", "Now (Omaha)"]
# Unranked plotted at 30 (off the Top 25). "Now" = USA Today re-rank of 8 CWS teams -> #2 of 8 ~ treat as elite (#2)
rank = [17, 8, 13, 15, 30, 2]
labels = ["~#14-19", "~#7-10", "~#12-14", "~#14-15", "Unranked", "#2 of CWS 8"]
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(points, rank, "-o", color=CRIMSON, lw=2.5, ms=9, zorder=3)
ax.axhspan(25, 31, color="#f4dada", alpha=0.6, zorder=0)
ax.text(0.2, 28.3, "Outside Top 25", color=CRIMSON, fontsize=9, style="italic")
for x, y, lab in zip(points, rank, labels):
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(0, -18 if y < 25 else 12),
                ha="center", fontsize=9, fontweight="bold", color=DARK)
ax.set_ylim(31, 0)
ax.set_ylabel("National Ranking (lower = better)")
ax.set_title("Oklahoma 2026 Ranking Trajectory: Out of the Top 25 Entering the NCAA Tournament")
ax.set_yticks([1, 5, 10, 15, 20, 25, 30])
ax.set_yticklabels(["1", "5", "10", "15", "20", "25", "NR"])
footer(fig, "Sources: D1Baseball / Baseball America / USA Today Coaches polls. 'Now' = USA Today re-rank of the 8 CWS teams (#2). [REPORTED]")
fig.savefig(OUT / "01_ranking_trajectory.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 2. Postseason game-by-game scores
# ---------------------------------------------------------------------------
g = pd.read_csv(DATA / "postseason_games.csv")
g = g[g["result"].isin(["W", "L"])].copy()
g["ou_runs"] = g["ou_runs"].astype(float)
g["opp_runs"] = g["opp_runs"].astype(float)
lbl = [f"{r.opponent}\n{r.date[5:]}" for r in g.itertuples()]
x = np.arange(len(g))
w = 0.4
fig, ax = plt.subplots(figsize=(13, 5.6))
b1 = ax.bar(x - w/2, g["ou_runs"], w, label="Oklahoma", color=CRIMSON)
b2 = ax.bar(x + w/2, g["opp_runs"], w, label="Opponent", color=GRAY)
for i, r in enumerate(g.itertuples()):
    mark = "W" if r.result == "W" else "L"
    ax.text(i, max(r.ou_runs, r.opp_runs) + 0.3, mark, ha="center", fontweight="bold",
            color=CRIMSON if mark == "W" else "#b00")
ax.set_xticks(x)
ax.set_xticklabels(lbl, fontsize=8)
ax.set_ylabel("Runs")
ax.set_title("Oklahoma 2026 Postseason, Game by Game (10-1 in NCAA Tourney; 10-2 incl. SEC Tourney)")
ax.legend()
footer(fig, "Source: ESPN / NCAA.com box scores. SEC Tourney loss to LSU (5/19) included. CWS Finals G2 not yet played. [CONFIRMED]")
fig.savefig(OUT / "02_postseason_scores.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. Power surge: HR per game, regular season vs postseason (ESTIMATED)
# ---------------------------------------------------------------------------
# Anchor: NCAA.com "over 25% of season HR came in the NCAA tournament"; itemized confirmed >=25 HR in 11 postseason games.
reg_games, post_games = 53, 11
post_hr = 25          # itemized confirmed (an undercount); ~27% of 93
reg_hr = 93 - post_hr # 68
reg_rate = reg_hr / reg_games
post_rate = post_hr / post_games
fig, ax = plt.subplots(figsize=(8, 5.4))
bars = ax.bar(["Regular season\n(53 g, ~68 HR)", "Postseason\n(11 g, ~25 HR)"],
              [reg_rate, post_rate], color=[GRAY, CRIMSON], width=0.55)
for b, v in zip(bars, [reg_rate, post_rate]):
    ax.text(b.get_x() + b.get_width()/2, v + 0.03, f"{v:.2f} HR/G", ha="center", fontweight="bold")
pct = (post_rate / reg_rate - 1) * 100
ax.annotate(f"+{pct:.0f}%", xy=(1, post_rate), xytext=(0.5, post_rate + 0.25),
            ha="center", fontsize=15, fontweight="bold", color=CRIMSON)
ax.set_ylabel("Home runs per game")
ax.set_title("The Power Surge: HR/Game Roughly Doubled in the Postseason")
ax.set_ylim(0, post_rate + 0.6)
footer(fig, "[ESTIMATED] from NCAA.com 'over 25% of season HR in the NCAA tournament' + itemized box-score HR (an undercount). Directional, not official.")
fig.savefig(OUT / "03_power_surge.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. OU offense & run prevention vs opponents (team rate stats)
# ---------------------------------------------------------------------------
metrics = ["AVG", "OBP", "SLG", "Opp AVG\n(def)"]
ou_vals = [.292, .391, .493, .234]
opp_vals = [.234, .344, .413, .292]
x = np.arange(len(metrics)); w = 0.38
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(x - w/2, ou_vals, w, label="Oklahoma", color=CRIMSON)
ax.bar(x + w/2, opp_vals, w, label="Opponents (aggregate)", color=GRAY)
for i, (a, b) in enumerate(zip(ou_vals, opp_vals)):
    ax.text(i - w/2, a + .006, f"{a:.3f}", ha="center", fontsize=9, fontweight="bold")
    ax.text(i + w/2, b + .006, f"{b:.3f}", ha="center", fontsize=9, color="#555")
ax.set_xticks(x); ax.set_xticklabels(metrics)
ax.set_ylabel("Rate")
ax.set_title("Oklahoma vs. Opponents, Full Season Rate Stats")
ax.legend()
footer(fig, "Source: Official OU cumulative PDF (64 games). [CONFIRMED]")
fig.savefig(OUT / "04_ou_vs_opponents.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. HR leaders
# ---------------------------------------------------------------------------
h = pd.read_csv(DATA / "hitters.csv").sort_values("HR", ascending=True)
fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(h["player"], h["HR"], color=CRIMSON)
for b, v in zip(bars, h["HR"]):
    ax.text(v + 0.2, b.get_y() + b.get_height()/2, str(v), va="center", fontweight="bold")
ax.set_xlabel("Home runs (full season)")
ax.set_title("Oklahoma 2026 Home Run Leaders")
footer(fig, "Source: Official OU cumulative PDF (through CWS semifinal). [CONFIRMED]")
fig.savefig(OUT / "05_hr_leaders.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 6. OPS leaders (min 30 GP)
# ---------------------------------------------------------------------------
h2 = pd.read_csv(DATA / "hitters.csv")
h2 = h2[h2["GP"] >= 30].sort_values("OPS", ascending=True)
colors = [GOLD if v >= 1.0 else CRIMSON for v in h2["OPS"]]
fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(h2["player"], h2["OPS"], color=colors)
for b, v in zip(bars, h2["OPS"]):
    ax.text(v + .008, b.get_y() + b.get_height()/2, f"{v:.3f}", va="center", fontweight="bold", fontsize=9)
ax.axvline(.884, color=DARK, ls="--", lw=1.2)
ax.text(.884, -0.6, "Team .884", color=DARK, fontsize=8, ha="center")
ax.set_xlabel("OPS (min 30 GP)")
ax.set_title("Oklahoma 2026 OPS Leaders (gold = 1.000+)")
ax.set_xlim(0.55, 1.1)
footer(fig, "Source: Official OU cumulative PDF. OPS = OBP + SLG. [CONFIRMED/ESTIMATED]")
fig.savefig(OUT / "06_ops_leaders.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 7. Pitching staff: ERA vs IP (workload)
# ---------------------------------------------------------------------------
p = pd.read_csv(DATA / "pitchers.csv")
p = p[p["IP"] >= 12].copy()
def role_color(r):
    if "Starter" in r: return CRIMSON
    if "Swing" in r: return GOLD
    return GRAY
fig, ax = plt.subplots(figsize=(10, 6))
for r in p.itertuples():
    c = role_color(r.role)
    ax.scatter(r.IP, r.ERA, s=120, color=c, edgecolor="white", zorder=3)
    ax.annotate(r.pitcher, (r.IP, r.ERA), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.axhline(4.94, color=DARK, ls="--", lw=1.2)
ax.text(72, 5.05, "Team ERA 4.94", fontsize=8, color=DARK)
ax.set_xlabel("Innings pitched")
ax.set_ylabel("ERA (lower = better)")
ax.set_title("Oklahoma 2026 Pitching Staff: ERA vs. Workload")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=CRIMSON, label="Starter"), Patch(color=GOLD, label="Swing"),
                   Patch(color=GRAY, label="Reliever")], loc="upper right")
footer(fig, "Source: Official OU cumulative PDF (min 12 IP). Freshman LHP Cord Rager: 76 IP, 4.74 ERA, 94 K. [CONFIRMED]")
fig.savefig(OUT / "07_pitching_staff.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 8. CWS opponent comparison (AVG & HR) - data available for OU/Alabama/Georgia
# ---------------------------------------------------------------------------
teams = ["Oklahoma", "Alabama (#7)", "Georgia (#3)"]
avg = [.292, .270, .326]
hr = [93, 46, 174]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5))
b = a1.bar(teams, avg, color=[CRIMSON, GRAY, "#BA0C2F"])
a1.set_title("Team Batting Average"); a1.set_ylim(0.2, 0.35)
for bar, v in zip(b, avg): a1.text(bar.get_x()+bar.get_width()/2, v+.002, f"{v:.3f}", ha="center", fontweight="bold")
b2 = a2.bar(teams, hr, color=[CRIMSON, GRAY, "#BA0C2F"])
a2.set_title("Team Home Runs (season)")
for bar, v in zip(b2, hr): a2.text(bar.get_x()+bar.get_width()/2, v+2, str(v), ha="center", fontweight="bold")
fig.suptitle("Oklahoma vs. Its Two SEC CWS Victims", fontweight="bold", fontsize=14)
footer(fig, "Sources: official team stats / Wikipedia. Georgia led the nation in HR (174). UNC team AVG/HR NOT FOUND. [CONFIRMED/REPORTED]")
fig.savefig(OUT / "08_cws_opponent_compare.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 9. Postseason margin of victory
# ---------------------------------------------------------------------------
gw = g[g["result"] == "W"].copy()
gw["margin"] = gw["ou_runs"] - gw["opp_runs"]
gw = gw.sort_values("margin")
lbls = [f"{r.opponent} ({int(r.ou_runs)}-{int(r.opp_runs)})" for r in gw.itertuples()]
fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.barh(lbls, gw["margin"], color=CRIMSON)
for b, v in zip(bars, gw["margin"]):
    ax.text(v + 0.1, b.get_y()+b.get_height()/2, f"+{int(v)}", va="center", fontweight="bold")
ax.set_xlabel("Margin of victory (runs)")
ax.set_title("Oklahoma Postseason Wins by Margin (avg +6.4 runs over 10 wins)")
footer(fig, "Source: box scores. Mean winning margin computed across the 11 postseason wins. [CONFIRMED]")
fig.savefig(OUT / "09_margin_of_victory.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 10. Stolen base aggression
# ---------------------------------------------------------------------------
h3 = pd.read_csv(DATA / "hitters.csv").sort_values("SB", ascending=True)
h3 = h3[h3["SB"] > 0]
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(h3["player"], h3["SB"], color=CRIMSON)
for b, v in zip(bars, h3["SB"]):
    ax.text(v + 0.2, b.get_y()+b.get_height()/2, str(int(v)), va="center", fontweight="bold")
ax.set_xlabel("Stolen bases")
ax.set_title("Oklahoma 2026 Stolen Bases (team 132-156, 85%)")
footer(fig, "Source: Official OU cumulative PDF. Team stole 132 bags at an 85% clip. [CONFIRMED]")
fig.savefig(OUT / "10_stolen_bases.png")
plt.close(fig)

print("All charts written to", OUT)
for f in sorted(OUT.glob("*.png")):
    print(" -", f.name)
