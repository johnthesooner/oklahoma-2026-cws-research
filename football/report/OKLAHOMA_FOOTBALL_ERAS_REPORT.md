# Oklahoma Football, 1999–2025: Three Eras, One Question

> **How has Oklahoma football's performance evolved across the Stoops (1999–2016), Riley (2017–2021) and Venables (2022–present) eras, and how much of the variance is explained by schedule, talent, unit efficiency and luck rather than by the coach?**

**Author:** John Seals · **Built:** 2026-09-06/07 · **Data window:** 27 completed seasons (356 games) + a 2026 tracker (1 game final, 11 pending) · **Build:** `make football` (validator → analysis → 8 charts), deterministic.

Every number below is traceable to a cell in `football/data/*.csv` with a `confidence` and `source` column, or is computed by `football/scripts/analyze_football.py` from those cells (the generated numbers file is `football/data/football_analysis_output.md`). Tags: `[CONFIRMED]` primary/official or ≥2 sources · `[REPORTED]` single credible source · `[ESTIMATED]` computed, formula shown · `NOT_AVAILABLE` does not exist in this build and was not guessed.

**Fallback-mode notice.** No CollegeFootballData API key was available, so this build uses the documented fallback: game logs parsed from the raw templates of Wikipedia season articles (two independent extractions diffed field by field), ESPN Power Index JSON for FPI / strength of schedule / efficiency ranks (2005+), Connelly's SP+ (Football Outsiders archive 2005–18; ESPN 2019; reprints 2020–25), and 247Sports Composite class ranks. Box-score drivers (turnovers, penalties, third downs, red zone) are **NOT_AVAILABLE** and are not analysed.

---

## 1. Executive summary

1. **The eras are 190-48 (.798), 56-10 (.848) and 32-20 (.615).** Oklahoma's only two losing seasons since 1999 are both Venables seasons (2022, 2024) and both were followed by 10-3. Riley's personal record is 55-10; the extra win is the 2021 Alamo Bowl coached by interim Bob Stoops. `[CONFIRMED]` — HIGH.
2. **The units swapped, not the program's ceiling.** Riley fielded SP+ offenses ranked #1, #1, #3, #3, #3 behind defenses ranked #43, #84, #48, #15 and #57 — four of the five were #43 or worse and 2018's #84 is the worst OU unit in the window, though 2020 (#15) was genuinely balanced and is the exception to the pattern. Venables rebuilt the defense #65 → #33 → #17 → #4 while the offense fell to #76 (2024) and #51 (2025), the two worst OU offenses since 2005. Two independent systems (SP+ and ESPN efficiency) agree on the shape. `[REPORTED]` — HIGH.
3. **The SEC move made the schedule much harder, but explains only ~40% of the margin drop.** ESPN strength-of-schedule rank went from a mean of #41 (2021–23) to #12 (2024–25) and the share of games against AP-ranked opponents from 26% to 46%. Raw margin fell 4.8 pts/game; opponent-adjusted strength (FPI) fell 2.9. The residual is the team. `[ESTIMATED from REPORTED]` — MEDIUM (n = 2 SEC seasons).
4. **2024 and 2025 were different teams, and the 2025 rebound survives schedule adjustment.** SP+ #34 → #14, FPI 10.4 → 15.9 (the 2021–23 Big 12 baseline was 16.1), 6-7 → 10-3 with a CFP berth against the #14 schedule. The 2024 collapse was real and offensive (SP+ offense #76). `[REPORTED]` — HIGH.
5. **Recruiting rank explains almost none of OU's year-to-year variance.** Every class from 2002 to 2026 ranked between #3 and #19 in the 247 Composite; lagged 2 or 3 years, class rank correlates with win% at R² ≤ 0.07 (not significant). Within OU's talent band, the coach and the roster's construction matter more than the class rank. `[CONFIRMED ranks / ESTIMATED fit]` — MEDIUM.
6. **Luck is not evenly distributed, and only two of the three era figures are robust.** Riley's teams beat their Pythagorean expectation by +6.3 wins (+1.27 per season) and went 20-7 in one-score games; Venables' teams are −3.0 and 9-10. Riley's sign holds for every exponent from 2.0 to 3.0 and every close-game threshold from 3 to 10 points; Venables' holds for every exponent, and for every threshold except the 6- and 7-point cuts, where his close-game record is exactly .500. The Stoops-era figure (−1.9) is **not** robust — it swings from +6.2 to −13.0 with the exponent — so no 27-season "total luck" number is reported. Year-to-year, luck does not persist (r = −0.06). `[ESTIMATED from CONFIRMED scores]` — HIGH on the Riley/Venables direction, MEDIUM on magnitude (one-score bootstrap intervals overlap).
7. **The Venables-era warning signs are situational, not just aggregate:** 0-4 in bowls and the playoff, 1-6 at neutral sites, 1-3 in the Red River game, 8-8 in the game after a loss (Stoops: 36-3, Riley: 6-1). The bowl comparison is less lopsided than it looks: Stoops went 9-9 and Riley 2-3 in bowls and the playoff once conference title games are excluded. Small samples, but every split points the same way. `[CONFIRMED]` — MEDIUM (n).

**Verdict on the research question.** Across 27 seasons the coach explains the *shape* of the team (which unit is elite) far more than the *level*: the program's floor moved only when both units were weak at once (2022) or the offense collapsed (2024). Schedule accounts for roughly 40% of the SEC-era margin decline; recruiting accounts for almost nothing within OU's #3–#19 band; luck accounts for about 1.3 wins a season in the Riley years and about −0.75 a season under Venables. The remaining variance is team quality, which in 2025 returned to the Big 12-era baseline while playing a top-15 schedule.

---

## 2. Data and methodology

| Layer | Source | Seasons | Tag | Notes |
|---|---|---|---|---|
| Game log (356 games) | Wikipedia season articles, raw `{{CFB Schedule Entry}}` templates (`scripts/ingest_wikipedia.py`) | 1999–2025 | CONFIRMED-score | Two independent extractions (template parse vs. three fetch-based passes) diffed: 346/356 matched on the first pass; 10 date-format misses and 7 rank/site cells resolved against the raw template text (see `audit/`). |
| Season table | Wikipedia list of seasons + season infoboxes; PF/PA summed from the game log | 1999–2025 | CONFIRMED | Conference records from the games' `nonconf` flag reconcile with the infobox for all 27 seasons. |
| Ratings | ESPN Power Index JSON (FPI, SOS, SOR, game control, efficiencies); SP+ from Football Outsiders archive (2005–18), ESPN final 2019, puntandrally.com reprints (2020–25) | 2005–2025 | REPORTED | 2020–22 SP+ offense/defense **ranks** derived by sorting the full published rating list; method validated on 2023 (derived 7/33 = published 7/33). 2022 overall rank CONFLICTING (18 vs 19; final list kept). |
| Recruiting | 247Sports team season pages (Composite + 247 own rank) | classes 2002–2026 | CONFIRMED | 2002–09 are retroactive reconstructions; 2022–23 CONFLICTING vs signing-day reports (documented). Rivals/ESPN sparse (403s). |
| Coaches | NCAA.com, Wikipedia coach pages, Saturday Down South | — | CONFIRMED | Stoops 190-48 (Wikipedia's 191-48 includes the interim 2021 bowl); Venables 32-20 through 2025. |
| 2026 tracker | Wikipedia 2026 season page; SoonerSports recap | 2026 | CONFIRMED/PENDING | 1 final (W 51-0 UTEP), 11 pending; never aggregated with completed seasons. |
| Second-source check | ESPN team-schedule API (`scripts/crosscheck_espn.py`) | 1999–2025 | CROSS-REF | 356/356 matched; 350 scores identical; 6 ESPN-side errors (1999 ×5, 2001 UNC) adjudicated with third sources; sites agree 100% from 2008. |
| Rebuild scripts | `build_seasons.py`, `build_ratings.py` | 1999–2025 / 2005–2025 | — | The seasons and ratings tables regenerate from committed code and refuse to write unless the infobox record, the game-log record and the conference-title count all reconcile. |
| SP+ 2005–18 snapshot | `sources/snapshots/sp_plus_footballoutsiders_2005_2018.csv` | 2005–2018 | REPORTED | Football Outsiders no longer resolves, so these values cannot be re-fetched anywhere; the snapshot preserves OU's row per season, each carrying that season's record as a cross-check. |
| Independent audit | 29-agent adversarial pass, 2026-09-07 | — | — | Every headline claim recomputed from the CSVs by an agent that did not read the generated numbers; 10 of 12 confirmed, 2 material prose defects found and fixed (see §5 and `audit/`). |

**Anchor checks (all pass, enforced by `validate_football.py` and `tests/`):** 2000 = 13-0; 2020 = 9-2 (11 games); 2024 = 6-7; 2025 = 10-3; Stoops seasons sum to 190-48; games ↔ seasons W/L/PF/PA and conference records reconcile for every season; no 2026 rows in the game log; PENDING rows carry no score.

**Definitions.** Era = head coach by season (2021 labelled Riley; its bowl noted). One-score = final margin ≤ 8. Pythagorean wins = G × PF^2.37 / (PF^2.37 + PA^2.37). "Ranked" = AP rank at kickoff as printed in the season article. "Postseason" = every game with `game_type != REG`, which includes conference championship games; "bowls + CFP" excludes them. Site is physical (2021 Tulane, relocated to Norman, is coded H).

---

## 3. Findings by question

### Q1 — Era comparison

| Era | Seasons | Record | Win% | Conf | Margin/G | vs AP-ranked | vs top-10 | Postseason (bowl/CCG/CFP) | Bowls + CFP only | Conf titles | AP top-10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Stoops | 18 | 190-48 | .798 | 121-29 | +17.4 | 59-30 (.663) | 20-15 (.571) | 16-10 (.615) | 9-9 (.500) | 10 | 11 |
| Riley | 5 | 56-10 | .848 | 37-7 | +16.3 | 16-6 (.727) | 5-4 (.556) | 6-3 (.667) | 2-3 (.400) | 4 | 5 |
| Venables | 4 | 32-20 | .615 | 18-16 | +8.6 | 9-9 (.500) | 3-4 (.429) | 0-4 (.000) | 0-4 (.000) | 0 | 0 |

The two postseason columns differ only by conference championship games, where Stoops went 7-1 and Riley 4-0. Read "Postseason" as every non-regular-season game; the bowl-and-playoff record on its own is the second column.

**Claim:** the Venables era is the first sustained step down in the window, but it is bimodal (6-7, 10-3, 6-7, 10-3), not a steady decline. **Evidence:** the two 10-3 seasons rate #13 and #14 in SP+, squarely in the Stoops-era range; the two 6-7 seasons rate #19 and #34. **Chart:** `01_winpct_margin_by_era.png`. **Confidence:** HIGH on the facts, LOW on any extrapolation from n = 4. *What would change my mind:* a third 10-3-or-better season in 2026 would make 2022/2024 look like rebuild noise rather than a new baseline.

### Q2 — Efficiency (2005–2025)

| Era | n | SP+ overall (mean rk) | SP+ off | SP+ def | ESPN off eff | ESPN def eff |
|---|---|---|---|---|---|---|
| Stoops | 12 | 8.8 | 15.0 | 17.3 | 20.2 | 14.9 |
| Riley | 5 | 7.2 | 2.2 | 49.4 | 3.6 | 47.6 |
| Venables | 4 | 20.0 | 36.8 | 29.8 | 45.5 | 20.2 |

**Claim:** Riley's OU was the most lopsided team in the window and Venables' is its mirror image. **Evidence:** SP+ offense #1/#1/#3/#3/#3 vs defense #43/#84/#48/#15/#57 under Riley; defense #65/#33/#17/#4 vs offense #13/#7/#76/#51 under Venables. Stoops' best teams (2007, 2008, 2011, 2012) were balanced (both units top-30). **Charts:** `02_sp_offense_vs_defense.png`, `03_unit_ranks_over_time.png`. **Confidence:** HIGH (two independent rating systems, same shape). *Caveat:* pre-2005 seasons, including the 2000 title team, have no adjusted efficiency data here (NOT_AVAILABLE).

### Q3 — The SEC transition

| Window | Record | Margin/G | ESPN SOS rk | Games vs ranked | vs ranked | FPI | SP+ rk | SP+ off / def |
|---|---|---|---|---|---|---|---|---|
| Big 12 2021–23 | 27-12 (.692) | +11.5 | 41 | 26% | 5-5 | 16.1 | 15.0 | 8 / 51 |
| SEC 2024–25 | 16-10 (.615) | +6.6 | 12 | 46% | 6-6 | 13.2 | 24.0 | 64 / 10 |
| — 2024 | 6-7 | +2.5 | 9 | 38% | 1-4 | 10.4 | 34 | 76 / 17 |
| — 2025 | 10-3 | +10.8 | 14 | 54% | 5-2 | 15.9 | 14 | 51 / 4 |

**Claim:** "the SEC hurt OU" is half right. The schedule did get much harder (only 2 of OU's 19 rated Big 12 schedules were harder than 2024's; 6 were harder than 2025's), but the opponent-adjusted rating fell by only 2.9 points against a 4.8-point raw-margin drop, so ~40% of the visible decline is schedule and ~60% is the team, concentrated in 2024. In 2025 OU beat ranked opponents 5-2 with FPI back at the Big 12 baseline. **Chart:** `04_sos_big12_vs_sec.png`. **Confidence:** MEDIUM (n = 2 SEC seasons; FPI is a single-source rating; the game-level bootstrap interval on the −4.8 margin drop is −15.7 to +6.0, Q8). *What would change my mind:* a 2026 SP+ finish outside the top 20 against a similar schedule.

### Q4 — Game-level drivers (limited)

Box-score drivers are NOT_AVAILABLE without the CFBD API. What the game log supports:

| Opponent bucket | Stoops | Riley | Venables | All |
|---|---|---|---|---|
| AP top-10 | 20-15 (.571) | 5-4 (.556) | 3-4 (.429) | 28-23 (.549) |
| AP 11–25 | 39-15 (.722) | 11-2 (.846) | 6-5 (.545) | 56-22 (.718) |
| Unranked | 131-18 (.879) | 40-4 (.909) | 23-11 (.676) | 194-33 (.855) |

**Claim:** the Venables-era gap is widest against *unranked* teams (.676 vs .879/.909), not against elite ones (.429 vs .571/.556). That pattern is consistent with an offense that could not put weaker teams away — but it is the part of the record that improved *most* in 2025, not least: against unranked opponents Venables went 18-10 (.643) in 2022-24 and 5-1 (.833) in 2025, while the record against AP top-10 teams did not improve (1-2, .333, against a .568 Stoops/Riley baseline). Home/ranked contingency: OU wins 93% of home games vs unranked teams and 61% of road/neutral games vs ranked teams (n = 133 / 94). **Confidence:** MEDIUM. *Future work:* turnover margin and third-down rates once a CFBD key is available.

### Q5 — Situational splits

| Split | Stoops | Riley | Venables | All |
|---|---|---|---|---|
| Home | 101-9 (.918) | 29-2 (.935) | 21-6 (.778) | 151-17 |
| Away | 61-20 (.753) | 17-4 (.810) | 10-8 (.556) | 88-32 |
| Neutral (Red River, bowls, CCGs) | 28-19 (.596) | 10-4 (.714) | 1-6 (.143) | 39-29 |
| Red River (incl. 2018 CCG) | 11-7 | 5-1 | 1-3 | 17-11 |
| Bedlam (through 2023) | 14-4 | 4-1 | 1-1 | 19-6 |
| One-score games | 36-22 (.621) | 20-7 (.741) | 9-10 (.474) | 65-39 (.625) |
| Postseason (bowl/CCG/CFP) | 16-10 | 6-3 | 0-4 | 22-17 |
| Bowls + CFP only (no CCGs) | 9-9 | 2-3 | 0-4 | 11-16 |
| Game after a loss | 36-3 (.923) | 6-1 (.857) | 8-8 (.500) | 50-12 |

**Claim:** the clearest era-specific signature is resilience. Stoops and Riley teams almost never lost the week after a loss (42-4 combined); Venables teams are 8-8. **Charts:** `07_red_river_timeline.png`, `08_one_score_by_era.png`. **Confidence:** MEDIUM (small Venables n in each cell), HIGH that every split points the same direction.

### Q6 — Recruiting vs results

| Lag | n | r (class rank, win%) | R² | p | r (class rank, SP+ rank) | p |
|---|---|---|---|---|---|---|
| 2 yr | 22 | −0.05 | 0.00 | .81 | −0.05 | .83 |
| 3 yr | 21 | +0.27 | 0.07 | .24 | −0.12 | .59 |

**Claim:** within OU's #3–#19 band, class rank has no measurable effect on win% two or three seasons later. **Evidence:** the fitted slope is wrong-signed and not significant; the five 12-win seasons in the lag-3 sample came from classes ranked #3 through #19 — though with every class in that band the comparison is close to vacuous either way. The per-era residuals (Stoops +0.018, Riley +0.065, Venables −0.136) are therefore descriptive, not talent-adjusted. **Chart:** `06_recruiting_vs_winpct.png`. **Confidence:** MEDIUM — 247's 2002–09 ranks are retroactive, 247 re-rates classes, and range restriction alone would depress R². *What would change my mind:* a player-level (blue-chip ratio, transfer-portal net) measure rather than class rank.

### Q7 — Luck vs skill

| Era | Actual W | Pythag W | Luck | Per season | One-score |
|---|---|---|---|---|---|
| Stoops | 190 | 191.9 | −1.9 | −0.11 | 36-22 (.621) |
| Riley | 56 | 49.7 | +6.3 | +1.27 | 20-7 (.741) |
| Venables | 32 | 35.0 | −3.0 | −0.75 | 9-10 (.474) |

**Claim:** Riley's three 12-2 seasons carried +1.2, +2.1 and +1.7 wins of Pythagorean over-performance; by points they were 10-win teams. Venables' 2022 and 2024 were each ~1.3 wins unlucky; 2025 was luck-neutral (−0.1) despite 4-1 in one-score games. Luck shows zero year-to-year persistence (r = −0.06, n = 26), and margin/game itself persists only weakly (r = +0.21, p = .30). **Chart:** `05_actual_vs_pythagorean.png`. **Confidence:** HIGH on the Riley/Venables direction (robust to exponent 2.0–3.0 and thresholds 3–10, Q8); the Stoops-era total is exponent-dependent and is not interpreted; one-score bootstrap intervals (Riley .556–.889, Venables .263–.684) overlap, so the close-game contrast is MEDIUM.

### Q8 — Robustness

| Check | Result |
|---|---|
| Pythagorean exponent 2.0 / 2.37 / 2.7 / 3.0 | Riley +8.5 / +6.3 / +4.6 / +3.1; Venables −1.8 / −3.0 / −3.9 / −4.7 (signs stable). Stoops +6.2 / −1.9 / −8.1 / −13.0 (**not stable**). |
| One-score threshold ≤3 / ≤7 / ≤8 / ≤10 | Riley .714 / .720 / .741 / .759; Venables .250 / .500 / .474 / .455; Stoops .500 / .600 / .621 / .620. |
| Bootstrap 95% (game-level, 5,000 draws) | Win%: Stoops .744–.849 (n 238), Riley .758–.924 (66), Venables .481–.750 (52). One-score win%: Riley .556–.889 (27), Venables .263–.684 (19). SEC-minus-Big-12 margin/G: −15.7 to +6.0 (26 vs 39 games). |
| Second-source score check | 356/356 games matched to ESPN's schedule API; 350 scores identical; all 6 disagreements adjudicated as ESPN-side errors with third sources (`audit/espn_crosscheck.md`). Sites agree 100% from 2008. |

**Read:** the era *shape* findings (Q1, Q2, Q5) and the Riley/Venables luck signs are robust. The SEC decomposition (Q3) and the close-game contrast are directionally supported but not statistically tight at these sample sizes.

---

## 4. SEC transition verdict

Oklahoma's SEC schedules rank #9 and #14 nationally by ESPN's measure, harder than all but a handful of its Big 12 slates, and the team played 46% of its games against ranked opponents versus 26% in its last three Big 12 years. Against that, the opponent-adjusted rating fell 2.9 points and the raw margin 4.8, so the schedule accounts for roughly 40% of the visible decline. The other 60% is a real 2024 collapse, driven by the #76 SP+ offense and a 2-2 one-score record, that 2025 reversed: SP+ #14, FPI 15.9, 5-2 against ranked teams, and a CFP berth. The conference did not make Oklahoma worse; it made Oklahoma's bad year visible and its good year harder to reach. `[ESTIMATED]`, MEDIUM.

## 5. Limitations

- **Fallback data.** No CFBD key: no play-by-play, EPA, success rate, havoc, turnover or down-and-distance data. Q4 is a stub.
- **Ratings are retroactive and single-source.** ESPN Power Index history for 2005–2013 is computed by ESPN after the fact; the Football Outsiders S&P+ archive applies a later formula version to older seasons; SP+ 2020–22 offense/defense ranks are derived, not published (validated on one season). All tagged REPORTED/ESTIMATED.
- **Recruiting.** 247 Composite pre-2010 is reconstructed; 247 re-rates classes; Rivals/ESPN coverage is sparse (403s). Class rank is a coarse talent proxy with range restriction.
- **Ranks are single-source.** AP rank at kickoff is taken from the Wikipedia schedule tables; ESPN's kickoff ranks disagree in 65 OU / 31 opponent cells, mostly 2000–13 gaps and CFP-vs-AP weeks. "vs ranked" splits carry that caveat; scores and margins do not.
- **Small samples.** Venables n = 4 seasons; SEC n = 2; several situational cells have n < 10; bootstrap intervals in Q8 quantify this.
- **2020** is an 11-game COVID season (3 cancellations) and is included as played.
- **2026** is in progress (1-0) and lives only in the tracker.
- **Era boundaries** are by season; the 2021 bowl and the 2021 mid-season staff turmoil are folded into "Riley".

## 6. Future work

1. CFBD ingest (`/games`, `/stats/season/advanced`, `/ratings/sp`, `/recruiting/teams`) to replace the fallback layer and unlock Q4 properly; the budgeted client design is in the Cursor prompt that specified this module.
2. Play-by-play win probability and game-control analysis (ESPN's game-control rank is a weak proxy and is in `ratings_football.csv`).
3. Player-level talent: blue-chip ratio, transfer-portal net rating (links to the `nil-portal` project).
4. Betting-line calibration by era, reusing `data/betting.csv` conventions from the baseball module.
5. Update the 2026 tracker weekly; promote 2026 to `games_football.csv` after the season with a `make football` re-run.

## 7. Appendix

**Era definitions:** Stoops 1999–2016 · Riley 2017–2021 · Venables 2022–present. **Conference:** Big 12 through 2023, SEC from 2024.
**Metric formulas:** win% = W/(W+L); margin/G = (PF−PA)/G; Pythagorean W = G·PF^e/(PF^e+PA^e), e = 2.37; one-score = |margin| ≤ 8; luck = W − Pythagorean W; residual (Q6) = win% − (a + b·rank).
**Data dictionary:** `football/data/README.md`. **Sources:** `football/sources/source_log_football.md`. **Audit trail:** `football/audit/FOOTBALL_DATA_AUDIT.md`.
