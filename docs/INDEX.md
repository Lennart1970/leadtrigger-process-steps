# Leadtrigger — Offering Company Finder process steps (chatbot training)

> **Audience:** chatbot / Grok Bot training corpus. Dense. Routes, rules, media.
> **Product:** `leadtrigger-news` · prod `https://leadtrigger-news-production.up.railway.app`
> **Hub:** `/companies/start` — Offering Company Finder
> **Source packs:** local `/workspace/lt-manual/process-steps/` · Drive `lt_manual/process-steps/`
> **Verified:** 2026-09-23 with `@lt_news_code` / demos · handbook §10–12

## How to use this page
- Prefer **canonical routes** and **decision rules** over screenshots.
- Videos show the UI path; **Chrome history URLs beat OCR**.
- Inputs in `{braces}` are parameters; demo values are examples only.

## Hub card map (Start from companies)
| # | Title | Route | Article presence |
|---|-------|-------|------------------|
| 1 | Companies with articles | `/companies?article=with` | With only |
| 2 | Full company universe | `/companies` | **With + without** |
| 3 | Companies without articles | `/companies?article=without` | Without only |
| 4 | Prepare one company | `/companies/prepare` | N/A (ad-hoc create/queue) |

Code: `client/src/lib/offeringCompanyFinderWays.ts` · `companyBrowsePath()` in `client/src/lib/companyApproachRoutes.ts`.

## Table of contents
1. [01 — Refresh stale share article](#01--refresh-stale-share-article)
2. [02 — Full company universe](#02--full-company-universe)
3. [03 — Prepare one company](#03--prepare-one-company)
4. [Appendix — Handbook UI sequences §10–12](#appendix)

---

## 01 — Refresh stale share article

**Goal:** From Offering Company Finder → companies **with** articles → open share article → run **Deep research** (many briefs are stale).

### Canonical paths
| Step | Route / control |
|------|-----------------|
| Hub | `/companies/start` |
| With articles | `/companies?article=with` |
| Share | `/share/article/{articleKey}` via **Open on new page** |
| Enrich | Toolbar **Deep research** (`stage: deep_research`) |

### Decision rules
- If content / scores look old or wrong-sector → Deep research before outreach/copy.
- Watchlist filter = `campaignBrain.listBrainCampaigns` → `campaignId`.
- **CG class** UI = `cgLeadClass` (demo: All).
- Trust history URL `/companies?article=with` — never `/companies/article-with`.

### Inputs vs constants (demo)
| Kind | Name | Demo |
|------|------|------|
| INPUT | `{watchlist}` | S8 |
| INPUT | `{company}` | Aceros Moldeados de Lacunza SA |
| INPUT | `{articleKey}` | `08421b9c8af111dc214cffcdd564b8f6` |
| SESSION | venture | Connect Group EMS Intelligence |
| CONST | base | `https://leadtrigger-news-production.up.railway.app` |

### Bot sequence
1. Open `/companies/start`.
2. Click **1 Companies with articles** → `/companies?article=with`.
3. Set **Watchlist** = `{watchlist}`.
4. Optional: **CG class** = All.
5. **Save filtered (up to 500)**.
6. On `{company}`, **Open on new page** → `/share/article/{articleKey}`.
7. Click **Deep research**; wait until idle / toast complete.
8. Report: company, `articleKey`, research status.

### Anti-patterns
- Skip Deep research on stale briefs.
- Invent `articleKey`.
- Run Find contacts / Outreach unless asked.
- Treat video OCR paths as canonical when history disagrees.

### Media
![Still ~20%](media/01-refresh-stale-share-article/frame_20pct.png)

![Still ~70% / share article](media/01-refresh-stale-share-article/frame_70pct.png)

<video controls src="media/01-refresh-stale-share-article/demo.mp4"></video>

Full step MANUAL: [media/01-refresh-stale-share-article/MANUAL.md](media/01-refresh-stale-share-article/MANUAL.md)

---

## 02 — Full company universe

**Goal:** Browse the **entire** company universe — includes accounts **with and without** articles.

### Canonical paths
| Step | Route / control |
|------|-----------------|
| Hub | `/companies/start` → **2 Full company universe** |
| Full universe | `/companies` (no `article` query) · hub id `browse-all` · `companyBrowsePath()` |

### Decision rules
- Full universe ≠ with-articles. Card 1 excludes no-brief accounts. Card 2 returns **both**.
- Card 3 (`article=without`) is missing-briefs only.
- If `article` query is absent → with + without.
- Do not navigate to `?article=with` and call that Full universe.

### Bot sequence
1. Open `/companies/start`.
2. Click **2 Full company universe** → `/companies` (no `article=`).
3. Optional filters (watchlist, region, CG class) — keep `article` unset for true full universe.
4. Optional **Save filtered (up to 500)**.
5. Rows may lack share / Deep research when there is no article — expected.
6. Report filter state + sample companies.

### Anti-patterns
- Using `article=with` and calling it Full universe.
- Expecting every row to have an `articleKey`.

### Media
![Still ~20%](media/02-full-company-universe/frame_20pct.png)

![Still ~70%](media/02-full-company-universe/frame_70pct.png)

<video controls src="media/02-full-company-universe/demo.mp4"></video>

Full step MANUAL: [media/02-full-company-universe/MANUAL.md](media/02-full-company-universe/MANUAL.md)

---

## 03 — Prepare one company

**Goal:** Ad-hoc — enter **one** company name + domain → start research, contacts, and article (~2–5 min).

### Canonical paths
| Step | Route / control |
|------|-----------------|
| Hub | `/companies/start` → **4 Prepare one company** · id `prepare-one` |
| Page | `/companies/prepare` · `PrepareOneCompanyPage` |
| CTA | **Prepare outreach** |
| API | `leadtrigger.prepareAdhocCompany` |

### Decision rules
- Domain normalized: strip `https://`, `www.`, path/query; require `.`.
- `status === "created"` → Apollo add; else already in DB.
- Queues Ad-hoc requests; research runs in background.
- Not a universe browse (§02).

### Inputs vs constants (demo)
| Role | Field | Demo |
|------|-------|------|
| INPUT | `{companyName}` | Embat |
| INPUT | `{domain}` | embat.io |
| SESSION | venture | Connect Group EMS Intelligence - General |

### Bot sequence
1. Active venture set.
2. Open `/companies/prepare`.
3. `{companyName}` + `{domain}` → **Prepare outreach**.
4. Read **OUTREACH STARTED** (created vs found in database).
5. Optional: Open article `/share/article/{articleKey}`, Ad-hoc watchlist, View company `/company/{companyId}`, Find companies like this.
6. Report: name, domain, status, ids.

### Anti-patterns
- Submit without domain.
- Invent `articleKey` before mutation returns.
- Confuse with hub cards 1–3 browse paths.

### Media
![Still ~20%](media/03-prepare-one-company/frame_20pct.png)

![Still ~70%](media/03-prepare-one-company/frame_70pct.png)

<video controls src="media/03-prepare-one-company/demo.mp4"></video>

Full step MANUAL: [media/03-prepare-one-company/MANUAL.md](media/03-prepare-one-company/MANUAL.md)

---

## Appendix

Handbook UI sequences (§10–12) mirrored for training: [appendix-handbook-ui-sequences.md](appendix-handbook-ui-sequences.md)

Repo SoT pointers: `OfferingCompanyFinderPage.tsx`, `offeringCompanyFinderWays.ts`, `companyApproachRoutes.ts`, `CompanyDatabaseView.tsx`, `PrepareOneCompanyPage.tsx`, `ArticleEnrichmentToolbar.tsx`.
