"""School Templates By Dr. Q — weekly fresh-pin generator (self-contained; run from the repo root).

    python3 system/make_pins.py --week 2 --start 2026-11-04 [--plan plans/week-02.json]

Reads system/catalog.json (220 products) and an optional weekly plan written by the research step.
Writes week-NN/*.jpg (one fresh 1000x1500 pin per product, 200/week) and two upload files:
  week-NN/DrQ_WeekNN_A_upload-Wed-MonDD.csv (100 pins, Wed-Fri) and DrQ_WeekNN_B_upload-Sat-MonDD.csv (100 pins, Sat-Tue)
(Pinterest bulk upload: max 200 rows per file). Times are scheduled in America/Chicago and written as UTC.
"""
import os, sys, json, csv, random, argparse, datetime as dt
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = os.path.join(ROOT, "system")
RAW = "https://raw.githubusercontent.com/QuenWade44/drq-pins/main"
PRO = "Created by a school psychologist (Ph.D.) and former 1st Grade Teacher of the Year."
CT, UTC = ZoneInfo("America/Chicago"), ZoneInfo("UTC")

BLACK, WHITE, AQUA, AQUA_DARK, AQUA_SOFT, GRAY = (17, 17, 17), (255, 255, 255), (0, 184, 186), (0, 128, 130), (224, 247, 247), (110, 110, 110)
F = os.path.join(SYS, "fonts")
bold = lambda s: ImageFont.truetype(os.path.join(F, "Poppins-Bold.ttf"), s)
med = lambda s: ImageFont.truetype(os.path.join(F, "Poppins-Medium.ttf"), s)
THEMES = [(WHITE, BLACK, AQUA_DARK, GRAY), (AQUA_SOFT, BLACK, AQUA_DARK, GRAY), (BLACK, WHITE, AQUA, (200, 200, 200)), (AQUA_DARK, WHITE, (190, 245, 245), (225, 245, 245))]


def text_w(d, t, f):
    l, _, r, _ = d.textbbox((0, 0), t, font=f)
    return r - l


def monogram(d, cx, cy, size):
    r = size // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AQUA)
    f = bold(int(size * 0.34))
    d.text((cx, cy), "Dr. Q", font=f, fill=WHITE, anchor="mm")


def shadowed(base, card, xy, angle=-3, blur=16, alpha=110, offset=(10, 18)):
    card = card.convert("RGBA")
    rot = card.rotate(angle, expand=True, resample=Image.BICUBIC)
    pad = blur * 3
    mask = Image.new("L", (rot.width + 2 * pad, rot.height + 2 * pad), 0)
    mask.paste(rot.split()[3].point(lambda a: alpha if a > 0 else 0), (pad, pad))
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGBA", mask.size, (0, 0, 0, 255)); sh.putalpha(mask)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(sh, (xy[0] + offset[0] - pad, xy[1] + offset[1] - pad))
    base.alpha_composite(layer)
    base.alpha_composite(rot, xy)


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if text_w(d, t, font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def fitwrap(d, text, fn, size, maxw, maxlines):
    while size > 28:
        f = fn(size); ls = wrap(d, text, f, maxw)
        if len(ls) <= maxlines:
            return f, ls
        size -= 3
    return fn(size), wrap(d, text, fn(size), maxw)[:maxlines]


def doc_card(p, w=660, h=820):
    card = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, w, 14], fill=AQUA)
    d.text((40, 50), "SCHOOL PSYCHOLOGY", font=bold(22), fill=AQUA_DARK)
    f, ls = fitwrap(d, p["name"], bold, 46, w - 80, 2)
    y = 88
    for l in ls:
        d.text((40, y), l, font=f, fill=BLACK); y += f.size + 8
    d.line([40, y + 10, w - 40, y + 10], fill=AQUA, width=4)
    y += 40
    if p["kind"] == "test":
        d.rectangle([40, y, w - 40, y + 44], fill=BLACK)
        for x, t in ((56, "Index / Composite"), (w - 300, "Score"), (w - 160, "%ile")):
            d.text((x, y + 10), t, font=bold(20), fill=WHITE)
        y += 44
        for i in range(6):
            d.rectangle([40, y, w - 40, y + 46], fill=(242, 251, 251) if i % 2 else WHITE, outline=(210, 210, 210))
            d.rectangle([56, y + 14, 56 + 180 + (i * 23) % 70, y + 30], fill=(205, 205, 205))
            d.rectangle([w - 300, y + 10, w - 230, y + 36], fill=(255, 242, 0))
            d.rectangle([w - 160, y + 10, w - 100, y + 36], fill=(255, 242, 0))
            y += 46
        y += 30
    for i in range(13):
        ln = w - 80 - (i * 37) % 160
        d.rectangle([40, y, 40 + ln, y + 12], fill=(215, 215, 215)); y += 30
        if y > h - 60:
            break
    return card


def make_pin(p, week, hook, ribbon, out):
    W, H = 1000, 1500
    bg, hc, ac, sc = THEMES[(week - 1) % 4]
    img = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(img)
    pill = p["fmt"]
    pw = text_w(d, pill, bold(24)) + 44
    d.rounded_rectangle([70, 64, 70 + pw, 112], radius=24, fill=ac if bg != WHITE else BLACK)
    d.text((70 + pw // 2, 88), pill, font=bold(24), fill=WHITE if bg in (WHITE, AQUA_SOFT) else BLACK, anchor="mm")
    if ribbon:  # optional seasonal ribbon, top right
        rf = bold(22); rw = text_w(d, ribbon.upper(), rf) + 40
        d.rounded_rectangle([W - 70 - rw, 64, W - 70, 112], radius=24, outline=ac, width=3)
        d.text((W - 70 - rw // 2, 88), ribbon.upper(), font=rf, fill=ac, anchor="mm")
    hf, hls = fitwrap(d, hook.upper(), bold, 34, W - 140, 1)
    d.text((70, 140), hls[0], font=hf, fill=ac)
    nf, nls = fitwrap(d, p["name"], bold, 84, W - 140, 2)
    y = 192
    for l in nls:
        d.text((70, y), l, font=nf, fill=hc); y += nf.size + 8
    if p["sub"]:
        sf, sls = fitwrap(d, p["sub"], med, 32, W - 140, 1)
        d.text((70, y + 16), sls[0], font=sf, fill=sc); y += 60
    top = max(y + 30, 470)
    ang = [-3, 3, -2, 2, -4, 4][(week - 1) % 6]
    if p["cover"]:
        size = min(820, 1290 - top)
        th = Image.open(os.path.join(SYS, p["cover"])).convert("RGB").resize((size, size), Image.LANCZOS)
        shadowed(img, th, ((W - size) // 2 - 10, top), angle=ang)
    else:
        card = doc_card(p)
        hmax = 1290 - top
        if card.height > hmax:
            card = card.resize((int(card.width * hmax / card.height), hmax), Image.LANCZOS)
        shadowed(img, card, ((W - card.width) // 2 - 10, top), angle=ang, alpha=120)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1330, W, H], fill=BLACK if bg != BLACK else AQUA_DARK)
    monogram(d, 140, 1415, 110)
    d.text((220, 1372), "School Templates By Dr. Q", font=bold(40), fill=WHITE)
    d.text((220, 1426), "Editable · Shop on TPT", font=med(30), fill=(0, 220, 222) if bg != BLACK else WHITE)
    img.convert("RGB").save(out, quality=84, optimize=True)


def copy_for(p, hook, cat, kw_extra):
    b = p["board"]; bkw = cat["board_keywords"][str(b)]
    if p["kind"] == "test":
        acr = p["name"].replace(" Report Template", ""); full = p["sub"]
        title = f"{acr} Report Template | {full} Write-Up | School Psychologist"
        desc = (f"Write {acr} reports faster. This editable Word template gives you organized score tables and interpretive write-up sections for "
                f"{acr} results, ready to customize for each psychoeducational evaluation. {PRO} Find it on TPT: School Templates By Dr. Q.")
        kw = [f"{acr} report template", f"{acr} write up", "school psychologist report template", "psychoeducational evaluation", "school psychology"]
    elif p["kind"] == "doc":
        title = f"{p['name']} | {p['sub']} | School Psychologist Templates"
        desc = (f"{p['name']}: {p['sub'][0].lower() + p['sub'][1:]}. An editable template that saves time on evaluation and special education paperwork. "
                f"{PRO} Find it on TPT: School Templates By Dr. Q.")
        kw = [p["name"].lower(), "school psychologist", "special education forms", "editable template"] + bkw[:2]
    else:
        title = p["title"]; lead = p["lead"]
        if len(lead) > 330:
            cut = lead[:330].rfind(".")
            lead = lead[:cut + 1] if cut > 0 else lead[:330]
        desc = f"{lead} {PRO} Find it on TPT: School Templates By Dr. Q."
        kw = p["tags"] + bkw[:2]
    if len(title) > 100:
        title = title[:title[:100].rfind(" |")]
    seen, kws = set(), []
    for k in kw + kw_extra:
        if k and k.lower() not in seen:
            seen.add(k.lower()); kws.append(k)
    return title, desc[:500], ", ".join(kws[:8])


# Pinterest holds at most 100 scheduled Pins at a time (confirmed by Pinterest's
# "More than 100 scheduled Pins" rejection email, Oct 2026). So each week is two
# uploads of 100 pins, and file A has fully published before file B is uploaded.
PER_FILE = 100
SKIP = 20                       # 220 products -> 200 pins/week; 20 rotate out
FIRST_PIN = 15 * 60             # first pin of each file: 3:00 pm Central on upload day
DAY_W = [1.0, 1.0, 1.0, 1.0, 1.05, 1.2, 1.3]   # Mon..Sun


def file_slots(days, n, prime_share=0.45):
    """n publish times (UTC, is_prime) spread over days=[(date, earliest_minute)], Central time."""
    w = []
    for d, first in days:
        frac = (max(0, 1050 - max(390, first)) + (1320 - max(1080, first))) / (660 + 240)
        w.append(DAY_W[d.weekday()] * frac)
    counts = [int(n * x / sum(w)) for x in w]
    order = sorted(range(len(days)), key=lambda i: -w[i])
    for i in range(n - sum(counts)):
        counts[order[i % len(order)]] += 1
    out = []
    for (d, first), c in zip(days, counts):
        a0 = max(390, first); a_len = max(0, 1050 - a0)       # daytime 6:30 am - 5:30 pm
        p0 = max(1080, first); p_len = 1320 - p0              # prime 6:00 - 10:00 pm
        prime = round(c * prime_share) if a_len else c
        early = c - prime
        mins = [(a0 + int(k * a_len / max(1, early)), False) for k in range(early)]
        mins += [(p0 + int(k * p_len / max(1, prime)), True) for k in range(prime)]
        for m, is_prime in sorted(mins):
            local = dt.datetime.combine(d, dt.time(m // 60, m % 60), tzinfo=CT)
            out.append((local.astimezone(UTC).replace(tzinfo=None), is_prime))
    return out


def week_files(start):
    """File A: upload Wednesday, pins Wed 3 pm - Fri 10 pm. File B: upload Saturday, pins Sat 3 pm - Tue 10 pm."""
    wed = start; sat = start + dt.timedelta(days=3)
    a_days = [(wed, FIRST_PIN), (wed + dt.timedelta(days=1), 0), (wed + dt.timedelta(days=2), 0)]
    b_days = [(sat, FIRST_PIN)] + [(sat + dt.timedelta(days=i), 0) for i in (1, 2, 3)]
    return [("A", wed, file_slots(a_days, PER_FILE)), ("B", sat, file_slots(b_days, PER_FILE))]


def pick_skips(week, prods, protected):
    """Rotate SKIP products out each week, oldest-skipped first, never focus boards or winners."""
    path = os.path.join(SYS, "rotation.json")
    rot = json.load(open(path)) if os.path.exists(path) else {}
    last = {}
    for k, ids in rot.items():
        wk = int(k.split("-")[1])
        if wk < week:
            for i in ids:
                last[i] = max(last.get(i, 0), wk)
    cands = [p["id"] for p in prods if p["id"] not in protected]
    cands.sort(key=lambda i: (last.get(i, 0), (int(i) * 2654435761 + week) % 1000003))
    skips = sorted(cands[:SKIP])
    rot[f"week-{week:02d}"] = skips
    json.dump(dict(sorted(rot.items())), open(path, "w"), indent=1)
    return set(skips)


def build(week, start, plan):
    cat = json.load(open(os.path.join(SYS, "catalog.json")))
    hooks = cat["hooks"]
    ph = plan.get("hooks", {})                      # board -> hook (from research)
    focus = {int(b): w for b, w in plan.get("focus_boards", {}).items()}   # board -> weight (seasonal)
    winners = set(map(str, plan.get("winners", [])))  # product ids with clicks/sales
    ribbons = {int(b): r for b, r in plan.get("ribbons", {}).items()}
    kw_extra = plan.get("extra_keywords", {})
    protected = winners | {p["id"] for p in cat["products"] if p["board"] in focus}
    skips = pick_skips(week, cat["products"], protected)
    prods = [p for p in cat["products"] if p["id"] not in skips]
    outdir = os.path.join(ROOT, f"week-{week:02d}")
    os.makedirs(outdir, exist_ok=True)
    rnd = random.Random(week * 7919)
    # priority: seasonal focus + proven winners get prime-time slots; everything else spreads evenly
    scored = sorted(((focus.get(p["board"], 0) + (2 if p["id"] in winners else 0) + rnd.random() * 0.5, p) for p in prods),
                    key=lambda x: -x[0])
    files = week_files(start)
    slots_all = [(t, pr, f) for f, _, sl in files for t, pr in sl]
    assert len(slots_all) == len(prods), (len(slots_all), len(prods))
    prime_slots = [x for x in slots_all if x[1]]; other = [x for x in slots_all if not x[1]]
    rnd.shuffle(prime_slots); rnd.shuffle(other)
    assigned = []
    for _, p in scored:
        t, _, f = prime_slots.pop() if prime_slots else other.pop()
        assigned.append((t, f, p))
    assigned.sort(key=lambda x: x[0])
    rows = {"A": [], "B": []}
    for t, f, p in assigned:
        b = str(p["board"])
        hook = ph.get(b) or hooks[b][(week - 1) % len(hooks[b])]
        fn = f"{p['id']}-w{week:02d}.jpg"
        make_pin(p, week, hook, ribbons.get(p["board"]), os.path.join(outdir, fn))
        title, desc, kw = copy_for(p, hook, cat, kw_extra.get(b, []))
        rows[f].append({"Title": title, "Media URL": f"{RAW}/week-{week:02d}/{fn}", "Pinterest board": cat["boards"][b], "Thumbnail": "",
                        "Description": desc, "Link": p["url"], "Publish date": t.strftime("%Y-%m-%dT%H:%M:%S"), "Keywords": kw})
    names = []
    for f, day, _ in files:
        name = f"DrQ_Week{week:02d}_{f}_upload-{day.strftime('%a-%b%d')}.csv"
        assert len(rows[f]) <= PER_FILE
        with open(os.path.join(outdir, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[f][0].keys())); w.writeheader(); w.writerows(rows[f])
        names.append((name, len(rows[f]), rows[f][0]["Publish date"], rows[f][-1]["Publish date"]))
    return names, sorted(skips)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--start", required=True, help="first publish day (YYYY-MM-DD, Central time)")
    ap.add_argument("--plan", default=None)
    a = ap.parse_args()
    plan = json.load(open(a.plan)) if a.plan else {}
    names, skips = build(a.week, dt.date.fromisoformat(a.start), plan)
    for n, c, f, l in names:
        print(f"{n}: {c} pins, {f} -> {l} UTC")
    print("rotated out this week:", ", ".join(skips))
