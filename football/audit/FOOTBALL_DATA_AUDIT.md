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
- Sanity assertion on every row: `result == (ou_pts > opp_pts)`; no duplicate (season, date, opponent).

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
| Opponent rank at kickoff | 325 | 31 |

**Adjudication of the six score/result disagreements — all ESPN-side, no module cell changed:**
- **1999 (5 games: Notre Dame, Texas, Colorado, Texas Tech, Ole Miss bowl):** ESPN assigns each loss's points to OU as a win. ESPN's 1999 record would be 12-0; OU's 1999 record is CONFIRMED 7-5 (Wikipedia list + infobox; NCAA-published). Module values kept.
- **2001 North Carolina:** ESPN shows 10-0; Wikipedia 41-27. Third sources: SoonerSports 2001 schedule/stats page and SoonerStats box score both give **41-27** (OU 31 points in the first quarter). Module value kept.

**Site disagreements (26):** all in 1999–2007 and all cases where ESPN's `neutralSite` flag is unset for Red River (Cotton Bowl, Dallas), Big 12 Championship Games and bowls, or where ESPN's home/away is simply wrong (2000 Nebraska, the famous 31-14 win in Norman, is "away" on ESPN). **From 2008 onward the two sources agree on 100% of sites.** Module (Wikipedia + physical site rule) kept.

**Rank disagreements:** concentrated in 2000–2013 (2000 alone: 13 OU-rank gaps) where ESPN's historical `curatedRank` is missing or sparse; 2014–2025 disagree on 8 OU ranks and 4 opponent ranks, mostly CFP-committee vs AP weeks. These do not touch scores, margins, Pythagorean or one-score results; the "vs ranked" splits use the Wikipedia/AP column and carry this caveat in the report.

**Net effect of the check:** the score/result layer of the game log is now double-sourced for 350/356 games and triple-sourced for the 6 exceptions; the site layer is double-sourced from 2008; ranks remain single-source (REPORTED).

