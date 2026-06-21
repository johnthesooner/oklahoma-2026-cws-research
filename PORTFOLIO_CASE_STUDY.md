# Portfolio Case Study — The 2026 Oklahoma Sooners CWS Run

> **Using public college baseball data, this project investigates why the 2026 Oklahoma Sooners made a deep College World Series run, separating sustainable team strength from a postseason hot streak.**

**Author:** John Seals · **Type:** End-to-end data-science project (research + data engineering + reproducible build) · **Last updated:** June 21, 2026 (live mid-Finals)

---

## 1. The problem

Oklahoma reached the 2026 College World Series Finals as a team almost no model or poll liked: **unranked, unseeded, 14–16 in the SEC (11th place), RPI #24 on selection day,** and fresh off a first-round SEC Tournament exit. Yet it beat the **No. 2, No. 7, and No. 3 national seeds** to get to the title series.

That gap — between a mediocre résumé and an elite result — is the question. Two hypotheses compete:
- **H1 (sustainable strength):** OU was a genuinely good team that the schedule and conference record disguised.
- **H2 (hot streak / luck):** OU caught lightning — a temporary power surge and a soft draw.

The project's job is to **quantify how much of the run each explanation accounts for**, using only data that actually exists for college baseball, and to be honest about what doesn't.

## 2. Why it's a real analytics problem (skills demonstrated)

- **Sourcing & verification under uncertainty** — the events post-date the analyst model's training cutoff, so 100% of the data was gathered live and **adversarially verified** (a 109-agent pass; 22 claims confirmed, 3 refuted-and-excluded).
- **Data engineering** — seven tidy, schema-validated CSVs with explicit provenance and confidence columns; a deterministic build (`make all`).
- **Integrity discipline** — a four-level confidence taxonomy applied to every figure; a maintained list of metrics that **don't exist** for college ball, never fabricated.
- **Analysis & communication** — a 10-phase report, a chart suite, and a probabilistic verdict that resists the easy "they just got hot" narrative.

## 3. Approach

1. **Verify the premise**, then pull data three ways in parallel: official cumulative stat lines, ESPN/NCAA box scores, and WarrenNolan/NCAA résumé data.
2. **Tag everything** `CONFIRMED` / `REPORTED` / `ESTIMATED` / `NOT AVAILABLE`.
3. **Adversarially verify** the load-bearing claims; exclude what fails.
4. **Engineer the datasets** (`data/*.csv`) and **validate** them programmatically (`scripts/validate_data.py`).
5. **Generate assets deterministically** (`scripts/build_report_assets.py` → charts + checksummed manifest).
6. **Synthesize** the 55/35/10 verdict in the report.

## 4. Headline result

| Driver | Estimated share | Repeatable? |
|---|---:|---|
| Sustainable team strength (OBP .391, 132 SB/85%, 10.4 K/9, +112 diff, #2 SOS) | **~55%** | Yes |
| Perfectly timed power surge (HR rate ~doubled; ~45 HR in last 20 games) | **~35%** | Partly |
| Favorable matchups | **~10%** | n/a — the bracket was *hard* |

**Conclusion:** Not a fluke and not a juggernaut — **a legitimately good, underrated team that the schedule disguised, which caught a real power wave at the perfect moment and beat elite competition to do it.** Strip the surge and OU is a solid regional team; add it on a strong base against a hard draw and you get a Finalist. *(The percentages are an explicit analyst `ESTIMATED` weighting, not a measured decomposition — labeled as such.)*

## 5. What I'd do with more/better data

The honest ceiling here is the data itself. With Trackman/exit-velo feeds or play-by-play, I could compute true wOBA/FIP, a real defensive-efficiency rating, and proper regular-season-vs-postseason split models — turning the `ESTIMATED` surge magnitude into a measured one and the 55/35/10 verdict into a fitted decomposition. Those inputs are not public for college baseball, which is itself a finding.

---

## Closing report

### Files changed (this packaging pass)

**New files**
- `PORTFOLIO_CASE_STUDY.md`, `LICENSE`, `.gitignore`, `requirements.txt`, `Makefile`, `run_analysis.sh`, `build_manifest.json`
- `scripts/validate_data.py`, `scripts/build_report_assets.py`
- `data/README.md`, `charts/README.md`, `report/README.md`
- `sources/source_log.md`, `methodology/confidence_framework.md`

**Modified**
- `README.md` — rewritten as a polished public project front page.
- All seven `data/*.csv` — added standardized `confidence` + `source` columns (data values unchanged; `cws_opponents.csv` cleaned of inline tags).
- `charts/*.png` — regenerated via the deterministic build.

*(The full research report `report/OKLAHOMA_2026_CWS_RESEARCH_REPORT.md` was authored/updated in prior passes and is unchanged here except as referenced by the new sub-READMEs.)*

### Reproducibility status — ✅ FULL

- `make all` / `./run_analysis.sh` runs: **validate (7/7 datasets pass, 0 warnings) → regenerate 10 charts → write checksummed manifest.**
- Build is **deterministic**: two consecutive runs produce **byte-identical** charts and manifest (SHA-256 verified).
- Dependencies pinned in `requirements.txt`; tested on Python 3.14 / pandas 3.0 / matplotlib 3.10.

### Data limitations

- **Advanced metrics do not exist** for public college baseball (wOBA, FIP, xFIP, exit velo, defensive efficiency, starter-vs-bullpen ERA split) — listed `NOT AVAILABLE`, never fabricated.
- **Phase splits estimated** — no public regular-season-vs-postseason slash lines; surge *magnitude* is `ESTIMATED`.
- **Opponent records/RPI partly refuted** and excluded; only opponent **seeds** are firmly confirmed.
- **One open data gap:** Caden Aoki's season pitching line (his CG vs. Georgia is box-confirmed; season totals `NOT_FOUND`).

### What still needs updating after Game 2 / Game 3

1. Fill `data/postseason_games.csv` rows 13–14 with actual scores (replace `PENDING`/`CONDITIONAL`); re-run `make all`.
2. Write Game 2/3 recaps in report **Part III** and name the **Series MVP**.
3. Update status banners (README, report header, report Part III, Part VII.1); if OU wins, replace "title not decided" with the confirmed championship (first since 1994) and resolve the MVP prediction.
4. Optionally revisit the **Definitive Verdict (Part VI)** — though the strength/streak/matchup split holds regardless of the title outcome.

### Is it ready to `git commit`?

**Yes — ready for an initial commit and to push to a public GitHub repo.** Structure, reproducibility, validation, licensing, and documentation are portfolio-grade. The single caveat is editorial, not technical: it is a **live snapshot mid-series**, clearly labeled as such. Recommended path: commit now as a tagged snapshot (e.g., `v0.9-finals-g1`), then a follow-up commit (`v1.0`) once Games 2–3 are filled in. No secrets, no large binaries, no fabricated data — safe to make public.
