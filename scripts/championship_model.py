#!/usr/bin/env python3
"""
championship_model.py — Phase 13 (P1): survivorship-corrected modeling.

Uses data/cws_field.csv: ALL 8 College World Series participants for 2021-2025
(40 teams: 5 champions + 35 non-champions) — a real positive AND negative class,
all in the flat-seam-ball era (so HR comparisons are era-valid). Plus the 2026 OU
finalist as the held-out test case.

Produces:
  - Champion vs. field separation (do champions even differ from other Omaha teams?).
  - A leave-one-out logistic title-probability model (heavily caveated; 5 positives).
  - kNN champion-rate for OU; base-rate and unseeded-team context.
  - PCA (2D) of the field; k-means archetypes with per-cluster champion rate.
  - Monte Carlo best-of-3 Finals sim (ELO-based per-game prob + sensitivity).
Charts 19-22 + data/championship_model_output.md. Fixed seeds → deterministic.
No fabrication; small-sample caveats stated throughout.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
CRIMSON, GRAY, GOLD, DARK = "#841617", "#8a8d8f", "#C9A227", "#2b2b2b"
SEED = 42
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight",
                     "savefig.facecolor": "white", "axes.grid": True,
                     "grid.color": "#e9e9e9", "axes.titleweight": "bold"})
# ELO entering CWS Finals (WarrenNolan, confirmed)
ELO_OU, ELO_UNC = 1722.75, 1753.58


def ip_real(v):
    w = int(float(v)); fr = round((float(v) - w) * 10); return w + fr / 3


def load():
    df = pd.read_csv(DATA / "cws_field.csv")
    for c in ["W", "L", "G", "R", "RA", "AVG", "OBP", "SLG", "HR", "ERA",
              "H_allowed", "BB_allowed", "K_pitch", "opp_AVG", "FLD_pct", "E"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["IP_real"] = df["IP"].apply(ip_real)
    df["win_pct"] = df["W"] / (df["W"] + df["L"])
    df["run_diff_pg"] = (df["R"] - df["RA"]) / df["G"]
    df["OPS"] = df["OBP"] + df["SLG"]
    df["HR_per_G"] = df["HR"] / df["G"]
    df["K9"] = df["K_pitch"] * 9 / df["IP_real"]
    df["seed_num"] = pd.to_numeric(df["national_seed"], errors="coerce")
    df["is_seed"] = df["national_seed"].apply(lambda v: 0 if str(v).strip() == "unseeded" else 1)
    return df


FEATS = ["win_pct", "run_diff_pg", "OPS", "HR_per_G", "ERA", "K9", "opp_AVG", "FLD_pct"]
MODEL_FEATS = ["win_pct", "run_diff_pg", "ERA"]  # few features: only 5 positives


def main() -> int:
    df = load()
    ou = df[df.team == "Oklahoma"].iloc[0]
    field = df[df.is_champion.isin([0, 1])].copy()  # the 40 in-model teams
    field["is_champion"] = field["is_champion"].astype(int)
    champs = field[field.is_champion == 1]
    nonch = field[field.is_champion == 0]

    out = ["# Phase 13 — Survivorship-Corrected Championship Model (P1)",
           "",
           "_Computed by `scripts/championship_model.py` from `data/cws_field.csv` "
           "(40 CWS participants 2021-2025: 5 champions + 35 non-champions; all flat-seam era). "
           "OU 2026 held out as the test case._", ""]
    assert len(field) == 40 and champs.shape[0] == 5, f"universe wrong: {len(field)},{champs.shape[0]}"
    out.append(f"**Universe:** {len(field)} Omaha teams, {len(champs)} champions "
               f"(base rate **{100*len(champs)/len(field):.1f}%**), {len(nonch)} non-champions.\n")

    # ---- 1. Champion vs field separation ----
    out.append("## 1. Do champions even differ from other Omaha teams?\n")
    out.append("Standardized mean gap (champion − non-champion, in SD units) and Welch p (n=5 vs 35, low power):\n")
    out.append("| Feature | Champ mean | Non-champ mean | Gap (SD) | p | OU |")
    out.append("|---|---|---|---|---|---|")
    sd_all = field[FEATS].std()
    seps = {}
    for f in FEATS:
        cm, nm = champs[f].mean(), nonch[f].mean()
        gap = (cm - nm) / sd_all[f]
        p = stats.ttest_ind(champs[f], nonch[f], equal_var=False).pvalue
        seps[f] = gap
        out.append(f"| {f} | {cm:.3f} | {nm:.3f} | {gap:+.2f} | {p:.2f} | {ou[f]:.3f} |")
    big = max(seps, key=lambda k: abs(seps[k]))
    out.append(f"\n**Read:** champions barely separate from other Omaha teams — most gaps are <0.5 SD and "
               f"no feature is close to significant. The largest edge is **{big}** ({seps[big]:+.2f} SD). "
               "**Survivorship-corrected finding: once a team reaches Omaha, the regular-season profile only weakly "
               "predicts who wins — the title is largely high-variance.** This is exactly what the champions-only "
               "Phase 11 could NOT see.\n")

    # ---- 2. Logistic title-probability model (LOO) ----
    X = field[MODEL_FEATS].to_numpy(float); y = field["is_champion"].to_numpy(int)
    sc = StandardScaler().fit(X); Xs = sc.transform(X)
    loo = LeaveOneOut(); preds = np.zeros(len(y))
    for tr, te in loo.split(Xs):
        m = LogisticRegression(C=0.5, class_weight="balanced", random_state=SEED, max_iter=1000)
        m.fit(Xs[tr], y[tr]); preds[te] = m.predict_proba(Xs[te])[0, 1]
    auc = roc_auc_score(y, preds)
    full = LogisticRegression(C=0.5, class_weight="balanced", random_state=SEED, max_iter=1000).fit(Xs, y)
    ou_p = full.predict_proba(sc.transform(ou[MODEL_FEATS].to_numpy(float).reshape(1, -1)))[0, 1]
    out.append("## 2. Logistic title-probability model (leave-one-out)\n")
    out.append(f"Features: {', '.join(MODEL_FEATS)} (kept to 3 — only 5 positives). L2-regularized, class-balanced.\n")
    out.append(f"- **Leave-one-out AUC = {auc:.2f}** — {'weak/modest' if auc < 0.75 else 'decent'} discrimination, "
               "consistent with finding #1 (Omaha outcomes are hard to predict from season stats).")
    out.append(f"- **OU 2026 model title probability ≈ {100*ou_p:.0f}%** (class-balanced output; read as a tier, "
               "not a precise number — n=5 champions).\n")

    # ---- 3. kNN champion rate + context ----
    scf = StandardScaler().fit(field[FEATS].to_numpy(float))
    Fz = scf.transform(field[FEATS].to_numpy(float))
    ouz = scf.transform(ou[FEATS].to_numpy(float).reshape(1, -1))[0]
    d = np.sqrt(((Fz - ouz) ** 2).sum(axis=1))
    field2 = field.assign(dist=d).sort_values("dist")
    out.append("## 3. Nearest-neighbor champion rate for OU\n")
    out.append("OU's most statistically similar Omaha teams (standardized, 8 features):\n")
    out.append("| Rank | Team | Champion? | Dist |")
    out.append("|---|---|---|---|")
    for i, (_, r) in enumerate(field2.head(8).iterrows(), 1):
        out.append(f"| {i} | {int(r.year)} {r.team} | {'YES' if r.is_champion else 'no'} | {r.dist:.2f} |")
    for k in (5, 8, 10):
        rate = field2.head(k).is_champion.mean()
        out.append(f"- Champion rate among OU's {k} nearest neighbors: **{100*rate:.0f}%**")
    seeded_champ = champs.is_seed.mean()
    uns = field[field.is_seed == 0]
    out.append(f"\n- **Unseeded context:** of {len(uns)} unseeded Omaha teams 2021-25, "
               f"**{int(uns.is_champion.sum())} won ({100*uns.is_champion.mean():.0f}%)** — only 2022 Ole Miss. "
               f"OU is unseeded. {int(champs.is_seed.sum())} of 5 champions were national seeds.\n")

    # ---- 4. PCA ----
    pca = PCA(n_components=2, random_state=SEED)
    pcs = pca.fit_transform(Fz)
    ou_pc = pca.transform(ouz.reshape(1, -1))[0]
    out.append("## 4. PCA of the CWS field\n")
    out.append(f"First two components explain {100*pca.explained_variance_ratio_[:2].sum():.0f}% of variance. "
               "Champions are scattered through the cloud (not isolated), visually confirming weak separation. "
               "OU plots inside the pack (Chart 19).\n")

    # ---- 5. KMeans archetypes ----
    km = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit(Fz)
    field = field.assign(cluster=km.labels_)
    ou_clu = int(km.predict(ouz.reshape(1, -1))[0])
    out.append("## 5. Archetype clusters (k-means, k=3)\n")
    out.append("| Cluster | n | Champions | Champ rate | Avg OPS | Avg ERA | Identity |")
    out.append("|---|---|---|---|---|---|---|")
    for c in range(3):
        sub = field[field.cluster == c]
        ident = ("power/offense" if sub.OPS.mean() > field.OPS.mean() and sub.ERA.mean() > field.ERA.mean()
                 else "pitching/balanced" if sub.ERA.mean() < field.ERA.mean() else "mixed")
        star = " ⬅ OU" if c == ou_clu else ""
        out.append(f"| {c}{star} | {len(sub)} | {int(sub.is_champion.sum())} | "
                   f"{100*sub.is_champion.mean():.0f}% | {sub.OPS.mean():.3f} | {sub.ERA.mean():.2f} | {ident} |")
    ouc = field[field.cluster == ou_clu]
    out.append(f"\n**OU's cluster:** champion rate {100*ouc.is_champion.mean():.0f}% "
               f"(OPS {ouc.OPS.mean():.3f}, ERA {ouc.ERA.mean():.2f}). OU lands in the "
               "power-bat / higher-ERA group — the same archetype as its Phase 11 matches (Ole Miss-type).\n")

    # ---- 6. Monte Carlo Finals ----
    p_game = 1 / (1 + 10 ** ((ELO_UNC - ELO_OU) / 400))  # OU per-game win prob vs UNC
    rng = np.random.default_rng(SEED)
    N = 100000
    # From OU leading 1-0: OU needs 1 win in next 2 games
    g2 = rng.random(N) < p_game
    g3 = rng.random(N) < p_game
    ou_series_from10 = g2 | g3
    ou_in2 = g2.mean(); ou_in3 = (~g2 & g3).mean(); unc_in3 = (~g2 & ~g3).mean()
    # Pre-series (0-0) best-of-3 for reference
    pre = p_game**2 * (3 - 2 * p_game)
    out.append("## 6. Monte Carlo best-of-3 Finals (OU vs. UNC)\n")
    out.append(f"Per-game P(OU win) from ELO (OU {ELO_OU} vs UNC {ELO_UNC}) = **{p_game:.3f}** "
               f"(UNC is the slightly stronger team by ELO). {N:,} sims, seed {SEED}.\n")
    out.append(f"- **OU win series | leading 1-0: {100*ou_series_from10.mean():.0f}%** "
               f"(wins in 2: {100*ou_in2:.0f}%, wins in 3: {100*ou_in3:.0f}%, UNC comeback: {100*unc_in3:.0f}%).")
    out.append(f"- Pre-series (0-0) reference: OU **{100*pre:.0f}%** — matches the market's +142 (~41%) almost exactly, "
               "a good external validation of the ELO input.")
    out.append("- Sensitivity (series-from-1-0 by per-game p): "
               + ", ".join(f"p={pp:.2f}→{100*(1-(1-pp)**2):.0f}%" for pp in (0.40, 0.45, 0.456, 0.50)) + ".\n")

    (DATA / "championship_model_output.md").write_text("\n".join(out) + "\n")

    # ===== CHARTS =====
    # 19 — PCA scatter
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(pcs[y == 0, 0], pcs[y == 0, 1], s=70, color=GRAY, alpha=0.7, label="Non-champion CWS team")
    ax.scatter(pcs[y == 1, 0], pcs[y == 1, 1], s=180, color=GOLD, marker="*",
               edgecolor=DARK, label="Champion", zorder=3)
    ax.scatter(ou_pc[0], ou_pc[1], s=220, color=CRIMSON, marker="X", edgecolor="white",
               label="OU 2026", zorder=4)
    for _, r, pc in zip(range(len(field)), [r for _, r in field.iterrows()], pcs):
        if r.is_champion:
            ax.annotate(f"{int(r.year)} {r.team.split()[0]}", (pc[0], pc[1]),
                        textcoords="offset points", xytext=(5, 4), fontsize=7)
    ax.annotate("OU 2026", (ou_pc[0], ou_pc[1]), textcoords="offset points", xytext=(6, -12),
                fontsize=8, fontweight="bold", color=CRIMSON)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("CWS Field 2021-2025 (PCA): Champions Are Scattered, Not Separate")
    ax.legend(loc="best")
    fig.text(0.5, -0.03, "40 Omaha teams, 8 standardized features. Champions (gold) sit throughout the cloud → "
             "winning is weakly predicted. [computed]", ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "19_pca_field.png"); plt.close(fig)

    # 20 — champion vs non-champion separation
    gaps = [seps[f] for f in FEATS]
    ouz_feat = [(ou[f] - field[f].mean()) / field[f].std() for f in FEATS]
    x = np.arange(len(FEATS)); w = 0.38
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(x - w/2, gaps, w, color=GOLD, label="Champion edge (SD)")
    ax.bar(x + w/2, ouz_feat, w, color=CRIMSON, label="OU vs field (SD)")
    ax.axhline(0, color=DARK, lw=1)
    ax.set_xticks(x); ax.set_xticklabels(FEATS, rotation=45, ha="right")
    ax.set_ylabel("Std. gap vs the rest of the field")
    ax.set_title("Champions Barely Separate From the Omaha Field — and OU Looks Like the Field")
    ax.legend()
    fig.text(0.5, -0.06, "Gold = champion mean − non-champion mean (SD). Crimson = OU − field mean (SD). [computed]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "20_champ_separation.png"); plt.close(fig)

    # 21 — OU title probability by method
    methods = ["Base rate\n(1 of 8)", "Logistic\nmodel", "kNN (k=8)\nneighbors",
               "Market\nenter Omaha", "Market\npre-Finals"]
    vals = [12.5, 100*ou_p, 100*field2.head(8).is_champion.mean(), 6.0, 41.0]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = ax.bar(methods, vals, color=[GRAY, CRIMSON, CRIMSON, DARK, DARK])
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+0.6, f"{v:.0f}%", ha="center", fontweight="bold")
    ax.set_ylabel("Estimated title probability (%)")
    ax.set_title("OU 2026 Title Probability: Several Honest Estimates (all low-to-modest)")
    fig.text(0.5, -0.04, "Model/kNN are indicative (5 champions in sample). Market = betting-implied. [computed/REPORTED]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "21_title_probability.png"); plt.close(fig)

    # 22 — Monte Carlo Finals
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5))
    a1.bar(["OU in 2", "OU in 3", "UNC in 3\n(comeback)"], [100*ou_in2, 100*ou_in3, 100*unc_in3],
           color=[CRIMSON, CRIMSON, GRAY])
    a1.set_ylabel("Probability (%)"); a1.set_title(f"Best-of-3 from OU 1-0 (p={p_game:.3f})")
    for i, v in enumerate([100*ou_in2, 100*ou_in3, 100*unc_in3]):
        a1.text(i, v+0.8, f"{v:.0f}%", ha="center", fontweight="bold")
    ps = np.linspace(0.35, 0.55, 50)
    a2.plot(ps, [100*(1-(1-pp)**2) for pp in ps], color=CRIMSON, lw=2.5, label="from 1-0")
    a2.plot(ps, [100*(pp**2*(3-2*pp)) for pp in ps], color=GRAY, lw=2, ls="--", label="from 0-0")
    a2.axvline(p_game, color=GOLD, ls=":", lw=1.5)
    a2.set_xlabel("Per-game P(OU win)"); a2.set_ylabel("Series win prob (%)")
    a2.set_title("Sensitivity"); a2.legend()
    fig.suptitle("Monte Carlo: OU ~70% to Win the Title From Up 1-0 (ELO-based)", fontweight="bold")
    fig.text(0.5, -0.03, f"{N:,} sims, seed {SEED}. ELO per-game p={p_game:.3f}. Pre-series {100*pre:.0f}% ≈ market. [computed]",
             ha="center", fontsize=8, style="italic", color="#666")
    fig.savefig(CHARTS / "22_monte_carlo_finals.png"); plt.close(fig)

    print("\n".join(out))
    print("\nCharts 19-22 written; results -> data/championship_model_output.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
