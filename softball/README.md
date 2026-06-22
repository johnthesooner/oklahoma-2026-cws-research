# `softball/` — Oklahoma Softball Dynasty Module

A data-driven, skeptical analytical record of Oklahoma softball's modern dynasty and future outlook — built inside the OU 2026 research repo, same integrity standard (every figure `CONFIRMED / REPORTED / ESTIMATED / NOT_FOUND / CONFLICTING`; nothing fabricated).

## Thesis (one line)
**The greatest *peak* in softball history (the first-ever four-peat, 2021-2024), but not the greatest *program* (UCLA leads career titles/appearances) — and as of 2025-26 the dynasty has cracked (0 titles, a missed WCWS, a rising ERA, Texas overtaking it).**

## Structure
```
softball/
├── report/OKLAHOMA_SOFTBALL_DYNASTY_REPORT.md   # 11-part report + final verdict
├── data/        # 9 datasets (all confidence + source tagged)
├── charts/      # 5 charts (01 dynasty timeline ... 05 best OU seasons)
├── scripts/     # analyze_softball.py (metrics+charts) + validate_softball.py
└── audit/       # data gaps, conflicts, corrections
```

## Datasets (`softball/data/`)
- `ou_softball_dynasty.csv` — season-by-season 2010-2026 (record, ranking, WCWS, titles, full team stats)
- `historical_dynasties.csv` — all-time title/WCWS leaders (UCLA, Arizona, OU, Texas…)
- `gasso_profile_softball.csv` — Patty Gasso record, advantages, staff, contract
- `recruiting_pipeline_softball.csv` — class ranks, signees, geography
- `portal_analysis_softball.csv` — transfers in/out + 7-program comparison
- `player_development_softball.csv` — 10 stars: recruit rank → peak → pro
- `sec_transition_softball.csv` — the 2025-26 SEC move and the run-prevention crack
- `future_outlook_softball.csv` — returning core, losses, bull/base/bear
- `cross_sport_oklahoma.csv` — softball vs OU football/gymnastics/baseball

## Reproduce
```bash
python3 softball/scripts/validate_softball.py   # 9/9 datasets valid
python3 softball/scripts/analyze_softball.py     # metrics + charts 01-05 (deterministic)
```

## Key computed facts
- 2010-2026: **892-133 (.870), 7 titles, 13 WCWS** in 17 seasons (8 titles all-time incl. 2000).
- Four-peat 2021-24: **235-15 (.940), 1.49 avg ERA** — the most dominant sustained run in the data.
- The crack: team ERA **0.96 (2023) → 3.09 (2026)**; 2026 offense PEAKED (187 HR) but OU missed the WCWS.
- Most dominant OU season: **2022 (59-3)**.
