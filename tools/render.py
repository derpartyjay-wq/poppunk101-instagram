#!/usr/bin/env python3
"""Render one POP PUNK 101 Instagram image (1080x1350) in the poppunk101.com look.

usage: render.py out.png "Artist" "Song" 2003 [photo_path] [credit_text]
Without photo_path a typographic cover is used (no photo needed).
Put the station logo at ./logo.png to show it in the header.
"""
import sys, html, base64, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent

def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def font_css():
    faces = [("Bebas Neue", 400, "bebas-neue-latin-400-normal.woff2")] + \
            [("Barlow", w, f"barlow-latin-{w}-normal.woff2") for w in (500, 600, 700)]
    return "\n".join(
        f'@font-face{{font-family:"{fam}";font-weight:{w};src:url(data:font/woff2;base64,{b64(HERE/"fonts"/fn)}) format("woff2")}}'
        for fam, w, fn in faces)

def build_html(artist, song, year, photo=None, credit=None):
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    logo = HERE / "logo.png"
    logo_html = f'<img src="data:image/png;base64,{b64(logo)}">' if logo.exists() else ""
    if photo:
        ext = pathlib.Path(photo).suffix.lstrip(".").lower().replace("jpg", "jpeg")
        photo_html = f'<img class="photo" src="data:image/{ext};base64,{b64(photo)}">'
        credit_html = f'<div class="credit">Photo: {html.escape(credit)}</div>' if credit else ""
    else:
        n = len(artist)
        size = 190 if n <= 10 else 150 if n <= 16 else 118 if n <= 24 else 92
        photo_html = f'<div class="typo"><span style="font-size:{size}px">{html.escape(artist)}</span></div>'
        credit_html = ""
    asize = int(min(104, 968 / (len(artist) * 0.43)))
    ssize = int(min(58, 700 / (len(song) * 0.43)))
    return (tpl.replace("__ASIZE__", str(asize)).replace("__SSIZE__", str(ssize))
               .replace("__FONTS__", font_css()).replace("__LOGO__", logo_html)
               .replace("__PHOTO__", photo_html).replace("__CREDIT__", credit_html)
               .replace("__ARTIST__", html.escape(artist)).replace("__SONG__", html.escape(song))
               .replace("__YEAR__", html.escape(str(year))))

def render_many(items, page):
    for out, artist, song, year, photo, credit in items:
        page.set_content(build_html(artist, song, year, photo, credit))
        page.evaluate("document.fonts.ready")
        page.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})

if __name__ == "__main__":
    out, artist, song, year = sys.argv[1:5]
    photo = sys.argv[5] if len(sys.argv) > 5 else None
    credit = sys.argv[6] if len(sys.argv) > 6 else None
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        render_many([(out, artist, song, year, photo, credit)], pg)
        b.close()
