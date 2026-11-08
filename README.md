# POP PUNK 101 – Instagram automation

Daily package of 24 Instagram posts for the POP PUNK 101 radio.

- `tools/` – image template (poppunk101.com look), renderer, fonts, logo
- `data/songliste.csv` – song list (artist, song)
- `data/used.json` – songs already used (rotation state)
- `data/bios.json` – verified release years and short bios per song/band
- `images/YYYY-MM-DD/` – rendered post images (public, linked from the Publer CSV)
- `publer/YYYY-MM-DD.csv` – Publer bulk upload file for that day

## News posts
- `tools/template_news.html`, `tools/render_news.py`, `tools/build_news.py` – NEWS image template (release / tour / just announced) and builder
- `data/news_used.json` – news items already posted (rotation state)
- `images/news/YYYY-MM-DD/` – rendered news images
- `publer/news-YYYY-MM-DD.csv` – Publer bulk upload file with 3 news posts (08:00, 12:00, 15:00)
