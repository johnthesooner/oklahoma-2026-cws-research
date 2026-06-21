# `charts/` — Visualization Suite

Ten 150-dpi PNG charts generated deterministically from `data/` by `make_charts.py`. Each PNG carries an on-image source/confidence footer. Rebuild:

```bash
python3 charts/make_charts.py      # charts only
# or
make charts
```

Builds are **reproducible** — identical inputs produce byte-identical PNGs (verified via SHA-256 in `build_manifest.json`).

| File | Chart | Key takeaway |
|---|---|---|
| `01_ranking_trajectory.png` | National ranking over the season | Fell out of the Top 25 entering the NCAAs |
| `02_postseason_scores.png` | OU vs. opponent runs, all 12 postseason games | 10–1 in the NCAA Tournament |
| `03_power_surge.png` | HR/game, regular season vs. postseason | Rate ~doubled *(ESTIMATED)* |
| `04_ou_vs_opponents.png` | Team AVG/OBP/SLG + opp AVG | Out-hit and out-pitched its schedule |
| `05_hr_leaders.png` | Individual HR leaders | Lachance (18), Brock (13) |
| `06_ops_leaders.png` | Individual OPS leaders (min 30 GP) | Six bats .880+; two over 1.000 |
| `07_pitching_staff.png` | Staff ERA vs. workload (IP) | Freshman Rager anchors a high-K staff |
| `08_cws_opponent_compare.png` | OU vs. Alabama vs. Georgia (AVG, HR) | Beat the nation's top HR team twice |
| `09_margin_of_victory.png` | Postseason wins by margin | Avg +6.4 runs over 10 wins |
| `10_stolen_bases.png` | Stolen bases by player | 132-for-156 (85%) team running game |
| `11_hr_era_timeline.png` | HR/G, OU vs. champions (by year) | Mind the bat eras (BBCOR / flat-seam) |
| `12_radar_vs_champion.png` | OU vs. typical champion (percentile radar) | Offense ≥ par; pitching below |
| `13_similarity_ranking.png` | Euclidean distance to each champion | Closest: 2022 Ole Miss |
| `14_strength_composite.png` | Champion strength-composite distribution | OU beats only ~28% of champions |
| `15_ou_zscores.png` | OU z-scores vs. modern champions | ERA/walks far below champion norm |

Charts 11–15 are produced by `scripts/championship_analysis.py` (Phase 11) from `data/champions.csv`; 01–10 by `charts/make_charts.py`. `make all` runs both.

## Charts intentionally NOT built

A **correlation heatmap** and a **radar-vs-elite-teams** chart were *not* produced: the inputs (multi-team game-level data; complete opponent rate stats) are **NOT AVAILABLE** for college baseball at the needed resolution, and building them would require fabricated values. Charts 04 and 08 are the honest, sourced substitutes.

## Style

OU crimson `#841617`, neutral gray for opponents, gold accents for highlights. All config lives at the top of `make_charts.py`.
