# leadtrigger-process-steps

Leadtrigger Offering Company Finder process steps — chatbot / RAG training corpus with demo media.

**Live site:** https://lennart1970.github.io/leadtrigger-process-steps/

## Crawlable pages (flat link graph)

| URL | Content |
|-----|---------|
| [/](https://lennart1970.github.io/leadtrigger-process-steps/) | Hub — intro + links to each step |
| [/01-refresh-stale-share-article.html](https://lennart1970.github.io/leadtrigger-process-steps/01-refresh-stale-share-article.html) | Process step 01 + media |
| [/02-full-company-universe.html](https://lennart1970.github.io/leadtrigger-process-steps/02-full-company-universe.html) | Process step 02 + media |
| [/03-prepare-one-company.html](https://lennart1970.github.io/leadtrigger-process-steps/03-prepare-one-company.html) | Process step 03 + media |
| [/appendix.html](https://lennart1970.github.io/leadtrigger-process-steps/appendix.html) | Handbook UI sequences §10–12 |
| [/media/…/MANUAL.html](https://lennart1970.github.io/leadtrigger-process-steps/media/01-refresh-stale-share-article/MANUAL.html) | Per-step MANUAL (SoT) |

Discovery uses **real HTML page links** (not `#` in-page jumps). Also: `docs/sitemap.xml`, `docs/robots.txt`.

## GitHub Pages

- Source: `docs/` on `main`
- Enable: **Settings → Pages → Deploy from a branch → `main` / `/docs`**

## Rebuild from pack

```bash
# unpack pack to /tmp/leadtrigger-pack (or adjust PACK in build_site.py)
python3 build_site.py
```

Requires `pip install markdown`.
