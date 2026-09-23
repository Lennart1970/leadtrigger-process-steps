# leadtrigger-process-steps

Leadtrigger Offering Company Finder process steps — chatbot training corpus with demo media.

**Live site:** https://lennart1970.github.io/leadtrigger-process-steps/

## What this is

A static GitHub Pages site (`/docs`) that publishes the Offering Company Finder process-step pack as one long training page:

1. **01 — Refresh stale share article** (with video + stills)
2. **02 — Full company universe** (with video + stills)
3. **03 — Prepare one company** (with video + stills)
4. **Appendix** — Handbook UI sequences §10–12

Audience is chatbot / Grok Bot training: dense routes, decision rules, and media — not marketing.

## GitHub Pages

- Source: `docs/` on `main`
- Homepage: `docs/index.html`
- Media: `docs/media/**` (relative paths for `<img>` / `<video>`)

Enable Pages: **Settings → Pages → Deploy from a branch → `main` / `/docs`**.

## Rebuild from pack

```bash
# unpack pack to /tmp/leadtrigger-pack (or adjust PACK in build_site.py)
python3 build_site.py
```

Requires `pip install markdown`.
