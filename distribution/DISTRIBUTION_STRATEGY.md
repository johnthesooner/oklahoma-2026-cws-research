# Distribution Strategy — 2026 Oklahoma CWS Analytics Project

**Prepared:** June 22, 2026 (Game 3 is **tonight**, 7 PM ET — result pending). **Goal:** maximum reach + credibility + portfolio value.

---

## The two facts that drive everything

1. **The quantitative lane is wide open.** Live competitive scan across ESPN, CBS, D1Baseball, Baseball America, The Oklahoman, OU Daily, StorminInNorman, Reddit, YouTube found **zero opponent-adjusted, survivorship-corrected, or model-based analysis of OU's run.** The most "analytical" existing piece (StorminInNorman's "10 revealing numbers") is raw counting stats + a quoted betting line. **Nobody has quantified the improbability.** That gap *is* the product.

2. **The result is unknown until tonight → the launch must be outcome-resilient.** Build both paths now:
   - **OU wins (champion):** "The improbable title, by the numbers." Peak traffic; lean celebratory-but-rigorous.
   - **OU loses (runner-up):** "The most improbable finalist in years — and why the data already said Game 3 was a coin flip." *This is arguably the stronger, more defensible launch* because the project's model called OU the Game-3 underdog (~41%); a loss validates the rigor, a win is a bonus upset. **Either way, the honest framing wins.**

> **Strategic posture:** credibility is the moat. Every competitor is faster and more famous; none is more rigorous. Lead with *honesty and method*, not hot takes. The headline angle that fits the evidence — and is unique — is **"both underrated AND vulnerable."**

---

## 1. Target audiences

| Audience | What they care about | Best format | Where they are | Hook | Trust signal |
|---|---|---|---|---|---|
| **OU Sooners fans** | Pride, validation, "see, they were good" | Charts + narrative; celebratory | r/sooners, X, StorminInNorman, C&CM | "How a team picked 11th in the SEC reached the Finals" | Real OU box-score data, not vibes |
| **College baseball fans** | The bracket, upsets, the sport's parity | Chart thread + historical comps | r/collegebaseball, X CBB community | "12 of 18 champs since 2004 were unseeded — where OU fits" | Cites Warren Nolan/Boyd's; era-aware |
| **Sports-analytics community** | Method, opponent adjustment, model honesty | Methodology writeup + repo | X (analytics), r/dataisbeautiful, Discords | "Survivorship-corrected: champions barely separate from the Omaha field (AUC 0.55)" | Reproducible code; flags uncertainty |
| **Data-science hiring managers** | End-to-end rigor, reproducibility, judgment | Portfolio case study + GitHub | LinkedIn, GitHub | "I built a reproducible, validated 21-dataset pipeline + 14-phase analysis" | `make all`, tests, confidence tags, contradiction log |
| **Sports-media writers** | A fresh angle they can cite/quote | Pitch email + shareable chart | X, public submission pages | "The data nobody else ran on OU's run" | Sourced, tagged, willing to be quoted/corrected |
| **CBB podcasts** | A segment-worthy talking point | One stat + one chart | Public Discords (Just Baseball, Prospects Live) | "Want a 60-sec data segment on the OU run?" | Clean visual, concise insight |
| **Reddit (r/collegebaseball, r/sooners)** | Original content, no link-spam | Native image + in-thread findings | Reddit | "[OC] OU's CWS run, opponent-adjusted" | Posts data natively, link last, answers comments |
| **X/Bluesky CBB + viz** | Punchy charts, a take to react to | Single chart per post | X | "OU's HR rate doubled in June. Here's the catch." | Source on every chart |
| **LinkedIn analytics** | Process, skills, business-relevant rigor | Case-study post | LinkedIn | "What a college baseball upset taught me about survivorship bias" | Shows method + humility |
| **GitHub/portfolio reviewers** | Clean repo, README, reproducibility | The repo itself | GitHub | "Deterministic build, schema-validated data, no fabricated stats" | Tags v0.9→v1.3, CI-style validation |

## 2. Distribution channels (ranked)

| Rank | Channel | Reach | Credibility | Format | Spam risk | Best timing | CTA |
|---|---|---|---|---|---|---|
| 1 | **X/Twitter thread** | High (CBB is alive on X) | Med-High | Chart thread, 6-10 tweets | Low if chart-led | Within hours of the final | "Full analysis + code 👇" |
| 2 | **r/collegebaseball** (~368K, has "Analysis" flair) | High | High (tough crowd = credibility) | Native [OC] post | Med — verify rules | Day after final | Link in comment |
| 3 | **GitHub repo** | Med (durable) | Very High | Polished README | None | Before launch (must be live first) | Star/fork; read the report |
| 4 | **LinkedIn case study** | Med | High (for jobs) | Process post + 1 chart | Low | Day 4 | "Repo in comments" |
| 5 | **r/sooners** (~25-28K) | Med | Med | Native image | Med | Right after final | Discussion |
| 6 | **StorminInNorman / C&CM (SB Nation FanPost)** | Med | Med | Guest viz / FanPost | Low (built for it) | Day 2-3 | Embed chart |
| 7 | **Substack/Medium (flagship home)** | Low-Med initially | Med | The flagship article | None | Day 1 | Subscribe |
| 8 | **Public CBB Discords** (Just Baseball, Prospects Live) | Low-Med | Med | Drop viz in analysis channel | Low | Day 1-2 | Feedback |
| 9 | **r/dataisbeautiful** ([OC] rules) | High (broad) | Med | [OC] viz + tools comment | Med (rule-heavy) | Day 3-4 | n/a |
| 10 | **Writer/podcast outreach (X reply/quote)** | Variable (amplification) | High if they bite | 1 chart + 1 line | Med | Day 5 | "Happy to share data" |
| 11 | **Hacker News** | Spiky | Med | "Show HN: reproducible sports-data project" | Med (niche fit) | Day 4 (optional) | Repo |
| — | **YouTube short / video** | Optional | Low-Med | 60-90s chart recap | Low | Day 6 | Repo |

> **Avoid:** cold-DMing writers; link-dropping in subreddits; posting the flagship *before* the GitHub repo is public and clean.

## 3. Content packaging (the assets)

| Asset | Goal | Audience | Working title | Hook | Structure | Length | CTA |
|---|---|---|---|---|---|---|
| **Flagship article** | Definitive, citable home | CBB + analytics + writers | "Oklahoma Was Underrated *and* Vulnerable: The 2026 CWS Run in Data" | The data says both things at once | Exec summary → the mask (14-16 SEC vs #2 SOS) → power surge → opponent-adjusted truth (19-17 vs the field) → survivorship model → the Game-3 coin flip → verdict | 1,500-2,500 words + 6 charts | Repo link |
| **GitHub repo** | Credibility + portfolio | Hiring mgrs, analysts | "oklahoma-2026-cws-research" | Reproducible, validated, no fabricated stats | README → make all → report → data dictionary | — | Star, read report |
| **LinkedIn post** | Jobs/portfolio | Hiring managers | "What survivorship bias looks like in a college baseball upset" | A method lesson disguised as a sports story | Problem → what I built → 1 chart → 1 honest finding → repo | 150-250 words | Repo in comments |
| **X/Twitter thread** | Reach + amplification | CBB + viz | "Oklahoma reached the CWS Finals as an unranked, 14-16 SEC team. I pulled the data on *why* — and what the numbers say about tonight. 🧵" | Curiosity + timeliness | 1 claim/chart per tweet; end with honesty + repo | 7-9 tweets | Repo |
| **Reddit post** | Community credibility | r/collegebaseball | "[OC] How improbable was Oklahoma's 2026 CWS run? I built an opponent-adjusted, survivorship-corrected model" | Rigor + a surprising result | TL;DR → 3 findings → method note → "data/code in comment" | Medium | Link in comment |
| **5 short chart posts** | Steady drip | X/IG | (per chart below) | One stat each | Single chart + 1-line insight + source | 1 image | Thread/repo |
| **Portfolio case study** | Hiring | DS managers | "2026 OU CWS: an end-to-end sports-analytics project" | Scope + rigor + reproducibility | Problem → data eng → modeling → findings → what I'd do next | 1 page | Repo |
| **Pitch email/DM to writers** | Earned media | OU/CBB writers | (subject lines in §4) | "Free, sourced data + charts you can use" | 3 sentences: who, the finding, the offer | <120 words | "Want the charts?" |
| **Short video script** | Optional reach | Casual fans | "Why OU's run was crazier than it looked" | Fast, visual | Hook → 3 charts → honest kicker | 60-90s | Repo |
| **Dashboard/demo** | Differentiation (high effort) | Everyone | "OU 2026 Sooners stats dashboard" | The interactive page that owns the SEO term | KPI cards + sortable tables + charts | — | Share |

### The 5 lead charts (in order)
1. **Ranking trajectory** (out of the Top 25 → Omaha) — the "mask" in one image.
2. **Power surge** (HR/game ~doubled) — the most shareable single stat.
3. **Opponent tiers** (19-17 vs the NCAA field; 12-0 vs cupcakes) — the skeptical/credible one.
4. **PCA of the CWS field** (champions scattered; OU by 2022 Ole Miss) — the "wow, real analytics" one.
5. **Title-probability triangulation** (ELO 41% + market 44% + history 33%) — the timely Game-3 one.

## 4. Headlines (ranked)

### 20 article headlines (best first)
1. **Oklahoma Was Underrated *and* Vulnerable: The 2026 CWS Run in Data**
2. The Data Behind Oklahoma's Improbable College World Series Run
3. How a 14-16 SEC Team Reached the College World Series Finals
4. Oklahoma's Run Looks Like 2022 Ole Miss — Until You Check the Pitching
5. I Built a Model for Oklahoma's CWS Run. It Said the Title Was a Coin Flip.
6. Oklahoma Wasn't Lucky. They Were Misread. (Mostly.)
7. The Numbers Say Oklahoma Is Both the Most Underrated *and* Most Vulnerable Team in Omaha
8. What 21 Datasets Say About Oklahoma's College World Series Run
9. Survivorship Bias, Explained by Oklahoma's 2026 Baseball Team
10. Oklahoma vs North Carolina: The 2026 CWS Finals, by the Numbers
11. The Schedule Hid Them: Oklahoma's 2026 Season, Opponent-Adjusted
12. Oklahoma Out-Homered the Field in Omaha. Here's What That Hides.
13. Once You Reach Omaha, the Title Is a Coin Flip — and the Data Proves It
14. The 14-16 Team That Beat Three Top-7 Seeds: Oklahoma, Quantified
15. Deiten Lachance Hit 0 Homers, Then 18. The Anatomy of a Power Surge.
16. A Freshman Rebuilt Oklahoma's Rotation in June. The Data Tells the Story.
17. How Improbable Was Oklahoma's Run? I Ran the Numbers.
18. Oklahoma's CWS Run: Sustainable Strength, Hot Streak, or Lucky Draw?
19. The Most Improbable College World Series Finalist in Years
20. Reproducible, Sourced, Skeptical: A Data Case Study of Oklahoma's 2026 Run

### 10 tweet hooks
1. "Oklahoma reached the CWS Finals as an unranked, 14-16 SEC team. I pulled the data on *why*. 🧵"
2. "Everyone says Oklahoma 'got hot.' I tried to quantify it. The answer is more interesting. 🧵"
3. "Oklahoma's HR rate roughly *doubled* in the postseason. But opponent-adjusted, they were a .500 team vs the NCAA field. Both are true. 🧵"
4. "I built a survivorship-corrected model of every CWS team since 2021. Champions barely separate from the field. Here's what that means for OU. 🧵"
5. "Before Game 3: ELO says 41%, the market says 44%, and history says the team that won Game 1 and lost Game 2 wins the decider just 4 of 12 times. 🧵"
6. "Oklahoma's closest statistical match? 2022 Ole Miss — until you look at the pitching. 🧵"
7. "Nobody had run the numbers on Oklahoma's run, so I did. 21 datasets, reproducible, sourced. 🧵"
8. "The stat that explains Oklahoma's season: +112 run differential, but most of it came vs sub-.500 cupcakes. 🧵"
9. "Deiten Lachance: 0 HR through April 9, then ~18. I charted the surge. 🧵"
10. "How do you tell skill from luck in a 3-week tournament run? I tried. (Spoiler: it's mostly variance.) 🧵"

### 10 LinkedIn hooks
1. "A college baseball upset is the best survivorship-bias lesson I've found. Here's the project."
2. "I built an end-to-end sports-analytics project: 21 schema-validated datasets, a deterministic build, zero fabricated stats. Here's what I learned."
3. "How do you separate 'good team' from 'got hot'? I spent a week trying to answer that with data."
4. "The hardest part of this analysis wasn't the modeling — it was refusing to fabricate the metrics that don't exist."
5. "What an unranked baseball team taught me about opponent-adjustment and honest uncertainty."
6. "I made my sports-data project reproducible (make all, validation, confidence tags). Here's why that matters for any analytics work."
7. "My model said the title was a coin flip. Win or lose tonight, here's why I'm comfortable with that."
8. "I kept a 'contradictions log' of every place my own analysis was wrong. Best decision of the project."
9. "Raw stats lie. Here's the same team before and after opponent-adjustment."
10. "A portfolio project that's actually reproducible: data dictionary, schema validation, sourced every number."

### 10 Reddit titles
1. "[OC] How improbable was Oklahoma's 2026 CWS run? Opponent-adjusted + survivorship-corrected analysis"
2. "[OC] Oklahoma was 19-17 against the NCAA tournament field this year. Their +112 run diff was mostly cupcakes."
3. "[OC] I modeled every CWS participant 2021-2025. Champions barely separate from the field (AUC 0.55)."
4. "[OC] Oklahoma's postseason HR rate vs regular season, charted"
5. "[OC] OU's closest statistical comp among champions is 2022 Ole Miss — with one big difference (pitching)"
6. "[OC] Game 3 by the numbers: ELO, betting market, and the historical base rate all agree"
7. "[OC] Visualizing Oklahoma's path: every CWS opponent by quality tier"
8. "[OC] The 'power surge' was real — here's exactly how big, and what it hides"
9. "[OC] A reproducible data project on Oklahoma's 2026 run (21 datasets, code included)"
10. "[OC] Deiten Lachance's 0-to-18 home run season, visualized"

### 5 writer-pitch subject lines
1. "Free charts: the data nobody ran on OU's CWS run"
2. "Opponent-adjusted: OU was 19-17 vs the NCAA field (sourced data + viz, yours to use)"
3. "A data angle on the OU run you might not have seen"
4. "Sourced charts on Oklahoma's CWS run — happy to share"
5. "The numbers behind OU's run (reproducible, cite-able)"

**Ranking logic:** lead with **honesty + specificity** (#1, #3 article; tweet #1, #3, #5). The "both underrated and vulnerable" and "19-17 vs the field" angles are unique, defensible, and survive any Game-3 outcome. Avoid pure-hype ("impossible run") as the *primary* — use it as a secondary spike grab.

## 5. SEO & search demand

> Volumes are **directional** (no paid keyword tool) — High/Med/Low inferred from who ranks + SERP freshness. A direct query for "OU 2026 CWS advanced metrics / data viz" returned the school site, recaps, and a stray softball schedule — **zero analytics content.** The gap is confirmed.

| Keyword | Intent | Vol (dir.) | Spike/Evergreen | Who ranks now | Winnable data angle | SEO title (≤60) |
|---|---|---|---|---|---|---|
| 2026 College World Series results / champion | News | High | Spike (tonight) | NCAA, ESPN, Wiki | Post-final box + win-prob chart | 2026 College World Series Results: OU vs UNC Final |
| Oklahoma vs North Carolina baseball (CWS finals) | News | High | Spike | NCAA, CBS, Yahoo | Head-to-head metric breakdown of the 3 games | OU vs UNC 2026 CWS Finals: The Numbers Behind It |
| **Oklahoma baseball stats 2026** | Info | Med | **Evergreen (best ROI)** | soonersports, SoonerStats, Wiki (raw tables) | Interactive sortable dashboard | Oklahoma Baseball Stats 2026: Full Sooners Dashboard |
| Oklahoma baseball 2026 / OU baseball | Nav/info | High (brand) | Evergreen+spike | soonersports, Wiki, ESPN | Season dashboard: run-diff trend, HR timeline | Oklahoma Baseball 2026: The Sooners' CWS Run in Data |
| **Deiten Lachance** (+ "Deitan LaChance" misspelling) | Info | Med (rising) | Spike | roster, ESPN, Yahoo | 0→18 HR spray + monthly OPS chart | Deiten Lachance 2026 Stats: The Sooners' Power Surge |
| OU baseball CWS / Oklahoma College World Series | Info/nav | Med-High | Spike+tail | soonersports, NCAA, Wiki | 1951/1994/2026 charted comparison | Oklahoma in the College World Series: A Data History |
| **2026 College World Series stats / analytics** | Info | Low-Med | Evergreen | NCAA stats, BA | Field-wide Omaha advanced leaderboard (unowned) | 2026 College World Series Stats & Analytics Breakdown |
| Cord Rager / Dayton Tockey | Info/nav | Low-Med | Spike | roster, SI, OUDaily | Freshman workload / JUCO-clutch single-stat hooks | Cord Rager: How a Freshman Became OU's October Arm |
| college baseball analytics | Info | Med (competitive) | Evergreen | SABR, .edu, GoRout | Applied OU case study, not generic explainer | College Baseball Analytics: A 2026 CWS Case Study |

**Meta description pattern:** "{Insight} — a data-driven breakdown of Oklahoma's 2026 College World Series run: {metric}, {metric}, fully sourced and charted."

**SEO playbook:** (a) publish the **OU vs UNC result** data piece within *hours* of tonight's final (two headline variants pre-written) to ride the spike; (b) the **"Oklahoma baseball stats 2026" dashboard** is the durable evergreen winner — build it to outlast the news; (c) hedge the **Lachance spelling** (target both "Deiten Lachance" and the "Deitan LaChance" the wire services indexed); (d) interlink all pages to the flagship.

## 6. Competitive scan & differentiation

**Verdict: the field is wide open.** Every accessible piece is narrative or raw counting stats — no opponent adjustment, no survivorship correction, no sabermetrics, no disclosed models.

| Source | Type | Has data/analytics? | Cite or respond? |
|---|---|---|---|
| StorminInNorman "10 revealing numbers" | OU fan listicle | Closest — but raw counts + a quoted odds line | **Respond** (the foil; do the adjustment they skip) |
| CBS "tale of the tape" picks | National preview | Box-score ERA/AVG/HR only | **Respond** (the box-score-only contrast) |
| ESPN championship preview | National narrative | No (the "got hot" framing) | **Cite** (the story your data complicates) |
| D1Baseball / Baseball America | National | Recaps; premium unread/paywalled | **Cite** as authority; don't duplicate |
| College Splits (Substack) | Independent analytics | Yes — but preseason, no OU CWS case | **Cite** as method peer (shows you know the field) |
| SABR Tooth Tigers (Medium) | Independent | D1 run-expectancy *methodology* only | **Cite** as a caveat if you publish win-prob |
| The Oklahoman / Sooners Wire | OU beat | Narrative (paywall/blocked) | Light cite |
| YouTube ("Wheels"), Reddit | Social | Highlights / discussion, no model | Engage, don't cite |

**Differentiation in one line:** *every* rating system already disagrees about OU (RPI #9, CBR #15, Boyd's ~#18, SEC ~11th) yet OU went 3-0 in Omaha — **the gap between résumé ratings and the tournament outcome is the survivorship/opponent-adjustment story nobody wrote.** That's the wedge.

**Free data sources to credit (shows rigor):** Warren Nolan (RPI/SOS/ELO), Boyd's World (ISR), collegebaseballratings.com (CBR/WAB), The Lab Analytics (BaseRuns), Baseball-Reference college register, ESPN box scores.

## 7. Outreach list (public-facing only — no private contacts)

> Lead with the **insight/visual**, never "check out my project." Verify each subreddit's rules and any handle before sending.

### Tier 1 — OU-specific, analytics-friendly (start here)
| Target | Public handle/page | Approach | Risk |
|---|---|---|---|
| Stormin' In Norman (FanSided) | @StorminInNorman / stormininnorman.com (ed. Dekota Gregory) | Reply with one chart; offer an embeddable graphic/guest viz via public contact | Low |
| Crimson & Cream Machine (SB Nation) | @CCMachine / crimsonandcreammachine.com | Tag on a punchy stat graphic; **SB Nation FanPost** is a built-in public submission path | Low |
| OU Daily Sports | @OUDailySports / oudaily.com/sports | Share viz; note you're an OU-adjacent analyst | Low |
| r/sooners (~25-28K, verify) | reddit.com/r/sooners | Native image post during/after a game, link last | Med |

### Tier 2 — National CBB reach / amplification
| Target | Public handle | Approach | Risk |
|---|---|---|---|
| r/collegebaseball (~368K; has "Analysis" flair) | reddit.com/r/collegebaseball | Native [OC] analysis post; engage in comments | Med |
| Kendall Rogers (D1Baseball) | @kendallrogersd1 | Quote-tweet a D1B post with one OU chart + one-line insight | Med |
| Aaron Fitt (D1Baseball) | @aaronfitt | Same; lead with the finding | Med |
| D1Baseball (outlet) + podcast | @D1Baseball | Tag on standout visuals | Med |
| Baseball America + podcast | @BaseballAmerica | Reply to their CWS coverage with a complementary chart | Med |
| Mike Rooney (ESPN CBB analyst) | @Mike_Rooney | Reply during a broadcast moment your data speaks to | Med |
| Kiley McDaniel (ESPN) | @kileymcd | Frame a viz around a draft-eligible OU player | Med |

### Tier 3 — Podcasts / Discords (lowest-friction submission)
| Target | Public channel | Approach | Risk |
|---|---|---|---|
| Just Baseball (College Baseball Show) | @JustBB_Media + **public Discord** | Drop the viz in the analysis channel; tag on X if it lands | Low-Med |
| Prospects Live (College Baseball Now) | @ProspectsLive + **public Discord** | Share in Discord; tag around an episode | Med |
| Locked On Sooners | public show pages | Offer an OU CWS data segment | Low-Med |

### Tier 4 — Data-viz / analytics amplifiers
| Target | Public handle | Approach | Risk |
|---|---|---|---|
| r/dataisbeautiful | reddit.com/r/dataisbeautiful | [OC] post + required source/tools comment | Med (rule-heavy) |
| Russell Carleton (BP) | @pizzacutter4 | Engage on method | Med |
| Sports-viz practitioners | public X accounts | Ask for a craft critique (viz people reshare viz) | Low |

**Caveats:** subscriber counts approximate (Reddit was tool-blocked — verify in-sidebar). Confirm Peter Flaherty's current handle on his BA author page. Teddy Cahill reportedly left BA — skip. **No private contact info was gathered or used.**

## 8. Seven-day launch calendar (two-track: champion / runner-up)

> **Pre-req (do before Day 0):** GitHub repo public + clean; flagship drafted with **both** result variants; 5 charts exported; "To finalize v1.4" pass ready to run the instant Game 3 ends.

| Day | Asset | Platform | Posting text (seed) | Goal | Success metric |
|---|---|---|---|---|---|
| **0 (today)** | Teaser | X + r/sooners game thread | "Whatever happens in Game 3, I spent a week pulling the data on OU's run — opponent-adjusted, survivorship-corrected, reproducible. Dropping the full breakdown after the final. One preview chart 👇 (ranking trajectory)" | Plant a flag pre-result; bank the chart | Engagement; saved/quoted |
| **1** | Flagship article + result data piece | Substack/Medium + X thread | Result-specific headline (champion or runner-up variant) + the 7-tweet thread | Definitive, citable home; ride the spike | Article reads; thread impressions |
| **2** | Chart thread (the 5 charts) | X (+ cross-post IG) | One chart/tweet, source on each, honest kicker | Reach + shareability | Reshares of charts 2 & 3 |
| **3** | Reddit [OC] post | r/collegebaseball (then r/sooners) | "[OC] How improbable was OU's run? Opponent-adjusted + survivorship-corrected" — findings in-thread, link in comment | Credibility with the tough crowd | Upvotes; quality comments |
| **4** | Case study | LinkedIn + GitHub README polish | "What survivorship bias looks like in a college baseball upset" + 1 chart, repo in comments | Portfolio/jobs | Profile views; recruiter DMs |
| **5** | Outreach | X replies/quotes + public Discords + SB Nation FanPost | Tier-1/2 targets: 1 chart + 1 line + "happy to share the data" | Earned amplification | A writer/pod reshare or feature |
| **6** | Short video / chart recap | YouTube Short / X video | 60-90s: 3 charts + honest kicker | Casual-fan reach | Views; new repo visits |
| **7** | Model self-evaluation | X + LinkedIn + repo (predictions ledger) | "How my pre-Game-3 model did: ELO 41% / market 44% / history 33% vs what happened. Here's the scorecard." | Credibility loop; close the story honestly | Engagement; "this is rigorous" sentiment |

## 9. Risk & tone

**Risks → mitigations**
- *Looks like self-promotion* → lead with the chart/insight; link last; participate in comments; never copy-paste the same blurb across subs.
- *Angering fan communities* → frame as pro-curiosity, not anti-OU/anti-UNC; in r/sooners, celebrate the run *and* be honest; don't dunk.
- *Overclaiming* → keep the project's [CONFIRMED]/[REPORTED]/[ESTIMATED]/NOT AVAILABLE tags visible; never present estimates as fact.
- *Unofficial stats* → cite official OU cumulative + ESPN box scores; flag estimated/blocked sources (you already do).
- *Posting before the final* → Day 0 is a *teaser only*, explicitly result-agnostic; no result claims until the box score is final.
- *Model-error dunking* → pre-empt it: publish the model's uncertainty up front; the Day-7 self-evaluation turns a "miss" into a credibility win.
- *Generic SEO feel* → the moat is interpretation + reproducibility; never publish a thin recap.

**Tone guidelines**
- **Transparent** — show sources, code, and what you couldn't get (the NOT-AVAILABLE list is a feature).
- **Fan-aware** — respect the fandom; you're adding to the conversation, not correcting it.
- **Evidence-first** — every claim has a chart or a citation.
- **Humble about uncertainty** — "the data suggests," not "the data proves"; lead with ranges.
- **No "I called it" arrogance** — the model framed Game 3 as a coin flip; present it that way win or lose.
- **Invite corrections** — "tell me where this is wrong" outperforms certainty with analytics crowds and builds trust.

## 10. Final distribution strategy

1. **Best launch format:** a **flagship article** (the definitive, citable home) + a **chart-led X thread**, both anchored to the **public GitHub repo**.
2. **Best headline:** **"Oklahoma Was Underrated *and* Vulnerable: The 2026 CWS Run in Data."** (Unique, defensible, outcome-proof.)
3. **Best first platform:** **X/Twitter** for the spike (Day 0 teaser → Day 1 thread), with **GitHub live first** as the credibility anchor.
4. **Best audience wedge:** the **sports-analytics + college-baseball crowd on X and r/collegebaseball** — they reward rigor, reshare charts, and confer credibility that spills to fans and recruiters.
5. **Best chart to lead with:** the **ranking trajectory** (out of the Top 25 → Omaha) — it tells the whole "mask" story instantly; follow with the **power-surge** chart.
6. **Best writer/podcast targets:** **Kendall Rogers / Aaron Fitt / D1Baseball** and **Baseball America** (quote-tweet amplification); **Just Baseball** & **Prospects Live** public Discords (lowest-friction); **StorminInNorman / C&CM FanPost** for OU reach.
7. **Best Reddit approach:** **native [OC] post in r/collegebaseball** (it has an "Analysis" lane), findings in-thread, code link in a comment — *not* a link drop.
8. **Best LinkedIn framing:** a **method/portfolio story** ("survivorship bias, via a baseball upset") that shows reproducibility and judgment to hiring managers.
9. **Best GitHub/portfolio framing:** "**reproducible, schema-validated, no fabricated stats**" — the README leads with `make all`, the data dictionary, and the confidence framework.
10. **Exact 7-day rollout:** §8 above (two-track for champion vs runner-up; Day 0 teaser today, flagship Day 1 after the final, self-evaluation Day 7).

### Prioritized checklist — do these first
1. **Tonight, before the result:** make the **GitHub repo public and clean** (README front-and-center, `make all` green). Nothing else ships until this is live.
2. **Tonight:** post the **Day-0 teaser** (result-agnostic) on X + the r/sooners game thread with the ranking-trajectory chart.
3. **Pre-write both flagship variants** (champion / runner-up) and export the 5 lead charts now.
4. **The instant Game 3 ends:** run the v1.4 finalization pass (fill the box score, flip banners, name the MOP), then publish the **result data piece + flagship + X thread** within hours.
5. **Day 3:** the **r/collegebaseball [OC]** post (highest-credibility reach).
6. **Day 4:** the **LinkedIn case study** + final README polish for recruiters.
7. **Day 5:** outreach — quote-tweet D1Baseball/BA with one chart; drop the viz in the Just Baseball / Prospects Live Discords; submit a FanPost.
8. **Day 7:** the **model self-evaluation** (honesty loop) — turns the prediction into a credibility asset regardless of who won.

> **North star:** you will never out-speed or out-famous ESPN/D1Baseball. You can out-*rigor* them — and right now, on this team, nobody else is even trying. Lead with honesty and method, and the credibility compounds into portfolio and reach.

