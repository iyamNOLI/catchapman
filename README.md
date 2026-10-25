# Cat Chapman Illustration — static site

A copy of catchapman.co.nz (all 47 pages, 446 images) as a plain static website, ready for **free** hosting on GitHub Pages instead of a paid 22slides plan.

- `docs/` — the finished website (this is what GitHub Pages publishes)
- `content.json` — all the page text, image lists and menu
- `build.py` — rebuilds `docs/` from `content.json`
- `assets/` — the stylesheet and the small script (slideshow, image viewer, mobile menu)

## Publish on GitHub Pages
1. Push this folder to a GitHub repository.
2. On GitHub, open the repo's **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then pick the **main** branch and the **/docs** folder.
3. After a minute the site is live at `https://catchapman.0-5.uk` (set by `CUSTOM_DOMAIN` in `build.py`).

### Using a custom domain
- **Her real domain:** set `CUSTOM_DOMAIN = "www.catchapman.co.nz"` in `build.py`, rebuild and push. Then, at her domain registrar, replace the 22slides DNS records with a `CNAME` from `www` to `<username>.github.io`, plus GitHub's four `A` records for the bare domain: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Tick **Enforce HTTPS** once it's available.
- **A free 0-5.uk name:** create a GitHub Pages subdomain at https://0-5.uk/dashboard, then enter that name as the custom domain.

The page addresses match the old site (`/little-owl`, `/picture-books`, …), so existing links and Google results keep working after the switch.

## Editing
Edit `content.json` (text, page order, image lists), add any new images to `docs/images/large/` and `docs/images/thumb/`, then run:
```bash
python3 build.py
```
Commit and push, and GitHub Pages updates within a minute or two.

## Contact form
GitHub Pages can't send email itself. To make the form work, create a free form at https://formspree.io (50 messages a month free) using Cat's email address, paste its endpoint into `FORM_ENDPOINT` in `build.py`, and rebuild. Until then, the form tells visitors to get in touch on Instagram.
