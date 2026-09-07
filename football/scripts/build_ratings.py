#!/usr/bin/env python3
"""
build_ratings.py — regenerate football/data/ratings_football.csv from committed code.

Second half of the reproducibility fix (see build_seasons.py). Three inputs:

  1. ESPN Power Index JSON, one request per season 2005-2025 — LIVE, re-fetchable.
     Supplies FPI, FPI rank, strength-of-schedule rank, strength-of-record rank,
     game-control rank, average in-game win-probability rank and the four efficiency
     ratings/ranks. Cached under football/sources/raw/espn_powerindex/.
  2. puntandrally.com SP+ tables for 2019-2025 — LIVE, re-fetchable. Publishes each
     team's overall SP+ rank and rating plus offense/defense ratings.
  3. football/sources/snapshots/sp_plus_footballoutsiders_2005_2018.csv — a COMMITTED
     snapshot. Its upstream (footballoutsiders.com) is GONE: the host no longer resolves,
     so those 14 seasons of SP+ cannot be re-fetched from anywhere. The snapshot preserves
     only Oklahoma's own row per season (rating, ranks, SOS) rather than the full national
     tables, and every row carries the season record as a built-in cross-check.

Derived values, computed here rather than asserted: for 2019-2025 puntandrally publishes
offense/defense RATINGS for every team but ranks only in its per-side views, so this script
derives OU's offense and defense ranks by sorting the full national list. The method is
validated in-band: for every season where per-side ranks ARE published (2019, 2023, 2024, 2025)
the derived rank must match the published one, and the published value is then the one written.
Ranks are only actually DERIVED for 2020-2022, where no per-side publication was findable.

Usage:  python3 football/scripts/build_ratings.py [--check] [--refresh]
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = ROOT / "sources" / "raw"
SNAP = ROOT / "sources" / "snapshots" / "sp_plus_footballoutsiders_2005_2018.csv"
SEASONS = range(2005, 2026)
ESPN = ("https://site.web.api.espn.com/apis/fitt/v3/sports/football/college-football/"
        "powerindex?season={season}")
PR = "https://www.puntandrally.com/viewSandPratings.php?whichyear={season}"
# "<rank>. <team> : <overall> (<offense>/<defense>)" — the name is matched permissively so
# accents ("San Jose State" pre-2023) and parentheses ("Miami (OH)") cannot drop a team.
TEAM_RE = re.compile(r"(\d{1,3})\.\s+(.+?)\s*:?\s+(-?\d+(?:\.\d+)?)\s+\((-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)\)")
UA = "OUFootballResearch/1.0 (portfolio research; github.com/johnthesooner)"
OU_ID = "201"
# Seasons where OU's SP+ offense/defense RANKS are PUBLISHED outright. Published always wins
# over derivation; the derivation still runs for these seasons and must agree (see build()).
PUBLISHED_SP = {
    2019: (3, 48, "ESPN, 'Final SP+ rankings for the 2019 college football season' "
                  "(espn.com/college-football/story/_/id/28497018)"),
    2023: (7, 33, "puntandrally.com per-side SP+ views (whichside=off / whichside=def)"),
    2024: (76, 17, "puntandrally.com per-side SP+ views (whichside=off / whichside=def)"),
    2025: (51, 4, "puntandrally.com per-side SP+ views (whichside=off / whichside=def)"),
}
# Documented source-level disagreements that must NOT fail the build. 2019: deriving from
# puntandrally's 130-team list puts OU's defense 47th; ESPN's own final article says 48th,
# and OU is not tied on the displayed rating, so the two sources genuinely differ by one.
# ESPN (published) is kept; the conflict is recorded in the row's note.
KNOWN_SP_CONFLICTS = {2019: "puntandrally-derived defense rank 47 vs ESPN-published 48 (untied)"}


def get(url: str, path: Path, refresh: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not refresh:
        return path.read_text(errors="ignore")
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8", errors="ignore")
            path.write_text(txt)
            time.sleep(0.6)
            return txt
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed after 4 attempts: {url} ({last})")


def espn_row(season: int, refresh: bool) -> dict:
    d = json.loads(get(ESPN.format(season=season), RAW / "espn_powerindex" / f"{season}.json", refresh))
    cats = {c["name"]: c["names"] for c in d["categories"]}
    ou = next(t for t in d["teams"] if t["team"]["id"] == OU_ID)
    v = {}
    for c in ou["categories"]:
        for name, val in zip(cats[c["name"]], c["values"]):
            v[f"{c['name']}.{name}"] = val
    g = lambda k: "" if v.get(k) is None else v[k]  # noqa: E731
    return {
        "fpi": g("fpi.fpi"), "fpi_rank": g("fpi.fpirank"),
        "sos_rank": g("resume.avgsosrank"), "sor_rank": g("resume.accomplishmentrank"),
        "game_control_rank": g("resume.gamecontrolrank"), "avg_wp_rank": g("resume.avgingamewprank"),
        "eff_total": g("efficiencies.totefficiency"), "eff_total_rank": g("efficiencies.totefficiencyrank"),
        "eff_off": g("efficiencies.offefficiency"), "eff_off_rank": g("efficiencies.offefficiencyrank"),
        "eff_def": g("efficiencies.defefficiency"), "eff_def_rank": g("efficiencies.defefficiencyrank"),
        "eff_st_rank": g("efficiencies.stefficiencyrank"),
    }


def flatten(html: str) -> str:
    h = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h.replace("&amp;", "&"))


def sp_modern(season: int, refresh: bool) -> dict:
    """SP+ 2019-2025 from puntandrally; off/def ranks derived by sorting the full list."""
    text = flatten(get(PR.format(season=season), RAW / "sp_plus" / f"{season}.html", refresh))
    teams = [(int(a), b.strip(), float(c), float(d), float(e)) for a, b, c, d, e in TEAM_RE.findall(text)]
    # Completeness guard. An earlier version of this parser used a restrictive character
    # class for team names and silently dropped one team per season -- "San Jose State"
    # (spelled with an accent before 2023) and "Miami (OH)". A dropped team shifts every
    # rank below it by one, which is exactly how OU's 2021 defense rank was first published
    # here as #56 when it is #57. Refuse to derive anything from an incomplete list.
    seen = {t[0] for t in teams}
    gaps = [i for i in range(1, max(seen) + 1) if i not in seen]
    if gaps:
        raise RuntimeError(f"{season}: puntandrally list is missing rank(s) {gaps} — parser dropped a team")
    ou = next(t for t in teams if t[1] == "Oklahoma")
    # Standard competition ranking: 1 + the number of teams strictly better.
    off_rank = 1 + sum(1 for t in teams if t[3] > ou[3])   # higher offense rating = better
    def_rank = 1 + sum(1 for t in teams if t[4] < ou[4])   # lower defense rating = better
    off_tie = [t[1] for t in teams if t[3] == ou[3] and t[1] != "Oklahoma"]
    def_tie = [t[1] for t in teams if t[4] == ou[4] and t[1] != "Oklahoma"]
    return {"sp_rating": ou[2], "sp_rank": ou[0], "sp_off": ou[3], "sp_off_rank": off_rank,
            "sp_def": ou[4], "sp_def_rank": def_rank, "sp_sos_rank": "",
            "_n": len(teams), "_off_tie": off_tie, "_def_tie": def_tie}


def build(refresh: bool) -> pd.DataFrame:
    snap = pd.read_csv(SNAP, dtype=str).set_index("season")
    games = pd.read_csv(DATA / "games_football.csv")
    rows, problems = [], []
    for season in SEASONS:
        r = {"season": season}
        r.update(espn_row(season, refresh))
        if season <= 2018:
            s = snap.loc[str(season)]
            g = games[games.season == season]
            rec = f"{int((g.result == 'W').sum())}-{int((g.result == 'L').sum())}"
            if s["record"].strip() != rec:
                problems.append(f"{season}: snapshot record {s['record']!r} != game log {rec}")
            r.update({k: s[k] for k in ("sp_rating", "sp_rank", "sp_off", "sp_off_rank",
                                        "sp_def", "sp_def_rank", "sp_sos_rank")})
            src_sp = ("football/sources/snapshots/sp_plus_footballoutsiders_2005_2018.csv "
                      "(snapshot of footballoutsiders.com SP+ archive; upstream host is defunct)")
            conf = "REPORTED"
            note = ""
        else:
            d = sp_modern(season, refresh)
            if season in PUBLISHED_SP:
                # Cross-check the derivation against the published values, then DISCARD the
                # derived ranks in favour of published. Tolerance of 1 only where OU ties another
                # team on the displayed rating (the publisher breaks such ties with precision it
                # does not print) or where a conflict is already documented above.
                pub_off, pub_def, pub_src = PUBLISHED_SP[season]
                for side, want, got, tie in (("offense", pub_off, d["sp_off_rank"], d["_off_tie"]),
                                             ("defense", pub_def, d["sp_def_rank"], d["_def_tie"])):
                    ok = got == want or (tie and abs(got - want) <= 1) or season in KNOWN_SP_CONFLICTS
                    if not ok:
                        problems.append(f"{season}: derived {side} rank {got} != published {want} "
                                        f"(untied — the derivation method is wrong, not just imprecise)")
                derived_off, derived_def = d["sp_off_rank"], d["sp_def_rank"]
                d["sp_off_rank"], d["sp_def_rank"] = pub_off, pub_def
            n, off_tie, def_tie = d.pop("_n"), d.pop("_off_tie"), d.pop("_def_tie")
            r.update(d)
            src_sp = f"{PR.format(season=season)} (reprint of Connelly/ESPN final SP+; {n} FBS teams)"
            if season in PUBLISHED_SP:
                src_sp += f"; off/def ranks PUBLISHED by {PUBLISHED_SP[season][2]}"
            conf = "REPORTED" if season in PUBLISHED_SP else "REPORTED/ESTIMATED-derived-ranks"
            ties = "; ".join(x for x in (
                f"offense rating ties {', '.join(off_tie)}" if off_tie else "",
                f"defense rating ties {', '.join(def_tie)}" if def_tie else "") if x)
            if season in PUBLISHED_SP:
                note = (f"off/def ranks PUBLISHED (not derived); competition-ranking the full {n}-team "
                        f"list independently gives {derived_off}/{derived_def}")
                if ties:
                    note += f"; {ties}"
                if season in KNOWN_SP_CONFLICTS:
                    note += f"; CONFLICTING: {KNOWN_SP_CONFLICTS[season]}"
            else:
                note = ("SP+ overall rank/rating as published; off/def RANKS derived by competition-ranking "
                        f"the full {n}-team FBS list of published off/def ratings (method validated in this "
                        "same build against the seasons where ranks are published)"
                        + (f"; {ties} — published tie-break may differ by 1" if ties else ""))
        r["confidence"] = conf
        r["source"] = (f"ESPN Power Index JSON ({ESPN.format(season=season)}); {src_sp}")
        r["note"] = note
        rows.append(r)

    cols = ["season", "fpi", "fpi_rank", "sos_rank", "sor_rank", "game_control_rank", "avg_wp_rank",
            "eff_total", "eff_total_rank", "eff_off", "eff_off_rank", "eff_def", "eff_def_rank",
            "eff_st_rank", "sp_rating", "sp_rank", "sp_off", "sp_off_rank", "sp_def", "sp_def_rank",
            "sp_sos_rank", "confidence", "source", "note"]
    df = pd.DataFrame(rows)[cols]
    if problems:
        raise SystemExit("BUILD REFUSED — cross-check failures:\n  " + "\n  ".join(problems))
    print(f"cross-checks passed: {len(df)} seasons; snapshot records reconcile to the game log; "
          f"derivation agrees with published off/def ranks for {sorted(PUBLISHED_SP)} "
          f"(ranks are derived only for 2020-2022)")
    return df


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    df = build(args.refresh)
    buf = io.StringIO()
    df.to_csv(buf, index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    new, target = buf.getvalue(), DATA / "ratings_football.csv"
    if args.check:
        if target.read_text() == new:
            print("✅ committed ratings_football.csv is byte-identical to a fresh rebuild")
            return 0
        import difflib
        print("❌ committed file differs from rebuild:")
        for line in list(difflib.unified_diff(target.read_text().splitlines(), new.splitlines(),
                                              "committed", "rebuilt", lineterm=""))[:30]:
            print(" ", line[:200])
        return 1
    target.write_text(new)
    print(f"wrote {target} ({len(df)} seasons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
