# Championships Module — Data Audit (conflicts, resolutions, gaps)

The skeptical record for the all-sports championships module. Everything here is
flagged in-data; nothing was silently resolved or fabricated. Research method:
four parallel research agents (football+baseball; softball+women's gym; men's
gym+wrestling; master reconciliation + other sports), each cross-checking
soonersports.com, NCAA.com, Wikipedia, ESPN, and sport governing bodies.

## Conflicts resolved
1. **Softball 2026 — did OU reach the WCWS?** One research agent asserted OU reached the
   2026 WCWS but lost before the final. **REFUTED** by a dedicated reconciliation agent with
   3+ independent sources: OU **lost the Norman Super Regional Game 3 to unseeded Mississippi
   State, 6–0, on May 24, 2026**, and **missed the WCWS** (first miss since 2015). Sources:
   NCAA.com ("Mississippi State ends Oklahoma's 9-year WCWS streak"), ESPN box score (gameId
   401873446), SI. This also confirms the separate `softball/` module's existing claim.
   **Resolution: OU did NOT reach the 2026 WCWS.** `CONFLICTING → resolved (CONFIRMED)`
2. **Wikipedia "2026 softball" mis-fetch** (in the softball module) once claimed Alabama won
   2026 — rejected via NCAA/ESPN consensus: **Texas** won 2025 and 2026 (def. Texas Tech both
   times; Teagan Kavan 2× MOP). `CONFLICTING → resolved`

## Conflicts flagged (documented, partially open)
- **Football unclaimed-title list is CONFLICTING across compilations.** The 10 years in
  `football_unclaimed_titles.csv` (1915, 1949, 1953, 1957, 1967, 1973, 1978, 1980, 1986, 2003)
  come from the Wikipedia article body; a separate search summary returned a partially different
  set. Each is tagged `REPORTED`; treat the *list* as `CONFLICTING`, not settled. OU itself claims
  none of them.
- **"7 AP / 6 Coaches" phrasing** seen in one search summary is imprecise/garbled and was **not**
  used; the verified, claimed football set is the 7 years in the master. `CONFLICTING → excluded`
- **Gasso career-win and Gasso WCWS-appearance counts** have minor source discrepancies (handled in
  the softball module); not material to the title count here.

## Co-championships (counted, but shared)
- **1977 men's gymnastics** — shared NCAA title (Paul Ziert). `CONFIRMED`
- **2014 women's gymnastics** — tied Florida 198.175, first tie in NCAA gym history; both champions.
  `CONFIRMED`
- Strict "outright only" view: OU = **44 outright + 2 shared = 46**.

## What is and isn't counted
- **Counted:** 39 NCAA-administered **team** titles + 7 **football selector** titles = 46 (OU's own
  claimed total). The split and basis are columns in `ou_all_championships.csv`.
- **Not counted as team titles:** individual national champions (e.g., OU's reported ~65 individual
  NCAA wrestling champions, gymnastics individual-event titlists). These are `REPORTED` aggregates
  noted in research, not in the master.
- **Not counted:** football minor-selector "unclaimed" years; the in-progress 2026 baseball CWS
  Finals (`NOT_FOUND` until final); runner-up finishes (in `near_misses.csv`).

## Data gaps (NOT_FOUND — not fabricated)
- **Men's gymnastics career individual-NCAA-champion total** — no clean single aggregate located.
  `NOT_FOUND`.
- **Some early scores/details** (1930s–1960s wrestling, older gymnastics) — outcome/coach confirmed,
  but per-final detail thin; left blank rather than invented.
- **soonersports.com "national championships" landing pages** are JS-rendered and did not return body
  text via fetch; corroboration came from Wikipedia, NCAA.com, NWHOF, and OU coach-bio pages instead.

## Cross-checks enforced in code (`validate_championships.py`)
- Master row count == 46; NCAA/football split == 39/7.
- `(year, sport)` is unique in the master (years repeat across sports — e.g., 2016/2017 appear in
  three+ sports; 1951 in wrestling & baseball; 1974 in football & wrestling; 2000 in football &
  softball — all legitimately distinct).
- `titles_by_sport`, `titles_by_decade`, and `championship_coaches` each independently sum to 46.
