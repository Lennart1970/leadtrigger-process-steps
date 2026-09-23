# Process step — Prepare one company

> Bot-optimal. Verified `PrepareOneCompanyPage.tsx` + hub `prepare-one` → `/companies/prepare` 2026-09-23.
> Demo: `demo.mp4` (teach-20260923T142836Z-8086504e-…).

## Intent
Start full research, contacts, and article for **one** named company (ad-hoc), without browsing the universe.

## Entry
| Control | Result |
|---------|--------|
| Hub `/companies/start` → **4 Prepare one company** | `/companies/prepare` |
| Sidebar **Prepare one** | same |
| Code | `PrepareOneCompanyPage` · `App.tsx` route `/companies/prepare` · hub id `prepare-one` |

## Inputs vs constants
| Role | Field | Demo |
|------|-------|------|
| INPUT | `{companyName}` | Embat |
| INPUT | `{domain}` | embat.io |
| SESSION | active brain / Connect Group | Connect Group EMS Intelligence - General |
| CONSTANT | CTA | **Prepare outreach** |
| API | mutation | `leadtrigger.prepareAdhocCompany` |

## Bot steps
1. Ensure active venture is set.
2. Open `/companies/prepare` (hub card 4 or sidebar Prepare one).
3. Fill **Company name** = `{companyName}`, **Domain** = `{domain}` (normalize: strip protocol/www/path; must contain `.`).
4. Click **Prepare outreach**; wait until not pending.
5. Read **OUTREACH STARTED** panel:
   - `status === "created"` → added from Apollo
   - else → found in database
6. Optional follow-ups from panel: Open article (`/share/article/{articleKey}`), Ad-hoc watchlist, View company record (`/company/{companyId}`), Find companies like this (match seed).
7. Report: companyName, domain, status, articleKey, campaignId, companyId.

## Decision rules
- Requires name trim ≥1 and domain ≥4 chars with `.`.
- Background work ~2–5 min — do not assume article content is final immediately; Deep research may still apply later (§10).
- Distinct from Full universe (§11) and with-articles browse (§10).

## Anti-patterns
- Submitting without domain.
- Treating prepare as browse/filter.
- Skipping the OUTREACH STARTED result links when the task needs the article.

## Related
- Handbook §12 · hub cards 1–3 in §10–11.
