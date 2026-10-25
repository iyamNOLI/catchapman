#!/usr/bin/env python3
"""Builds the static site in docs/ from content.json.

    python3 build.py

Every page in content.json becomes docs/<slug>.html. GitHub Pages serves
/<slug> from <slug>.html, so the old 22slides URLs (e.g. /little-owl) keep working.
"""
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
SITE_NAME = "Cat Chapman Illustration"

# To make the contact form send email, create a free form at https://formspree.io
# and paste its endpoint here (e.g. "https://formspree.io/f/abcdwxyz"), then rebuild.
FORM_ENDPOINT = ""

esc = html.escape
site = json.load(open(os.path.join(ROOT, "content.json"), encoding="utf-8"))


def href(slug):
    return "index.html" if slug in ("index", "") else f"{slug}.html"


def focal(img):
    return f' style="object-position:{esc(img["focal"])}"' if img.get("focal") else ""


def img_tag(img, size="thumb", cls="", eager=False, extra=""):
    return (
        f'<img src="images/{size}/{esc(img["file"])}" width="{img["w"]}" height="{img["h"]}" '
        f'alt="{esc(img["alt"])}"{" " if cls else ""}{cls}{"" if eager else " loading=\"lazy\""}{focal(img)}{extra}>'
    )


def lightbox_attrs(img):
    return f'data-full="images/large/{esc(img["file"])}"'


# ---------- blocks ----------

def gallery(block):
    images, layout = block["images"], block["layout"]
    if not images:
        return ""
    if layout == "slideshow":
        slides = "".join(
            f'<figure class="slide{" is-active" if n == 0 else ""}">'
            f'{img_tag(i, "large", eager=n == 0)}</figure>'
            for n, i in enumerate(images)
        )
        return (
            f'<section class="slideshow" aria-roledescription="carousel">{slides}'
            '<button class="slideshow__nav slideshow__nav--prev" aria-label="Previous">&#8249;</button>'
            '<button class="slideshow__nav slideshow__nav--next" aria-label="Next">&#8250;</button></section>'
        )

    def item(i):
        cap = f'<figcaption>{esc(i["caption"])}</figcaption>' if i.get("caption") else ""
        ratio = f'style="--r:{i["w"] / max(i["h"], 1):.4f}"'
        return f'<figure class="g-item" {ratio}><a href="images/large/{esc(i["file"])}" {lightbox_attrs(i)}>{img_tag(i)}</a>{cap}</figure>'

    cols = " gallery--few" if layout == "grid" and len(images) <= 4 else ""
    return f'<section class="gallery gallery--{esc(layout or "grid")}{cols}">{"".join(item(i) for i in images)}</section>'


def collection(block):
    items = "".join(
        f'<a class="c-item" href="{href(it["slug"])}">'
        f'<div class="c-item__img">{img_tag(it["image"]) if it.get("image") else ""}</div>'
        f'<span class="c-item__title">{esc(it["title"])}</span></a>'
        for it in block["items"]
    )
    return f'<section class="collection">{items}</section>'


def text(block):
    if not block["html"]:
        return ""
    return "".join(f'<section class="text">{h}</section>' for h in block["html"])


def spread(block):
    img = block.get("image")
    pic = f'<figure class="spread__img">{img_tag(img, "large", eager=True)}</figure>' if img else ""
    return f'<section class="spread spread--{esc(block["layout"] or "textright")}">{pic}<div class="spread__text">{"".join(block["html"])}</div></section>'


def form(block):
    labels = block["fields"]
    names = ["name", "email", "message"]
    fields = []
    for label, name in zip(labels, names):
        required = "" if name == "name" else " required"
        if name == "message":
            control = f'<textarea name="message" placeholder="{esc(label)}" rows="6"{required}></textarea>'
        else:
            control = f'<input type="{"email" if name == "email" else "text"}" name="{name}" placeholder="{esc(label)}"{required}>'
        fields.append(f'<label><span class="visually-hidden">{esc(label)}</span>{control}</label>')
    action = f' action="{esc(FORM_ENDPOINT)}" method="post"' if FORM_ENDPOINT else ""
    return (
        f'<form class="contact-form"{action} data-connected="{"yes" if FORM_ENDPOINT else "no"}">'
        f'{"".join(fields)}<button type="submit">Send Message</button><p class="form-note" role="status"></p></form>'
    )


RENDER = {"gallery": gallery, "collection": collection, "text": text, "spread": spread, "form": form}


# ---------- page ----------

INSTAGRAM_ICON = (
    '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
    '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor"/></svg>'
)


def nav(current):
    links = "".join(
        f'<li><a href="{href(n["slug"])}"{" aria-current=\"page\"" if n["slug"] == current else ""}>{esc(n["label"])}</a></li>'
        for n in site["nav"]
    )
    social = "".join(
        f'<li><a class="social" href="{esc(s["url"])}" target="_blank" rel="noopener" title="{esc(s["name"].title())}">{INSTAGRAM_ICON}</a></li>'
        for s in site["social"]
    )
    return links + social


def page(slug, data):
    title = SITE_NAME if slug == "index" else f'{data["title"]} - {SITE_NAME}'
    body = "".join(RENDER[b["type"]](b) for b in data["blocks"] if b["type"] in RENDER)
    logo = site["logo"]
    desc = data.get("description") or SITE_NAME
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="images/{esc(site["favicon"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body class="page-{esc(slug)}">
<header class="header">
  <a class="logo" href="index.html"><img src="images/{esc(logo["file"])}" width="{logo["w"]}" height="{logo["h"]}" alt="{esc(logo["alt"])}"></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav id="nav"><ul>{nav(slug)}</ul></nav>
</header>
<main class="content">{body}</main>
<footer class="footer">{site["footer"]}</footer>
<script src="site.js" defer></script>
</body>
</html>
"""


def main():
    for slug, data in site["pages"].items():
        with open(os.path.join(OUT, href(slug)), "w", encoding="utf-8") as f:
            f.write(page(slug, data))
    for asset in ("style.css", "site.js"):
        shutil.copy(os.path.join(ROOT, "assets", asset), os.path.join(OUT, asset))
    # 404 page and GitHub Pages config
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(page("404", {"title": "Page not found", "blocks": [
            {"type": "text", "html": ['<p style="text-align:center">Sorry, that page doesn\'t exist. <a href="index.html">Back to the home page</a>.</p>']}
        ]}))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"Built {len(site['pages'])} pages into docs/")


if __name__ == "__main__":
    main()
