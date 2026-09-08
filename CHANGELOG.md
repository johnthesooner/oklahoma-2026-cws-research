# Changelog

All notable changes to this research package. Versions are git tags; the project
follows a research-iteration cadence (each release adds a verified analysis layer,
never a fabricated result). Format loosely follows [Keep a Changelog](https://keepachangelog.com).

## [v1.9-warehouse] — 2026-09-08
- **Added `transform/`, a dbt + DuckDB warehouse** over the committed CSVs: 5 staging views, 3 marts
  (`mart_era_summary`, `mart_season_performance`, `mart_unit_swap`), and **35 data tests**, building in
  ~1.5s with no server and no credentials. Wired into `make dbt` and into CI on every push.
- **Ported the Python cross-foots into dbt tests**, which is the point of the layer: the games-to-seasons
  reconciliation, the derived-column checks, the exact 14 sourced conference titles (2003 excluded), the
  bowl-versus-postseason distinction that this repo once got wrong, and a test pinning the mart to the
  figures printed in the report so neither can drift silently. Each was verified to fail on the defect it
  targets — shifting one game's `margin` by 10 while leaving the score alone fails the derived-column test.
- **`mart_unit_swap` corroborates the second headline in SQL**: SP+ and play-level EPA agree on the
  offense-led vs defense-led classification in all five overlapping seasons.
- **Added a weekly `data-freshness` workflow.** CI proved the report regenerates from the CSVs but never
  that the CSVs regenerate from their live, publicly editable upstreams. A Monday cron now runs
  `build_seasons --check`, `build_ratings --check` and the ESPN cross-check against the network, and opens
  a labelled issue on divergence.

## [v1.8-credibility-pass] — 2026-09-08
- **Retired a false `NOT_AVAILABLE`.** Play-level EPA and success rate were marked unavailable, blaming
  a missing CollegeFootballData key. They were freely available: sportsdataverse publishes ESPN-derived
  play-by-play as open Release assets needing no key. Added `ingest_pbp.py` (`make football-pbp`) and
  `football/data/epa_football.csv` for 2021-2025, raw and garbage-time-filtered by Connelly's published
  thresholds. Logged as contradictions-log **C32** rather than quietly corrected.
  EPA independently reproduces the "units swapped" finding: offense #3 → #100, defense #81 → #6.
- **Fixed three published claims that were false.** The site said every figure was cross-verified against
  two or more sources (true only for football); the README claimed CI SHA-verifies byte-identical charts
  (CI byte-diffs one file and deliberately does not pixel-diff PNGs); `data/champions.csv` still tagged
  the 2026 Oklahoma row `FINALIST` with confidence CONFIRMED eleven weeks after OU won the title. The
  last is now `CHAMPION-SUBJECT` with a validator rule that refuses the stale label.
- **Uncertainty now binds the headline.** The SEC decomposition was published as "~40% of the margin drop"
  while its own bootstrap interval ran −15.7 to +6.0. It is now stated as directional only, on every
  surface, and `methodology/confidence_framework.md` carries a rule forbidding a point estimate in a
  summary when the interval crosses zero.
- **Removed agent counts** from every document in favour of the protocol they stood for (81 claims
  extracted, 25 reviewed under a 3-vote rule, 22 confirmed and 3 refuted-and-excluded, now named).
- **Presentation:** filled the GitHub description, homepage and topics (all previously empty, which is why
  the repo surfaced in no search); removed the marketing "Launch copy" section from the public page; added
  an author byline, outbound links to the methodology, contradictions log and predictions ledger, and
  Open Graph/Twitter card metadata. Added an up-front Limitations section to the README.

## [v1.7.2-football-audited] — 2026-09-07
- **Independent adversarial audit** re-derived every headline claim from the CSVs without reading the
  generated numbers. 10 of 12 claims confirmed exactly; 2 material defects found; 44 code findings.
- **Data corrections** (none change a finding; all corrected because they are wrong): 2016 Houston
  opponent rank 14 -> **15** (five sources); 2005 Texas Tech 19 -> **21** (three sources); 2021 SP+
  defense rank 56 -> **57**; 2002 conference finish -> "T-1st South".
- **Report defects fixed**: Riley's defense range was published as "#43-#84" in five places when 2020
  was **#15**; "Postseason" silently included conference title games, printing Stoops 16-10 and Riley
  6-3 where the **bowl/CFP records are 9-9 and 2-3**; the verdict overstated Riley's luck as "about two
  wins a season" against a computed **+1.27**; Q4 claimed the unranked-opponent record "improved least
  in 2025" when it improved **most**; chart 05's title read "trail it by -3.0", a double negative.
- **Reproducibility**: added `build_seasons.py` and `build_ratings.py` (`make football-data`), which
  rebuild the two largest tables from source and refuse to write unless the infobox record, the game
  log and the conference-title count reconcile. That guard caught two bugs while being written.
- **Preserved a dead source**: footballoutsiders.com no longer resolves, so SP+ 2005-2018 is now
  committed as `sources/snapshots/sp_plus_footballoutsiders_2005_2018.csv`.
- **Validator + tests**: recompute margin/one_score/G/win_pct/margin_pg and range-check every rating
  (the audit showed all of these could previously be corrupted undetected); 25 -> 31 tests.
- **Second-source recruiting**: Rivals/Scout/ESPN ranks for 2006-2015 from the season-article recruit
  templates, used only where the snapshot post-dates signing day; independently confirms the 247 rank
  for 2014, 2015 and 2024. Contradictions log C26 resolved, C27-C31 added.

## [v1.7.1-football-hardened] — 2026-09-07
- **Second-sourced every football game** against ESPN's public schedule API
  (`football/scripts/crosscheck_espn.py`, `make football-crosscheck`): 356/356 matched, 350
  scores identical; the 6 disagreements are ESPN-side errors (five 1999 results flipped, 2001
  UNC 10-0 vs the correct 41-27) adjudicated with third sources; sites agree 100% from 2008.
- **Robustness section (Q8)**: Pythagorean-exponent and one-score-threshold sensitivity plus
  game-level bootstrap intervals. Finding: Riley +/Venables − luck is robust; the Stoops-era
  luck total is exponent-dependent, so the earlier "+1.4 wins over 27 seasons" framing was
  withdrawn from the report, README and chart 05.
- Validator now cross-foots conference titles (14) and era wins to `coaches_football.csv` and
  the rivalry table to the game log; CI runs the football analysis twice and fails on any
  byte difference; prediction ledger P7 (falsifiable 2026 call); GitHub Pages enabled.

## [v1.7-football-module] — 2026-09-07
- **Added `football/`** — a self-contained Oklahoma FOOTBALL eras module (1999–2025, 356 games):
  7 validated datasets (game log, seasons, ESPN FPI/SOS/efficiency + SP+ ratings 2005–25,
  247 recruiting 2002–26, rivalries, coaches, 2026 tracker), a reproducible Wikipedia-template
  ingest with cached raw sources, a cross-footing validator (games ↔ seasons W/L/PF/PA and
  conference records reconcile 27/27; anchors 2000 13-0, 2024 6-7, 2025 10-3, Stoops 190-48),
  an offline pytest suite, 8 charts, and `report/OKLAHOMA_FOOTBALL_ERAS_REPORT.md`.
- **Fallback-mode build** (no CollegeFootballData key): box-score drivers are `NOT_AVAILABLE`,
  not estimated. Sports-Reference/Massey/Rivals blocked; documented in `football/audit/`.
- Key results: eras 190-48 / 56-10 / 32-20; the units swapped (Riley #1 offenses over #43–84
  defenses; Venables defense #65→#4 with a #76/#51 offense); the SEC move explains **~40%** of
  the margin drop (SOS #41→#12, FPI −2.9 of −4.8) and 2025 rebounded to the Big 12 baseline;
  recruiting rank explains ~nothing inside OU's #3–19 band (R² ≤ 0.07); Riley +6.3 Pythagorean
  wins (20-7 one-score), Venables −3.0 (9-10, 0-4 postseason, 8-8 after a loss).
- Wired into `Makefile` (`make football`, `make test`, `make all`), CI, `.gitignore`,
  `requirements.txt` (pytest, Pillow), `data/contradictions_log.csv` (C22–C26), and the
  public site (football case-study section + 4 gallery charts).

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
- Built from live web research + a structured adversarial verification pass (22 confirmed,
  3 refuted-and-excluded of 25 reviewed). Nothing recalled from model memory.
