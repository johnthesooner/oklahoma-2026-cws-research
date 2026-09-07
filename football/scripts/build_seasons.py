#!/usr/bin/env python3
"""
build_seasons.py — regenerate football/data/seasons_football.csv from committed code.

Closes a reproducibility gap: the seasons table was originally assembled by an ad-hoc
script that was never committed, so a reader could not rebuild it. This script derives
every column from two auditable inputs:

  1. football/data/games_football.csv  — G, W, L, win_pct, conf_W, conf_L, PF, PA, margin_pg
  2. the {{Infobox ...}} of each Wikipedia season article (same cached raw wikitext that
     ingest_wikipedia.py downloads) — coach, final AP/Coaches ranks, bowl result, and the
     conference-championship marker.

Only `conf_finish` is a transcribed table (CONF_FINISH below, sourced from Wikipedia's
List of Oklahoma Sooners football seasons); it is committed, inline and auditable.

Cross-checks enforced at build time — the script REFUSES to write on any mismatch:
  * infobox overall record  == record computed from the game log, for all 27 seasons
  * infobox conference record == conference record computed from the game log
  * conf_title derived from the infobox "champion"/"conf_champ" field must total 14 and
    must equal the conference-title counts in coaches_football.csv (Stoops 10, Riley 4)

Usage:  python3 football/scripts/build_seasons.py [--check] [--refresh]
  --check    rebuild in memory and diff against the committed CSV; exit 1 on any difference
  --refresh  re-download the raw wikitext instead of using the cache
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from football_lib import conference_for_season, era_for_season  # noqa: E402
from ingest_wikipedia import fetch_raw  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEASONS = range(1999, 2026)
LIST_URL = "https://en.wikipedia.org/wiki/List_of_Oklahoma_Sooners_football_seasons"

# Conference finish is the one column with no machine-readable source in the season
# infoboxes. Transcribed from the season articles / List of Oklahoma Sooners football
# seasons (accessed 2026-09-06). Kept inline so it is committed, diffable and auditable.
# 2002 is "T-1st South": OU and Texas both finished 6-2 in the division and OU advanced on
# the head-to-head tiebreaker, matching how 2008 and 2010 division ties are labelled here.
CONF_FINISH = {
    1999: "T-2nd South", 2000: "1st South", 2001: "2nd South", 2002: "T-1st South",
    2003: "1st South", 2004: "1st South", 2005: "T-2nd South", 2006: "1st South",
    2007: "1st South", 2008: "T-1st South", 2009: "T-3rd South", 2010: "T-1st South",
    2011: "T-3rd", 2012: "T-1st", 2013: "T-2nd", 2014: "T-4th", 2015: "1st",
    2016: "1st", 2017: "1st", 2018: "1st", 2019: "1st", 2020: "1st", 2021: "3rd",
    2022: "T-7th", 2023: "T-2nd", 2024: "T-13th", 2025: "T-5th",
}
INFOBOX_NAMES = ("Infobox college sports team season", "Infobox NCAA team season")


def extract_template(text: str, name: str) -> str | None:
    """Return the full {{name ...}} template body, brace-matched."""
    i = text.find("{{" + name)
    if i < 0:
        return None
    depth, j = 0, i
    while j < len(text):
        if text.startswith("{{", j):
            depth += 1; j += 2; continue
        if text.startswith("}}", j):
            depth -= 1; j += 2
            if depth == 0:
                return text[i:j]
            continue
        j += 1
    return None


def split_top(body: str) -> dict[str, str]:
    """Split a template body on top-level '|' (ignoring nested links/templates)."""
    parts, sq, cu, cur, i = [], 0, 0, "", 0
    while i < len(body):
        if body.startswith("[[", i):
            sq += 1; cur += "[["; i += 2; continue
        if body.startswith("]]", i):
            sq -= 1; cur += "]]"; i += 2; continue
        if body.startswith("{{", i):
            cu += 1; cur += "{{"; i += 2; continue
        if body.startswith("}}", i):
            cu -= 1; cur += "}}"; i += 2; continue
        c = body[i]
        if c == "|" and sq == 0 and cu == 0:
            parts.append(cur); cur = ""
        else:
            cur += c
        i += 1
    parts.append(cur)
    out = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def clean(v: str) -> str:
    v = re.sub(r"<ref[^>]*/>", "", v)
    v = re.sub(r"<ref[^>]*>.*?</ref>", "", v, flags=re.S)
    v = re.sub(r"\[\[([^|\]]*)\|([^\]]*)\]\]", r"\2", v)
    v = re.sub(r"\[\[([^\]]*)\]\]", r"\1", v)
    v = v.replace("<br>", " / ").replace("<br/>", " / ").replace("<br />", " / ")
    v = re.sub(r"<sup>(.*?)</sup>", r" \1", v)
    v = re.sub(r"<[^>]+>", "", v)
    v = re.sub(r"\{\{[^{}]*\}\}", "", v)
    v = v.replace("–", "-").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", v).strip(" /")


def infobox(season: int, refresh: bool) -> dict[str, str]:
    txt = fetch_raw(season, refresh)
    tpl = next((t for t in (extract_template(txt, n) for n in INFOBOX_NAMES) if t), None)
    if not tpl:
        raise RuntimeError(f"{season}: no season infobox found in wikitext")
    return {k: clean(v) for k, v in split_top(tpl[2:-2]).items()}


def conf_title_from(box: dict[str, str]) -> str:
    """Y only for an outright or shared CONFERENCE title.

    Two traps this guards against, both real:
      * division-only: 2003's infobox says "Big 12 South Division champion" while OU LOST
        that year's Big 12 Championship Game 7-35 — the "division" part is skipped.
      * the conf_champ field often holds the NAME of the title game played ("Big 12
        Championship Game"), not a title won, so `champions?` is anchored with \b to stop
        it matching the prefix inside "Championship".
    """
    blob = f"{box.get('champion', '')} / {box.get('conf_champ', '')}"
    for part in blob.split("/"):
        p = part.strip().lower()
        if "division" in p:
            continue
        if re.search(r"\b(big 12|sec)\b.*\b(co-)?champions?\b", p):
            return "Y"
    return "N"


def build(refresh: bool) -> pd.DataFrame:
    games = pd.read_csv(DATA / "games_football.csv")
    rows, problems = [], []
    for season in SEASONS:
        box = infobox(season, refresh)
        g = games[games.season == season]
        w, l = int((g.result == "W").sum()), int((g.result == "L").sum())
        cg = g[g.conf_game == "Y"]
        cw, cl = int((cg.result == "W").sum()), int((cg.result == "L").sum())
        pf, pa, n = int(g.ou_pts.sum()), int(g.opp_pts.sum()), len(g)

        # --- cross-checks against the infobox -------------------------------
        if box.get("record", "").strip() != f"{w}-{l}":
            problems.append(f"{season}: game log {w}-{l} vs infobox record {box.get('record')!r}")
        if box.get("conf_record", "").strip() != f"{cw}-{cl}":
            problems.append(f"{season}: game log conf {cw}-{cl} vs infobox {box.get('conf_record')!r}")

        # postseason: bowl NAME from the infobox, result/score/opponent from the game log,
        # so the string can never disagree with the games it summarises.
        post = g[g.game_type != "REG"].sort_values("date")
        if len(post):
            last = post.iloc[-1]
            bowl_name = box.get("bowl", "").strip() or last.game_type
            bowl = f"{last.result} {bowl_name} vs {last.opponent} {last.ou_pts}-{last.opp_pts}"
        else:
            bowl = "no postseason game"
        rows.append({
            "season": season, "era": era_for_season(season),
            "coach": clean(box.get("head_coach", "")) + (
                " (Bob Stoops interim, bowl)" if season == 2021 else ""),
            "conference": conference_for_season(season),
            "G": n, "W": w, "L": l, "win_pct": round(w / n, 3),
            "conf_W": cw, "conf_L": cl, "conf_finish": CONF_FINISH[season],
            "conf_title": conf_title_from(box),
            "PF": pf, "PA": pa, "margin_pg": round((pf - pa) / n, 2),
            "postseason": bowl,
            "ap_final": box.get("APRank", ""), "coaches_final": box.get("CoachRank", ""),
            "confidence": "CONFIRMED-record/ESTIMATED-derived",
            "source": f"{LIST_URL}; season infobox; PF/PA summed from games_football.csv",
            "note": "",
        })

    df = pd.DataFrame(rows)
    titles = int((df.conf_title == "Y").sum())
    coaches = pd.read_csv(DATA / "coaches_football.csv")
    expected = int(coaches.conf_titles.sum())
    if titles != expected:
        problems.append(f"conf_title total {titles} != coaches_football.csv total {expected}")
    for coach, want in (("Bob Stoops", 10), ("Lincoln Riley", 4)):
        era = "Stoops" if coach == "Bob Stoops" else "Riley"
        got = int((df[(df.era == era) & (df.conf_title == "Y")]).shape[0])
        if got != want:
            problems.append(f"{era}-era conference titles {got} != {want}")
    if problems:
        raise SystemExit("BUILD REFUSED — cross-check failures:\n  " + "\n  ".join(problems))
    print(f"cross-checks passed: 27 seasons reconcile to the game log; "
          f"{titles} conference titles ({', '.join(str(s) for s in df[df.conf_title == 'Y'].season)})")
    return df


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="diff against the committed CSV, do not write")
    ap.add_argument("--refresh", action="store_true", help="re-download raw wikitext")
    args = ap.parse_args()
    df = build(args.refresh)
    buf = io.StringIO()
    df.to_csv(buf, index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    new = buf.getvalue()
    target = DATA / "seasons_football.csv"
    if args.check:
        old = target.read_text()
        if old == new:
            print("✅ committed seasons_football.csv is byte-identical to a fresh rebuild")
            return 0
        import difflib
        print("❌ committed file differs from rebuild:")
        for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                              "committed", "rebuilt", lineterm=""))[:40]:
            print(" ", line)
        return 1
    target.write_text(new)
    print(f"wrote {target} ({len(df)} seasons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
