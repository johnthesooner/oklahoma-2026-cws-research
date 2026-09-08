# `transform/` — dbt + DuckDB warehouse

A dbt project over the repository's committed CSVs. It exists for two reasons: to express the
project's integrity checks as **data tests a reviewer can read**, and to give every published figure
a queryable lineage from raw file to headline number.

**It changes no published figure.** The Python pipeline remains the source of the report and charts;
this layer reads the same CSVs and asserts the same invariants in SQL. `assert_era_summary_matches_report.sql`
pins the mart to the figures printed in the report, so if either side drifts, the build fails.

## Why DuckDB

File-backed, no server, no credentials. The whole warehouse is one artifact CI rebuilds from source
in about a second, which keeps the project's determinism guarantee intact. Nothing here needs a cloud
account to run or to review.

## Run it

```bash
pip install dbt-duckdb
cd transform
DBT_PROFILES_DIR=. dbt deps
DBT_PROFILES_DIR=. dbt build      # 5 views, 3 tables, 35 data tests
DBT_PROFILES_DIR=. dbt docs generate && DBT_PROFILES_DIR=. dbt docs serve
```

## Layout

```
transform/
├── models/staging/     stg_games, stg_seasons, stg_ratings, stg_epa, stg_recruiting
│                       typed views over the CSVs; derived flags defined once here rather
│                       than repeated across analysis scripts
├── models/marts/       mart_era_summary          the report's Q1 table, in SQL
│                       mart_season_performance   record + ratings + EPA + lagged recruiting,
│                                                 with Pythagorean expectation and luck
│                       mart_unit_swap            offense-led vs defense-led by season, judged
│                                                 independently by SP+ and by play-level EPA
└── tests/              singular tests porting the Python validators' cross-foots
```

## The tests are the point

Generic tests cover the column vocabulary — `accepted_values` on result, site, game type, era,
conference and confidence; `not_null`/`unique` on every key; `relationships` from the season mart
back to the seasons table. The singular tests carry the invariants that actually matter:

| Test | What it prevents |
|---|---|
| `assert_games_reconcile_to_seasons` | The central cross-foot: every season's record, points and conference record recomputed from the 356-game log must equal the seasons table |
| `assert_derived_game_columns` | `margin`, the one-score flag and the result must never drift from the score they derive from |
| `assert_conference_titles_are_the_sourced_fourteen` | The exact 14 sourced title seasons. 2003 must not appear — Oklahoma won the division and lost the title game 7-35 |
| `assert_bowl_record_differs_from_postseason` | The real defect this repo shipped once: "postseason" silently included conference title games, publishing Stoops at 16-10 and Riley at 6-3 when their bowl records are 9-9 and 2-3 |
| `assert_era_summary_matches_report` | The published headline figures, pinned |
| `assert_games_span_1999_to_2025` | 2026 is in progress and must stay in the tracker, never the game log |
| `assert_epa_ranks_within_field` | A rank must lie inside the field it was computed over; success rates must be rates |

Each was verified to fail on the defect it targets before being committed. Shifting one game's
`margin` by 10 while leaving the score alone fails `assert_derived_game_columns` — the exact
corruption the Python validator missed until an audit found it.
