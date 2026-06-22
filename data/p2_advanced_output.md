# Phase 14 — P2 Advanced: Opponent Adjustment, Luck, Market Calibration, Innings

_Computed by `scripts/p2_advanced.py`. The full PBP/WPA engine is NOT built (public college play-by-play is JS-rendered / blocked) — flagged, not fabricated._

## 1. Opponent-adjusted: OU by opponent quality tier

14 of OU's 27 distinct opponents made the 2026 NCAA Tournament (9 national seeds).

| Tier | Games | OU W-L | OU R/G | Opp R/G | Run diff/G | Avg opp win% |
|---|---|---|---|---|---|---|
| 1. National seed | 24 | 13-11 | 6.1 | 6.2 | -0.1 | 0.724 |
| 2. NCAA (regional) | 12 | 6-6 | 7.6 | 7.9 | -0.3 | 0.633 |
| 3. Non-NCAA .500+ | 16 | 11-5 | 5.9 | 4.4 | +1.6 | 0.577 |
| 4. Sub-.500 | 12 | 12-0 | 10.2 | 2.3 | +7.8 | 0.385 |

**vs. 2026 NCAA Tournament teams overall: 19-17** (-0.2 run diff/G). Games-weighted average opponent win% = **0.607** (a brutal slate). OU crushed the cupcakes (Feb) but was merely solid, not dominant, vs the tournament field — consistent with a good-not-great team that the schedule both toughened and flattered.

## 2. Game-level opponent adjustment (official opponent rates only)

Over 19 games vs. opponents with **official** scoring rates (estimated-rate opponents excluded to avoid inflation):
- **Offense: +0.52 runs/game vs. what those defenses normally allow** (OU scored 6.4/G; those opponents allowed 5.8/G on average).
- **Defense: +2.81 runs/game vs. what those offenses normally score** (OU allowed 4.9/G; those opponents scored 7.8/G on average).
- ⚠ **Caveat:** this naive adjustment is fragile — opponents' *season* R/g rates are themselves inflated by their own cupcake games, so the +2.8 'defense above expectation' is overstated. The **robust** opponent-adjusted result is the head-to-head **tier table above: vs the NCAA field OU was 19-17, −0.2 run diff/G** — a good-not-elite team against quality, whose +112 overall margin came mostly from a 12-0 demolition of sub-.500 cupcakes. [ESTIMATED]

## 3. Luck / variance battery

| Test | Result | Read |
|---|---|---|
| Pythagorean (exp 1.83) | exp 40.1 W vs 42 actual (+1.9) | ~neutral season luck |
| One-run games | 11-3 (.786) | favorable close-game variance (the real luck) |
| Blowouts (>=5) | 20-11 | high-variance team (offsets Pythagorean) |
| BaseRuns | 396 expected vs 454 actual (+58) | see caveat |

> **BaseRuns caveat:** the formula is MLB-calibrated and **systematically under-predicts the higher college run environment**, so the +58 gap is mostly calibration, NOT clean sequencing luck. The trustworthy luck signals are **Pythagorean (≈neutral)** and the **11-3 one-run record (favorable)** — OU's variance was concentrated in close games, balanced by blowout losses. Verdict: **mild positive luck in close games; not a broadly lucky season.**

## 4. Betting-market calibration (small n — indicative)

OU was an **underdog in all 4 priced postseason games** (implied < 50% each); it went **3-1** in them.

| Game | OU odds | Implied | Result |
|---|---|---|---|
| Super Regional G1 vs Kansas | +130 | 44% | W |
| CWS bracket vs Alabama | +100 | 50% | W |
| CWS Finals G1 vs North Carolina | +134 | 43% | W |
| CWS Finals G2 vs North Carolina | +140 | 42% | L |

- **Brier score 0.268** vs naive-0.5 **0.250** — the market did **worse than a coin flip** on OU because it kept pricing OU as an underdog while OU won 3-1. **The market was biased LOW on Oklahoma throughout the run** — the surprise was persistent, not a one-off. (n=4; directional.) Game 2 (the one loss) is the market's lone 'correct' underdog call.

## 5. Inning distribution (6 postseason games with line scores)

- First-inning runs: **8** over 6 games (1.3/G); OU scored in the 1st in **4 of 6**.
- Early (1-3): **18** (33%) · Middle (4-6): **23** (43%) · Late (7-9): **13** (24%).
- Read: OU was **not purely a late-rally team** — scoring was spread across the game and peaked in the **middle innings**. (6-game sample; full inning data for all 64 games needs PBP, NOT obtained.)

## 6. RE24 / WPA framework — status

A run-expectancy (24 base-out states) engine would power RE24 and per-player WPA. **Per-event base-out data requires play-by-play, which is not publicly obtainable for OU 2026** (StatBroadcast/NCAA PBP is JS-rendered and blocks automated retrieval). The framework is specified for a future build; **no WPA numbers are fabricated here.** Inning-level scoring (above) is the obtainable substitute.

