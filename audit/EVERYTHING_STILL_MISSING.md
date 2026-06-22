# Everything Still Missing From The Oklahoma 2026 Analysis

### A skeptical 90-minute research-sprint audit — what the project lacks, what's wrong in it, and the highest-ROI ways to make it best-in-class

**Date:** June 21, 2026 · **Author:** John Seals · **Mode:** adversarial peer review (analytics director / pro bettor / front-office analyst / historian / sabermetrician / skeptical reviewer). **This document does not summarize existing work — it attacks it.**

> **✅ UPDATE — P2 block executed (v1.3).** Built the feasible best-in-class slices: **game-level/tier opponent adjustment** (`opponents_2026.csv` + `p2_advanced.py`; key result: **vs the NCAA field OU was 19-17, −0.2 run diff/G** — good-not-elite, +112 overall came from a 12-0 cupcake demolition); a **luck battery** (Pythagorean ≈ neutral; one-run 11-3 = favorable close-game variance; BaseRuns flagged as MLB-calibration-biased); a **betting-calibration study** (OU underdog in all 4 priced games, went 3-1 → market underrated it, Brier 0.27 > 0.25); **inning distribution** (6 games); and a **predictions ledger + contradictions log** (P2 #16). Charts 23–25, **report Phase 14**. **The one item the data defeats — the full play-by-play/WPA engine (#11) — is flagged NOT BUILT, not faked** (public college PBP is JS-rendered/blocked). Also folded in the **live Game 2 result (UNC 6-2; series tied 1-1, Game 3 June 22)**, which validated prediction P5.

> **✅ UPDATE — P1 block executed (v1.2).** The survivorship-bias fix is built: `data/cws_field.csv` (all 40 CWS participants 2021-25 = 5 champions + 35 non-champions = a real negative class), `scripts/championship_model.py` (champion-vs-field separation, leave-one-out logistic, kNN, PCA, k-means archetypes, Monte Carlo Finals), charts 19–22, **report Phase 13**. Headline results: **champions barely separate from the Omaha field (LOO AUC 0.55) → the title is high-variance once in Omaha**; OU's grounded title probability entering the tournament was **~6–13%**; OU's archetype cluster (power bat + 4.94 ERA) produced **0 champions** in the window (it's *more* pitching-deficient than its twin Ole Miss '22); but from up 1-0 the **Monte Carlo gives OU ~70%** (pre-series 43% ≈ market). P1 items 6–10 done. (Roster-churn/draft context also integrated into Phase 1.1.)

> **✅ UPDATE — P0 block executed (v1.1).** The "next 10 hours" items are now built: `data/game_log.csv` (64 games, reconciles to 42-22), `data/ratings.csv` (ELO/RPI/ISR), `data/betting.csv`, `scripts/gamelog_market_analysis.py`, charts 16–18, and a new **report Phase 12**. Two of this audit's own numbers were **corrected by the fuller data**: (a) **one-run record is 11-3 (.786), NOT 6-4** — the earlier figure was a subset, and .786 *is* a real variance signal; (b) the monthly log revealed the **June turnaround was substantially a pitching story (May 8.4 RA/G → June 2.9 RA/G)**, correcting the report's "offense-only transformation" framing. Pythagorean (≈neutral luck), K%/BB%, and the bullpen-vs-starter split (pen 4.76 < rotation 5.04) are now computed and integrated. The §-references below to "6-4" are left as written to show the self-correction.

> **Headline:** the project is strong on *narrative and sourcing* but has three structural weaknesses — **(1) survivorship bias** (it compares OU only to champions), **(2) zero opponent adjustment** (raw stats never adjusted for the nation's hardest schedule), and **(3) no game-log / play-by-play layer** (so one-run records, monthly splits, situational hitting, and luck tests were never computed). This sprint already *found or computed* several of the missing pieces — they change or sharpen the conclusions.

---

## 0. Live status gap (trivial, fix first)
The **CWS Finals are still unresolved** — Game 2 (June 21) had not been played at last check; OU leads 1–0. Every "finalist" framing is correct, but the title is undecided. **Next step:** pull Game 2/3 box scores when final, fill `data/postseason_games.csv` rows 13–14, rerun `make all`.

---

## 1. New sources discovered (inventory + quality + unique contribution)

| Source | URL | Quality (1–5) | Unique contribution NOT already in the project |
|---|---|---|---|
| **WarrenNolan ELO** | warrennolan.com/baseball/2026/elo | **5** | Opponent-adjusted, **postseason-updated** rating. **OU = #4 nationally, 1722.75** (Georgia 1781, UNC 1753, GT 1742, OU 1722, UCLA 1720). Quantifies the surge revaluation (≈#18 pre-tourney → #4). |
| **Betting markets** (BetMGM/CBS/SBD/Kalshi) | see source_log | **5** | Title-futures time series + per-game lines — the cleanest "surprise" quantifier the project entirely lacks. |
| **WarrenNolan game log** | warrennolan.com/college-baseball/team/schedule/.../Oklahoma | **5** | Full 64-game results → one-run, extra-inning, monthly, comeback records (never pulled). |
| **Boyd's World ISR / pseudo-RPI** | boydsworld.com/baseball/isr | **4** | Independent opponent-adjusted rating; **frozen ~June 6 (pseudo-RPI #18, .588)** = a clean *pre-tournament* baseline. |
| **Massey Ratings (cbase)** | masseyratings.com/cbase | **4** | Third independent opponent-adjusted rating w/ offense/defense split (value needs manual lookup; 403 to scrapers). |
| **StatBroadcast PBP archive** | oklahoma.statbroadcast.com | **4** | At-bat-level play-by-play for all games → RISP, inning-by-inning, WPA approximations (engineering required). |
| **NCAA official RPI ladder** | ncaa.com/rankings/baseball/d1/rpi | **4** | Official RPI (**#24**) — distinct from WarrenNolan's recompute (#9 current). |
| **Local OU coverage + pressers** | The Oklahoman, StorminInNorman, OU Daily, News9/On6, SI/John Hoover | **4** | The *only* place player-development/coaching explanations and quotes live (see §3). |
| **MLB Draft records** | MLB.com / SI draft | **4** | Talent baseline: OU lost **both Witherspoons** (Kyson 1st rd/15th, Malachi 2nd rd) + 5 drafted pitchers. |
| **Opponent box scores** | georgiadogs.com, kuathletics.com | **3** | Opponent-side lines + PBP for matchup detail. |
| **SABR "PING Ratings"** | sabr.org | **3** | Methodology reference for a regression-based alternative rating (no live 2026 value). |

**Net:** the project leaned on official cume + ESPN + NCAA + WarrenNolan RPI + BA/Wikipedia. It **never used** opponent-adjusted ratings (ELO/ISR/Massey), betting markets, the game log, play-by-play, draft data, or local development reporting. Those are the richest untapped veins.

---

## 2. New datasets discovered / computed this sprint

- **Opponent-adjusted ratings:** ELO #4 (1722.75, postseason); pseudo-RPI #18 (pre-tourney); NCAA RPI #24; WarrenNolan RPI #9 (current). *Four different "how good is OU" numbers — the project used only two.*
- **Betting futures progression [CONFIRMED]:** season open **+6600** → regionals **+15000 (150/1)** → entering Omaha **+1400–1800 (~5–7%, 7th of 8 teams)** → after 2–0 **+275** → Finals **+142**. OU was an **underdog in every postseason series** and *never* a favorite.
- **One-run record: 6–4** (.600); **extra-inning: 3–1** (Vandy 13-11, A&M 12-11, GT 8-7/10; loss Texas 3-4/10). *Found from the game log — not abnormally lucky.*
- **Roster churn:** 9 transfers in, ~12 out, 5 pitchers drafted. Most impactful add = **Deiten Lachance (JUCO, McLennan CC)**. Transfer arms Rerick (ex-Texas), Bixby (ex-TCU).
- **Computed quick-wins (this sprint, from existing CSVs):**
  - **Pythagorean:** expected ~40–41 wins vs **42 actual → +1.2 to +1.9 luck**, i.e., essentially none.
  - **K% ≈ 22.3%, BB% ≈ 12.5%** (BB/K 0.56) — previously reported only as raw totals.
  - **Bullpen vs. starter split:** relievers **4.76 ERA** (K/9 9.6) vs. starters **5.04 ERA** (K/9 11.0) — the bullpen was *better*, contradicting any "shaky bullpen" assumption. *(Rough role-bucketing; swing arms split by primary role.)*

---

## 3. Contradictions & corrections discovered (the project is WRONG or shaky here)

1. **"Key lineup changes sparked the turnaround" is OVERSTATED.** The *only* documented lineup change is **Dayton Tockey re-inserted at the 8-hole** for the regular-season finale and kept there. No other batting-order moves are sourced. → **Soften Phase 8; the surge was "same core got hot," not a reshuffle.**
2. **Lachance's power breakout has NO documented mechanical/swing change.** He attributes it to a mid-season **mental "refresh / time off"** ("I was looking for myself for the first 31 games"). The report implies a transformation; the honest finding is *undocumented mechanically.*
3. **The one genuinely documented coaching adjustment is on the mound, and it's underused:** Skip Johnson raised **Cord Rager's arm slot** ("take his hand away from his head a little bit to free him up"). Rager also pitched through a **midseason lat injury.** → **This is the strongest "coaching changed outcomes" evidence and deserves promotion.**
4. **Home-run figures don't reconcile across sources.** Official season total **93** (incl. Finals G1) vs. "**91 regular-season HR**" vs. "**43 of 91 in the last 16 games**" vs. "**26 HR in 10 tournament games**." These mix timestamps and denominators. → **Pick one CONFIRMED spine (93 total; 26 in 10 NCAA-tourney games) and reconcile the rest explicitly.**
5. **The "2022 Ole Miss = statistical twin (14-16 SEC)" claim needs verification.** A source cites Ole Miss at **7-14 SEC in early May**; the *final* SEC record may not be exactly 14-16. The broader profile match (unseeded, power, shaky ERA) holds, but **verify the exact conference record before calling it identical.**
6. **The best opponent-adjusted rating favors OU's opponent.** ELO ranks **UNC #2 ahead of OU #4.** The project's optimism should acknowledge that the most defensible computer rating sees UNC as the stronger team.
7. **"Unseeded deep run" is far less shocking than implied.** **12 of 18 champions since 2004 were NOT nationally seeded.** Unseeded deep runs are the *norm* in this high-variance format. The genuine outlier is the **sub-.500 conference record**, not the lack of a seed. → **Re-anchor the "surprise" thesis on conference record + betting odds, not on "unseeded."**
8. **"National seed" is a moving target:** top-8 (1999–2017), top-16 (2018–2025), reportedly **top-32 in 2026.** Cross-era seed comparisons are muddy and should be caveated.
9. Minor: regular-season record cited as both **32-20 and 32-21**.

---

## 4. Weak assumptions discovered (methodology)

1. **Survivorship bias (biggest).** The champion comparison uses *winners only*. That answers "how does OU compare to teams that won," not "how likely is OU to win." Without **finalists, runners-up, and a tournament-field baseline**, the similarity model and the Ole Miss "closest match" risk over-reading n=1.
2. **The 55/35/10 "strength/streak/matchup" verdict is unfalsifiable** — an analyst's subjective weighting presented with decimal precision. Either ground it in a model or label it explicitly as a prior.
3. **Power-surge magnitude was ESTIMATED** ("~doubled," from "25% of HR in the tournament"). The firmer figure is **26 HR in 10 NCAA-tourney games**; lead with sourced numbers, demote the estimate.
4. **"Clutch" is treated as a skill.** In baseball, clutch/one-run performance is largely **non-predictive noise.** OU's 6-4 one-run record supports "not lucky," but the narrative "clutch wins" should be framed as *variance OU survived*, not a repeatable trait.
5. **Opponent quality rests on partly-refuted records.** Specific opponent RPI/records were excluded in verification; the matchup analysis leans on REPORTED opponent stats.
6. **Apples-to-oranges samples:** OU's line includes Finals G1 (64 g) while champions are full-season; HR/era confounding spans the comparison window.
7. **Luck was asserted, never tested.** The project hedged ("partly variance-driven") without computing Pythagorean, one-run, or BaseRuns. The luck test (now run) says **season = not lucky; postseason = genuine dominance (+6.4 avg margin), with normal one-run variance.**

---

## 5. Missing analyses discovered (Tracks 2–4, 9)

**Calculable now from data already in the repo (low effort):**
- ✅ Pythagorean / luck (done above) · ✅ K%/BB% (done) · ✅ bullpen-vs-starter ERA (done)
- Monthly W-L + monthly HR/run splits (quantify May collapse → June surge) — from the game log.
- One-run / extra-inning / blowout records (found: 6-4, 3-1) — integrate.
- ISO already derivable; add to player tables.

**Obtainable with moderate effort (new data pull):**
- Opponent-adjusted offense/pitching: compare OU's .292/.234 to **SEC and national averages**; integrate ELO/ISR/Massey. (Track 3 — currently *entirely absent*.)
- BaseRuns / run-expectancy-lite using team totals.
- Betting-market-implied win probabilities per game vs. actual (calibration).

**Obtainable only via play-by-play parsing (high effort):**
- RISP AVG, two-out RBI, bases-loaded, leadoff splits (StatBroadcast PBP).
- Inning-by-inning, first-inning, late-inning scoring; comeback wins; WPA approximations.

**Genuinely impossible / not public (confirmed — do not attempt):**
- Exit velocity / launch angle / hard-hit% (no public Statcast for college).
- vs-LHB/RHB splits; inherited-runners-stranded (not published; PBP doesn't reliably tag handedness).
- True wOBA/FIP/xFIP (no public component inputs).

---

## 6. Most valuable next analyses (ranked by insight ÷ effort)

| # | Analysis | Expected insight | Effort | Priority |
|---|---|---|---|---|
| 1 | **Game-log layer** (monthly splits, one-run/XI, comeback, Pythagorean) | Quantifies the collapse→surge inflection and kills/confirms the luck debate | Low | **P0** |
| 2 | **Opponent adjustment** (ELO/ISR/Massey + SEC/national baselines) | "How good was OU *really*" — the project's single biggest hole | Low–Med | **P0** |
| 3 | **Betting-market surprise module** | Hard numbers for the underdog thesis (150/1 → finals dog) | Low | **P0** |
| 4 | **Fix survivorship bias** — add finalists + field baseline | Makes the champion comparison valid; reframes the Ole Miss match | Med | **P1** |
| 5 | **Real championship-probability model** (logistic w/ negative class) | Replaces the "can't do probability" punt with an actual estimate | Med | **P1** |
| 6 | **PCA + clustering champion taxonomy** | Data-driven "archetypes" (power/pitching/balanced); places OU rigorously | Med | **P1** |
| 7 | **Monte Carlo Finals/tournament sim** | Series win prob from run distributions; honest variance bounds | Med | **P2** |
| 8 | **PBP situational build** (RISP, inning, WPA) | Unlocks ~10 metrics; tests the "clutch" claim properly | High | **P2** |

---

## 7. Highest-ROI future research projects

1. **The "How Good Was OU, Really?" opponent-adjustment study** — the highest-leverage fix; likely *raises* OU's offense (hardest schedule) while confirming its pitching is below champion grade.
2. **The survivorship-corrected champion model** — add ~30 finalists + a 50-team tournament-field sample → first *valid* probability estimate.
3. **The play-by-play situational engine** — one parser unlocks RISP, leverage, inning splits, comeback wins for OU and opponents; reusable for future seasons (portfolio-grade infrastructure).
4. **Betting-market calibration** — compare market-implied probs to model probs across the run; a distinctive, pro-bettor-flavored chapter.

---

## 8. Top 25 ways to improve the project

1. Add the **game log** dataset (all 64 games, H/A, scores).
2. Compute **monthly splits** (Feb–June) to date the collapse→surge.
3. Add **one-run (6-4)** and **extra-inning (3-1)** records.
4. Add **Pythagorean** + luck delta (+1.2 to +1.9).
5. Add **K%/BB%** (22.3% / 12.5%) to team/player tables.
6. Add **bullpen-vs-starter** split (4.76 vs 5.04).
7. Integrate **WarrenNolan ELO** (#4) as an opponent-adjusted rating.
8. Add **Boyd's ISR / Massey** for a multi-rating consensus.
9. Build the **betting-odds time series** module (surprise quantifier).
10. Add **per-game market-implied win probabilities** and calibration.
11. **Fix survivorship bias:** add CWS *finalists/runners-up* to the comparison DB.
12. Add a **tournament-field baseline** (50+ regular tournament teams).
13. Build a **logistic championship-probability model** with a negative class.
14. Run **PCA** on the team-stat matrix; plot OU in champion space.
15. Run **k-means/hierarchical clustering** → champion archetypes.
16. Build a **Monte Carlo best-of-3 Finals simulation.**
17. **Verify Ole Miss 2022's exact SEC record** before the "twin" claim.
18. **Reconcile the HR figures** (93 vs 91 vs 43 vs 26) into one sourced spine.
19. **Promote the Rager arm-slot change** as the documented coaching lever; **soften "lineup changes."**
20. State Lachance's breakout as a **mental "refresh," mechanically undocumented.**
21. Add the **roster-churn / draft context** (both Witherspoons, 5 drafted arms, JUCO Lachance).
22. Replace/annotate the **55/35/10 verdict** as a labeled subjective prior or model output.
23. **Opponent-adjust** OU's slash line vs SEC/national averages.
24. Add **falsifiable, tracked predictions** with a results ledger (already partly present — formalize).
25. Add a **"national-seed definition by era" footnote** and re-anchor "surprise" on conference record + odds, not "unseeded."

---

## 9. What would elevate this from excellent to best-in-class

- **Opponent adjustment everywhere** — no serious analyst trusts raw college slash lines against the #2 schedule; this is table stakes the project skips.
- **A valid probability statement** — replace "we can't" with a real model (negative class + calibration), honestly bounded.
- **A play-by-play situational layer** — turns "NOT AVAILABLE" into computed RISP/leverage and tests the clutch narrative.
- **Market integration** — betting odds as an external, liquid "wisdom of crowds" benchmark for the surprise thesis and for model calibration.
- **Adversarial self-review baked in** — a standing "contradictions log" (this document) maintained alongside the report; surface where the best opponent-adjusted rating (ELO) *disagrees* with OU optimism.
- **Reproducible models, not just charts** — commit the simulation/PCA/logistic code under `scripts/` so every claim is rerunnable (the project's existing `make all` discipline extended to the modeling layer).

---

## 10. Gap report — High / Medium / Low impact

### HIGH-IMPACT GAPS
| Gap | Why it matters | Data required | Difficulty | Expected insight | Next step |
|---|---|---|---|---|---|
| **No opponent adjustment** | Raw stats vs the #2 SOS are misleading; could *raise* OU's offense and confirm pitching weakness | ELO/ISR/Massey + SEC/national averages | Low–Med | A defensible "true talent" estimate | Pull ELO (#4) + Massey; compare slash to SEC avg |
| **Survivorship bias (champions-only)** | Can't infer championship odds from winners alone; Ole Miss "twin" may be n=1 noise | Finalists + tournament-field stats | Med | Valid placement + probability | Extend `champions.csv` with finalists + field flag |
| **No game-log / luck layer** | The central "strength vs hot streak" debate was never tested | 64-game log (found) | Low | Pythagorean (no season luck) + monthly inflection | Build `game_log.csv`; compute splits |
| **No probability model** | The project punts on the headline question | Negative class + features | Med | An actual, bounded title probability | Logistic on champions+field |
| **Betting market ignored** | Best external surprise benchmark unused | Futures + game lines (found) | Low | 150/1 → finals-dog quantification | Add odds module + calibration |

### MEDIUM-IMPACT GAPS
| Gap | Why it matters | Data | Difficulty | Insight | Next step |
|---|---|---|---|---|---|
| **No situational/RISP/leverage** | "Clutch" claims are untested narrative | StatBroadcast PBP | High | Real clutch/leverage profile | Parse PBP → RISP, WPA-lite |
| **No PCA/cluster taxonomy** | Archetype claims are qualitative | champions.csv (have) | Med | Data-driven archetypes | sklearn PCA + k-means |
| **No Monte Carlo sim** | Variance bounds are hand-waved | team run dists | Med | Series/title win prob w/ CI | Simulate best-of-3 |
| **Thin development/coaching evidence** | Causal claims under-sourced | local coverage (found) | Low | Rager arm-slot, Lachance refresh, roster churn | Integrate §3 findings |
| **HR-figure & Ole Miss record conflicts** | Factual integrity | verification | Low | Clean spine | Reconcile + verify |

### LOW-IMPACT GAPS
| Gap | Why it matters | Data | Difficulty | Insight | Next step |
|---|---|---|---|---|---|
| **K%/BB%, ISO, bullpen split** | Completeness | have (computed) | Low | Minor sharpening | Drop into tables |
| **1951/1994 OU title teams** | Program-history depth | archives | Med | Dynasty context | Media-guide dig |
| **vs-L/R, inherited runners, exit velo** | Nice-to-have | not public | Impossible | n/a | Mark unavailable (done) |
| **National-seed-era footnote** | Avoids cross-era error | known | Low | Cleaner framing | One footnote |

---

## Prioritized roadmap

### Next 10 hours (P0 — mostly already-found data; sharpens/changes conclusions)
1. Build `data/game_log.csv` from the WarrenNolan log; add **monthly splits, one-run (6-4), extra-inning (3-1), comeback wins, blowout record.** (3h)
2. Add **Pythagorean (+1.2/+1.9), K%/BB% (22.3/12.5), bullpen-vs-starter (4.76/5.04)** to the datasets + report. (1h)
3. Add **opponent-adjusted ratings** (ELO #4, ISR #18, Massey, NCAA RPI #24) as a `data/ratings.csv`; write the "how good was OU really" subsection. (3h)
4. Add the **betting-odds time series** + per-game implied probabilities; write the surprise module. (2h)
5. Reconcile the **HR figures** and **verify Ole Miss 2022 SEC record**; correct the **"lineup changes"** and **Lachance** claims; promote **Rager arm-slot**. (1h)

### Next 25 hours (P1 — fixes the methodology)
6. Extend the champion DB with **CWS finalists/runners-up + a 50-team tournament-field sample** (negative class). (8h)
7. Build a **logistic championship-probability model** with calibration; report OU's honest title probability. (6h)
8. **PCA + k-means** champion-archetype taxonomy; place OU rigorously; replace qualitative archetype talk. (5h)
9. **Monte Carlo** best-of-3 Finals + full-bracket sim from run distributions. (4h)
10. Integrate **development/coaching** findings (§3) with quotes; add roster-churn/draft context. (2h)

### Next 50 hours (P2 — best-in-class infrastructure)
11. Build the **play-by-play parser** (StatBroadcast/NCAA) → RISP, two-out, inning-by-inning, late-inning, comeback, **WPA-lite** for OU *and* opponents. (20h)
12. Build a **college run-expectancy table** to power leverage/WPA. (6h)
13. **Opponent-adjust at the game level** (each OU game vs that opponent's season rates) → schedule-adjusted offense/defense. (8h)
14. **Betting calibration study** (market vs model across the run) + a written methodology appendix. (4h)
15. Extend the **luck/variance battery** (BaseRuns, cluster-luck, sequencing) and a sensitivity analysis on every headline claim. (6h)
16. Formalize a **predictions ledger** and a standing **contradictions log** (maintain this document). (6h)

---

### Bottom line
The project is a strong *report*. To become the **definitive analytical record**, it needs to stop trusting raw numbers (opponent-adjust), stop comparing only to winners (fix survivorship), and start computing the game-flow layer it currently asserts around (game log + PBP). The good news: **the three P0 items are mostly data already found in this sprint**, and the first computations (Pythagorean, one-run record, bullpen split) **already tighten the central verdict** — OU was *not* a season-level fluke; it was an underrated, schedule-masked team whose postseason power surge was real, against a market that never believed it.
