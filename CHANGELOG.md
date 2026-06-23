# Changelog

All notable changes to this research package. Versions are git tags; the project
follows a research-iteration cadence (each release adds a verified analysis layer,
never a fabricated result). Format loosely follows [Keep a Changelog](https://keepachangelog.com).

## [v1.6-public-site] — 2026-06-22
- **Added `site/`** — a dependency-free static landing page that tells the whole project's
  story in <3 minutes and lets readers explore deeper. Sections: hero ("Oklahoma is not just
  a football school"), the **interactive 47-title championship wall** (sport / decade /
  NCAA-vs-selector filters, hover cards, dynasty-streak connectors, mobile-friendly), baseball
  & softball case studies, "what the project demonstrates" (for analysts), a chart gallery,
  a portfolio case-study summary, and ready-to-use launch copy (GitHub/LinkedIn/X/Reddit/email).
- `site/build_site.py` (`make site`) copies + web-optimizes a curated chart set into
  `site/assets/` (deterministic; source charts never moved). Relative paths → deploys to
  GitHub Pages as-is. Verified in-browser: no console errors, all assets 200, filters work
  (NCAA 40 / football 7 / 2020s 9), mobile layout readable. README + Makefile updated.

## [v1.4-champion] — 2026-06-22
- 🏆 **Oklahoma won the 2026 College World Series** (beat North Carolina 2–1: G1 9–3,
  G2 2–6, **G3 13–2**) — 3rd CWS title, first since 1994. Verified via ESPN's data feed
  (box 401874453, two endpoints) the moment it went final.
- **Baseball finalized:** Game 3 written to `postseason_games.csv`, `game_log_enriched.csv`,
  `pitching_usage.csv`; predictions resolved (`predictions_ledger.csv`: P1 MISS, P2 HIT,
  P5 HIT; P6 MOP = pending, **not fabricated** — award not yet officially posted). Report,
  README, and PORTFOLIO_CASE_STUDY banners updated to champion. `game_log.csv` and the
  season-rate tables intentionally stay pegged to the official cumulative through Finals G1.
- **47th national championship — cross-module cascade:** the title is also OU's 47th overall,
  so the `championships/` module (master + by-sport/decade/coaches), its validator cross-foot
  (now **47 = 40 NCAA + 7 selector**, Baseball 2→3), report/README/audit, the interactive
  `championships/viz/index.html`, and the `social/` assets (hero **47**, **79%** Olympic) were
  all updated and regenerated. `make all` green across all modules; deterministic.

## [Unreleased] — social viz module — 2026-06-22
- **Added** `social/` module: deep research (4 parallel agents) on what sports
  visualizations perform on social in 2025-26, synthesized into `SOCIAL_VIZ_PLAYBOOK.md`
  (share triggers, per-platform canvas specs, posting tactics, IP/Reddit guardrails — sourced).
- **Added** `social/scripts/make_social_assets.py` (`make social`): deterministic generator
  producing a 6-slide carousel (hero "47" → "79% Olympic" surprising stat → title wall →
  by-decade → coaches → CTA) at exact platform pixels (1080×1350 / 1080×1080) plus an
  animated cumulative-title GIF (720×720, PillowWriter, no ffmpeg). School colors + facts
  only — no team logos/photos (trademark-safe). Browser/visually QA'd.

## [Unreleased] — championships module — 2026-06-22
- **Added** self-contained `championships/` module: an all-sports accounting of every OU
  national championship — 6 datasets, 4 charts, full report, validator (with cross-foot
  checks), and `make championships`. Built from 4 parallel research agents cross-checking
  soonersports.com / NCAA.com / Wikipedia / ESPN.
- Result: **47 titles = 40 NCAA team titles + 7 football selector titles** across 7 sports
  (Men's Gym 12, Softball 8, Women's Gym 8, Football 7, Wrestling 7, Baseball 3, Men's Golf 2).
  79% are Olympic/non-revenue sports; 28 of 47 since 2000; peak decade 2010s (12).
  (Baseball reached 3 and the total reached 47 when OU won the 2026 CWS — see the v1.4 entry.)
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
