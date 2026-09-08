# `report/` — Full Research Report

**`OKLAHOMA_2026_CWS_RESEARCH_REPORT.md`** is the report that answers the question (~2,500 words; the full ~19k-word working analysis moved to `APPENDIX_FULL_ANALYSIS.md`, 8 parts, 14 research phases). It is the narrative companion to the `data/` and `charts/` assets.

## Structure

| Part | Contents |
|---|---|
| **I** | Executive Summary — one-paragraph answer, headline findings, top-line numbers |
| **II** | Full Research Report — Phases 1–14 (raw data, transformation, player dossiers, strength of competition, advanced stats, power surge, pitching, coaching, visuals, ranked Top 10, **historical championship comparison**, **survivorship-corrected modeling**, **opponent adjustment / luck / market**) |
| **III** | **CWS Finals Dossier (live tracker)** — Game 1 & 2 recaps, Game 3 placeholder, MVP candidates, what changed |
| **IV** | Statistical Appendix — full data tables (mirrors `data/`) |
| **V** | The Final Answer — one paragraph / one page / full |
| **VI** | **The Definitive Verdict** — sustainable strength vs. hot streak vs. matchups (~55/35/10, analyst-estimated) |
| **VII** | Predictive Conclusions — Finals read, 2027 outlook, falsifiable predictions |
| **VIII** | Methodology, Sources & Limitations |

## How to read it

- Every figure is tagged **[CONFIRMED] / [REPORTED] / [ESTIMATED] / NOT AVAILABLE**.
- Charts referenced inline live in `../charts/`; raw tables in `../data/`.
- **Live-series note:** Finals **tied 1–1** (OU won G1 9–3; UNC won G2 6–2). **Game 3 (June 22, 7 PM ET) is the winner-take-all decider — not yet played.** Season-rate datasets are pegged to the official cumulative through Finals Game 1 (42-22); the Finals dossier/model track the series live.

## To finalize v1.4 (the moment Game 3 is final)

One pass, ~15 minutes:
1. Get the Game 3 box score (champion + score + line + stars + Most Outstanding Player).
2. `data/postseason_games.csv` row 14 → fill the result (W/L, runs); `data/predictions_ledger.csv` → resolve **P1** (Game 3) and **P6** (MOP), and resolve **P2** (champion-or-finalist).
3. Report **Part III** → write the Game 3 recap + name the **MOP**; flip every status banner (header, Part III, Part V one-page, Part VII.1, footer, READMEs) from "tied 1–1 / Game 3 pending" to the **final result** (champion or runner-up).
4. `data/contradictions_log.csv` → set C13 to the final series result.
5. `make all` (must stay green + deterministic) → commit + tag **`v1.4-champion`** or **`v1.4-runner-up`**.

## Provenance

No content is recalled from model memory (the 2026 postseason post-dates the training cutoff); everything was pulled live and cited. Full source list: `../sources/source_log.md`.

- `APPENDIX_FULL_ANALYSIS.md` — the complete 19,000-word working analysis, preserved unedited. The main report is the 2,500-word version that answers the question.
