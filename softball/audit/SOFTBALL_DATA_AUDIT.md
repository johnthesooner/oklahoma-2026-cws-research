# Softball Module — Data Audit (gaps, conflicts, corrections)

The skeptical record for the softball module. Everything here is flagged in-data; nothing was silently resolved or fabricated.

## Premise corrections caught during research
1. **The dynasty has cracked — OU did NOT win 2025 or 2026.** Texas won **both** (back-to-back; Teagan Kavan 2x WCWS MOP). In **2026 OU lost the Norman Super Regional to Mississippi State and missed the WCWS** (~#8). The prompt's framing of unbroken dominance is outdated. `CONFIRMED`
2. **"Player development" is not the dynasty's driver.** All 10 stars studied were **elite recruits or transfers**, not developed-from-sleeper. OU's edge is talent *acquisition + showcasing*, not creating growth from low-rated players. `CONFIRMED`
3. **Sydney Romero** played for **Mexico** (not USA) at Tokyo 2020 — not a USA silver medalist. `CONFIRMED`
4. **Keilani Ricketts** was a Tokyo 2020 **alternate** (did not compete/medal). `CONFIRMED`
5. **Sam Landry** pitched for OU in **2025 only** (transfer; then pro, AUSL #1) — relevant to the 2026 "no true ace" problem. `CONFIRMED`
6. **JT Gasso ≠ DJ Gasso:** JT (Patty's son) is OU's hitting coach; DJ left Arkansas to become **Tulsa HC in 2026** — not an OU staffer. `CONFIRMED`
7. A Wikipedia "2026" fetch wrongly claimed **Alabama** won 2026 / OU finished #2 — **rejected** via NCAA/ESPN/NFCA consensus (Texas champ, OU #8). `CONFLICTING → resolved`

## Conflicts flagged (not silently resolved)
- **Gasso WCWS-appearance count:** 17 (aggregate) vs Wikipedia infobox **14**. `CONFLICTING`
- **Gasso career win total:** OU-only 1,567-361 `CONFIRMED`; overall 1,619-371 single-sourced `REPORTED`.
- **UCLA titles:** 12 recognized (1995 vacated); UCLA markets 13. `CONFLICTING`
- **Four-peat record:** 235-15 (Wikipedia season-by-season) vs a cited 232-15 variant. `CONFLICTING`
- **2012/2018 Big 12 records, 2021/2020 ERA:** official-sheet vs Wikipedia/aggregator discrepancies — resolved to the official/mathematically-consistent value (noted in `ou_softball_dynasty.csv`).
- **2025 final ranking:** NFCA #2 vs SoonerStats #3. Used #2 (`REPORTED` on that field).

## Data gaps (NOT_FOUND — not fabricated)
- **Fielding % for 2016 & 2017** — SoonerStats tables empty / official PDF 404. NOT_FOUND.
- **2020 final ranking** — COVID-cancelled; no final poll issued.
- **2019/2022 overall recruiting-class ranks** — strong per-player ranks but no clean class number.
- **Recruiting geography** is a bottom-up `ESTIMATED` aggregate (no single quantified source).
- **OU women's gymnastics exact title count** (cross-sport) — `REPORTED`, not independently verified in this module.
- **Single-source cells** (2016/2017 batting/pitching via SoonerStats only) tagged `REPORTED` even where the season outcome is `CONFIRMED`.

## Scope notes
- The dynasty database window is **2010-2026**; the **2000 title team predates it** (so the CSV shows 7 in-window titles vs 8 all-time). The "best OU seasons" ranking is therefore 2010-2026 only.
- WHIP values are computed `(BB+H)/IP` from official totals, not published directly (`ESTIMATED`-grade where so).
