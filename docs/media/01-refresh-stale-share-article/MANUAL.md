# Process step 01 — Refresh stale share article (Company finder → Deep research)

> **Audience:** Grok Bots (`lt_*`). Spec-like. Not a human tutorial.
> **Demo:** 2026-09-23 16:14–16:16 Europe/Amsterdam · teach session `teach-20260923T141440Z-3d20767a-6a76-491a-a590-ab88758060d2`
> **Env:** `https://leadtrigger-news-production.up.railway.app` · venture Connect Group EMS Intelligence
> **Related skill:** [Refresh share article via Deep research](sand-workflow:refresh-share-article-via-deep-research)
> **Parent handbook:** `LEADTRIGGER_BOT_MANUAL.md` §10 (summary only). This folder is the **source of truth** for the step.

## Why
Many `/share/article/{articleKey}` briefs are **stale**. After opening from Company finder, run **Deep research** before trusting fit/urgency/copy.

## Assets
| File | Role |
|------|------|
| `demo.mp4` | Full screen recording — restored 2026-09-23 from teach-20260923T135442Z (~55s; ends on share article Deep research). |
| `assets/frame_20pct.png` | Still ~18s into demo (hub → loading) |
| `assets/frame_70pct.png` | Still ~63s (share article / PEOPLE) |
| `assets/after_deep_research.webp` | Post–Deep research click on Aceros Moldeados |

## Canonical paths
| Step | Route / control |
|------|-----------------|
| Hub | `/companies/start` — Offering Company Finder |
| With articles | `/companies?article=with` — Browse companies |
| Share | `/share/article/{articleKey}` — `Open on new page` |
| Enrich | Toolbar **Deep research** (`stage: deep_research`) |

## Inputs vs constants
| Kind | Name | Demo value |
|------|------|------------|
| INPUT | `{watchlist}` | S8 |
| INPUT | `{company}` | Aceros Moldeados de Lacunza SA |
| INPUT | `{articleKey}` | `08421b9c8af111dc214cffcdd564b8f6` |
| SESSION | venture / brain | Connect Group EMS Intelligence |
| CONST | base URL | `https://leadtrigger-news-production.up.railway.app` |
| CONST | article filter | `article=with` |
| CONST | CG class | All (`cgLeadClass` empty) |

## Sequence
1. Open `{base}/companies/start`.
2. Click **1 Companies with articles** → `{base}/companies?article=with`.
3. Set **Watchlist** = `{watchlist}` (dropdown from `campaignBrain.listBrainCampaigns` → `campaignId`).
4. Leave **CG class** at All unless specified.
5. Click **Save filtered (up to 500)**.
6. On `{company}` row, click **Open on new page** → new tab `{base}/share/article/{articleKey}`.
7. Click **Deep research**. Wait until toolbar idle / toast complete.
8. Report: company, `articleKey`, research status.

## Chrome history (trust over OCR)
- `2026-09-23T14:15:00Z` → `/companies?article=with`
- `2026-09-23T14:15:50Z` → `/share/article/08421b9c8af111dc214cffcdd564b8f6`
- Do **not** use `/companies/article-with` (video OCR misread).

## Code SoT
- Browse: `client/src/pages/CompanyDatabaseView.tsx` — filters, `Save filtered (up to 500)`, `Open on new page` → `publicShareArticleUrl`
- Share: `client/src/App.tsx` `/share/article/:articleKey` · `BrainCampaignArticlePage`
- Enrich: `client/src/components/article/ArticleEnrichmentToolbar.tsx` (`deep_research`)
- Article filter mirror: `server/services/copilotCompanies.ts` (`article=with|without`)
- Hub: `client/src/pages/OfferingCompanyFinderPage.tsx` · `client/src/lib/offeringCompanyFinderWays.ts` (`OFFERING_COMPANY_FINDER_PATH="/companies/start"`; card 1 **"Companies with articles"** → `/companies?article=with`) · `client/src/App.tsx:82` · `main` @ `7a7bdb440d` PR #116

## Anti-patterns
- Skip Deep research on stale briefs.
- Invent `articleKey` / scores.
- Run Find contacts / Outreach / Apollo unless asked.
- Treat video OCR paths as canonical when history disagrees.

## Verify status
- `/companies/start` hub: **VERIFIED** `@lt_news_code` 2026-09-23 — `main` `7a7bdb440d` PR #116 · `App.tsx:82` · `offeringCompanyFinderWays.ts`
- `/companies?article=with`, Save filtered, Open on new page, Deep research toolbar: **repo-backed**
