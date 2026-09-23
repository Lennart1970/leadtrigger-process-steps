#!/usr/bin/env python3
"""Build flat, crawlable GitHub Pages site from the Leadtrigger process-steps pack."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify

ROOT = Path(__file__).resolve().parent
PACK = Path("/tmp/leadtrigger-pack")
DOCS = ROOT / "docs"
SITE_BASE = "https://lennart1970.github.io/leadtrigger-process-steps"

# Real pages (no #-only discovery). Paths relative to docs/.
PAGES = [
    {
        "slug": "01-refresh-stale-share-article",
        "file": "01-refresh-stale-share-article.html",
        "heading": "## 01 — Refresh stale share article",
        "title": "01 — Refresh stale share article",
        "manual": "media/01-refresh-stale-share-article/MANUAL.html",
        "blurb": "Companies with articles → open share article → Deep research (stale briefs).",
    },
    {
        "slug": "02-full-company-universe",
        "file": "02-full-company-universe.html",
        "heading": "## 02 — Full company universe",
        "title": "02 — Full company universe",
        "manual": "media/02-full-company-universe/MANUAL.html",
        "blurb": "Browse the entire company universe — with and without articles.",
    },
    {
        "slug": "03-prepare-one-company",
        "file": "03-prepare-one-company.html",
        "heading": "## 03 — Prepare one company",
        "title": "03 — Prepare one company",
        "manual": "media/03-prepare-one-company/MANUAL.html",
        "blurb": "Ad-hoc: one company name + domain → research, contacts, article.",
    },
]

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
  margin-bottom: 1.75rem;
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

nav.site-nav {
  margin: 0 0 1.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.9rem;
}

nav.site-nav a {
  color: var(--link);
  margin-right: 1rem;
  text-underline-offset: 2px;
}

nav.site-nav a:hover {
  color: var(--link-hover);
}

.hub-links {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0 2rem;
}

.hub-links li {
  margin: 0 0 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--border);
}

.hub-links a.primary {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--link);
}

.hub-links .blurb {
  display: block;
  color: var(--muted);
  font-size: 0.95rem;
  margin: 0.25rem 0 0.35rem;
}

.hub-links .manual {
  font-size: 0.88rem;
}

.prose h1 {
  display: none; /* page title is in header */
}

.prose h2 {
  font-family: "IBM Plex Serif", Georgia, serif;
  font-size: 1.55rem;
  font-weight: 600;
  margin: 2.25rem 0 1rem;
  padding-top: 0.35rem;
  border-top: 1px solid var(--border);
}

.prose h2:first-of-type {
  border-top: none;
  margin-top: 0.5rem;
}

.prose h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 1.75rem 0 0.65rem;
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


def css_href(depth: int) -> str:
    return "../" * depth + "styles.css"


def page_shell(
    title: str,
    body_html: str,
    *,
    blurb: str,
    depth: int = 0,
    show_nav: bool = True,
    back_href: str | None = None,
) -> str:
    back = ""
    if back_href:
        back = f'<p class="eyebrow"><a href="{back_href}">← Hub (process steps)</a></p>'

    nav = ""
    if show_nav and depth == 0:
        # Real page links only — no # jumps as discovery path.
        nav = """\
<nav class="site-nav" aria-label="Process steps">
  <a href="index.html">Hub</a>
  <a href="01-refresh-stale-share-article.html">01 Refresh</a>
  <a href="02-full-company-universe.html">02 Full universe</a>
  <a href="03-prepare-one-company.html">03 Prepare one</a>
  <a href="appendix.html">Appendix §10–12</a>
</nav>
"""
    elif show_nav and depth > 0:
        prefix = "../" * depth
        nav = f"""\
<nav class="site-nav" aria-label="Process steps">
  <a href="{prefix}index.html">Hub</a>
  <a href="{prefix}01-refresh-stale-share-article.html">01 Refresh</a>
  <a href="{prefix}02-full-company-universe.html">02 Full universe</a>
  <a href="{prefix}03-prepare-one-company.html">03 Prepare one</a>
  <a href="{prefix}appendix.html">Appendix §10–12</a>
</nav>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Leadtrigger Offering Company Finder process steps — chatbot / RAG training corpus with demo media.">
{FONT_LINKS}
<link rel="stylesheet" href="{css_href(depth)}">
</head>
<body>
<div class="wrap">
<header class="site">
{back}
<p class="eyebrow">Leadtrigger · leadtrigger-news · chatbot / RAG training</p>
<h1>{title}</h1>
<p>{blurb}</p>
</header>
{nav}
<article class="prose">
{body_html}
</article>
<footer class="site">
  <p>Static training site · <a href="{SITE_BASE}/">{SITE_BASE.replace("https://", "")}</a> · GitHub Pages (<code>docs/</code>)</p>
</footer>
</div>
</body>
</html>
"""


def split_index_sections(index_md: str) -> dict[str, str]:
    """Split INDEX.md into intro + per-step sections (by ## headings)."""
    # Normalize MANUAL links to .html for crawlable pages.
    index_md = re.sub(
        r"\(media/([^)/]+)/MANUAL\.md\)",
        r"(media/\1/MANUAL.html)",
        index_md,
    )

    # Find all ## sections.
    parts = re.split(r"(?=^## )", index_md, flags=re.MULTILINE)
    intro = parts[0].strip()
    sections: dict[str, str] = {"intro": intro}
    for part in parts[1:]:
        first_line = part.split("\n", 1)[0].strip()
        sections[first_line] = part.strip()
    return sections


def strip_leading_h2(section_md: str) -> str:
    """Keep section body; page header already has the title."""
    return re.sub(r"^## .+\n+", "", section_md, count=1).strip()


def rewrite_toc_to_real_pages(intro_md: str) -> str:
    """Replace in-page # TOC with real HTML page links."""
    intro_md = re.sub(
        r"\[01 — Refresh stale share article\]\(#01--refresh-stale-share-article\)",
        "[01 — Refresh stale share article](01-refresh-stale-share-article.html)",
        intro_md,
    )
    intro_md = re.sub(
        r"\[02 — Full company universe\]\(#02--full-company-universe\)",
        "[02 — Full company universe](02-full-company-universe.html)",
        intro_md,
    )
    intro_md = re.sub(
        r"\[03 — Prepare one company\]\(#03--prepare-one-company\)",
        "[03 — Prepare one company](03-prepare-one-company.html)",
        intro_md,
    )
    intro_md = re.sub(
        r"\[Appendix — Handbook UI sequences §10–12\]\(#appendix\)",
        "[Appendix — Handbook UI sequences §10–12](appendix.html)",
        intro_md,
    )
    # Drop the in-document TOC block if present — hub uses explicit link list.
    intro_md = re.sub(
        r"## Table of contents\n(?:.*\n)*?(?=^---|\Z)",
        "",
        intro_md,
        count=1,
        flags=re.MULTILINE,
    )
    return intro_md.strip()


def hub_body_html(intro_md: str) -> str:
    intro_md = rewrite_toc_to_real_pages(intro_md)
    # Remove trailing --- separators left after TOC removal.
    intro_md = re.sub(r"\n---\s*$", "", intro_md).strip()

    intro_html = md_to_html(intro_md)

    links = ['<h2>Process steps (crawlable pages)</h2>', '<ul class="hub-links">']
    for p in PAGES:
        links.append(
            "<li>"
            f'<a class="primary" href="{p["file"]}">{p["title"]}</a>'
            f'<span class="blurb">{p["blurb"]}</span>'
            f'<a class="manual" href="{p["manual"]}">Step MANUAL</a>'
            "</li>"
        )
    links.append(
        "<li>"
        '<a class="primary" href="appendix.html">Appendix — Handbook UI sequences §10–12</a>'
        '<span class="blurb">Handbook §10–12 mirrored for training (routes, rules, sequences).</span>'
        '<a class="manual" href="appendix-handbook-ui-sequences.md">Source markdown</a>'
        "</li>"
    )
    links.append("</ul>")

    more = md_to_html(
        "Repo SoT pointers: `OfferingCompanyFinderPage.tsx`, `offeringCompanyFinderWays.ts`, "
        "`companyApproachRoutes.ts`, `CompanyDatabaseView.tsx`, `PrepareOneCompanyPage.tsx`, "
        "`ArticleEnrichmentToolbar.tsx`."
    )
    return intro_html + "\n" + "\n".join(links) + "\n" + more


def extract_h1(md: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else "Leadtrigger process step"


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


def write_robots() -> None:
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_BASE}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    if not PACK.is_dir():
        raise SystemExit(f"Pack not found at {PACK}. Unpack the process-steps pack there first.")

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    shutil.copytree(PACK / "media", DOCS / "media")
    shutil.copy2(PACK / "INDEX.md", DOCS / "INDEX.md")
    shutil.copy2(PACK / "appendix-handbook-ui-sequences.md", DOCS / "appendix-handbook-ui-sequences.md")

    index_src = (PACK / "INDEX.md").read_text(encoding="utf-8")
    appendix_src = (PACK / "appendix-handbook-ui-sequences.md").read_text(encoding="utf-8")
    sections = split_index_sections(index_src)

    # --- Hub ---
    hub_title = "Leadtrigger — Offering Company Finder process steps"
    hub_blurb = (
        "Chatbot / RAG training corpus. Flat pages with real links — canonical routes, "
        "decision rules, and demo media."
    )
    (DOCS / "index.html").write_text(
        page_shell(hub_title, hub_body_html(sections["intro"]), blurb=hub_blurb, depth=0),
        encoding="utf-8",
    )
    print("wrote index.html")

    # --- Step pages ---
    for p in PAGES:
        heading = p["heading"]
        if heading not in sections:
            raise SystemExit(f"Missing section {heading!r} in INDEX.md; have: {list(sections)}")
        body_md = strip_leading_h2(sections[heading])
        # Ensure MANUAL link stays crawlable HTML.
        body_md = re.sub(
            r"\(media/([^)/]+)/MANUAL\.md\)",
            r"(media/\1/MANUAL.html)",
            body_md,
        )
        # Append explicit MANUAL + hub links for crawlers (plain hrefs).
        body_md += (
            f"\n\n---\n\n"
            f"**Related crawlable pages:** "
            f"[Step MANUAL]({p['manual']}) · "
            f"[Hub](index.html) · "
            f"[Appendix](appendix.html)\n"
        )
        body_html = md_to_html(body_md)
        (DOCS / p["file"]).write_text(
            page_shell(
                p["title"],
                body_html,
                blurb=p["blurb"],
                depth=0,
                back_href="index.html",
            ),
            encoding="utf-8",
        )
        print(f"wrote {p['file']}")

    # --- Appendix page ---
    appendix_md = (
        "Handbook UI sequences (§10–12) mirrored for training.\n\n"
        + appendix_src.strip()
        + "\n\n---\n\n"
        "**Related crawlable pages:** "
        "[Hub](index.html) · "
        "[01 Refresh](01-refresh-stale-share-article.html) · "
        "[02 Full universe](02-full-company-universe.html) · "
        "[03 Prepare one](03-prepare-one-company.html) · "
        "[Source markdown](appendix-handbook-ui-sequences.md)\n"
    )
    (DOCS / "appendix.html").write_text(
        page_shell(
            "Appendix — Handbook UI sequences §10–12",
            md_to_html(appendix_md),
            blurb="Handbook §10–12 for chatbot training (routes, rules, bot sequences).",
            depth=0,
            back_href="index.html",
        ),
        encoding="utf-8",
    )
    print("wrote appendix.html")

    (DOCS / "styles.css").write_text(CSS, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # --- MANUAL.html under media/ ---
    for manual in sorted((DOCS / "media").glob("*/MANUAL.md")):
        md = manual.read_text(encoding="utf-8")
        title = extract_h1(md)
        html_body = md_to_html(md)
        out = manual.with_suffix(".html")
        out.write_text(
            page_shell(
                title,
                html_body,
                blurb="Process step MANUAL (source of truth for this step).",
                depth=2,
                back_href="../../index.html",
            ),
            encoding="utf-8",
        )
        print(f"wrote {out.relative_to(DOCS)}")

    # --- Sitemap + robots ---
    crawl_urls = [
        f"{SITE_BASE}/",
        f"{SITE_BASE}/index.html",
        f"{SITE_BASE}/01-refresh-stale-share-article.html",
        f"{SITE_BASE}/02-full-company-universe.html",
        f"{SITE_BASE}/03-prepare-one-company.html",
        f"{SITE_BASE}/appendix.html",
        f"{SITE_BASE}/media/01-refresh-stale-share-article/MANUAL.html",
        f"{SITE_BASE}/media/02-full-company-universe/MANUAL.html",
        f"{SITE_BASE}/media/03-prepare-one-company/MANUAL.html",
    ]
    write_sitemap(crawl_urls)
    write_robots()
    print("wrote sitemap.xml")
    print("wrote robots.txt")
    print("media tree copied")


if __name__ == "__main__":
    main()
