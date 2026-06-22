# Data Ingestion Sprint — Pre-Game-3 (June 21–22, 2026)

A source-discovery + data-acquisition sprint (not a writing pass). Goal: deepen the evidence base before the winner-take-all Game 3. Six new datasets ingested, four improved, build still green/deterministic.

---

## 1. New sources discovered (ingestible vs. blocked)

| Source | What it has | Ingestible? | Reliability |
|---|---|---|---|
| **ESPN box scores** (`espn.com/college-baseball/boxscore/_/gameId/<id>`) | line scores, lineups, pitching lines, **pitch counts**, attendance, HR | **YES** (clean HTML tables) | ★★★★★ — the workhorse |
| **WarrenNolan** ELO / RPI-live / SOS | post-G2 OU vs UNC ratings | YES | ★★★★★ |
| **Wikipedia rankings aggregator** | final human polls (D1B, BA, Coaches, NCBWA, PG) | YES | ★★★★ |
| **Wikipedia MCWS finals history** | every best-of-3 finals + Game-3 outcomes since 2003 | YES | ★★★★ |
| **VegasInsider / BetMGM** | Game 3 moneyline (UNC −160 / OU +125) | YES | ★★★ |
| **SI / 247Sports / ESPN** | G3 starters, UNC injury (Lynch oblique), coach quotes | YES (article) | ★★★ |
| **NWS Omaha / AccuWeather** | Game 3 weather/wind | YES | ★★★ |

## 2. New datasets created

| File | Rows | Contents |
|---|---|---|
| `data/game_log_enriched.csv` | 13 | **All 13 postseason games, inning-by-inning** (OU + opp), attendance, HR detail |
| `data/pitching_usage.csv` | 47 | Every OU pitcher-game in the postseason: IP/H/R/ER/BB/K/decision/**pitch count** |
| `data/player_postseason_splits.csv` | 40 | Per-game CWS AB/H/HR/RBI for 8 key hitters |
| `data/lineups_postseason.csv` | 6 | Batting orders 1–9 + C/DH for the CWS games |
| `data/game3_preview.csv` | 15 | Starters, bullpen status, injuries, weather, park, quotes, line, base rate |
| `data/historical_cws_context.csv` | 22 | Best-of-3 Game-3 history, sub-.500-conference finalists, power surges |

## 3. Existing datasets improved

- `data/ratings.csv` — **widened to head-to-head OU vs UNC** across 14 systems; filled UNC ranks; refreshed **post-G2 ELO (OU #6 1708 / UNC #2 1768)**.
- `data/betting.csv` — added the **Game 3 line** (BetMGM UNC −160 / OU +125) and the confirmed **Game 2 result** (UNC 6-2).
- `data/contradictions_log.csv` — **+6 entries (14→20)** from the contradiction hunt (below).
- `data/predictions_ledger.csv` — **P1 (Game 3)** updated to the post-G2 ELO + market + base-rate triangulation.

## 4. Sources rejected / blocked (documented, not worked around with fabrication)

- **SoonerSports box scores, NCAA.com `/game/`, StatBroadcast** — JS-rendered / browser-gate → **BLOCKED** (no line-score/PBP ingestion). ESPN substituted.
- **Massey Ratings** — HTTP 403 → **NOT_AVAILABLE** (needs manual browser lookup).
- **Boyd's World ISR** — scraper-blocked → exact value **NOT_FOUND**.
- **CBS G1 betting (403), SportsLine G3 pick (PAYWALLED)**.
- **Game durations** — not exposed by any ingestible source for any game → **NOT_FOUND** (all 13).
- **Game 3 run line + total** — not yet posted → **NOT_FOUND**.
- **UNC Game 3 starter** — genuinely undecided ("all hands on deck") → **NOT_FOUND** (did not invent a probable).
- **KPI / NET-equivalent for baseball** — does not exist.

## 5. Contradictions discovered (Track 10)

1. **Roster (C15):** the player list given (Carmichael / Nicklaus / Pettis) is **stale** — none are on the 2026 team (2024–25 players, since drafted/departed). Not ingested.
2. **Lineup static (C16):** the postseason batting order was **100% unchanged** across all CWS games, and **Tockey was already hitting 8th by the June 1 regional final** — so the "lineup changes sparked the run" narrative is *further* deflated; there were **no in-run lineup changes**.
3. **ELO moved (C17):** post-Game-2 ELO dropped OU to **#6** (UNC #2) → Game 3 P(OU) ~**41%**, not ~46%.
4. **Game-3 base rate (C18, contrarian):** the **Game-1 winner who loses Game 2 wins the decider only 4 of 12 times (.333)** — OU is the historical Game-3 **underdog**.
5. **Consensus polls (C19):** **UNC out-rates OU in every human poll** (UNC top-4; OU unranked/#19) — consensus correctly has UNC the better team; tempers OU optimism.
6. **Power suppressible (C20):** Game 2 (OU **0 HR, 2 runs**) is direct evidence the power surge is neutralizable by elite arms.

## 6. Most valuable newly-ingested data

1. **`historical_cws_context.csv` Game-3 base rate (.333)** — the single most decision-relevant Game-3 input; converges with ELO (41%) and market (44%).
2. **`game_log_enriched.csv`** — full-postseason inning data (upgrades the prior 6-game inning sample to all 13).
3. **`pitching_usage.csv`** — enables real bullpen/rotation/rest + Game-3 availability analysis (with pitch counts).
4. **`ratings.csv` head-to-head** — OU-vs-UNC across 14 systems for the Game-3 framing.
5. **`player_postseason_splits.csv` + `lineups_postseason.csv`** — real per-game CWS production on a confirmed-static lineup.

## 7. Data still missing (after the sprint)

- Game durations (all 13) — **NOT_FOUND** anywhere ingestible.
- Game 3 run line / total, UNC G3 starter — **NOT_FOUND** (not yet posted / undecided).
- Full play-by-play / per-event WPA — **BLOCKED** (JS-gated); inning-level is the ceiling.
- Massey rating, Boyd ISR exact values — **BLOCKED/NOT_FOUND**.
- Attendance for ~7 games — **NOT_FOUND** on ESPN.

## 8. Top 10 strongest next analyses now enabled

1. Full-postseason inning distribution (13 games) — first-inning, late-inning, scored-first %.
2. Bullpen workload + rest model → Game-3 availability (Wesloski rested SP; Cleveland fresh; X.Mercurius/Rager unavailable).
3. Rotation-cadence analysis (Rager 6–7-day; X.Mercurius Fri/Sun).
4. Per-game player postseason-vs-season delta (who actually elevated, game by game).
5. OU-vs-UNC head-to-head ratings dashboard (Game-3 preview).
6. **Game-3 win-probability triangulation** — ELO 41% + market 44% + history 33% → OU ~38–44%.
7. Power-surge-by-opponent-quality (5-HR cupcake/UGA games vs the Game-2 shutout).
8. Lineup-stability finding folded into the coaching section (retire the "lineup changes" claim).
9. Sub-.500-conference-finalist cohort study (OU '26, Ole Miss '22, OSU '07, UVA '15).
10. Pitch-count/fatigue flags for Game 3 (who threw 88–105 in G1/G2).

## 9. Exact files changed

**New (6):** `data/game_log_enriched.csv`, `data/pitching_usage.csv`, `data/player_postseason_splits.csv`, `data/lineups_postseason.csv`, `data/game3_preview.csv`, `data/historical_cws_context.csv`.
**Updated (4 data):** `data/ratings.csv`, `data/betting.csv`, `data/contradictions_log.csv`, `data/predictions_ledger.csv`.
**Scripts:** `scripts/validate_data.py` (+7 schema registrations / 1 schema change), `scripts/gamelog_market_analysis.py` (head-to-head ratings + numpy import).
**Removed:** stray `~/data/pitching_usage.csv` (agent wrote to wrong path; relocated + year-fixed 2025→2026).

## 10. Is the repo cleaner, stronger, reproducible?

**Yes on all three.** Datasets **15 → 21**; every new file carries `confidence` + `source`; `BLOCKED`/`NOT_FOUND`/`PAYWALLED`/`NOT_AVAILABLE` used throughout; no fabricated values. **`make all` passes (21/21 validate, 0 warnings) and is byte-for-byte deterministic.** No existing data overwritten without backup (ratings widened additively; betting/ledger/contradictions appended/edited in place). Net: a deeper, more skeptical, more ingestible evidence base — and the contradiction hunt made it *more* honest about OU's Game-3 underdog status, not less.
