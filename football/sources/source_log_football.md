# Source log — football module

Access dates: 2026-09-06 (game logs, ESPN JSON, SP+ archive, 247, coaches) and 2026-09-07 (SP+ 2019–22 reprints, recruiting retry). Tiers: `PRIMARY` official/box-score-grade · `SECONDARY` credible outlet or aggregator · `CROSS-REF` corroboration only.

| Source | URL pattern | Supports | Tier |
|---|---|---|---|
| Wikipedia season articles (raw wikitext) | `en.wikipedia.org/w/index.php?title=YYYY_Oklahoma_Sooners_football_team&action=raw` | every game 1999–2025 (date, opponent, ranks, site, score, OT, nonconf, game name); season infobox records | SECONDARY (scores cross-checked by W/L consistency and three independent extractions) |
| Wikipedia list of OU seasons | `en.wikipedia.org/wiki/List_of_Oklahoma_Sooners_football_seasons` | coach, conference finish, bowl result, final AP/Coaches rank | SECONDARY |
| Wikipedia 2026 season article; SoonerSports recap 2026-09-04 | `…/2026_Oklahoma_Sooners_football_team`; `soonersports.com/news/2026/9/4/…` | 2026 tracker (UTEP 51-0; schedule; AP #10) | PRIMARY (recap) / SECONDARY |
| ESPN Power Index JSON | `site.web.api.espn.com/apis/fitt/v3/sports/football/college-football/powerindex?season=YYYY` (cached `pi_YYYY.json`) | FPI, FPI rank, AVG SOS rank, accomplishment (SOR) rank, game-control rank, avg in-game WP rank, total/off/def/ST efficiencies + ranks, 2005–25 | SECONDARY (single source, partly retroactive) |
| Football Outsiders S&P+ archive | `footballoutsiders.com/stats/ncaa/sp/overall/YYYY` (2005–2018, cached) | SP+ rating/rank, off/def/ST ranks, SOS rank | SECONDARY |
| ESPN — "Final SP+ rankings for 2019" | `espn.com/college-football/story/_/id/28497018/…` | 2019 SP+ | SECONDARY |
| puntandrally.com SP+ tables | `puntandrally.com/viewSandPratings.php?whichyear=YYYY` (2019–2025) | SP+ overall rank/rating and off/def ratings; off/def ranks derived 2020–22 | SECONDARY (reprint of ESPN/Connelly) |
| stormininnorman.com, 2023-01-10 | post-bowl SP+ top-25 reprint | 2022 SP+ #18 (CONFLICTING vs 19) | CROSS-REF |
| 247Sports team season pages | `247sports.com/college/oklahoma/Season/YYYY-Football/Commits/` (2002–2026) | 247 Composite + 247 team rank, signee counts, notable signees | PRIMARY (service's own page) |
| stormininnorman.com top-5 classes; Yahoo/SoonersWire "last 10 classes"; SI/Tulsa World snippets | various | class-rank corroboration; Rivals/ESPN ranks 2022–26 | CROSS-REF |
| NCAA.com Stoops retirement story; Wikipedia Bob Stoops / Lincoln Riley / Brent Venables; Saturday Down South coach page | various | coach records, conference titles, CFP appearances | SECONDARY |
| ESPN box score — Alabama 34, Oklahoma 24 (2025-12-19) | `espn.com/college-football/game/_/gameId/401779840/…` | 2025 CFP first-round anchor | PRIMARY |
| CollegeFootballData API tiers / key pages | `collegefootballdata.com/api-tiers`, `/key` | fallback rationale (1,000 calls/mo free; key required) | CROSS-REF |

**Blocked (not used):** sports-reference.com (Cloudflare), masseyratings.com (403), teamrankings.com (403), n.rivals.com (403), ESPN+ final SP+ articles 2020–22 (paywall).
