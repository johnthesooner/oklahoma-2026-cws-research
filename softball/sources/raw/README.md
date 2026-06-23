# Raw source captures (softball module)

Unprocessed text captures kept for provenance/auditability. These are **inputs to
the research**, not cleaned datasets — the analysis-ready data lives in
[`softball/data/`](../../data/) with per-cell confidence + source tags.

| File | What it is | Used for |
|------|------------|----------|
| `mg2019.txt` | OU softball media-guide text dump (2019) | season records, historical context |
| `mg2022.txt` | OU softball media-guide text dump (2022) | four-peat-era records, stats |
| `ou_sb_2024_mg.txt` | OU softball media-guide text dump (2024) | titles/WCWS counts, roster, staff |
| `wiki_ou2019.txt` | Wikipedia 2019 OU softball season (wikitext) | cross-check of season line |

All figures derived from these were re-verified against a second source where
possible and tagged accordingly in the datasets; single-sourced cells are marked
`REPORTED`. See [`softball/audit/SOFTBALL_DATA_AUDIT.md`](../../audit/SOFTBALL_DATA_AUDIT.md).
