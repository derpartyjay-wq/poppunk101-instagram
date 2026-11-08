#!/usr/bin/env python3
"""Build the daily NEWS package: images + Publer CSV (3 posts: release 08:00, tour 12:00, announced 15:00).

usage: python3 tools/build_news.py news.json   (run from repo root)
news.json: {"date": "2026-11-09", "posts": [
  {"type": "release|tour|announced", "time": "08:00", "id": "release:<slug>",   # id is stored in data/news_used.json
   "artist": "Good Charlotte", "headline": "Greetings From California is back as a Good Charlotte album",
   "facts": [["OUT", "6 Nov 2026"], ["LABEL", "MDDN / Atlantic"]], "dateline": "9 NOV 2026",
   "body": "2-3 English sentences, facts only", "tags": ["GoodCharlotte"], "used_ids": ["announced:2000trees-2027|New Found Glory"]} ]}
Writes images/news/DATE/NN-type-slug.png, publer/news-DATE.csv, updates data/news_used.json.
"""
import csv, datetime as dt, json, pathlib, re, sys, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from playwright.sync_api import sync_playwright
import render_news
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_BASE = "https://raw.githubusercontent.com/derpartyjay-wq/poppunk101-instagram/main"
CTA = "📻 POP PUNK 101 is your pop-punk radio, on air 24 hours a day. Tune in via the link in bio! 🔗"
HEAD = {"release": "🆕 NEW RELEASE", "tour": "🎟️ TOUR NEWS", "announced": "📣 JUST ANNOUNCED"}
TYPE_TAGS = {"release": ["NewMusic", "NewRelease"], "tour": ["TourAnnouncement", "LiveMusic"], "announced": ["JustAnnounced", "Festival"]}
CORE = ["PopPunk", "PopPunk101", "PopPunkRadio", "PunkRock", "MusicNews"]
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "x"
def caption(p):
    tags = TYPE_TAGS[p["type"]] + CORE + [t for t in p.get("tags", []) if t]
    return "\n".join([f"{HEAD[p['type']]}: {p['headline']}", "", p["body"].strip(), "", CTA, "", " ".join("#" + t for t in tags)])
def main(path):
    cfg = json.load(open(path, encoding="utf-8"))
    day = cfg["date"]
    img_dir = ROOT / "images" / "news" / day
    img_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "publer").mkdir(exist_ok=True)
    rows, outs = [], []
    for i, p in enumerate(cfg["posts"], 1):
        name = f"{i:02d}-{p['type']}-{slug(p['artist'])}.png"
        outs.append(str(img_dir / name))
        when = dt.datetime.strptime(f"{day} {p['time']}", "%Y-%m-%d %H:%M")
        url = f"{RAW_BASE}/images/news/{day}/{name}"
        rows.append([when.strftime("%Y/%m/%d %H:%M"), caption(p), "", url, "", "", f"POP PUNK 101 news: {p['headline']}", "", "", "Photo", "", ""])
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        render_news.render_many(cfg["posts"], outs, pg)
        b.close()
    header = ["Date", "Text", "Link", "Media URL", "Title", "Label", "Alt text(s)", "Comment(s)",
              "Pin board, FB album, or Google category", "Post subtype", "CTA", "Reminder"]
    with open(ROOT / "publer" / f"news-{day}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL); w.writerow(header); w.writerows(rows)
    up = ROOT / "data" / "news_used.json"
    used = json.load(open(up, encoding="utf-8")) if up.exists() else {"used": []}
    for p in cfg["posts"]:
        for x in p.get("used_ids", [p["id"]] if p.get("id") else []):
            if x not in used["used"]: used["used"].append(x)
    json.dump(used, open(up, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"ok: {len(rows)} news posts, images/news/{day}, publer/news-{day}.csv")
if __name__ == "__main__":
    main(sys.argv[1])
