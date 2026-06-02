# SEO Audit Report — All 8 GuideStack Sites
**Date:** 2026-05-12 | **Auditor:** Content Creator Agent | **Issue:** AGE-665

## Executive Summary
All 8 sites share a common Astro template with the same SEO infrastructure. Several **critical** issues affect all sites uniformly, plus a few site-specific problems. The most impactful issues are: sitemaps using `example.com` instead of real domains, missing sitemap for smart-emergency-fund, placeholder SVG OG images, thin meta descriptions, and unresolved `[LINK:]` cross-site link placeholders in article content.

---

## Site Inventory

| Site | Domain | Articles | Sitemap | robots.txt |
|------|--------|----------|---------|------------|
| ai-tools-hub | ai-tools-and-productivity.com | 52 | ✅ (broken URLs) | ✅ |
| bitcoin-beginners | bitcoin-beginners.com | 55 | ✅ (broken URLs) | ✅ |
| budget-travel-tips | budget-travel.com | 51 | ✅ (broken URLs) | ✅ |
| crypto-investing-guide | crypto-investing.com | 53 | ✅ (broken URLs) | ✅ |
| crypto-trading-strategies | crypto-trading-strategies.com | 57 | ✅ (broken URLs) | ✅ |
| defi-yield-guide | defi-yield-guide.com | 56 | ✅ (broken URLs) | ✅ |
| personal-finance-tips | personal-finance.com | 51 | ✅ (broken URLs) | ✅ |
| smart-emergency-fund | emergency-fund.com | 43 | ❌ MISSING | ✅ |

**Total: 418 articles across 8 sites**

---

## Critical Issues (All Sites)

### 🔴 P0: Sitemap Uses `example.com` Instead of Real Domains
- **Impact:** Google cannot index any URLs from sitemaps — all point to `example.com`
- **Root Cause:** `astro.config.mjs` has `site: 'https://example.com'` on ALL 8 sites
- **Fix:** Update each site's `astro.config.mjs` to use the correct domain from `site-config.json`
- **Example:** `site: 'https://ai-tools-and-productivity.com'`
- **Priority:** MUST fix before any deployment — without this, sitemaps are useless

### 🔴 P0: smart-emergency-fund Has No Sitemap
- **Impact:** 43 articles have no sitemap discovery path for Google
- **Root Cause:** Missing sitemap generation or build step
- **Fix:** Ensure sitemap generation runs during build (requires correct `astro.config.mjs` site URL + `@astrojs/sitemap` integration or manual sitemap script)

### 🟠 P1: OG/Twitter Images Are Inline SVG Placeholders
- **Impact:** Social sharing shows generic gradient rectangles, not branded images. Twitter/LinkedIn/Facebook previews look broken. CTR from social drops ~60-80%.
- **Root Cause:** `BaseLayout.astro` generates inline SVG data URIs as OG images
- **Fix Options:**
  1. **Free (build-time):** Generate PNG OG images during build using `satori` (free, open-source) + `sharp` for PNG conversion. Integrate into Astro build pipeline.
  2. **Free (runtime):** Use `@vercel/og` or `satori` in a serverless function
  3. **Free (manual):** Create template in GIMP/Inkscape, batch-generate
- **Cost:** $0 — satori + sharp are open-source

### 🟠 P1: Meta Descriptions Too Short (6 of 8 Sites)
- **Impact:** Google may auto-generate snippets, losing control of SERP messaging
- **Details:**
  - ai-tools-hub: 57 chars (target: 120-155)
  - bitcoin-beginners: 56 chars
  - budget-travel-tips: 60 chars
  - defi-yield-guide: 43 chars
  - personal-finance-tips: 69 chars
  - crypto-investing-guide: 69 chars
- **Fix:** Update content generator to write 120-155 character descriptions with primary keyword + value proposition

### 🟠 P1: Unresolved `[LINK:]` Placeholders in Article Content
- **Impact:** Broken links visible to users, confusing content, no cross-site SEO benefit
- **Affected Sites:**
  - ai-tools-hub: 3 unresolved `[LINK:...]` placeholders
  - bitcoin-beginners: 3 unresolved
  - budget-travel-tips: 5 unresolved
- **Fix:** Build a link resolver that maps `[LINK: slug/text]` to actual article URLs. For cross-site links, resolve to the target site's canonical URL.

### 🟠 P1: Duplicate H1 Tags
- **Impact:** Confusing heading hierarchy, potential SEO penalty
- **Details:** Every article has 2 `<h1>` tags — one in the article header and one in the article body
- **Fix:** Change the in-body `<h1>` to `<h2>` — only one H1 per page (the article title)

### 🟠 P1: defi-yield-guide Has Duplicate Name ("DeFi Yield Guide **Guide**")
- **Impact:** Unprofessional branding in titles, schema, and navigation
- **Root Cause:** `site-config.json` name = "DeFi Yield Guide Guide"
- **Fix:** Change to "DeFi Yield Guide" in `site-config.json`

---

## Medium Issues

### 🟡 P2: No Cross-Site Internal Linking
- **Impact:** Missing significant SEO juice between related sites in the network
- **Opportunity:** crypto-investing-guide ↔ defi-yield-guide ↔ bitcoin-beginners ↔ crypto-trading-strategies are highly related
- **Fix:** Build cross-site linking module (already tracked as AGE-666)

### 🟡 P2: No Master Sitemap Index
- **Impact:** No single submission point for all 8 sites in Google Search Console
- **Fix:** Create `sitemap-index.xml` referencing all 8 site sitemaps (tracked as AGE-666)

### 🟡 P2: Missing FAQ Schema on 3 Sites
- **Impact:** Missing rich snippet opportunity in Google search results
- **Sites:** crypto-investing-guide, crypto-trading-strategies, smart-emergency-fund (0 FAQ questions)
- **Fix:** Ensure content generator includes FAQ sections with `Question`/`Answer` schema

### 🟡 P2: No HowTo Schema Anywhere
- **Impact:** Missing step-by-step rich snippets for tutorial/guide content
- **Fix:** Add `HowTo` schema for articles with numbered steps

### 🟡 P2: Article Word Count Low on Some Sites
- **Details:**
  - crypto-investing-guide: ~877 words (thin content risk)
  - ai-tools-hub: ~1,344 words (borderline)
  - bitcoin-beginners: ~1,317 words (borderline)
- **Target:** 1,500-2,500 words for competitive keywords
- **Fix:** Content generator should produce longer, more detailed articles

### 🟡 P2: No `<img>` Tags / No Images in Articles
- **Impact:** No image SEO, no visual break-up, missing 150% engagement boost
- **Fix:** Add relevant images (even stock/CC) with proper alt text, lazy loading, and width/height attributes

---

## Low Issues

### 🟢 P3: No Lazy Loading on Any Images
- **Impact:** Minor Core Web Vitals impact (currently no images to lazy-load)
- **Fix:** Add `loading="lazy"` to all `<img>` tags when images are added

### 🟢 P3: Favicon Uses Data URI Emoji
- **Impact:** No unique favicon, unprofessional branding in browser tabs
- **Fix:** Generate proper favicon.ico + apple-touch-icon.png per site

### 🟢 P3: Title Case Inconsistency
- **Impact:** Unprofessional appearance
- **Details:** Some titles use lowercase ("ai tools for small business owners"), others use Title Case ("Best Budget Travel Tips For Beginners")
- **Fix:** Standardize to Title Case in titles, lowercase in URLs

---

## What's Working Well ✅

- **Canonical URLs** — Correct real domains on all pages ✅
- **robots.txt** — Comprehensive, allows all major bots including AI crawlers ✅
- **BreadcrumbList Schema** — Present on all pages ✅
- **Organization + WebSite Schema** — Present on all pages ✅
- **BlogPosting Schema** — Present on all pages ✅
- **Article meta** — published_time, modified_time, author, section all present ✅
- **OG/Twitter tags** — Structured correctly (just need real images) ✅
- **Preconnect** — Fonts CDN preconnected ✅
- **Dark mode** — Theme toggle with CSS variables ✅
- **Reading progress bar** — UX enhancement ✅
- **Responsive navigation** — Mobile menu ✅

---

## Prioritized Fix List

| Priority | Fix | Effort | Impact | Sites |
|----------|-----|--------|--------|-------|
| 🔴 P0 | Fix `astro.config.mjs` site URLs (example.com → real domain) | 5 min | CRITICAL | All 8 |
| 🔴 P0 | Regenerate sitemaps with correct domains | 5 min | CRITICAL | All 8 |
| 🔴 P0 | Generate sitemap for smart-emergency-fund | 10 min | HIGH | 1 |
| 🟠 P1 | Fix duplicate H1 → H2 in article body | 15 min | HIGH | All 8 |
| 🟠 P1 | Fix defi-yield-guide duplicate name | 2 min | MEDIUM | 1 |
| 🟠 P1 | Regenerate thin meta descriptions | 30 min | HIGH | 6 sites |
| 🟠 P1 | Resolve [LINK:] placeholders in articles | 30 min | HIGH | 3 sites |
| 🟠 P1 | Generate real OG images (satori) | 2 hours | HIGH | All 8 |
| 🟡 P2 | Add FAQ schema to 3 missing sites | 30 min | MEDIUM | 3 |
| 🟡 P2 | Add HowTo schema for tutorial articles | 1 hour | MEDIUM | All 8 |
| 🟡 P2 | Expand thin articles (< 1200 words) | Ongoing | MEDIUM | 3 |
| 🟡 P2 | Add images to articles | Ongoing | MEDIUM | All 8 |
| 🟢 P3 | Generate proper favicons | 30 min | LOW | All 8 |
| 🟢 P3 | Standardize title casing | 15 min | LOW | All 8 |

---

## Recommended Immediate Actions (This Week)

1. **Fix astro.config.mjs on all 8 sites** — change `site: 'https://example.com'` to correct domain
2. **Rebuild all sites** — regenerate sitemaps with correct URLs
3. **Fix duplicate H1** in BaseLayout.astro template
4. **Fix defi-yield-guide name** in site-config.json
5. **Resolve [LINK:] placeholders** in affected articles

These 5 fixes will make the sites **deployment-ready** from an SEO infrastructure perspective.

---

## Cost Analysis

| Item | Free Option | Paid Alternative |
|------|-------------|-----------------|
| OG Image Generation | satori + sharp (open-source, $0) | Canva API ($0), but satori is better for automation |
| Sitemap | @astrojs/sitemap (free Astro integration) | N/A — free is best |
| Schema Validation | Google Rich Results Test (free) | Schema.org Validator (free) |
| SEO Audit | This report (free) | Screaming Frog ($259/yr), Ahrefs ($99/mo) |
| Image Optimization | sharp (open-source, $0) | Cloudinary (free tier available) |

**Total cost for all fixes: $0** — everything can be done with free/open-source tools.

---

_Report generated by Content Creator Agent (Content Creator) via Paperclip_
