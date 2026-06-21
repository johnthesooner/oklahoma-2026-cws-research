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

| System | OU rank | Note |
|---|---|---|
| NCAA RPI | 24 | Selection-day figure that left OU unseeded |
| WarrenNolan RPI | 9 | Inflated by the postseason run (different timestamp than #24) |
| WarrenNolan ELO | 4 | Top5 Georgia 1781.59 / UNC 1753.58 / Georgia Tech 1742.41 / OU 1722.75 / UCLA 1720.42 - UNC ranks ABOVE OU |
| Boyd's World pseudo-RPI | 18 | Frozen pre-tournament baseline (does not reflect the run) |
| Boyd's World ISR | NF | Value blocked to scrapers; pre-tournament snapshot |
| Massey Ratings | NF | Opponent-adjusted with off/def split; exact OU value needs manual lookup (403 to scrapers) |
| WarrenNolan SOS | 2 | Hardest-schedule context - 2nd nationally |

**Read:** the postseason-updated, opponent-adjusted **ELO ranks OU #4 nationally** — a far cry from its #24 selection RPI — but **still behind finals opponent UNC (#2)**. So opponent adjustment *raises* OU materially, yet does NOT make it the favorite. Honest synthesis: a top-5-caliber team that the seed badly underrated, not a dominant #1.

