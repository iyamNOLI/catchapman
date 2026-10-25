# Cat Chapman Illustration — self-hosted copy

An exact copy of catchapman.co.nz (all 47 pages, 446 images), served free on GitHub Pages instead of a paid 22slides plan. Live at https://catchapman.0-5.uk.

- `source/` — the original pages exactly as 22slides serves them, plus its two theme scripts (`source/dist/`)
- `mirror.py` — copies `source/` into `docs/`, swapping every 22slides image address for the local copies in `docs/images/`
- `docs/` — the finished website (this is what GitHub Pages publishes)
- `serve.py` — local preview that behaves like GitHub Pages (`/little-owl` → `little-owl.html`)

The page HTML, layout, slideshow, image viewer and styling are 22slides' own, unchanged. Only the asset addresses are rewritten. Note that the theme code belongs to 22slides: using it long-term after cancelling 22slides may not be covered by its terms.

## Publish
GitHub Pages is set to **main** branch, **/docs** folder, with the custom domain from `docs/CNAME` (`CUSTOM_DOMAIN` in `mirror.py`).
```bash
python3 mirror.py
git add -A && git commit -m "Update site" && git push
```

Preview locally with `python3 serve.py`, then open http://localhost:8790.

## Updating content
Re-save a changed page from the live 22slides site into `source/<page>.html`. If it uses new images, download them into `docs/images/large/` and `docs/images/thumb/`. Then rerun `mirror.py`, which stops and names any image it can't find locally.

## Moving her real domain
Set `CUSTOM_DOMAIN = "www.catchapman.co.nz"` in `mirror.py`, rerun it and push. Then, at her domain registrar, replace the 22slides DNS records with a `CNAME` from `www` to `iyamnoli.github.io`, plus GitHub's four `A` records for the bare domain: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Tick **Enforce HTTPS** in the repo's Pages settings once it's available.

## Contact form
The form still posts to 22slides' servers, which GitHub Pages can't stand in for, so it won't send. A free service like Formspree can replace it.
