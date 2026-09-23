# leadtrigger-process-steps

Leadtrigger Offering Company Finder process steps — flat chatbot / RAG training corpus.

**Live site:** https://lennart1970.github.io/leadtrigger-process-steps/

## What this is

One long flat page (`docs/index.html`) that is the training handbook as-is:

1. `INDEX.md` (process steps 01/02/03 + media embeds)
2. `appendix-handbook-ui-sequences.md` (handbook §10–12)
3. Each `media/*/MANUAL.md` inlined

No hub nav chrome, no sticky TOC, no multi-page site chrome — readable body text for crawler / RAG extraction. Stills and videos stay inline where the markdown embeds them.

Standalone MANUAL pages also exist under `docs/media/*/MANUAL.html` (same content, no nav).

## GitHub Pages

Deploy from branch `main` / folder `/docs`.

## Rebuild

```bash
# pack unpacked at /tmp/leadtrigger-pack
python3 build_site.py
```

Requires `pip install markdown`.
