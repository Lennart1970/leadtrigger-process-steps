#!/usr/bin/env python3
"""Build static GitHub Pages site from the Leadtrigger process-steps pack."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify

ROOT = Path(__file__).resolve().parent
PACK = Path("/tmp/leadtrigger-pack")
DOCS = ROOT / "docs"

CSS = """\
:root {
  --bg: #0f1419;
  --surface: #1a222c;
  --text: #e7ecf1;
  --muted: #9aa7b5;
  --link: #6db3f2;
  --link-hover: #9cccf7;
  --border: #2a3542;
  --code-bg: #121820;
  --accent: #3d8fd1;
  --blockquote: #8b9aab;
  --table-stripe: #151c24;
  --max: 52rem;
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #f7f5f1;
    --surface: #ffffff;
    --text: #1a1f26;
    --muted: #5a6570;
    --link: #0b6bcb;
    --link-hover: #084a8c;
    --border: #d5dbe3;
    --code-bg: #eef1f5;
    --accent: #0b6bcb;
    --blockquote: #5a6570;
    --table-stripe: #f0ede8;
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: "IBM Plex Sans", "Segoe UI", "Helvetica Neue", sans-serif;
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--text);
  background:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(61, 143, 209, 0.12), transparent),
    radial-gradient(ellipse 60% 40% at 100% 0%, rgba(30, 80, 120, 0.1), transparent),
    var(--bg);
  min-height: 100vh;
}

.wrap {
  max-width: var(--max);
  margin: 0 auto;
  padding: 1.5rem 1.25rem 4rem;
}

header.site {
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}

header.site .eyebrow {
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 0.35rem;
}

header.site h1 {
  font-family: "IBM Plex Serif", Georgia, "Times New Roman", serif;
  font-size: clamp(1.6rem, 4vw, 2.15rem);
  font-weight: 600;
  line-height: 1.25;
  margin: 0 0 0.5rem;
}

header.site p {
  margin: 0;
  color: var(--muted);
  font-size: 0.95rem;
}

nav.toc-jump {
  position: sticky;
  top: 0;
  z-index: 10;
  background: color-mix(in srgb, var(--bg) 92%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  margin: 0 -1.25rem 1.75rem;
  padding: 0.65rem 1.25rem;
  font-size: 0.85rem;
  overflow-x: auto;
  white-space: nowrap;
}

nav.toc-jump a {
  color: var(--muted);
  text-decoration: none;
  margin-right: 1rem;
}

nav.toc-jump a:hover {
  color: var(--link);
}

.prose h1 {
  display: none; /* page title is in header */
}

.prose h2 {
  font-family: "IBM Plex Serif", Georgia, serif;
  font-size: 1.55rem;
  font-weight: 600;
  margin: 2.75rem 0 1rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border);
  scroll-margin-top: 3rem;
}

.prose h2:first-of-type {
  border-top: none;
  margin-top: 1.5rem;
}

.prose h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 1.75rem 0 0.65rem;
  scroll-margin-top: 3rem;
}

.prose p,
.prose ul,
.prose ol {
  margin: 0.75rem 0;
}

.prose ul,
.prose ol {
  padding-left: 1.35rem;
}

.prose li {
  margin: 0.3rem 0;
}

.prose a {
  color: var(--link);
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
}

.prose a:hover {
  color: var(--link-hover);
}

.prose blockquote {
  margin: 1rem 0;
  padding: 0.65rem 1rem;
  border-left: 3px solid var(--accent);
  background: var(--surface);
  color: var(--blockquote);
}

.prose blockquote p {
  margin: 0.35rem 0;
}

.prose code {
  font-family: "IBM Plex Mono", ui-monospace, "Cascadia Code", monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 0.12em 0.35em;
  border-radius: 3px;
  border: 1px solid var(--border);
}

.prose pre {
  overflow-x: auto;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.9rem 1rem;
  font-size: 0.88rem;
}

.prose pre code {
  border: none;
  padding: 0;
  background: none;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  margin: 1rem 0;
  display: block;
  overflow-x: auto;
}

.prose th,
.prose td {
  border: 1px solid var(--border);
  padding: 0.45rem 0.65rem;
  text-align: left;
  vertical-align: top;
}

.prose th {
  background: var(--surface);
  font-weight: 600;
}

.prose tr:nth-child(even) td {
  background: var(--table-stripe);
}

.prose hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

.prose img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem 0;
  border: 1px solid var(--border);
  border-radius: 4px;
}

.prose video {
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 1rem 0;
  background: #000;
  border: 1px solid var(--border);
  border-radius: 4px;
}

.prose strong {
  font-weight: 650;
}

footer.site {
  margin-top: 3rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.85rem;
}

@media (max-width: 640px) {
  body {
    font-size: 1rem;
  }

  .wrap {
    padding: 1rem 0.9rem 3rem;
  }

  .prose table {
    font-size: 0.82rem;
  }
}
"""

FONT_LINKS = """\
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,650;1,400&family=IBM+Plex+Serif:wght@500;600&display=swap" rel="stylesheet">
"""


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "smarty",
            "toc",
        ],
        extension_configs={
            "toc": {
                "permalink": False,
                "slugify": slugify,
            }
        },
    )


def page_shell(title: str, body_html: str, *, is_home: bool = False, back_href: str | None = None) -> str:
    nav = ""
    if is_home:
        nav = """\
<nav class="toc-jump" aria-label="Jump links">
  <a href="#01--refresh-stale-share-article">01 Refresh</a>
  <a href="#02--full-company-universe">02 Full universe</a>
  <a href="#03--prepare-one-company">03 Prepare one</a>
  <a href="#appendix">Appendix §10–12</a>
</nav>
"""
    back = ""
    if back_href:
        back = f'<p class="eyebrow"><a href="{back_href}">← Back to process steps</a></p>'

    header_title = title
    if is_home:
        header_blurb = (
            "Chatbot / Grok Bot training corpus — Offering Company Finder process steps with media. "
            "Canonical routes and decision rules over screenshots."
        )
    else:
        header_blurb = "Process step manual (source of truth for this step)."

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Leadtrigger Offering Company Finder process steps — chatbot training corpus with demo media.">
{FONT_LINKS}
<link rel="stylesheet" href="{"styles.css" if is_home else "../../styles.css"}">
</head>
<body>
<div class="wrap">
<header class="site">
{back}
<p class="eyebrow">Leadtrigger · leadtrigger-news</p>
<h1>{header_title}</h1>
<p>{header_blurb}</p>
</header>
{nav}
<article class="prose">
{body_html}
</article>
<footer class="site">
  <p>Static training site · <a href="https://lennart1970.github.io/leadtrigger-process-steps/">lennart1970.github.io/leadtrigger-process-steps</a> · GitHub Pages (<code>docs/</code>)</p>
</footer>
</div>
</body>
</html>
"""


# GitHub-style heading ids from INDEX.md TOC (em dash → empty → double hyphen).
GITHUB_IDS = {
    "01-refresh-stale-share-article": "01--refresh-stale-share-article",
    "02-full-company-universe": "02--full-company-universe",
    "03-prepare-one-company": "03--prepare-one-company",
}


def align_github_heading_ids(html: str) -> str:
    """Make Python-Markdown toc ids match INDEX.md GitHub-style anchors."""
    for py_id, gh_id in GITHUB_IDS.items():
        html = html.replace(f'id="{py_id}"', f'id="{gh_id}"')
        html = html.replace(f'href="#{py_id}"', f'href="#{gh_id}"')
    return html


def prepare_index_markdown(index_md: str, appendix_md: str) -> str:
    # Prefer same-page #appendix (INDEX TOC already links there).
    index_md = index_md.replace(
        "[appendix-handbook-ui-sequences.md](appendix-handbook-ui-sequences.md)",
        "[Appendix — Handbook UI sequences §10–12](#appendix)",
    )
    # Point MANUAL links at HTML companions for browser reading.
    index_md = re.sub(
        r"\(media/([^)/]+)/MANUAL\.md\)",
        r"(media/\1/MANUAL.html)",
        index_md,
    )

    # Under ## Appendix, keep intro then embed appendix body.
    appendix_body = appendix_md.strip()
    # Drop a leading H1 if any; keep ## 10 / ## 11 / ## 12 as subsections.
    replacement = (
        "## Appendix\n\n"
        "Handbook UI sequences (§10–12) mirrored for training.\n\n"
        + appendix_body
        + "\n\n"
        "Repo SoT pointers: `OfferingCompanyFinderPage.tsx`, `offeringCompanyFinderWays.ts`, "
        "`companyApproachRoutes.ts`, `CompanyDatabaseView.tsx`, `PrepareOneCompanyPage.tsx`, "
        "`ArticleEnrichmentToolbar.tsx`.\n"
    )

    # Replace from ## Appendix through end (INDEX ends with appendix + SoT line).
    pattern = re.compile(r"^## Appendix\n.*\Z", re.MULTILINE | re.DOTALL)
    if not pattern.search(index_md):
        raise SystemExit("Could not find ## Appendix section in INDEX.md")
    return pattern.sub(replacement, index_md)


def extract_h1(md: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else "Leadtrigger process step"


def main() -> None:
    if not PACK.is_dir():
        raise SystemExit(f"Pack not found at {PACK}")

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    # Copy full media tree (videos, stills, MANUAL.md).
    shutil.copytree(PACK / "media", DOCS / "media")

    # Also keep source markdown at docs root for reference / crawlers.
    shutil.copy2(PACK / "INDEX.md", DOCS / "INDEX.md")
    shutil.copy2(PACK / "appendix-handbook-ui-sequences.md", DOCS / "appendix-handbook-ui-sequences.md")

    index_src = (PACK / "INDEX.md").read_text(encoding="utf-8")
    appendix_src = (PACK / "appendix-handbook-ui-sequences.md").read_text(encoding="utf-8")
    combined = prepare_index_markdown(index_src, appendix_src)
    body = align_github_heading_ids(md_to_html(combined))

    home_title = "Leadtrigger — Offering Company Finder process steps"
    (DOCS / "index.html").write_text(
        page_shell(home_title, body, is_home=True),
        encoding="utf-8",
    )
    (DOCS / "styles.css").write_text(CSS, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # Convert each MANUAL.md → MANUAL.html (relative media paths stay valid).
    for manual in sorted((DOCS / "media").glob("*/MANUAL.md")):
        md = manual.read_text(encoding="utf-8")
        title = extract_h1(md)
        html_body = md_to_html(md)
        out = manual.with_suffix(".html")
        out.write_text(
            page_shell(title, html_body, is_home=False, back_href="../../index.html"),
            encoding="utf-8",
        )
        print(f"wrote {out.relative_to(DOCS)}")

    print(f"wrote {DOCS / 'index.html'}")
    print(f"wrote {DOCS / 'styles.css'}")
    print("media tree copied")


if __name__ == "__main__":
    main()
