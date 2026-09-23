# Process step — Full company universe

> Bot-optimal. Verified against `offeringCompanyFinderWays.ts` + `companyBrowsePath()` 2026-09-23.
> Demo video: `demo.mp4` (teach-20260923T142501Z-8f8d55f2-…).

## Intent
Open the **full** company universe for the active venture so the set includes accounts **with articles and without articles**.

## Entry
| Control | Result |
|---------|--------|
| Hub `/companies/start` → **2 Full company universe** | `/companies` |
| Code | `id: browse-all` · `companyBrowsePath()` · empty `BrowsePathParams` |

## Article presence
| Hub card | Route | Article presence |
|----------|-------|------------------|
| 1 Companies with articles | `/companies?article=with` | With only |
| **2 Full company universe** | **`/companies`** | **With + without** |
| 3 Companies without articles | `/companies?article=without` | Without only |

## Bot steps
1. Navigate `/companies/start`.
2. Click **2 Full company universe** → land on `/companies` with **no** `article` query.
3. Apply other filters only if the task requires (watchlist, region, CG class). Keep `article` unset for true full universe.
4. Optional: **Save filtered (up to 500)**.
5. Expect some rows **without** share / Deep research — that is correct.

## Demo chrome history (this recording)
1. `/companies/start`
2. `/companies` ← Full universe
3. Later narrowed in-session to `?article=with` then `?region=Europe&article=with` — **do not** treat those as the Full-universe definition; they are optional post-entry filters.

## Anti-patterns
- Using `article=with` and calling it Full universe.
- Expecting every row to have an articleKey.

## Related
- Handbook §11 · §10 (with-articles → Deep research).
- Sibling process-step `01-refresh-stale-share-article` (card 1 path).
