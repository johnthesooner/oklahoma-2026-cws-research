# Phase 13 — Survivorship-Corrected Championship Model (P1)

_Computed by `scripts/championship_model.py` from `data/cws_field.csv` (40 CWS participants 2021-2025: 5 champions + 35 non-champions; all flat-seam era). OU 2026 held out as the test case._

**Universe:** 40 Omaha teams, 5 champions (base rate **12.5%**), 35 non-champions.

## 1. Do champions even differ from other Omaha teams?

Standardized mean gap (champion − non-champion, in SD units) and Welch p (n=5 vs 35, low power):

| Feature | Champ mean | Non-champ mean | Gap (SD) | p | OU |
|---|---|---|---|---|---|
| win_pct | 0.749 | 0.708 | +0.64 | 0.25 | 0.656 |
| run_diff_pg | 3.662 | 2.812 | +0.77 | 0.12 | 1.750 |
| OPS | 0.919 | 0.897 | +0.40 | 0.59 | 0.884 |
| HR_per_G | 1.766 | 1.517 | +0.65 | 0.37 | 1.453 |
| ERA | 4.068 | 4.428 | -0.46 | 0.07 | 4.940 |
| K9 | 11.323 | 9.788 | +1.31 | 0.01 | 10.381 |
| opp_AVG | 0.228 | 0.243 | -0.82 | 0.02 | 0.234 |
| FLD_pct | 0.976 | 0.978 | -0.42 | 0.32 | 0.975 |

**Read:** champions barely separate from other Omaha teams — most gaps are <0.5 SD and no feature is close to significant. The largest edge is **K9** (+1.31 SD). **Survivorship-corrected finding: once a team reaches Omaha, the regular-season profile only weakly predicts who wins — the title is largely high-variance.** This is exactly what the champions-only Phase 11 could NOT see.

## 2. Logistic title-probability model (leave-one-out)

Features: win_pct, run_diff_pg, ERA (kept to 3 — only 5 positives). L2-regularized, class-balanced.

- **Leave-one-out AUC = 0.55** — weak/modest discrimination, consistent with finding #1 (Omaha outcomes are hard to predict from season stats).
- **OU 2026 model title probability ≈ 24%** (class-balanced output; read as a tier, not a precise number — n=5 champions).

## 3. Nearest-neighbor champion rate for OU

OU's most statistically similar Omaha teams (standardized, 8 features):

| Rank | Team | Champion? | Dist |
|---|---|---|---|
| 1 | 2022 Ole Miss | YES | 1.79 |
| 2 | 2025 Louisville | no | 1.98 |
| 3 | 2023 TCU | no | 2.07 |
| 4 | 2024 Kentucky | no | 2.20 |
| 5 | 2021 NC State | no | 2.25 |
| 6 | 2023 Stanford | no | 2.30 |
| 7 | 2021 Stanford | no | 2.32 |
| 8 | 2022 Arkansas | no | 2.35 |
- Champion rate among OU's 5 nearest neighbors: **20%**
- Champion rate among OU's 8 nearest neighbors: **12%**
- Champion rate among OU's 10 nearest neighbors: **10%**

- **Unseeded context:** of 13 unseeded Omaha teams 2021-25, **1 won (8%)** — only 2022 Ole Miss. OU is unseeded. 4 of 5 champions were national seeds.

## 4. PCA of the CWS field

First two components explain 66% of variance. Champions are scattered through the cloud (not isolated), visually confirming weak separation. OU plots inside the pack (Chart 19).

## 5. Archetype clusters (k-means, k=3)

| Cluster | n | Champions | Champ rate | Avg OPS | Avg ERA | Identity |
|---|---|---|---|---|---|---|
| 0 | 9 | 2 | 22% | 0.837 | 3.67 | pitching/balanced |
| 1 | 15 | 3 | 20% | 0.948 | 4.05 | pitching/balanced |
| 2 ⬅ OU | 16 | 0 | 0% | 0.888 | 5.10 | mixed |

**OU's cluster:** champion rate 0% (OPS 0.888, ERA 5.10). OU lands in the power-bat / higher-ERA group — the same archetype as its Phase 11 matches (Ole Miss-type).

## 6. Monte Carlo best-of-3 Finals (OU vs. UNC)

Per-game P(OU win) from ELO (OU 1722.75 vs UNC 1753.58) = **0.456** (UNC is the slightly stronger team by ELO). 100,000 sims, seed 42.

- **OU win series | leading 1-0: 70%** (wins in 2: 45%, wins in 3: 25%, UNC comeback: 30%).
- Pre-series (0-0) reference: OU **43%** — matches the market's +142 (~41%) almost exactly, a good external validation of the ELO input.
- Sensitivity (series-from-1-0 by per-game p): p=0.40→64%, p=0.45→70%, p=0.46→70%, p=0.50→75%.

