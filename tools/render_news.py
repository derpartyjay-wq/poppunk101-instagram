#!/usr/bin/env python3
"""Render one POP PUNK 101 NEWS image (1080x1350). Types: release, tour, announced."""
import html, base64, pathlib
HERE = pathlib.Path(__file__).parent
STYLE = {
  "release":   dict(tape="NEW RELEASE", tcolor="var(--primary)", glow="rgba(248,10,114,.20)", cardglow="rgba(248,10,114,.55)",
                    tapebg="var(--primary)", tapefg="var(--foreground)"),
  "tour":      dict(tape="TOUR NEWS", tcolor="var(--accent)", glow="rgba(27,195,243,.20)", cardglow="rgba(27,195,243,.5)",
                    tapebg="var(--accent)", tapefg="#06090d"),
  "announced": dict(tape="JUST ANNOUNCED", tcolor="var(--primary)", glow="rgba(248,10,114,.16)", cardglow="rgba(248,10,114,.45)",
                    tapebg="linear-gradient(120deg,var(--primary),var(--accent))", tapefg="var(--foreground)"),
}
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def font_css():
    faces = [("Bebas Neue", 400, "bebas-neue-latin-400-normal.woff2")] + [("Barlow", w, f"barlow-latin-{w}-normal.woff2") for w in (500, 600, 700)]
    return "\n".join(f'@font-face{{font-family:"{f}";font-weight:{w};src:url(data:font/woff2;base64,{b64(HERE/"fonts"/fn)}) format("woff2")}}' for f, w, fn in faces)
def build_html(p):
    st = STYLE[p["type"]]
    tpl = (HERE / "template_news.html").read_text(encoding="utf-8")
    logo = HERE / "logo.png"
    logo_html = f'<img src="data:image/png;base64,{b64(logo)}">' if logo.exists() else ""
    wm = f'<img class="wm" src="data:image/png;base64,{b64(logo)}">' if logo.exists() else ""
    tape = " ✦ ".join([st["tape"]] * 6)
    facts = "".join(f'<div class="fact"><i>{html.escape(k)}</i><b>{html.escape(v)}</b></div>' for k, v in p["facts"][:3])
    rep = {"__FONTS__": font_css(), "__LOGO__": logo_html, "__WM__": wm, "__TAPE__": tape, "__DATE__": html.escape(p.get("dateline", "")),
           "__ARTIST__": html.escape(p["artist"]), "__HEADLINE__": html.escape(p["headline"]), "__FACTS__": facts,
           "__TCOLOR__": st["tcolor"], "__GLOW__": st["glow"], "__CARDGLOW__": st["cardglow"], "__TAPEBG__": st["tapebg"], "__TAPEFG__": st["tapefg"]}
    for k, v in rep.items(): tpl = tpl.replace(k, v)
    return tpl
def render_many(posts, outs, page):
    for p, out in zip(posts, outs):
        page.set_content(build_html(p))
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(150)
        page.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
