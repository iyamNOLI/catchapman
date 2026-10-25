#!/usr/bin/env python3
"""Turn the saved 22slides pages in source/ into a self-hosted copy in docs/.

    python3 mirror.py

The HTML is kept exactly as 22slides made it; only asset addresses change:
- images on m2.22slides.com  -> /images/thumb/... and /images/large/...
- /dist/...scripts.js?123     -> /dist/...scripts.js (copied from source/dist)
- links to www.catchapman.co.nz/<page> -> /<page>
"""
import html
import os
import re
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "source")
OUT = os.path.join(ROOT, "docs")
IMAGES = os.path.join(OUT, "images")

# The domain GitHub Pages serves this copy on (written to docs/CNAME, used for share-preview images).
CUSTOM_DOMAIN = "catchapman.0-5.uk"
OLD_SITE = "https://www.catchapman.co.nz"
IMG_HOST = re.compile(r"https://m2\.22slides\.com/catchapman/([^?\"'\s,)]+)(\?[^\"'\s,)]*)?")
SPECIAL = {"cat-logo-601.png": "/images/logo.png", "bear-web-785.jpg": "/images/favicon.jpg"}


def widths():
    """Pixel width of every local image, read once with macOS `sips`."""
    out = {}
    for size in ("thumb", "large"):
        folder = os.path.join(IMAGES, size)
        files = sorted(os.listdir(folder))
        result = subprocess.run(["sips", "-g", "pixelWidth", *files], cwd=folder, capture_output=True, text=True)
        current = None
        for line in result.stdout.splitlines():
            if not line.startswith(" "):
                current = os.path.basename(line.strip())
            elif "pixelWidth" in line:
                out[(size, current)] = int(line.split(":")[1])
    return out


W = widths()


def local(file, size="thumb"):
    return SPECIAL.get(file, f"/images/{size}/{file}")


def srcset(value):
    m = IMG_HOST.search(html.unescape(value))
    if not m:
        return value
    file = m.group(1)
    if file in SPECIAL:
        return SPECIAL[file]
    t, l = W.get(("thumb", file)), W.get(("large", file))
    if not t or not l:
        raise SystemExit(f"missing local image for {file}")
    return f"{local(file)} {t}w" if t == l else f"{local(file)} {t}w, {local(file, 'large')} {l}w"


def rewrite(page):
    # srcset / data-srcset: swap the list of 22slides sizes for our two local sizes.
    page = re.sub(r'((?:data-)?srcset)="([^"]*)"', lambda m: f'{m.group(1)}="{srcset(m.group(2))}"', page)
    # Share-preview images need a full address.
    page = re.sub(
        r'(<meta [^>]*content=")([^"]*m2\.22slides\.com[^"]*)"',
        lambda m: m.group(1) + IMG_HOST.sub(lambda i: f"https://{CUSTOM_DOMAIN}{local(i.group(1), 'large')}", html.unescape(m.group(2))) + '"',
        page,
    )
    # Remaining image addresses (src, favicon, lightbox links).
    page = IMG_HOST.sub(lambda m: local(m.group(1), "large" if m.group(2) and "w=1&" not in m.group(2) and "w=1&amp;" not in m.group(2) else "thumb"), page)
    page = re.sub(r'<link rel="(?:preconnect|dns-prefetch)" href="https://m2\.22slides\.com">\s*', "", page)
    page = re.sub(r'(src="/dist/[^"?]+\.js)\?\d+"', r'\1"', page)
    # Internal links to the old domain (keep <link rel="canonical"> and og:url pointing at her real site).
    page = re.sub(r'(<a\b[^>]*href=")' + re.escape(OLD_SITE) + r'(/[^"]*)"', r"\1\2" + '"', page)
    leftover = re.findall(r"m2\.22slides\.com[^\"'\s]{0,40}", page)
    if leftover:
        raise SystemExit(f"unrewritten 22slides addresses: {leftover[:3]}")
    return page


def main():
    count = 0
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".html"):
            continue
        with open(os.path.join(SRC, name), encoding="utf-8") as f:
            page = rewrite(f.read())
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(page)
        count += 1
    shutil.copytree(os.path.join(SRC, "dist"), os.path.join(OUT, "dist"), dirs_exist_ok=True)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "CNAME"), "w") as f:
        f.write(CUSTOM_DOMAIN + "\n")
    print(f"Mirrored {count} pages into docs/")


if __name__ == "__main__":
    main()
