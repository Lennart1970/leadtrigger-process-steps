## 10. UI sequence — refresh stale share article (Company finder)

> **Verified 2026-09-23** with `@lt_news_code` — `/companies/start` on `main` @ `7a7bdb440d` (PR #116). Demo same day.
> Why: many share articles are **stale** — run **Deep research** after opening.

### Goal
From Offering Company Finder → companies that already have articles → open share article → **Deep research**.

### Canonical paths
| Step | Route / control | Notes |
|------|-----------------|-------|
| Hub | `/companies/start` | Offering Company Finder · `OfferingCompanyFinderPage` · `OFFERING_COMPANY_FINDER_PATH` · `App.tsx:82` · PR #116 |
| With articles | `/companies?article=with` | Hub card **1** · `article=with` only |
| Full universe | `/companies` | Hub card **2** · **no** `article` param → with **and without** articles |
| Without articles | `/companies?article=without` | Hub card **3** · `article=without` only |
| Share | `/share/article/{articleKey}` | `publicShareArticleUrl(articleKey)` · `Open on new page` |
| Deep research | toolbar stage `deep_research` | Label **Deep research** · `ArticleEnrichmentToolbar` / `campaignBrain.enrichCampaignMember` |

### Decision rules
- If article content / scores look old or wrong-sector → **Deep research** before outreach/copy.
- Watchlist filter = `campaignBrain.listBrainCampaigns` → `watchlistId` = `campaignId` on `lt_mns_brain_campaigns`.
- **CG class** UI label maps to `cgLeadClass` (demo left at All).
- Trust history URL `/companies?article=with` — never `/companies/article-with`.

### Sequence (bot)
1. Open `/companies/start` (active venture already set).
2. Click **1 Companies with articles** → `/companies?article=with`.
3. Set **Watchlist** = `{watchlist}` (demo: **S8**).
4. Optional: **CG class** = All (default).
5. Click **Save filtered (up to 500)**.
6. On row `{company}`, click **Open on new page** → `/share/article/{articleKey}`.
7. Click **Deep research**; wait until toolbar idle / toast complete.
8. Report: company, `articleKey`, research status.

### Inputs vs constants
| Input | Example from demo |
|-------|-------------------|
| `{watchlist}` | S8 |
| `{company}` | Aceros Moldeados de Lacunza SA |
| `{articleKey}` | `08421b9c8af111dc214cffcdd564b8f6` |
| venture | Connect Group EMS Intelligence (session) |
| base URL | `https://leadtrigger-news-production.up.railway.app` |

### Anti-patterns
- Skipping Deep research on stale briefs.
- Treating video-OCR URL `/companies/article-with` as real.
- Opening share without `articleKey` / inventing keys.
- Running Find contacts / Outreach unless asked.

### SoT pointers
- Browse + open: `client/src/pages/CompanyDatabaseView.tsx` (`Save filtered (up to 500)`, `Open on new page`, `articleFilter`, `watchlistId`, `cgLeadClass`).
- Share route: `client/src/App.tsx` `/share/article/:articleKey` · `BrainCampaignArticlePage`.
- Enrichment: `client/src/components/article/ArticleEnrichmentToolbar.tsx` (`deep_research`).
- Copilot mirror of article filter: `server/services/copilotCompanies.ts` (`article=with|without`).
- Hub: `client/src/pages/OfferingCompanyFinderPage.tsx` · `client/src/lib/offeringCompanyFinderWays.ts` (`OFFERING_COMPANY_FINDER_PATH="/companies/start"`; card 1 → `article=with`; card 2 → `/companies`; card 3 → `article=without`) · `companyBrowsePath` in `client/src/lib/companyApproachRoutes.ts` · route `client/src/App.tsx:82`.

---

## 11. UI sequence — Full company universe

> **Verified 2026-09-23** — hub card id `browse-all` in `offeringCompanyFinderWays.ts` → `companyBrowsePath()` → `/companies` (no `article` query). Demo same day (teach session `teach-20260923T142501Z-…`).
> Process pack: `/workspace/lt-manual/process-steps/02-full-company-universe/` · Drive under `lt_manual/process-steps/`.

### Goal
Browse the **entire** company universe for the active venture — includes accounts **with articles and without articles**.

### Canonical paths
| Step | Route / control | Notes |
|------|-----------------|-------|
| Hub | `/companies/start` | Offering Company Finder |
| Full universe | `/companies` | Hub **2 Full company universe** · `id: browse-all` · `companyBrowsePath()` with empty params |
| Optional narrow | `?article=with\|without` | UI can still set article filter **after** entry; default Full universe has **none** |
| Optional region | `?region=…` | e.g. demo later used `region=Europe` |

### Decision rules
- **Full universe ≠ with-articles.** Card 1 (`article=with`) excludes no-brief accounts. Card 2 (`/companies`) returns **both**.
- Card 3 (`article=without`) is the inverse slice (missing briefs only).
- If a bot needs “everyone including no article” → open **Full company universe** / `/companies`, **do not** use `article=with`.
- If `article` query is absent → treat as unfiltered article presence (with + without).
- Watchlist / CG class / Save filtered behave the same as §10 once on browse.

### Sequence (bot)
1. Open `/companies/start`.
2. Click **2 Full company universe** → `/companies` (no `article=`).
3. Optional filters (watchlist, region, CG class) — keep `article` unset unless the task requires a slice.
4. **Save filtered (up to 500)** if persisting the set.
5. Rows may lack **Open on new page** / share when there is **no** article — expected for without-article accounts.
6. Report: filter state (`article` absent vs `with`/`without`), counts if available, sample companies.

### Anti-patterns
- Calling Full universe then navigating to `?article=with` and treating that as the full universe result.
- Assuming every Full-universe row has a share article / Deep research path.
- Confusing card 2 with card 3 (`without` only).

### SoT pointers
- Hub ways: `client/src/lib/offeringCompanyFinderWays.ts` — `browse-all` → `companyBrowsePath()`.
- Browse path builder: `client/src/lib/companyApproachRoutes.ts` — `article` only set when `"with"` \| `"without"`.
- Browse UI: `client/src/pages/CompanyDatabaseView.tsx` (`articleFilter`).
- Copilot mirror: `server/services/copilotCompanies.ts`.

---

## 12. UI sequence — Prepare one company

> **Verified 2026-09-23** — `PrepareOneCompanyPage` · route `/companies/prepare` · hub id `prepare-one` · mutation `leadtrigger.prepareAdhocCompany`. Demo: Embat / `embat.io`.
> Process pack: `/workspace/lt-manual/process-steps/03-prepare-one-company/`.

### Goal
Ad-hoc: enter **one** company name + domain → start research, contacts, and article (~2–5 min).

### Canonical paths
| Step | Route / control | Notes |
|------|-----------------|-------|
| Hub | `/companies/start` → **4 Prepare one company** | `id: prepare-one` · href `/companies/prepare` |
| Page | `/companies/prepare` | `PrepareOneCompanyPage` · `App.tsx` |
| CTA | **Prepare outreach** | disabled until name + valid domain |
| Result | OUTREACH STARTED panel | Open article / Ad-hoc watchlist / View company / Find like this |

### Decision rules
- Domain normalized: strip `https://`, `www.`, path/query; require `.`.
- `status === "created"` → Apollo add; else already in DB.
- Queues into Ad-hoc requests / watchlist; research runs in background.
- Not a universe browse — use §11 for full list.

### Sequence (bot)
1. Active venture set.
2. Open `/companies/prepare`.
3. `{companyName}` + `{domain}` → **Prepare outreach**.
4. Capture result ids (`articleKey`, `campaignId`, `companyId`, `status`).
5. Report + optional Open article.

### Inputs vs constants
| Input | Demo |
|-------|------|
| `{companyName}` | Embat |
| `{domain}` | embat.io |

### Anti-patterns
- Empty domain; inventing articleKey before mutation returns.
- Confusing with card 1–3 browse paths.

### SoT pointers
- `client/src/pages/PrepareOneCompanyPage.tsx`
- Hub: `client/src/lib/offeringCompanyFinderWays.ts` (`prepare-one`)
- Admin queues: `/admin/prepare-requests` · `AdhocPrepareRequestsPage`
