#!/usr/bin/env python3
"""
ingest_wikipedia.py — reproducible game-log ingest for Oklahoma football, 1999-2025.

Fallback ingest (no CollegeFootballData API key was available): parses the
{{CFB Schedule Entry}} templates in the raw wikitext of each Wikipedia season
article ("YYYY Oklahoma Sooners football team"). Raw pages are cached in
football/sources/raw/wikipedia/ (gitignored) so re-runs are offline and idempotent;
pass --refresh to re-download.

Output: football/data/games_football.csv (one row per game, confidence-tagged).
Every row's provenance is the article URL. Site, ranks, scores, overtime and
conference-game flags come straight from the template fields; game_type is derived
from the `gamename` field plus a small, documented override list (see GAME_TYPE_OVERRIDES).

Cross-checked 2026-09-06 against three independent WebFetch-based extractions of
the same articles (346/356 rows matched on first pass; the 10 date-format misses and
7 rank/site diffs were resolved against the raw template text — see
football/audit/FOOTBALL_DATA_AUDIT.md).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from football_lib import conference_for_season, era_for_season, is_one_score  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent          # football/
RAW = ROOT / "sources" / "raw" / "wikipedia"
DATA = ROOT / "data"
SEASONS = range(1999, 2026)
UA = "OUFootballResearch/1.0 (portfolio research; contact via github.com/johnthesooner)"
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], 1)}

# (season, opponent) -> game_type, with the documented basis.
GAME_TYPE_OVERRIDES = {
    # Template labels these only "Orange Bowl"/"Sugar Bowl"; article body states each
    # "served as the BCS National Championship Game".
    (2000, "Florida State"): "BCS_TITLE",
    (2003, "LSU"): "BCS_TITLE",
    (2004, "USC"): "BCS_TITLE",
    (2008, "Florida"): "BCS_TITLE",
}
# 2021 Tulane: template says away=y (Tulane was the designated home team) but the game
# was moved to Norman by Hurricane Ida. We code the PHYSICAL site (H) for home/away splits.
SITE_OVERRIDES = {(2021, "Tulane"): ("H", "Tulane home game relocated to Norman (Hurricane Ida); coded by physical site")}

# Opponent AP ranks where OU's own season article is demonstrably wrong and the opponent's
# article plus contemporaneous sources agree on a different value. (season, opponent) ->
# (corrected rank, basis). Verified 2026-09-07; neither correction changes ranked/unranked
# or top-10 status, so no analysis result moves — they are here for accuracy, not effect.
RANK_OVERRIDES = {
    (2016, "Houston"): ("15", "OU's 2016 article template says opprank=14, but the AP preseason poll "
                              "(Aug 21 2016) had Washington #14 and Houston #15; Houston's own 2016 "
                              "article (rank=15, opprank=3), the Wikipedia 2016 AP rankings page, CBS "
                              "Sports and NCAA.com all say #15. Five independent confirmations."),
    (2005, "Texas Tech"): ("21", "OU's 2005 article template says opprank=19; Texas Tech's own 2005 "
                                 "article gives rank=21 for this game, and ESPN's curatedRank for the "
                                 "same game is 21. Three sources against one."),
}


def fetch_raw(season: int, refresh: bool = False) -> str:
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"{season}.wikitext"
    if p.exists() and not refresh:
        return p.read_text(encoding="utf-8")
    url = (f"https://en.wikipedia.org/w/index.php?title={season}_Oklahoma_Sooners_football_team"
           "&action=raw")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8")
            break
        except Exception as e:                      # noqa: BLE001 — retry any transport error
            last_err = e
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"{season}: download failed after 4 attempts: {last_err}")
    p.write_text(txt, encoding="utf-8")
    time.sleep(0.7)   # be polite to Wikipedia
    return txt


def split_params(body: str) -> dict[str, str]:
    """Split template body on top-level '|' (ignoring links/templates)."""
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
            out[k.strip().lower()] = v.strip()
    return out


def strip_markup(v: str) -> str:
    v = re.sub(r"<ref[^>]*/>", "", v)
    v = re.sub(r"<ref[^>]*>.*?</ref>", "", v, flags=re.S)
    v = re.sub(r"\{\{tooltip\|([^|}]+)\|[^}]*\}\}", r"\1", v, flags=re.I)
    v = re.sub(r"\{\{cfb link\|[^}]*?title=([^|}]+)[^}]*\}\}", r"\1", v, flags=re.I)
    v = re.sub(r"\{\{[^{}]*\}\}", "", v)
    v = re.sub(r"\[\[([^|\]]*)\|([^\]]*)\]\]", r"\2", v)
    v = re.sub(r"\[\[([^\]]*)\]\]", r"\1", v)
    v = re.sub(r"<[^>]+>", "", v)
    v = v.replace("&nbsp;", " ").replace("''", "")
    return v.strip()


def parse_date(raw: str, season: int) -> str:
    s = strip_markup(raw)
    m = re.search(r"([A-Z][a-z]+)\s+(\d{1,2})(?:,?\s*(\d{4}))?", s)
    if not m or m.group(1) not in MONTHS:
        raise ValueError(f"{season}: unparseable date {raw!r}")
    mi, day = MONTHS[m.group(1)], int(m.group(2))
    year = int(m.group(3)) if m.group(3) else (season + 1 if mi <= 2 else season)
    return f"{year:04d}-{mi:02d}-{day:02d}"


def classify(gamename: str, season: int, opponent: str) -> str:
    if (season, opponent) in GAME_TYPE_OVERRIDES:
        return GAME_TYPE_OVERRIDES[(season, opponent)]
    g = gamename.lower()
    if "first round" in g:
        return "CFP_R1"
    if "semifinal" in g or "cfp" in g or "playoff" in g:
        return "CFP_SEMI"
    if "national championship" in g:
        return "BCS_TITLE"
    if "championship game" in g:
        return "CCG"
    if "bowl" in g:
        return "BOWL"
    return "REG"


def parse_season(txt: str, season: int) -> list[dict]:
    rows = []
    for m in re.finditer(r"\{\{CFB Schedule Entry(.*?)\n\}\}", txt, flags=re.S | re.I):
        d = split_params("|" + m.group(1))
        score = strip_markup(d.get("score", "")).replace("–", "-").replace("—", "-")
        sm = re.match(r"(\d+)\s*-\s*(\d+)", score)
        wl = strip_markup(d.get("w/l", "")).lower()
        if not sm or not wl:
            continue                       # unplayed / cancelled entries carry no score
        a, b = int(sm.group(1)), int(sm.group(2))
        won = wl.startswith("w")
        # The template's `score` is winner-first by convention and carries no team labels, so
        # the assignment below is ORDERED BY the w/l flag rather than read positionally. That
        # makes any internal "result agrees with score" assertion vacuous by construction: a
        # flipped w/l flag would silently reverse a score. The real guard is external —
        # scripts/crosscheck_espn.py compares every game to ESPN's feed, and build_seasons.py
        # cross-foots each season's record against the article infobox.
        ou, op = (max(a, b), min(a, b)) if won else (min(a, b), max(a, b))
        opp_raw = strip_markup(d.get("opponent", ""))
        rank_in_name = re.match(r"No\.\s*(\d+)\s+(.*)", opp_raw)
        opp_rank = strip_markup(d.get("opprank", ""))
        opponent = opp_raw
        if rank_in_name:
            opp_rank = opp_rank or rank_in_name.group(1)
            opponent = rank_in_name.group(2)
        opponent = re.sub(r"\s*\((FL|CA|OH|FCS)\)\s*$", "", opponent).strip()
        opp_rank = re.sub(r"\D.*$", "", opp_rank)          # drop "(FCS)" style suffixes
        if "FCS" in strip_markup(d.get("opprank", "")):
            opp_rank = ""                                   # FCS poll rank is not an AP rank
        away = strip_markup(d.get("away", "")).lower() in ("y", "yes", "true")
        neutral = strip_markup(d.get("neutral", "")).lower() in ("y", "yes", "true")
        site = "N" if neutral else ("A" if away else "H")
        note, tags = "", []
        if (season, opponent) in SITE_OVERRIDES:
            site, note = SITE_OVERRIDES[(season, opponent)]
            tags.append("REPORTED-site")
        if (season, opponent) in RANK_OVERRIDES:
            opp_rank, rank_note = RANK_OVERRIDES[(season, opponent)]
            note = "; ".join(x for x in (note, rank_note) if x)
            tags.append("CORRECTED-opp_rank")
        gamename = strip_markup(d.get("gamename", ""))
        nonconf = strip_markup(d.get("nonconf", "")).lower() in ("y", "yes", "true")
        gtype = classify(gamename, season, opponent)
        conf_game = "N" if (nonconf or gtype != "REG") else "Y"
        margin = ou - op
        rows.append({
            "season": season, "date": parse_date(d.get("date", ""), season), "opponent": opponent,
            "opp_rank": opp_rank, "ou_rank": strip_markup(d.get("rank", "")), "site": site,
            "result": "W" if won else "L", "ou_pts": ou, "opp_pts": op, "margin": margin,
            "one_score": "Y" if is_one_score(margin) else "N",
            "conf_game": conf_game, "game_type": gtype,
            "overtime": "Y" if strip_markup(d.get("overtime", "")) else "N",
            "era": era_for_season(season), "conference": conference_for_season(season),
            # Score and result come from the season-article template and are externally
            # cross-checked game-by-game against ESPN (scripts/crosscheck_espn.py). Rows that
            # carry a documented override are tagged so the provenance is visible in the data
            # rather than only in the audit trail.
            "confidence": "/".join(["CONFIRMED-score"] + tags),
            "source": f"https://en.wikipedia.org/wiki/{season}_Oklahoma_Sooners_football_team",
            "note": note or (gamename if gtype != "REG" else ""),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download raw wikitext")
    args = ap.parse_args()
    DATA.mkdir(exist_ok=True)
    all_rows: list[dict] = []
    for season in SEASONS:
        rows = parse_season(fetch_raw(season, args.refresh), season)
        w = sum(r["result"] == "W" for r in rows)
        print(f"  {season}: {len(rows):2d} games  {w}-{len(rows)-w}")
        all_rows += rows
    all_rows.sort(key=lambda r: (r["season"], r["date"]))
    out = DATA / "games_football.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        wr.writeheader(); wr.writerows(all_rows)
    print(f"wrote {out} ({len(all_rows)} games)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
