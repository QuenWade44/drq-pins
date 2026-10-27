# Pinterest Strategy · School Templates By Dr. Q

Every weekly run reads this file first. It is the standing brief for all 52 weeks.

## 1. Objective

The goal is TPT sales, not Pinterest vanity numbers. Each week, publish one fresh pin for every live TPT product (220 pins). Every pin links straight to that product's TPT page.

| Funnel step | What it means | Pinterest/TPT metric | What drives it |
|---|---|---|---|
| Discovery | A teacher searches Pinterest and sees the pin | Impressions | Keyword-rich title, description and keywords; the right board; steady fresh pins; seasonal timing |
| Interest | The teacher stops and clicks | Outbound clicks, outbound CTR | Product name as the big headline; a clear "who it's for" hook; a real cover image |
| Conversion | The teacher buys on TPT | TPT views → sales | A strong TPT listing (title, previews, price); the pin promises exactly what the listing delivers |

**North star:** outbound clicks to TPT each month, and TPT sales.

Ignore follower counts. Saves are a secondary signal.

## 2. Theme of a fresh pin

- A fresh pin is a new image, never a repin. It gets a new color theme, tilt and hook each week, and links to the same TPT product.
- **Headline** is the product name, e.g. "WISC-V Report Template". This is what people search for.
- **Hook** is one short line above the headline, aimed at the audience or the benefit. Examples: "For school SLPs", "Report cards in minutes".
- **Visual** is the real product cover for products made in Batches 1–6. Older report templates use a School-Templates-style report-page graphic.
- **Branding** is always "School Templates By Dr. Q". Never use Psych Report Assistant branding.
- **Color themes** rotate every 4 weeks: white, light aqua, black, dark aqua. Hooks rotate from catalog.json unless the weekly plan overrides them.

## 3. Rules (do not break)

1. **Be honest.** No invented statistics, no "best-selling" or "#1" claims, no testimonials, and no time-saved numbers ("half the time"). Describe only what is actually in the product.
2. **Use test names as plain descriptive references.** Keep ® where the TPT title uses it. Never imply endorsement by test publishers or state agencies.
3. **One pin per product per week.** Don't flood any single URL.
4. **Board names must exactly match catalog.json.** Pinterest creates a new board if a name doesn't match.
5. **Stay within Pinterest's limits.** Titles are 100 characters or fewer and descriptions are 500 or fewer. Each CSV holds at most 200 rows, so always split into two files.
6. **Media URLs** must be public raw GitHub links under week-NN/.

## 4. Weekly research (real-time search) → plan file

Each week, run 3–5 web searches. Use them to decide what to emphasize, then write `plans/week-NN.json`.

**What to look for:**
- **The school calendar for the target week, US-wide.** See the seasonal map below.
- **Current education news that affects demand.** Examples: new state reading laws, IEP or legal deadlines, testing windows, new test editions.
- **Pinterest education trends.** If a trends source is reachable, use it. If not, rely on the seasonal map.

**Seasonal map (pin 2–6 weeks ahead of the need):**
| Months | Focus boards (by number) |
|---|---|
| Aug–Sep | 12 sub plans, 11 paras, 2 IEP, 7 reading data (BOY benchmarks), 9 SLP, 10 counselor |
| Oct–Nov | 8 report cards and conferences, 5 MTSS, 7 reading data, 4 behavior |
| Dec–Jan | 7 MOY benchmarks, 8 report cards (2nd quarter), 6 state reading plans, 1 evaluations |
| Feb–Mar | 1 school psych (evaluation season), 2 IEP (annual reviews), 5 MTSS, 6 reading plans |
| Apr–May | 2 IEP plus transition, 7 EOY benchmarks, 8 report cards, 3 data trackers, 1 reevaluations |
| Jun–Jul | 1 school psych and summer report prep, 2 IEP planning, 11 para binder, 12 teacher organization |

**Plan file schema** (every key is optional):
```json
{
  "week": 2,
  "start": "2026-11-04",
  "research_notes": ["one line per finding, with source URL"],
  "focus_boards": {"8": 3, "5": 2, "7": 2},
  "hooks": {"8": "Report cards in minutes", "1": "Evaluation season, simplified"},
  "ribbons": {"8": "Report card season"},
  "extra_keywords": {"8": ["report card comments November"]},
  "winners": ["18086254"]
}
```
- `focus_boards` puts those boards' pins in prime-time slots (6–10 pm Central and weekends).
- `hooks` replaces the default hook for a board this week. Use 34 characters or fewer.
- `ribbons` adds a small seasonal tag on the pin. Use 22 characters or fewer, and only when the season clearly applies.
- `winners` lists product IDs with outbound clicks or sales, taken from data/. They get prime-time slots.

## 5. Learning loop (data/)

Monthly, Q drops exports into data/:
- `pinterest_*.csv`: a Pinterest Analytics export (top pins, outbound clicks)
- `tpt_*.csv`: TPT sales or product stats

Each run reads the newest files and works out:
- **Top 20 products** by outbound clicks or sales. Add these to `winners`.
- **Boards with impressions but low CTR.** Test new hooks for those boards.
- **Products with zero impressions after 8 weeks.** Flag these to Q as listings to retitle on TPT.

Summarize the findings in 3 lines in the run report.

## 6. Schedule

- One run every Sunday morning (Central). It builds the pins for Wednesday through Tuesday.
- Week 1 started 2026-10-28. Week N starts on 2026-10-28 + 7×(N−1) days.
- The program ends after week 52 (starting 2027-10-20). After week 52, stop and tell Q.
