# Confidence & Integrity Framework

This project's central methodological commitment: **every quantitative claim is labeled with its evidentiary status, and nothing is fabricated.** This document defines the labels and the rules.

## The four labels

| Label | Definition | Example in this project |
|---|---|---|
| **CONFIRMED** | Stated by an official/primary source, or agreed upon by ≥2 independent credible sources. | Team slash line `.292/.391/.493` (official OU PDF); final scores (ESPN box). |
| **REPORTED** | Stated by a single credible secondary source; not independently corroborated. | Opponent records; "Tockey: 6 HR in 9 games"; SOS #2 / RPI ~#9 (WarrenNolan). |
| **ESTIMATED** | Computed, derived, or inferred by the analyst. The formula or basis is always shown. | `OPS = OBP+SLG`; `K/9`, `WHIP`, run differential; the postseason HR-rate ~doubling; the 55/35/10 verdict split. |
| **NOT AVAILABLE / NOT_FOUND** | Could not be located, or **does not exist** for public college baseball. Never replaced with a guess. | wOBA, FIP, xFIP, exit velocity, defensive efficiency, starter-vs-bullpen ERA split. |

In the datasets the label lives in a `confidence` column (with optional suffixes like `CONFIRMED-score` for game rows). In the report it appears inline as `[CONFIRMED]`, `[REPORTED]`, `[ESTIMATED]`, or `NOT AVAILABLE`.

## Rules

1. **No fabrication.** If a metric is unavailable, it is listed as unavailable — never estimated into existence. The list of non-existent college-baseball metrics is maintained in `data/README.md`.
2. **Estimates are transparent.** Any `ESTIMATED` value shows its formula or basis so a reader can reproduce or challenge it.
3. **Conflicts are surfaced, not buried.** Where sources disagree, both values are shown and the conflict is flagged (see `sources/source_log.md`); it is reconciled only when there is a defensible basis (e.g., the RPI timestamp reconciliation).
4. **Primary beats secondary.** The official OU cumulative PDF supersedes aggregator sites when they disagree (e.g., HR 93 official vs. 91 lagged).
5. **Live-series honesty.** Unplayed games are marked `PENDING`/`CONDITIONAL` and never assigned a score.

## Verification pipeline

1. **Premise check** — confirm the core claim before analysis (the run actually happened).
2. **Parallel direct pulls** — independent agents gathered (a) official stat lines, (b) box scores, (c) résumé/seeding.
3. **Adversarial verification** — a multi-agent deep-research pass extracted 81 falsifiable claims and verified the top 25 under 3-vote review (need 2/3 to refute). Result: **22 confirmed, 3 refuted-and-excluded.**
4. **Cross-check** — verified claims reconciled against the direct pulls; conflicts logged.
5. **Automated validation** — `scripts/validate_data.py` enforces schema, row counts, missing-value, confidence-vocabulary, and source-presence rules on every CSV.

## How to challenge a number

Each figure is traceable: dataset cell → `source` column → `sources/source_log.md` entry → original URL. `ESTIMATED` figures additionally carry their formula. If you find a better primary source, update the cell, its `source`, and re-run `make all`.
