# P0 Audit Additions — Game Log, Luck Tests, Ratings & Market

_Computed by `scripts/gamelog_market_analysis.py`. Totals reconcile to 42-22._

**Reconciliation:** 42-22, 454 RF / 342 RA — matches official totals. ✓

## Monthly splits — the collapse → surge, quantified

| Month | W-L | RF | RA | Run diff | RA/G |
|---|---|---|---|---|---|
| Feb | 10-1 | 131 | 36 | +95 | 3.3 |
| Mar | 10-7 | 72 | 80 | -8 | 4.7 |
| Apr | 9-6 | 87 | 88 | -1 | 5.9 |
| May | 6-8 | 102 | 118 | -16 | 8.4 |
| Jun | 7-0 | 62 | 20 | +42 | 2.9 |

**Read:** Feb 10-1 hot start → Mar/Apr ~.500 → **May collapse (6-8, RA/G 8.4)** → **June surge (7-0, RA/G 2.9)**. The June turnaround is as much a *run-prevention* story (8.4 → 2.9 RA/G) as an offensive one — a correction to the 'offense-only transformation' framing.

## Luck / variance signals

- **One-run games: 11-3** (.786). A .786 one-run record IS a variance/clutch marker — one-run records are largely non-predictive in baseball. **This corrects the audit's earlier 6-4 (that was a subset).**
- **Extra-inning: 3-1** [REPORTED, recap-verified]: W Texas A&M 12-11 (3/15), Vanderbilt 13-11 (4/10), Georgia Tech 8-7 (6/1, 10); L Texas 3-4 (3/27, 10).
- **Blowouts (margin ≥5): 20-11.** OU was a high-variance team — many lopsided games both ways, which is why the strong one-run record coexists with only a small Pythagorean overperformance.

## Pythagorean expectation (luck test)

| Exponent | Pyth win% | Expected W | Actual W | Luck (W − exp) |
|---|---|---|---|---|
| 2.0 | 0.638 | 40.8 | 42 | +1.2 |
| 1.83 | 0.627 | 40.1 | 42 | +1.9 |

**Read:** by total run differential OU was **essentially NOT lucky** (+1–2 wins). The variance lived in *close games* (11-3 one-run), offset by blowout losses — net Pythagorean luck is small.

## Plate-discipline rates (were missing)

- Approx PA = 2466.0 (AB 2106 + BB 309 + HBP 51; SF/SH omitted). **K% ≈ 22.3%, BB% ≈ 12.5%, BB/K = 0.56.** [ESTIMATED]

## Bullpen vs. starter split (was 'NOT FOUND' — calculable)

| Bucket | IP | ERA | K/9 | BB/9 | n |
|---|---|---|---|---|---|
| Reliever | 223.0 | 4.76 | 9.6 | 5.1 | 9 |
| Starter | 291.3 | 5.04 | 11.0 | 3.9 | 5 |

**Read:** the **bullpen (4.76 ERA) was slightly BETTER than the rotation (5.04)** — refutes any 'shaky bullpen' assumption. (Rough role-bucketing; swing arms split by primary role.) [ESTIMATED]

## How good was OU *really*? (opponent-adjusted)

Raw record (.656) and NCAA RPI (#24) understate OU because they don't fully reward the **#2 strength of schedule**. Opponent-adjusted systems disagree sharply with the seed:

| System | OU rank | UNC rank | Note |
|---|---|---|---|
| NCAA RPI | 24 | 5 | OU was an unseeded at-large (selection-day RPI ~24); UNC was the No. 5 national seed. Official NCAA RPI value not published per-team. |
| WarrenNolan RPI | 9 | 2 | Live page now shows OU #9 / UNC #2 (UNC SOS rank 9). OU figure inflated vs selection-day #24 by the postseason run. |
| WarrenNolan ELO | 6 | 2 | Post-G2 snapshot: Georgia 1781.59 #1, UNC 1768.16 #2, Georgia Tech 1742.41 #3, UCLA 1720.42 #4, Texas 1710.79 #5, OU 1708.16 #6. Pre-finals frozen values were UNC 1753.58 #2 / OU 1722.75 #4. UNC ranks ABOVE OU. |
| Boyd's World pseudo-RPI | 18 | NF | Frozen pre-tournament baseline; does not reflect the run. UNC pseudo-RPI value not captured. |
| Boyd's World ISR | NF | NF | Value blocked to scrapers; pre-tournament snapshot. Neither team's ISR captured. |
| Massey Ratings | NF | NF | BLOCKED: masseyratings.com returns HTTP 403 to fetch tools; exact OU/UNC values need manual browser lookup. |
| KPI / NET-equivalent | NF | NF | No published KPI/NET-equivalent for D1 baseball located; baseball has no NET. NOT_FOUND. |
| D1Baseball Top 25 | UR | 4 | Final pre-tournament poll: UNC #4 (45-11), OU unranked. Top 5: UCLA, Georgia Tech, Georgia, UNC, Auburn. A Wikipedia variant lists a different D1B top-5; see contradictions_log. Polls pause during the tournament until a final post-CWS poll. |
| Baseball America Top 25 | 19 | 7 | Final regular-season BA poll: UNC #7, OU #19. Top 5: UCLA, Georgia Tech, UNC, Georgia, Texas. |
| USA Today Coaches Poll | UR | 4 | Final regular-season Coaches poll: UNC #4, OU unranked. Top 5: UCLA, Georgia Tech, UNC, Texas, Auburn. |
| NCBWA Top 30 | UR | 3 | Final regular-season NCBWA poll: UNC #3, OU unranked. Top 5: UCLA, Georgia Tech, UNC, Georgia, Texas. |
| Perfect Game Top 25 | UR | 2 | Final regular-season PG poll: UNC #2, OU unranked. Top 5: UCLA, UNC, Georgia Tech, Georgia, Texas. |
| ESPN | NF | NF | ESPN re-publishes the D1Baseball/Coaches polls rather than an independent baseball power index; no standalone ESPN baseball rating located. See D1Baseball/Coaches rows. |
| WarrenNolan SOS | 2 | 9 | OU hardest-schedule context (SOS #2); UNC SOS rank 9. UNC SOS value not captured. |

**Read:** opponent adjustment *raises* OU vs its #24 selection RPI (WarrenNolan RPI #9; ELO top-10), **but UNC out-rates OU in every system** — D1Baseball #4, Coaches #4, NCBWA #3, Perfect Game #2, BA #7 (OU unranked/#19), and **post-Game-2 ELO has OU #6 (1708) behind UNC #2 (1768).** Honest synthesis: OU was badly underrated by its *seed*, but the consensus correctly has **UNC as the stronger team** — OU is the underdog entering Game 3.

