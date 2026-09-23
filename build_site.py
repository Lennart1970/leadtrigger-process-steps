#!/usr/bin/env python3
"""Build a flat handbook-style training corpus for GitHub Pages (RAG-friendly)."""

from __future__ import annotations

import shutil
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify

ROOT = Path(__file__).resolve().parent
PACK = Path("/tmp/leadtrigger-pack")
DOCS = ROOT / "docs"
SITE_BASE = "https://lennart1970.github.io/leadtrigger-process-steps"

MANUAL_ORDER = [
    "01-refresh-stale-share-article",
    "02-full-company-universe",
    "03-prepare-one-company",
]

CSS = """\
:root {
  --bg: #111418;
  --text: #e8eaed;
  --muted: #9aa0a6;
  --link: #8ab4f8;
  --border: #3c4043;
  --code-bg: #1e2227;
  --surface: #1a1e23;
  --max: 48rem;
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #fafafa;
    --text: #202124;
    --muted: #5f6368;
    --link: #1a73e8;
    --border: #dadce0;
    --code-bg: #f1f3f4;
    --surface: #fff;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Georgia, "Times New Roman", "Liberation Serif", serif;
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--text);
  background: var(--bg);
}

main {
  max-width: var(--max);
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3.5rem;
}

h1, h2, h3, h4 {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  line-height: 1.3;
  font-weight: 650;
}

h1 { font-size: 1.75rem; margin: 0 0 1rem; }
h2 { font-size: 1.4rem; margin: 2.25rem 0 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }
h3 { font-size: 1.15rem; margin: 1.5rem 0 0.5rem; }
h4 { font-size: 1.05rem; margin: 1.25rem 0 0.4rem; }

p, ul, ol { margin: 0.7rem 0; }
ul, ol { padding-left: 1.35rem; }
li { margin: 0.25rem 0; }

a { color: var(--link); }

blockquote {
  margin: 1rem 0;
  padding: 0.5rem 0.9rem;
  border-left: 3px solid var(--border);
  color: var(--muted);
}

code {
  font-family: ui-monospace, "Cascadia Code", "SF Mono", Menlo, monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 0.1em 0.3em;
  border-radius: 3px;
}

pre {
  overflow-x: auto;
  background: var(--code-bg);
  border: 1px solid var(--border);
  padding: 0.75rem 1rem;
  font-size: 0.88rem;
}

pre code { background: none; padding: 0; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  margin: 1rem 0;
  display: block;
  overflow-x: auto;
}

th, td {
  border: 1px solid var(--border);
  padding: 0.4rem 0.6rem;
  text-align: left;
  vertical-align: top;
}

th { background: var(--surface); }

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem 0;
  border: 1px solid var(--border);
}

video {
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 1rem 0;
  background: #000;
}

@media (max-width: 640px) {
  body { font-size: 1rem; }
  main { padding: 1rem 0.85rem 2.5rem; }
}
"""


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "smarty", "toc"],
        extension_configs={"toc": {"permalink": False, "slugify": slugify}},
    )


def page(title: str, body_html: str, *, css_href: str = "styles.css") -> str:
    """Bare document shell — no nav, no hub chrome, no sticky TOC."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Leadtrigger Offering Company Finder process steps — flat chatbot / RAG training corpus.">
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<main>
{body_html}
</main>
</body>
</html>
"""


def build_corpus_markdown() -> str:
    """Concatenate INDEX + appendix + each MANUAL as one flat handbook extract."""
    index_md = (PACK / "INDEX.md").read_text(encoding="utf-8")
    appendix_md = (PACK / "appendix-handbook-ui-sequences.md").read_text(encoding="utf-8")

    parts: list[str] = [index_md.strip(), "", "---", "", appendix_md.strip()]

    for slug in MANUAL_ORDER:
        manual_path = PACK / "media" / slug / "MANUAL.md"
        manual_md = manual_path.read_text(encoding="utf-8").strip()
        parts.extend(
            [
                "",
                "---",
                "",
                f"<!-- source: media/{slug}/MANUAL.md -->",
                "",
                manual_md,
            ]
        )

    return "\n".join(parts) + "\n"


def write_sitemap(urls: list[str]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    (DOCS / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not PACK.is_dir():
        raise SystemExit(f"Pack not found at {PACK}")

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    shutil.copytree(PACK / "media", DOCS / "media")
    shutil.copy2(PACK / "INDEX.md", DOCS / "INDEX.md")
    shutil.copy2(PACK / "appendix-handbook-ui-sequences.md", DOCS / "appendix-handbook-ui-sequences.md")

    corpus_md = build_corpus_markdown()
    (DOCS / "corpus.md").write_text(corpus_md, encoding="utf-8")

    body = md_to_html(corpus_md)
    (DOCS / "index.html").write_text(
        page(
            "Leadtrigger — Offering Company Finder process steps (chatbot training)",
            body,
        ),
        encoding="utf-8",
    )
    print("wrote index.html (flat corpus)")

    (DOCS / "styles.css").write_text(CSS, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # Standalone MANUAL.html — content only, no hub/nav chrome.
    for slug in MANUAL_ORDER:
        manual_md = (DOCS / "media" / slug / "MANUAL.md").read_text(encoding="utf-8")
        first = manual_md.split("\n", 1)[0]
        title = first.lstrip("# ").strip() if first.startswith("#") else slug
        out = DOCS / "media" / slug / "MANUAL.html"
        out.write_text(
            page(title, md_to_html(manual_md), css_href="../../styles.css"),
            encoding="utf-8",
        )
        print(f"wrote {out.relative_to(DOCS)}")

    write_sitemap(
        [
            f"{SITE_BASE}/",
            f"{SITE_BASE}/index.html",
            f"{SITE_BASE}/media/01-refresh-stale-share-article/MANUAL.html",
            f"{SITE_BASE}/media/02-full-company-universe/MANUAL.html",
            f"{SITE_BASE}/media/03-prepare-one-company/MANUAL.html",
        ]
    )
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_BASE}/sitemap.xml\n",
        encoding="utf-8",
    )
    print("wrote sitemap.xml, robots.txt")
    print("done")


if __name__ == "__main__":
    main()
