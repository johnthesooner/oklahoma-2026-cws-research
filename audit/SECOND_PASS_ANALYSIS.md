# Second-Pass Data Analysis — OU 2026 CWS

_Independent re-analysis of `data/` (15 CSVs). Run 2026-06-21. Every number below is computed by
`/tmp/second_pass.py` → raw log at `audit/second_pass_findings.txt`; nothing hand-entered._

**Scope of this pass:** the existing Phase 11–14 outputs are all *team-level*. This pass adds (A) a
full **cross-file reconciliation/integrity audit** and (B) the **player-level** analysis the pipeline
never did, then flags two documentation inconsistencies not yet in `contradictions_log.csv`.

**Series status at run time:** Finals tied 1–1. OU won G1 9–3 (6/20), lost G2 2–6 (6/21). Game 3 is
winner-take-all 6/22. No game outcomes were invented; G3 row remains a placeholder.

---

## 0. Integrity baseline (verified, not asserted)

| Check | Result |
|---|---|
| `scripts/validate_data.py` | ✅ PASS — 15 datasets, 0 warnings |
| Build determinism | ✅ two consecutive `build_report_assets.py` runs → **byte-identical** manifest |
| Earlier chart-22 byte change | Explained: committed asset was stale vs. uncommitted Phase 12–14 code, **not** nondeterminism |

---

## A. Cross-file reconciliation — all green except two flags

| # | Check | Result |
|---|---|---|
| A1 | `game_log` → record/runs | **42–22, RF 454, RA 342** — exact match to `team_batting`, `champions`, `cws_field` |
| A3 | Player tables → team totals | HR 92/93 · SB 131/132 · SB_att 155/156 · **W 41/42** · **SV 16/16 exact** · IP 514/550 — residuals = sub‑threshold arms (min ~12 IP) ✓ |
| A4 | Mirror checks | OU hits 615 == opp H‑allowed 615; OU HR 93 == opp HR‑allowed 93; opp hits 477 == OU H‑allowed 477 ✓ |
| A5 | `postseason_games` ↔ `game_log` | All 12 played games: scores & results reconcile. **2 date mismatches (flag F2)** |
| A6 | `champions` ↔ `cws_field` | All 5 in‑scope champions (2021–25) match exactly on W/HR/AVG/ERA. (2000–20 absent from `cws_field` by design — 2021–25 only) ✓ |

The **W 41/42** residual is meaningful: it corroborates the "Aoki 8.0IP CG" starter logged in
`postseason_games` G10 (vs Georgia, 6/15) who has **no row in `pitchers.csv`** (below the ~12‑IP cut).
`team_pitching_fielding` shows exactly **1 complete game** all season — internally consistent.

---

## B. Player-level findings (net-new)

### B1. Hitters
- **OPS column integrity:** stored `OPS == OBP+SLG` for **all 12** hitters → the `ESTIMATED` tag on
  that derived column is honest and exact.
- **A genuinely deep lineup:** **6 of 12 regulars carry OPS ≥ .900.** Stars are
  **Deiten Lachance** (C, 1.039, 18 HR — power from the catcher spot) and **Dasan Harris**
  (.370/1.028). Top ISO: **Tockey .313, Lachance .293, Gambill .238**.
- **The lineup's real engine is OBP + the run game, not contact:** **zero** hitters have BB > SO —
  a high-K profile (team K% ≈ 22.3%). It plays because of **plate patience** (Gambill .433 OBP,
  best BB/K 0.87) and **aggressive, efficient base-stealing: 131/155 = 84.5%** in the table, with
  four 17+ steal threats (C. Johnson 30, Brock 28, Harris 18, Walk 18).
- **Reframe:** the team narrative is "power surge," but the player data shows a **3-true-outcomes +
  speed** club — walks and steals manufacture the OBP that the HR then cashes.

### B2. Pitchers
- **Ace = a freshman.** **Cord Rager** (FR): 76 IP, **4.95 K/BB, 0.95 WHIP, .215 opp AVG** — far and
  away the staff's most reliable starter despite a deceptive 4.74 ERA.
- **Staff identity = miss-bats-and-walk-bats.** 10.4 K/9 (champion-caliber) paired with 4.5 BB/9
  (well above champion norm) — exactly the K9-strength / BB9-weakness the Phase-13 model flagged.
- **Control outliers:** Cameron Johnson (7.21 BB/9 yet .205 opp AVG — wild but unhittable),
  Reid Hensley (9.00 BB/9, 2.33 WHIP, small sample) drag the walk rate.
- **Bullpen ≥ rotation, reproduced from raw rows:** Reliever **4.76 ERA** (223.0 IP, n=9) vs Starter
  **5.04** (291.3 IP, n=5) — independently confirms the Phase-12 claim from `pitchers.csv` role
  buckets, not just the team file.

---

## C. Data-quality flags (NOT in `contradictions_log.csv`)

**F1 — Label contradiction on the 64-game cumulative.**
`team_batting.csv` "Games" note reads *"through CWS semifinal; Finals NOT included."* But the data
say otherwise: `game_log` game 64 is the **6/20 Finals G1 win (9–3)**, the 64-game RF sums to **454 ==
team Runs**, and both `champions.csv` and `cws_field.csv` label the identical line *"thru Finals G1."*
**The cumulative includes Finals G1; the `team_batting` note is wrong.** Numbers are fine — it's a
documentation error, but a confusing one for a provenance-first project. _Severity: low; fix the note._

**F2 — Kansas Super Regional dates disagree across files.**
`postseason_games` dates the two Kansas wins **6/06 & 6/08**; `game_log` dates both **6/07**. Scores
and results match (8–1, 13–2). One ledger is wrong on dates. _Severity: low; reconcile to the box-score
dates._

(One traceability nit: the only CG of the season is credited to "Aoki" in `postseason_games`, a name
that appears in no other file. Consistent with the 41/42 win residual, but untraceable elsewhere.)

---

## D. Repo state (flagged per commit-discipline standard)

A large block of finished work is **uncommitted**: `p2_advanced.py`, `predictions_ledger.csv`,
`opponents_2026.csv`, `contradictions_log.csv`, charts 23–25, plus modified scripts/report. The
analysis is done and deterministic — it just isn't on the remote. Recommend a commit + push.

---

## Bottom line
The dataset is in strong shape: validator clean, build deterministic, and **every cross-file total
reconciles**. The two flags (F1, F2) are documentation/date nits, not data errors. The net-new
**player-level read** sharpens the team story: OU is a **patient, base-stealing, high-K lineup** fronted
by a **freshman ace** and a **bullpen that out-pitched its rotation** — a good-not-great profile whose
postseason power surge, not its season-long identity, carried it to Omaha.
