# Football module — data audit (2026-09-06/07)

Skeptical record of how the data was gathered, what was cross-checked, what conflicted, and what was left out.

## 1. Source access log
| Attempt | Result | Consequence |
|---|---|---|
| CollegeFootballData API key on this machine | none found (`nil-portal/.env.example` only); creating an account is out of scope for an automated build | **Fallback mode** for the whole module |
| sports-reference.com (curl, WebFetch, in-app browser) | 403 / Cloudflare bot check — not bypassed | No SRS/SOS from SR; ESPN Power Index used instead |
| masseyratings.com, teamrankings.com | 403 | — |
| ESPN FPI pages / Power Index JSON | OK (2005–2025) | Ratings backbone |
| Football Outsiders S&P+ archive (2005–18) | OK (cached HTML) | SP+ 2005–18 |
| ESPN final SP+ articles 2020–22 | ESPN+ paywall | Replaced by puntandrally.com reprints (2019–25); 2019 cross-checked to ESPN |
| 247Sports team season pages | OK (all 25 classes) | Recruiting |
| Rivals team rankings, n.rivals.com | 403 | Rivals sparse (5 years via news) |
| Wikipedia raw wikitext (`action=raw`) | OK, cached | Game log |

## 2. Game-log cross-check
Three fetch-based extractions (agents, seasons 1999–2007 / 2008–16 / 2017–25) were diffed against a fully independent parse of the raw `{{CFB Schedule Entry}}` templates (`scripts/ingest_wikipedia.py`).
- 356 vs 356 games; every season's W-L matched both the infobox and each other.
- 346/356 rows matched on the (season, date) key at first pass; the 10 misses were `{{tooltip|...}}`-wrapped dates the first parser version did not handle (fixed; all 356 now key-match).
- Field diffs (7) resolved against the raw template text: 2010 Texas A&M opp_rank (agent 19 → blank per template), 2014 Texas Tech ou_rank (18 → blank), 2017 Big 12 CCG ou_rank (2 → 3), 2020 Texas Tech (rank 24 belongs to OU, not TTU), 2021 Tulane site (template `away=y`, game physically in Norman → coded H with note), 2018 Texas / 2024 Tennessee, Texas, Ole Miss opp ranks embedded in the opponent string (parser now extracts "No. N").
- One flagged-not-corrected item from the agents: 2016 Houston is printed as "No. 14" in the article (AP had Houston #15 that week per memory). Recorded as printed.
- No duplicate (season, date, opponent). **Correction (2026-09-07):** an earlier version of this file cited `result == (ou_pts > opp_pts)` as a sanity assertion. It is vacuous by construction — the template's score field is winner-first and carries no team labels, so the ingest *orders* the score by the W/L flag rather than reading it positionally. A flipped W/L flag would silently reverse a score and no internal check could see it. The real guards are external: the ESPN game-by-game cross-check (§9) and the infobox record cross-foot in `build_seasons.py`.

## 3. Season table cross-check
- Conference records computed from the templates' `nonconf` flag equal the infobox conference record in **27/27** seasons (validator-enforced).
- PF/PA are sums of the game log; the Wikipedia list page was used only for coach, finish, bowl and final polls.
- Anchors: 2000 13-0, 2020 9-2, 2024 6-7, 2025 10-3, Stoops 190-48 (validator + tests).

## 4. Ratings
- ESPN JSON category names were mapped explicitly (`resume.avgsosrank`, `resume.accomplishmentrank`, `efficiencies.offefficiencyrank`, …). A WebFetch summary of the 2024 efficiencies page had reported OU's offense rank as **37**; the JSON says **95** (offense eff 39.2). JSON kept; the summary was a fetch-model error. This is why no numbers in this module come from summarised pages.
- SP+ 2020–22: the reprint page publishes overall rank + rating and off/def **ratings** for all FBS teams but not off/def ranks. Ranks were derived by sorting; on 2023 (where the site publishes ranks) derived 7/33 == published 7/33. 2019 derived def rank 47 vs ESPN 48 (tie) — ESPN kept.
- 2022 overall SP+: reprint final list #19 vs stormininnorman.com post-bowl reprint #18 → `CONFLICTING`, 19 kept.
- ESPN historical efficiency/FPI for 2005–13 are ESPN's retroactive computations; tagged REPORTED.

## 5. Recruiting
- 247 Composite 2002–09 are retroactive reconstructions (247Sports launched 2010); 247 re-rates classes after the cycle, so 2022 (signing-day #5 → now #8) and 2023 (#4 → #5) are `CONFLICTING`; current page values kept, signing-day figures in notes.

## 6. Coaches
- Wikipedia lists Stoops 191-48 (includes the interim 2021 Alamo Bowl); NCAA/ESPN 190-48 for the 1999–2016 tenure — 190-48 kept. Venables' infobox shows 33-20 (includes the 2026 opener); 32-20 through 2025 kept.

## 7. Not done / not faked
- No box-score drivers (Q4 stub). No play-by-play. No per-game opponent SRS. No pre-2005 adjusted ratings. Bedlam post-2023 does not exist. 2026 is tracker-only.

## 8. Self-corrections made during analysis
- Chart 07 title originally said "three straight losses" to Texas under Venables; the data says 2022 L, 2023 W, 2024 L, 2025 L → rewritten as "lost 3 of 4", now computed from data.
- Chart 04 title originally hardcoded a comparison; now computed (2 of 19 Big 12 schedules harder than 2024's, 6 harder than 2025's).
- Q7 text originally said margin "persists" at r = +0.21 (p = .30); softened to "weakly positive, not significant".
- Q6 residual table originally read as a talent-adjusted verdict; the lag-3 slope is wrong-signed and non-significant, so the residuals are now labelled descriptive.

## 9. ESPN second-source cross-check (2026-09-07, `scripts/crosscheck_espn.py`)
Every one of the 356 games was matched to an event in ESPN's public team-schedule API (regular + postseason, dates converted to US/Central). Full table: `audit/espn_crosscheck.md`.

| Field | Agree | Disagree |
|---|---|---|
| Score (both teams) | 350 | 6 |
| Result | 351 | 5 |
| Site H/A/N | 330 | 26 |
| OU rank at kickoff | 291 | 65 |
| Opponent rank at kickoff | 327 | 29 |

**Adjudication of the six score/result disagreements — all ESPN-side, no module cell changed:**
- **1999 (5 games: Notre Dame, Texas, Colorado, Texas Tech, Ole Miss bowl):** ESPN assigns each loss's points to OU as a win. ESPN's 1999 record would be 12-0; OU's 1999 record is CONFIRMED 7-5 (Wikipedia list + infobox; NCAA-published). Module values kept.
- **2001 North Carolina:** ESPN shows 10-0; Wikipedia 41-27. Third sources: SoonerSports 2001 schedule/stats page and SoonerStats box score both give **41-27** (OU 31 points in the first quarter). Module value kept.

**Site disagreements (26):** all in 1999–2007 and all cases where ESPN's `neutralSite` flag is unset for Red River (Cotton Bowl, Dallas), Big 12 Championship Games and bowls, or where ESPN's home/away is simply wrong (2000 Nebraska, the famous 31-14 win in Norman, is "away" on ESPN). **From 2008 onward the two sources agree on 100% of sites.** Module (Wikipedia + physical site rule) kept.

**Rank disagreements:** concentrated in 2000–2013 (2000 alone: 13 OU-rank gaps) where ESPN's historical `curatedRank` is missing or sparse; 2014–2025 disagree on 8 OU ranks and 4 opponent ranks, mostly CFP-committee vs AP weeks. These do not touch scores, margins, Pythagorean or one-score results; the "vs ranked" splits use the Wikipedia/AP column and carry this caveat in the report.

**Re-run after the 2026-09-07 corrections:** opponent-rank agreement rose from 325 to **327** — both corrected
cells (2016 Houston, 2005 Texas Tech) moved the module *into* agreement with ESPN, which is independent
support that the corrections went the right way. Score, result and site counts are unchanged.

**Net effect of the check:** the score/result layer of the game log is now double-sourced for 350/356 games and triple-sourced for the 6 exceptions; the site layer is double-sourced from 2008; ranks remain single-source (REPORTED).

## 10. Independent adversarial audit (2026-09-07)
A 29-agent audit re-derived every headline claim straight from the CSVs without reading the generated
numbers file, reviewed the code, and hunted third sources. Results: **10 of 12 claims confirmed exactly**,
2 material defects found, 44 code findings (10 high severity), 5 source tasks. Everything below is fixed.

**Data corrections**
| Where | Was | Now | Basis |
|---|---|---|---|
| `games_football.csv` 2016 Houston `opp_rank` | 14 | **15** | AP preseason had Washington #14 and Houston #15; Houston's own article (`rank=15, opprank=3`), the Wikipedia AP rankings page, CBS Sports and NCAA.com agree. Five sources vs one bad template parameter. |
| `games_football.csv` 2005 Texas Tech `opp_rank` | 19 | **21** | Texas Tech's own 2005 article gives `rank=21` for the game; ESPN's curatedRank agrees. Three sources vs one. |
| `ratings_football.csv` 2021 `sp_def_rank` | 56 | **57** | Found while writing `build_ratings.py`: the original derivation parsed the SP+ table with a character class that silently dropped one team per season — San Jose State (accented before 2023) and Miami (OH). A dropped team shifts every rank below it. Only 2020-22 ranks were ever derived; of those only 2021 was wrong. |
| `seasons_football.csv` 2002 `conf_finish` | 1st South | **T-1st South** | OU and Texas both finished 6-2 in the division and OU advanced on the tiebreaker; 2008 and 2010 division ties are already labelled "T-1st South". |

Neither rank correction changes ranked/unranked or top-10 status, and the 2021 rank moves the Riley-era
mean defense rank from 49.2 to 49.4 — no finding moves. They are corrected because they are wrong.

**Report defects fixed**
1. **"#43–#84" was the wrong range for Riley's defenses** and appeared in five places. The real values are
   #43, #84, #48, **#15**, #57 — 2020 was a top-15 defense, i.e. one of Riley's five teams was balanced, not
   lopsided. Chart 02 plotted 2020 at #15 directly under a title claiming the floor was #43.
2. **"Postseason" silently included conference championship games.** Stoops' bowl/CFP record is **9-9** and
   Riley's is **2-3**, not the 16-10 and 6-3 printed; Riley's flips from winning to losing. Both tables now
   carry a separate bowls-and-playoff column, and the term is defined in §2.
3. **"about two wins a season" of Riley luck** overstated the computed +1.27/season by 58%, in the one
   sentence that answers the research question.
4. **Q4 stated the opposite of the data.** The record against unranked opponents was called "the part that
   improved least in 2025"; it improved *most* (.643 in 2022-24 to .833 in 2025) while the top-10 record
   did not improve (1-2).
5. **Chart 05's title read "trail it by −3.0"** — a double negative asserting the opposite of the finding.
6. **"the seven 12-win seasons"** matched no construction (8 seasons have exactly 12 wins, 9 have 12+).
7. **Close-game robustness was overstated.** Venables' negative luck is exactly .500 at the 6- and 7-point
   thresholds, so "survives every threshold" was wrong for him (it holds for Riley).

**Validator gaps closed.** The audit demonstrated, by mutating copies of the data, that the validator would
pass while: every margin was shifted by 10; a season's `G` was changed from 13 to 20; ratings ranks were
arbitrarily rewritten. It now recomputes `margin`, `one_score`, `G`, `win_pct` and `margin_pg` from their
inputs and range-checks every rating. One class of tampering remains uncatchable internally — swapping two
games' outcomes within a season preserves every aggregate — which is exactly why the ESPN cross-check exists.

**Reproducibility.** Six of seven datasets had no committed generator. `build_seasons.py` and
`build_ratings.py` now rebuild the two largest from source with cross-checks that refuse to write on a
mismatch; that guard immediately caught two of my own bugs (a regex matching "champion" inside
"Championship Game", which had credited OU with the 2003 title it lost 7-35, and the dropped-team rank shift).

**Findings I rejected.** The critic claimed chart 04's "19 Big 12 schedules" should be 25; the ratings table
holds 21 seasons of which 19 are Big 12 (2005-2023), so 19 is correct and the chart is unchanged. An agent
recommended ingesting the season articles' recruit-template ranks as CONFIRMED; those are point-in-time
snapshots with an access date, and the 2020 one reads #1 because it was captured in December 2019, so only
post-signing-day snapshots were used.

