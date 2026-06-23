# Social Visualization Playbook — OU 2026 Research

How to turn this project's data into visuals that actually travel on social, grounded in
2025–2026 research (every claim tagged `[CONFIRMED]` = primary/benchmark source,
`[REPORTED]` = industry/vendor consensus; sources at bottom). Companion to
[`../distribution/DISTRIBUTION_STRATEGY.md`](../distribution/DISTRIBUTION_STRATEGY.md).
The reproducible asset generator that implements this is in [`scripts/`](scripts/).

---

## TL;DR — the five things that matter

1. **One number per graphic.** Lead with a single bold figure, not a busy chart — a feed gives you ~2 seconds. `[CONFIRMED]`
2. **Carousels + documents win for data; short video wins for reach.** IG carousels and LinkedIn document/PDF posts get the most *saves* (the signal that matters for reference graphics); Reels/TikTok/Shorts get the most *discovery*. Static single images are in measurable decline. `[CONFIRMED — Socialinsider 2025/26]`
3. **Design once at three canvases:** `1080×1350` (4:5 portrait hero), `1080×1080` (square/carousel), `1080×1920` (9:16 video/stories). These three cover all 10 platforms. `[CONFIRMED-2026]`
4. **Frame each graphic as *awe* OR *debate* — not both.** Awe = "look how dominant" (streaks, totals). Debate = "where do they rank" (vs peer schools). Both are proven share triggers; mixing them muddies the takeaway. `[CONFIRMED]`
5. **Be honest and credit the source on the image.** No truncated axes (the bias survives even when viewers are warned), color-blind-safe palette, source/date footer. It also reduces takedown/credibility risk. `[CONFIRMED]`

---

## What performs — ranked share triggers (apply to our data)

| Trigger | Why it works | Our angle |
|---|---|---|
| **Single big stat** | Decodable in 1–2s | "46" hero card |
| **Surprising/counterintuitive** | Violated expectation = reshare reflex | "OU isn't a football school — 80% of titles are Olympic sports" |
| **Awe at dominance / streaks** | Re-live the high | Softball four-peat, men's gym 12, the 2013–26 surge |
| **Debate-bait / ranking** | Implicit argument → quote-tweets | OU vs peer blue-bloods (where does 39 NCAA rank?) |
| **Identity / fandom** | Fans reshare to signal affiliation | School colors, "every Sooner title" |
| **Nostalgia / "on this day"** | Low-controversy, high-affinity | Anniversary card auto-filled from the dataset |
| **Narrative arc over time** | Reads as a journey | Cumulative title timeline / race |

`[CONFIRMED]` across Sportico 2025, NBA social (Shorty Awards), fandom psychology (PLOS One 2025, APS).

---

## Platform canvas spec (design 3 sizes, adapt everywhere)

| Platform | Best format for data | Image size | Video size |
|---|---|---|---|
| Instagram | **Carousel (4:5)** + Reels for reach | 1080×1350 | 1080×1920 |
| LinkedIn | **Document/PDF carousel** (highest reach for data) | 1080×1080 pages | 1920×1080 |
| X / Twitter | Single chart or 2–4 img thread | **1600×900 or 1:1** (timeline crops outside 2:1–1:1) | 1920×1080 / 1080×1920 |
| TikTok / Reels / Shorts | Short vertical, animated stat reveal | — | 1080×1920 (keep data in center safe zone) |
| Facebook / Threads | Portrait single or carousel | 1080×1350 | 1080×1920 |
| Reddit | One clean chart, OC, matches sub norms | 1200×1200 / 1200×900 | — |
| Bluesky | Square/portrait, **export tight** (~1MB cap, ~1000px downscale) | 1000×1000 | — |

**Master workflow:** build at `1080×1350`, derive a centered `1080×1080` safe-crop for X/LinkedIn/Reddit/Bluesky, keep a separate `1080×1920` video master with all text in the **center ~1080×1350 safe zone** (clears every app's UI rails). `[CONFIRMED-2026]`

---

## The OU asset set (what `make social` generates)

Implemented in [`scripts/make_social_assets.py`](scripts/make_social_assets.py) from
`championships/data/ou_all_championships.csv` — deterministic, exact pixel sizes
(`pixels = figsize_inches × dpi`, dpi=100), color-blind-aware crimson/gold/charcoal.

| Asset | Size | Trigger | Concept |
|---|---|---|---|
| `01_hero_46` (+ square) | 1080×1350 / 1080×1080 | single stat | "46" national titles hero card |
| `02_olympic_split` | 1080×1350 | surprising | "80% are Olympic-sport titles" stacked split |
| `03_title_wall` | 1080×1350 | awe / narrative | every title, sport × year dot timeline |
| `04_by_decade` | 1080×1080 | narrative | titles by decade (2010s = 12 peak) |
| `05_coaches` | 1080×1350 | dominance | 3 coaches won 25 of 46 |
| `06_cta` | 1080×1350 | — | "full data + interactive in the repo" close slide |
| `title_race.gif` | 1080×1080 | narrative arc | animated cumulative title count 1936→2026 |

Slides 01–06 also function as a **6-slide carousel** (cover → surprising stat → the wall →
the decade race → the coaches → CTA), the highest-engagement format for data content.

### The 5 reusable graphic concepts (from research)
1. **Big-number hero card** — one figure, school mark, rarity hook.
2. **Title timeline / dynasty ribbon** — dots by sport; clusters = golden eras.
3. **Bump chart vs peer schools** — OU's all-time NCAA-title rank vs rivals (built-in debate; needs a small peer dataset — *next step*).
4. **Trophy grid / "wall of banners"** — saveable wallpaper + "how many can you name?" participation post.
5. **"On this day" anniversary template** — date-stamped card auto-filled from the dataset; a year-round evergreen drip.

---

## Posting tactics

- **Caption hook in line 1:** "Oklahoma has won 46 national titles. Almost none are football →". Front-load the payoff; tell people to **save it**. `[REPORTED]`
- **Hashtags: 3–5 specific** (`#Sooners #BoomerSooner #CollegeBaseball #CWS`), not generic stuffing. `[REPORTED]`
- **Cadence:** override generic best-times with **event timing** — post around OU games and the CWS June window. Reddit sports engagement +26% YoY; CWS spikes r/collegebaseball + r/CWS. `[CONFIRMED — Reddit/Sensor Tower Mar 2026]`
- **Serialize it:** a numbered "OU title history" series outperforms one-offs (binge + return). `[REPORTED]`
- **Communities (public):** r/Sooners, r/CFB, r/collegebaseball, r/CWS, X "CFB Twitter," IG carousels+Reels, Threads. Reference `@OU_Athletics`; never impersonate.
- **Always write alt text** naming the chart type + the key number (X allows 1,000 chars, Bluesky 2,000).

## Guardrails / risks

- **No team logos or game photos.** Logos/marks are trademarked and schools/NCAA police them; game photos are copyrighted. Use **school colors + factual data + original graphics** — what this generator does. `[CONFIRMED — IP sources]`
- **Export clean, upload natively.** IG down-ranks TikTok-watermarked/recycled video ~30–70%. Re-caption per platform; don't blind cross-post. `[REPORTED]`
- **Reddit 9:1 rule.** ≥90% genuine participation before any self-promo; read each sub's sidebar; post as OC with a source line — the #1 way a data project gets banned. `[REPORTED]`
- **Engagement deflation is structural** (IG overall ER −24% YoY) — optimize for **saves/shares** and niche communities, not raw reach. `[CONFIRMED]`
- **Honesty = reach insurance.** Cite the source on the graphic; never truncate a bar axis. `[CONFIRMED]`

---

## Sources (accessed June 2026)
Socialinsider 2026 Instagram Benchmarks (35M posts); Reddit × Sensor Tower sports-fandom report (Mar 2026, via Social Media Today); Sportico "Best Sports Data Visualization 2025"; Hootsuite/Buffer/Sprout social image-size guides 2026; Datawrapper Academy (color, accessibility, fewer colors); Observable "Five ways to effectively use animation"; ScienceDirect (truncated-bar bias, peer-reviewed); Flourish (bar-chart race, social charts); NBA social graphics (Shorty Awards); PLOS One 2025 + APS (fandom psychology); Metricool short-form video 2025 + best-time-to-post 2026; trademark/fair-use sources (Trademarkia, Justia, UpCounsel); Reddit self-promotion/9:1 (multiple). Full per-claim attributions live in the research pass that generated this doc.
