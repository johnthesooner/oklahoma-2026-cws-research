# Source Log

Every external source used, what it supports, its quality tier, and the access date. All retrieval occurred **June 20–21, 2026** via live web research (the 2026 postseason post-dates the analyst model's training cutoff, so nothing is from memory).

**Quality tiers:** `PRIMARY` (official/box score) · `SECONDARY` (credible outlet) · `CROSS-REF` (used only to corroborate).

## Primary / official

| Source | URL | Supports | Tier |
|---|---|---|---|
| OU official cumulative stats PDF (as of 2026-06-20) | soonersports.com stats feed (`/stats/baseball/2026/pdf/cume.pdf`) | **All team, individual & fielding tables** — the data spine | PRIMARY |
| SoonerSports.com — NCAA selection (Atlanta Regional) | soonersports.com/news/2026/5/25/... | Seed, at-large bid | PRIMARY |
| SoonerSports.com — SEC Tourney loss to LSU | soonersports.com/news/2026/5/20/... | SEC Tourney 2–6 result | PRIMARY |
| SoonerSports.com — Tockey walk-off vs Georgia Tech | soonersports.com/news/2026/6/1/... | Regional final 8–7 (10) | PRIMARY |
| SoonerSports.com — "Championship Series bound" (Georgia) | soonersports.com/news/2026/6/17/... | 11–4 clincher, 5 HR | PRIMARY |
| NCAA.com — official RPI rankings | ncaa.com/rankings/baseball/d1/rpi | **RPI #24 at selection** | PRIMARY |
| NCAA.com — MCWS bracket/schedule/scores | ncaa.com/news/baseball/article/2026-06-20/... | CWS bracket, scores | PRIMARY |
| ESPN — box score, Finals G1 (OU 9, UNC 3) | espn.com/college-baseball/game/_/gameId/401874451 | Game 1 line, Lachance 2 HR | PRIMARY |
| ESPN — box scores: Georgia 11–4 (401874448), Georgia 4–3 (401874444), Alabama 9–0 (401874399), Kansas 8–1 (401874374), Kansas 13–2 (401874375), Georgia Tech (401873796) | espn.com/college-baseball/game/... | Per-game lines | PRIMARY |
| ESPN — Game 2 page (status check, 2026-06-21) | espn.com/college-baseball/game/_/gameId/401874452 | **Confirms Game 2 not yet played** | PRIMARY |
| WarrenNolan — OU team clubhouse | warrennolan.com/baseball/2026/team-clubhouse?team=Oklahoma | RPI ~#9 (current), SOS #2, Quad-1 17–15 | PRIMARY |
| Cord Rager player page | soonersports.com/sports/baseball/roster/cord-rager/19886 | Rager bio/line | PRIMARY |

## Secondary

| Source | Supports | Tier |
|---|---|---|
| Baseball America — "No. 19 Oklahoma 2026 preview" | Preseason #19; Witherspoon departure; SEC projection | SECONDARY |
| Baseball America — 2026 SEC season preview | Picked low in SEC | SECONDARY |
| Baseball America — final in-season Top 25 | OU dropped from rankings | SECONDARY |
| Baseball America — Cord Rager breakout | Rager CWS profile | SECONDARY |
| OU Daily — Super Regional (Kansas) live | Rager 6 IP; Lachance "0 HR in first 31 games" quote | SECONDARY |
| OU Daily — CWS vs Alabama | Rager 7 IP shutout, 88 pitches, "since 1973" | SECONDARY |
| OU Daily — Skip Johnson / pitching | Coaching, usage | SECONDARY |
| ESPN — Lachance rolled-ankle / 409-ft HR feature (49063381) | The "Kirk Gibson" game | SECONDARY |
| ESPN — MCWS Finals preview (49108933) | OU title history (1951, 1994), UNC 0-title history, Game-2 storylines | SECONDARY |
| ESPN — OU tops UNC G1 (49129839) | Game 1 recap | SECONDARY |
| SI.com — Skip Johnson pitchers; Rager vs Alabama; Super Regional weather suspension | Pitching narrative, G2 suspension | SECONDARY |
| Yahoo Sports — CWS bracket live; Finals G1 live; CWS teams & odds | Bracket, odds, Game 1 detail | SECONDARY |
| CBS Sports — CWS schedule/scores/TV; UNC–OU tale of the tape | Schedule, Game-2 status, picks | SECONDARY |
| On3 — Citadel 15–5; USA Today ranks 8 CWS teams; Skip Johnson Omaha; UNC No. 5 seed | Regional, re-rank, seeding | SECONDARY |
| News9 — Rager 9–0 vs Alabama | Alabama shutout | SECONDARY |
| Saturday Down South — Lachance multi-HR Finals group | Finals G1 power | SECONDARY |
| Daily Tar Heel — Finals G1 | UNC-side recap | SECONDARY |
| georgiadogs.com — Georgia No. 3 national seed | Georgia seed/SEC champ | SECONDARY |
| goheels.com — UNC tops WVU for Finals berth | UNC path | SECONDARY |

## Cross-reference only

| Source | Supports | Tier |
|---|---|---|
| Wikipedia — 2026 Oklahoma / Georgia / Alabama / North Carolina season pages | Corroboration of records, dates, bracket | CROSS-REF |

## Claims that FAILED verification (excluded from the report)

The adversarial verification pass refuted these under 3-vote review; they are **not** used:
1. "UNC finished #4 RPI with a 45-11 record" — refuted (only UNC's **No. 5 national seed** is confirmed).
2. "Alabama #6 RPI / 37-19" and "Georgia #7 RPI / 46-12" — specific opponent RPI/records refuted.
3. A compound "10-2 postseason / 4-0 CWS / 8-7 10-inning GT win" phrasing — refuted as a unit (individual scores are box-confirmed; the rollup phrasing was inaccurate).

## Phase 11 — champion database sources (2000–2025)

Compiled into `data/champions.csv`. Per-cell confidence is in the CSV (17/22 rows CONFIRMED, 5 REPORTED). Primary pattern: official school cumulative stat sheets + ESPN archived conference team-stat pages, cross-checked against Wikipedia / TheBaseballCube / WarrenNolan.

| Champion(s) | Primary source |
|---|---|
| 2025 LSU, 2009 LSU, 2000 LSU | official LSU StatCrew cumulative files (`static.lsusports.net/.../teamcume.htm`) |
| 2024 Tenn, 2023 LSU, 2022 Ole Miss, 2021 Miss St, 2019 Vandy, 2017 Florida | ESPN archived SEC team pages (`a.espncdn.com/sec/baseball/<yr>/lgteams.htm`) + WarrenNolan |
| 2018 Oregon State | OSU media guide "2018 In Review" PDF |
| 2016 Coastal Carolina | goccusports.com official cumulative stats |
| 2015 Virginia, 2013 UCLA, 2014 Vanderbilt | official school cumulative pages / stat PDFs |
| 2011 & 2010 South Carolina | gamecocksonline.com cumulative stats |
| 2008 Fresno State | gobulldogs.com cume (Wayback) + CWS Game 16 box (reconciled to 47-31) |
| 2006/2007 Oregon State, 2004 CSF | TheBaseballCube + osubeavers / fullertontitans cume (Wayback) |
| Seeds (all) | NCAA tournament bracket pages (Wikipedia) |

**Data gaps (NOT_FOUND, not fabricated):** 2012 Arizona full pitching/fielding line (only AVG/ERA/HR/record sourceable — excluded from distance math); historical RPI for most pre-2022 champions; opponent AVG for 2006/2007 Oregon State; detailed 1951/1994 Oklahoma team stats.

## Known source conflicts (flagged, not silently resolved)

- **RPI #24 vs #9** — reconciled as two timestamps (selection day vs. current/post-run), not a contradiction.
- **Preseason rank** — a stray "#3" contradicted by BA's "#19"; treated as ~#14–19, the #3 unverified.
- **Lachance RBI** — official PDF 68 vs. an ESPN/CBS pregame display of 65; 68 treated as authoritative.
- **Catcher name** — "Deiten Lachance" (official) vs. "Deitan LaChance" (some recaps).
- **HR total** — SoonerStats lagged at 91; official PDF 93 used.
