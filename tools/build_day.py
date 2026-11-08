#!/usr/bin/env python3
"""Build one day's package: PNG images + Publer bulk CSV + rotation state.

usage: python3 tools/build_day.py posts.json

posts.json:
{
  "start": "2026-11-09 07:00",          # first post, Europe/Berlin, then +1 hour each
  "raw_base": "https://raw.githubusercontent.com/derpartyjay-wq/poppunk101-instagram/main",
  "posts": [
    {"artist": "...", "song": "...", "year": 2004,
     "bio": "1-2 English sentences, facts only",
     "band_tag": "GoodCharlotte",          # optional, no #, no spaces
     "photo": "/abs/path.jpg", "credit": "Author / Wikimedia Commons, CC BY-SA 2.0"}  # optional
  ]
}
Run from the repo root. Writes images/DATE/NN-slug.png, publer/DATE.csv, updates data/used.json.
"""
import csv, datetime as dt, json, pathlib, re, sys, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from playwright.sync_api import sync_playwright
import render

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORE_TAGS = ["PopPunk", "PopPunkRadio", "PopPunk101", "NowPlaying", "PunkRock", "PopPunkForever"]
CTA = "📻 POP PUNK 101 is your pop-punk radio, on air 24 hours a day. Tune in via the link in bio! 🔗"

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "x"

def decade_tag(year):
    y = int(year)
    return f"{str(y)[:3]}0sMusic" if y < 2020 else f"{y // 10 * 10}sMusic"

def caption(p):
    tags = CORE_TAGS + ([p["band_tag"]] if p.get("band_tag") else []) + [decade_tag(p["year"])]
    lines = [f"🎧 NOW PLAYING: {p['song']} by {p['artist']} ({p['year']})", "", p["bio"].strip(), "", CTA]
    if p.get("photo") and p.get("credit"):
        lines += ["", f"📷 Photo: {p['credit']}"]
    lines += ["", " ".join("#" + t for t in tags)]
    return "\n".join(lines)

def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    start = dt.datetime.strptime(cfg["start"], "%Y-%m-%d %H:%M")
    day = start.strftime("%Y-%m-%d")
    img_dir = ROOT / "images" / day
    img_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "publer").mkdir(exist_ok=True)
    rows, items = [], []
    for i, p in enumerate(cfg["posts"], 1):
        name = f"{i:02d}-{slug(p['artist'])}-{slug(p['song'])}.png"
        items.append((str(img_dir / name), p["artist"], p["song"], p["year"], p.get("photo"), p.get("credit")))
        when = start + dt.timedelta(hours=i - 1)
        url = f"{cfg['raw_base']}/images/{day}/{name}"
        alt = f"Now playing on POP PUNK 101: {p['song']} by {p['artist']}"
        rows.append([when.strftime("%Y/%m/%d %H:%M"), caption(p), "", url, "", "", alt, "", "", "Photo", "", ""])
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        render.render_many(items, pg)
        b.close()
    header = ["Date", "Text", "Link", "Media URL", "Title", "Label", "Alt text(s)", "Comment(s)",
              "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
    with open(ROOT / "publer" / f"{day}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(header)
        w.writerows(rows)
    used_path = ROOT / "data" / "used.json"
    used = json.load(open(used_path, encoding="utf-8"))
    used["used"] += [f"{p['artist']} | {p['song']}" for p in cfg["posts"]]
    json.dump(used, open(used_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"ok: {len(rows)} posts, images/{day}, publer/{day}.csv")

if __name__ == "__main__":
    main(sys.argv[1])
