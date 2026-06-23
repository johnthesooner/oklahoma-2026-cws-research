# Changelog

All notable changes to this research package. Versions are git tags; the project
follows a research-iteration cadence (each release adds a verified analysis layer,
never a fabricated result). Format loosely follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased] — v1.4 (pending Game 3 final)
- **Finalize the CWS Finals.** Game 3 (winner-take-all, June 22) result, champion/
  runner-up banners, Most Outstanding Player, resolution of the open Game-3 and
  champion entries in `data/predictions_ledger.csv`. Will tag `v1.4-champion` or
  `v1.4-runner-up`. *No result is written until the game is officially final.*

## [Unreleased] — championships module — 2026-06-22
- **Added** self-contained `championships/` module: an all-sports accounting of every OU
  national championship — 6 datasets, 4 charts, full report, validator (with cross-foot
  checks), and `make championships`. Built from 4 parallel research agents cross-checking
  soonersports.com / NCAA.com / Wikipedia / ESPN.
- Result: **46 titles = 39 NCAA team titles + 7 football selector titles** across 7 sports
  (Men's Gym 12, Softball 8, Women's Gym 8, Football 7, Wrestling 7, Baseball 2, Men's Golf 2).
  80% are Olympic/non-revenue sports; 27 of 46 since 2000; peak decade 2010s (12).
- Resolved a research conflict: OU did **not** reach the 2026 softball WCWS (lost the Norman
  Super Regional to Mississippi State 6-0), confirming the softball module.
- CI now validates the championships datasets too.

## [v1.5-softball-module] — 2026-06-22
- **Added** self-contained `softball/` module: 9 datasets, 5 charts, own report
  (`OKLAHOMA_SOFTBALL_DYNASTY_REPORT.md`), validator, and `make softball` target.
- Skeptical thesis: greatest *peak* (first-ever four-peat 2021-24, 235-15/.940/1.49 ERA)
  but not greatest *program* (UCLA leads career titles/WCWS); dynasty cracked in 2025-26.
- Corrected the "player development" premise (all 10 stars were elite recruits/transfers).

## [v1.3-data-sprint-pre-game3] — 2026-06-21
- **Added** 6 datasets (game_log_enriched, pitching_usage, player_postseason_splits,
  lineups_postseason, game3_preview, historical_cws_context); head-to-head `ratings.csv`.
- **Found/corrected**: 3 stale player names removed; postseason lineup was 100% static
  (killed the "lineup changes" narrative); OU is the Game-3 underdog (decider 4/12 historically).
- Future-outlook module (`report/OKLAHOMA_BASEBALL_FUTURE_OUTLOOK.md`) + distribution strategy.

## [v1.3-p2-advanced] — 2026-06-21
- **Added** `p2_advanced.py` (tier opponent adjustment, luck battery, betting calibration),
  `opponents_2026.csv`, living `predictions_ledger.csv` + `contradictions_log.csv` (Phase 14).
- Key result: vs the 2026 NCAA field OU was **19-17 (−0.2 run diff/G)** — good, not elite;
  the +112 overall margin was inflated by a 12-0 cupcake demolition. Full PBP/WPA flagged NOT BUILT.

## [v1.2-survivorship-model] — 2026-06-21
- **Added** `championship_model.py` (logistic / kNN / PCA / k-means / Monte Carlo) and
  `cws_field.csv` (all 40 CWS participants 2021-25 = champion vs negative class) — Phase 13.
- Key result: champions barely separate from the Omaha field (LOO AUC 0.55); OU's grounded
  entering-title-prob **~6-13%**; its power-bat/4.94-ERA cluster had **0 past champions**.

## [v1.1-opponent-adjusted] — 2026-06-21
- **Added** `gamelog_market_analysis.py`, `game_log.csv`, `ratings.csv`, `betting.csv` (Phase 12).
- **Self-corrected**: one-run record is **11-3** (not 6-4); the June turnaround was a *pitching*
  story (8.4 → 2.9 RA/G); "lineup changes" overstated; Pythagorean ≈ neutral season luck.
- Preceded by `audit/EVERYTHING_STILL_MISSING.md` (skeptical gap audit + 10/25/50h roadmap).

## [v1.0-phase11] — 2026-06-21
- **Added** `champions.csv` (21 champions 2000-2025) and `championship_analysis.py`
  (era baselines, z-scores, standardized Euclidean + regularized Mahalanobis) — Phase 11.
- Key result: OU's closest statistical twin = **2022 Ole Miss**; its 4.94 ERA would be the
  highest of any champion since 2000; only ~28% of past champions were statistically weaker.

## [v0.9-finals-g1] — 2026-06-21
- **Initial portfolio package**: main report, 28→ growing dataset suite, chart suite,
  validator, `make all` deterministic build, confidence framework, source log, case study.
- Built from live web research + a 109-agent adversarial verification pass (22 confirmed,
  3 refuted-and-excluded of 25 reviewed). Nothing recalled from model memory.
