#!/usr/bin/env python3
"""
update_2026.py — refresh football/data/season_2026_tracker.csv from two live sources.

The 2026 season is in progress, so the tracker is the one dataset in this module that
legitimately changes week to week. It is held to the same standard as the historical data:
two independent sources, cross-checked, and the script REFUSES to write when they disagree
about a completed game.

Sources (both key-free):
  1. ESPN team-schedule API — scores, status, site, opponent rank at kickoff.
  2. The Wikipedia season article's {{CFB Schedule Entry}} templates — the same feed
     ingest_wikipedia.py uses for 1999-2025, so the in-progress season is sourced exactly
     like the completed ones.

A dating trap this script handles explicitly. ESPN stores a not-yet-scheduled kickoff as
midnight Central (04:00/05:00 UTC) on the correct Saturday and flags it `timeValid=false`.
Converting that to Central rolls the date back to Friday, which would silently shift seven
of this season's dates by a day. When `timeValid` is false the UTC date is authoritative;
only a confirmed kickoff is converted to local time.

Usage:  python3 football/scripts/update_2026.py [--check]
  --check   report what would change and exit non-zero if anything differs; write nothing

Status values: FINAL (completed, score cross-checked), IN_PROGRESS (kicked off, NO score
recorded), PENDING (not started). A partial score is not a result and is never written.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Reuse the historical ingest's brace-aware template parser rather than maintaining a second
# one. A naive "split fields on |" breaks on {{tooltip|September 4|Friday}}, which is exactly
# how the 2026 opener first failed this script's own cross-check.
from ingest_wikipedia import split_params, strip_markup  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "season_2026_tracker.csv"
SEASON = 2026
ESPN = ("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/201/"
        f"schedule?season={SEASON}&seasontype=2")
WIKI = (f"https://en.wikipedia.org/w/index.php?title={SEASON}_Oklahoma_Sooners_football_team"
        "&action=raw")
WIKI_URL = f"https://en.wikipedia.org/wiki/{SEASON}_Oklahoma_Sooners_football_team"
UA = "OUFootballResearch/1.0 (portfolio research; github.com/johnthesooner)"
CENTRAL = ZoneInfo("America/Chicago")
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], 1)}


def get(url: str) -> str:
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed after 4 attempts: {url} ({last})")


def espn_rows() -> dict[str, dict]:
    import json
    d = json.loads(get(ESPN))
    out = {}
    for ev in d.get("events", []):
        c = ev["competitions"][0]
        st = c.get("status", {}).get("type", {})
        ou = next(x for x in c["competitors"] if x["team"]["id"] == "201")
        op = next(x for x in c["competitors"] if x["team"]["id"] != "201")
        # See the module docstring: only a confirmed kickoff may be converted to local time.
        raw = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
        date = (raw.astimezone(CENTRAL) if c.get("timeValid") else raw).strftime("%Y-%m-%d")

        def score(x):
            s = x.get("score")
            if s is None:
                return ""
            v = s["value"] if isinstance(s, dict) else s
            return str(int(float(v)))

        def rank(x):
            r = x.get("curatedRank", {}).get("current")
            return "" if r in (None, 99) else str(int(r))

        final = bool(st.get("completed"))
        state = st.get("state")            # "pre" | "in" | "post"
        # A game that has kicked off but not finished is neither scheduled nor final. It gets
        # its own status and still carries NO score: a partial score is not a result, and this
        # project's rule is that an unfinished contest is never assigned one.
        if final:
            status = "FINAL"
        elif state == "in" or st.get("name") == "STATUS_IN_PROGRESS":
            status = "IN_PROGRESS"
        else:
            status = "PENDING"
        out[date] = {
            "opponent_espn": op["team"]["displayName"],
            "site": "N" if c.get("neutralSite") else ("H" if ou["homeAway"] == "home" else "A"),
            "status": status,
            "detail": st.get("shortDetail", ""),
            "result": ("W" if ou.get("winner") else "L") if final else "",
            "ou_pts": score(ou) if final else "",
            "opp_pts": score(op) if final else "",
            "opp_rank": rank(op),
        }
    return out


def wiki_rows() -> dict[str, dict]:
    txt = get(WIKI)
    out = {}
    for m in re.finditer(r"\{\{CFB Schedule Entry(.*?)\n\}\}", txt, flags=re.S | re.I):
        f = split_params("|" + m.group(1))
        clean = strip_markup

        dm = re.match(r"([A-Z][a-z]+)\s+(\d{1,2})", clean(f.get("date", "")))
        if not dm or dm.group(1) not in MONTHS:
            continue
        date = f"{SEASON:04d}-{MONTHS[dm.group(1)]:02d}-{int(dm.group(2)):02d}"
        score = clean(f.get("score", "")).replace("–", "-").replace("−", "-")
        sm = re.match(r"(\d+)\s*-\s*(\d+)", score)
        wl = clean(f.get("w/l", "")).lower()
        row = {"opponent_wiki": clean(f.get("opponent", "")), "ou_rank": clean(f.get("rank", "")),
               "opp_rank_wiki": clean(f.get("opprank", "")), "result": "", "ou_pts": "", "opp_pts": ""}
        if sm and wl:
            a, b = int(sm.group(1)), int(sm.group(2))
            won = wl.startswith("w")
            # the template's score is winner-first and carries no team labels
            row.update(result="W" if won else "L",
                       ou_pts=str(max(a, b) if won else min(a, b)),
                       opp_pts=str(min(a, b) if won else max(a, b)))
        out[date] = row
    return out


def build() -> tuple[pd.DataFrame, list[str]]:
    espn, wiki = espn_rows(), wiki_rows()
    problems, rows = [], []
    for date in sorted(set(espn) | set(wiki)):
        e, w = espn.get(date, {}), wiki.get(date, {})
        if not e or not w:
            problems.append(f"{date}: present in only one source "
                            f"(ESPN={'yes' if e else 'no'}, Wikipedia={'yes' if w else 'no'})")
            continue
        status = e["status"]
        if status == "FINAL":
            # cross-check every completed game; a disagreement stops the build
            if w["result"] and (e["result"], e["ou_pts"], e["opp_pts"]) != (w["result"], w["ou_pts"], w["opp_pts"]):
                problems.append(
                    f"{date} {e['opponent_espn']}: ESPN {e['ou_pts']}-{e['opp_pts']} {e['result']} "
                    f"vs Wikipedia {w['ou_pts']}-{w['opp_pts']} {w['result']}")
                continue
            if not w["result"]:
                problems.append(f"{date} {e['opponent_espn']}: ESPN reports final, Wikipedia has no score yet")
                continue
        rows.append({
            "season": SEASON, "date": date, "opponent": w["opponent_wiki"] or e["opponent_espn"],
            "site": e["site"], "status": status,
            "result": e["result"], "ou_pts": e["ou_pts"], "opp_pts": e["opp_pts"],
            "ou_rank": w["ou_rank"], "opp_rank": e["opp_rank"] or w["opp_rank_wiki"],
            "confidence": "CONFIRMED-score" if status == "FINAL" else "PENDING",
            "source": f"{WIKI_URL}; ESPN team-schedule API (site.api.espn.com, team 201)",
            "note": ("score agreed by ESPN and the season article" if status == "FINAL"
                     else (f"in progress at last refresh ({e['detail']}); no score assigned"
                           if status == "IN_PROGRESS" else "scheduled; no score assigned")),
        })
    return pd.DataFrame(rows), problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    df, problems = build()
    if problems:
        print("REFUSING TO WRITE — source disagreement:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    fin = df[df.status == "FINAL"]
    live = df[df.status == "IN_PROGRESS"]
    w, l = int((fin.result == "W").sum()), int((fin.result == "L").sum())
    pf, pa = (pd.to_numeric(fin.ou_pts).sum(), pd.to_numeric(fin.opp_pts).sum()) if len(fin) else (0, 0)
    print(f"2026: {w}-{l} through {len(fin)} completed game(s); "
          f"{len(df) - len(fin) - len(live)} scheduled. Points {pf}-{pa} ({pf - pa:+d}).")
    for r in live.itertuples():
        print(f"  LIVE NOW: {r.date} vs {r.opponent} — no score recorded until final")
    for r in fin.itertuples():
        print(f"  {r.date}  {r.result} {r.ou_pts}-{r.opp_pts}  "
              f"{'vs' if r.site == 'H' else ('at' if r.site == 'A' else 'vs (N)')} "
              f"{('#' + r.opp_rank + ' ') if r.opp_rank else ''}{r.opponent}")

    buf = io.StringIO()
    df.to_csv(buf, index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    new = buf.getvalue()
    if args.check:
        old = OUT.read_text() if OUT.exists() else ""
        if old == new:
            print("✅ tracker is up to date")
            return 0
        import difflib
        print("\ntracker differs from live sources:")
        for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                              "committed", "live", lineterm=""))[:30]:
            print(" ", line[:170])
        return 1
    OUT.write_text(new)
    print(f"wrote {OUT} ({len(df)} games)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
