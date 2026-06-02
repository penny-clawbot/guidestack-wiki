# GuideStack — Cloudflare Pages Deployment Pipeline & Domain Strategy

> **Status:** Ready for execution — step-by-step guide for Daniel
> **Created:** 2026-05-12 by Senior Developer (Paperclip)
> **Project:** GuideStack PSEO Network (8 sites)

---

## 1. Current State Overview

| Site | Niche | Articles | Build Size | Status |
|------|-------|----------|------------|--------|
| ai-tools-hub | AI tools & productivity | 52 | 2.3 MB | Built ✅ |
| bitcoin-beginners | Bitcoin education | 52 | 2.5 MB | Built ✅ |
| budget-travel-tips | Budget travel | 52 | 2.3 MB | Built ✅ |
| crypto-investing-guide | Crypto investing | 53 | 2.6 MB | Built ✅ |
| crypto-trading-strategies | Crypto trading | 52 | 2.6 MB | Built ✅ |
| defi-yield-guide | DeFi yields | 43 | 2.5 MB | Built ✅ |
| personal-finance-tips | Personal finance | 52 | 2.2 MB | Built ✅ |
| smart-emergency-fund | Emergency funds | 20 | 1.8 MB | Built ✅ |
| **TOTAL** | | **376** | **~19 MB** | |

All sites are **static Astro builds** — output in `dist/` folders. No server-side rendering. No runtime dependencies.

---

## 2. Domain Strategy

### 2.1 Domain Name Recommendations

For PSEO, **exact-match or near-match domains** help with SEO. Budget-friendly options:

| Site | Primary Pick | Alternative 1 | Alternative 2 |
|------|-------------|---------------|---------------|
| ai-tools-hub | `aitoolshub.io` | `best-ai-tools.org` | `ai-tools-guide.com` |
| bitcoin-beginners | `bitcoinbeginners.org` | `btc-beginners.com` | `learn-bitcoin.org` |
| budget-travel-tips | `budgettraveltips.org` | `cheap-travel-tips.com` | `budget-travel-guide.com` |
| crypto-investing-guide | `cryptoinvesting.guide` | `crypto-invest.io` | `invest-crypto.org` |
| crypto-trading-strategies | `cryptotradingstrategies.com` | `crypto-trading-tips.org` | `trade-crypto.net` |
| defi-yield-guide | `defiyield.guide` | `defi-yields.com` | `defi-yield-guide.org` |
| personal-finance-tips | `personalfinancetips.org` | `finance-tips.com` | `smart-finance.org` |
| smart-emergency-fund | `emergencyfund.guide` | `smart-emergency-fund.com` | `emergency-fund-tips.org` |

### 2.2 Budget-Friendly Registrars (FREE/Open-Source Priority)

| Registrar | `.com` | `.org` | `.io` | `.guide` | `.net` | Notes |
|-----------|--------|--------|-------|----------|--------|-------|
| **Cloudflare Registrar** ⭐ | $9.77/yr | $9.93/yr | ~$35/yr | ~$20/yr | $10.44/yr | **At-cost pricing, no markup. Best choice since we're using CF Pages.** |
| Porkbun | $10.87/yr | $10.87/yr | $35.18/yr | $22.87/yr | $12.87/yr | Free WHOIS privacy, good UX |
| Namecheap | $9.48/yr | $9.98/yr | $29.88/yr | ~$20/yr | $11.98/yr | Cheap first year, renewal higher |
| Spaceship | $8.98/yr | $8.58/yr | $25.88/yr | ~$18/yr | $9.48/yr | New registrar, aggressive pricing |

**Recommendation: Cloudflare Registrar** — Zero markup, integrated DNS, one less account to manage. Transfer domains to CF after purchase if buying elsewhere.

### 2.3 Domain Cost Estimate

| Scenario | Domains | Cost/yr |
|----------|---------|---------|
| **Budget** — Mix of `.org` / `.com` via Cloudflare | 8 | ~$80-85/yr |
| **Premium** — All `.com` via Cloudflare | 8 | ~$78/yr |
| **Minimum** — Use CF Pages subdomains first, domains later | 0 | $0/yr |

**Recommended approach:** Start with **Cloudflare Pages subdomains** (`site-name.pages.dev`) for immediate deployment. Purchase domains after verifying Google indexing and initial traffic (saves money if a niche underperforms).

---

## 3. GitHub Repository Setup

### 3.1 Repository Structure

One monorepo with each site as a subdirectory:

```
guidestack-pseo/
├── ai-tools-hub/           # Full Astro project
│   ├── src/
│   ├── dist/               # ⚠️ Gitignored — built by CF Pages
│   ├── public/
│   ├── astro.config.mjs
│   ├── package.json
│   └── ...
├── bitcoin-beginners/
├── budget-travel-tips/
├── crypto-investing-guide/
├── crypto-trading-strategies/
├── defi-yield-guide/
├── personal-finance-tips/
├── smart-emergency-fund/
├── .github/
│   └── workflows/          # CI/CD (optional — CF Pages handles builds)
├── shared/                 # Shared templates, configs
└── README.md
```

### 3.2 Setup Commands

```bash
# 1. Create monorepo on GitHub (already exists as DBOT-DC/guidestack-pseo)
cd /Users/penny/Documents/Penny/pseo-network

# 2. Initialize git in output/sites
cd output/sites
git init
git remote add origin git@github.com:DBOT-DC/guidestack-pseo.git

# 3. Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
dist/
.astro/
.DS_Store
*.log
EOF

# 4. Push all sites
git add .
git commit -m "Initial commit: 8 PSEO sites, 376 articles"
git branch -M main
git push -u origin main
```

**Alternative: One repo per site** — If you prefer separate repos (easier per-site CF Pages config):

```bash
for site in ai-tools-hub bitcoin-beginners budget-travel-tips \
  crypto-investing-guide crypto-trading-strategies defi-yield-guide \
  personal-finance-tips smart-emergency-fund; do
  
  # Create repo on GitHub (via gh CLI)
  gh repo create DBOT-DC/gs-${site} --private
  
  # Init & push
  cd /Users/penny/Documents/Penny/pseo-network/output/sites/${site}
  git init
  echo "node_modules/\ndist/\n.astro/\n.DS_Store" > .gitignore
  git add .
  git commit -m "Initial: ${site} PSEO site"
  git remote add origin git@github.com:DBOT-DC/gs-${site}.git
  git branch -M main
  git push -u origin main
done
```

**Recommendation:** **Monorepo** — simpler management, single CI pipeline, easier bulk updates. Use CF Pages "root directory" setting to deploy subdirectories.

---

## 4. Cloudflare Pages Setup

### 4.1 Prerequisites

- Cloudflare account (free tier works — 500 builds/month, unlimited bandwidth)
- GitHub account connected to Cloudflare
- Sites pushed to GitHub

### 4.2 Create Each Project

For each of the 8 sites, create a separate Cloudflare Pages project:

**Via Cloudflare Dashboard:**

1. Go to **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Select `DBOT-DC/guidestack-pseo` repo
3. Configure:

| Setting | Value |
|---------|-------|
| Project name | `ai-tools-hub` (or site name) |
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Root directory | `ai-tools-hub` ← **Critical: points to subdirectory** |
| Node.js version | `20` |

4. Click **Save and Deploy**

**Via Cloudflare Wrangler CLI (faster for bulk setup):**

```bash
# Install wrangler (FREE, open-source)
npm install -g wrangler

# Login
wrangler login

# Create projects for each site
for site in ai-tools-hub bitcoin-beginners budget-travel-tips \
  crypto-investing-guide crypto-trading-strategies defi-yield-guide \
  personal-finance-tips smart-emergency-fund; do
  
  wrangler pages project create gs-${site} --production-branch main
done
```

### 4.3 First Deploy (Manual — for pre-built dist/)

If you want to deploy immediately without waiting for GitHub integration:

```bash
for site in ai-tools-hub bitcoin-beginners budget-travel-tips \
  crypto-investing-guide crypto-trading-strategies defi-yield-guide \
  personal-finance-tips smart-emergency-fund; do
  
  echo "Deploying ${site}..."
  cd /Users/penny/Documents/Penny/pseo-network/output/sites/${site}
  npx wrangler pages deploy dist --project-name=gs-${site}
done
```

This gives you instant URLs like:
- `gs-ai-tools-hub.pages.dev`
- `gs-bitcoin-beginners.pages.dev`
- etc.

### 4.4 Auto-Deploy on Push (GitHub Integration)

Once GitHub is connected in CF Pages dashboard:

1. Every `git push` to `main` triggers a rebuild
2. Cloudflare runs `npm install && npm run build` in the site's root directory
3. Deployed automatically to production

**Content workflow after setup:**
```bash
# Generate new content
python3 scripts/content-burst.py --site budget-travel-tips --count 5

# Rebuild site
cd output/sites/budget-travel-tips && npm run build

# Commit & push (auto-deploys)
git add .
git commit -m "Add 5 new budget travel articles"
git push
```

---

## 5. DNS Configuration

### 5.1 Custom Domain Setup (After Purchasing Domains)

For each site, in Cloudflare Pages:

1. Go to **Project Settings** → **Custom Domains**
2. Click **Add domain** → enter your domain (e.g., `aitoolshub.io`)
3. Cloudflare will auto-configure DNS if domain is on CF Registrar
4. If domain is at another registrar, add these DNS records:

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| CNAME | `@` | `gs-ai-tools-hub.pages.dev` | Proxied ✅ |
| CNAME | `www` | `gs-ai-tools-hub.pages.dev` | Proxied ✅ |

### 5.2 DNS Propagation

- **CF Registrar domains:** Instant
- **External registrars:** 5 min - 48 hours (usually <1 hour with CF proxy)

### 5.3 SSL/HTTPS

- **Cloudflare provides free SSL automatically** — no configuration needed
- Universal SSL covers all `*.pages.dev` subdomains and custom domains
- Certificate type: **Full (strict)** recommended
- No additional cost — included in free tier

---

## 6. Performance Optimization

### 6.1 Cloudflare Cache Rules

Add these in **Rules** → **Cache Rules** for each site:

```yaml
# Static assets — aggressive caching
Rule 1:
  If: URI Path contains "/_astro/"
  Then:
    Edge TTL: 1 year
    Browser TTL: 1 year
    Cache everything

# HTML pages — moderate caching
Rule 2:
  If: URI Path does not contain "/_astro/"
  Then:
    Edge TTL: 4 hours
    Browser TTL: 1 hour
    Cache everything
```

### 6.2 Cloudflare Image CDN (FREE — Polish)

- **Polish (free tier):** Auto-compresses images (lossless/lossy)
- Enable in **Speed** → **Optimization** → **Polish**
- Also enable **Auto Minify** (JS, CSS, HTML) — free
- **Rocket Loader:** Enable for faster JS loading

### 6.3 Additional Performance (All FREE)

| Feature | Setting | Where |
|---------|---------|-------|
| Brotli compression | Enabled | Speed → Optimization |
| Early Hints | Enabled | Speed → Optimization |
| HTTP/2 | Enabled by default | Automatic |
| 0-RTT Connection Resumption | Enabled | SSL/TLS → Edge Certificates |
| Always Online | Enabled | Caching → Configuration |

### 6.4 Astro Build Optimizations (Already Configured)

- `cssMinify: true` in `astro.config.mjs` ✅
- `inlineStylesheets: 'auto'` ✅
- Static output (no SSR overhead) ✅
- Sitemap generation via `@astrojs/sitemap` ✅

---

## 7. Google Search Console & SEO Setup

### 7.1 Verify Each Domain

For each site (8 total):

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Click **Add Property** → enter domain (e.g., `aitoolshub.io`)
3. Verify via **DNS record** (easiest with CF):
   - GSC gives you a TXT record
   - Add it in **CF Dashboard** → **DNS** → **Records** → **Add** → TXT
   - Name: `@` | Value: `google-site-verification=XXXXX`
4. Click **Verify**

**Alternative:** Use **HTML tag verification** — add meta tag to Astro layouts before building.

### 7.2 Submit Sitemaps

Each site already generates `sitemap-index.xml` via `@astrojs/sitemap`. After verification:

1. In GSC → **Sitemaps**
2. Submit: `https://yourdomain.com/sitemap-index.xml`
3. Google will crawl and index all pages

### 7.3 Request Indexing (Speed Up)

- Use **URL Inspection** tool in GSC for key pages
- Request indexing for: homepage, top 5 articles per site
- Google typically indexes within 1-7 days

### 7.4 robots.txt

Each site should have `public/robots.txt`:

```txt
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap-index.xml
```

---

## 8. Monetization — AdSense/Ezoic Integration

### 8.1 Google AdSense (FREE)

**Requirements:**
- Original content ✅ (376 articles)
- Privacy policy ✅ (already generated)
- Terms of service ✅ (already generated)
- About page ✅ (already generated)
- Minimum traffic: None officially, but 50+ daily visits recommended
- 18+ years old, valid address

**Setup Steps:**
1. Apply at [adsense.google.com](https://adsense.google.com)
2. Add all 8 domains as sites
3. Add AdSense code to Astro layout:

```html
<!-- In src/layouts/BaseLayout.astro <head> -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXX" crossorigin="anonymous"></script>
```

4. Auto-ads will place ads automatically
5. Wait for approval (1-14 days)

**Estimated Revenue:**
- RPM for finance/crypto niches: $8-20
- With 500 visits/month/site: ~$4-10/site/month = **$32-80/month network**
- With 2,000 visits/month/site: ~$16-40/site/month = **$128-320/month network**

### 8.2 Ezoic (Alternative — Higher RPM)

**Pros:**
- Higher RPM than AdSense (AI-optimized ad placement)
- Free site speed tools included
- No minimum traffic requirement (Ezoic Access Now program)

**Cons:**
- More complex setup (name server integration)
- Ad quality can be lower
- Revenue share: Ezoic takes 10% (Access Now) or custom deal

**Recommendation:** Start with **AdSense** (simpler, owned by Google, better for small sites). Switch to Ezoic when traffic > 10K/month for higher RPM.

### 8.3 Alternative Ad Networks (FREE)

| Network | Min Traffic | RPM | Notes |
|---------|-------------|-----|-------|
| **MediaVine** | 50K sessions/month | $15-40 | Best RPM but high barrier |
| **Raptive** | 100K pageviews/month | $15-35 | Premium, hard to get in |
| **Monetag** | No minimum | $3-8 | Easy approval, lower RPM |
| **HilltopAds** | No minimum | $2-6 | Adult-friendly, lower quality |
| **RevenueHits** | No minimum | $2-5 | Smart geo-targeting |

**Tier Strategy:**
1. **Month 1-2:** AdSense (or Monetag if AdSense rejects)
2. **Month 3-6:** AdSense + optimize
3. **Month 6+:** Apply to MediaVine (50K threshold)

---

## 9. Complete Cost Analysis

### 9.1 Monthly Costs

| Item | Free Tier | Paid Alternative |
|------|-----------|-----------------|
| **Hosting** (Cloudflare Pages) | $0 ✅ | $0 (always free for static) |
| **Domains** (8 × .com via CF) | — | $9.77 × 8 = **$78/yr (~$6.50/mo)** |
| **SSL Certificates** | $0 ✅ (CF free) | — |
| **CDN** (Cloudflare) | $0 ✅ | — |
| **Analytics** (CF Web Analytics) | $0 ✅ | Google Analytics $0 |
| **Content Generation** (MiniMax M2.7) | $0 ✅ (free tier) | — |
| **Email** (forwarding) | $0 ✅ (CF Email Routing) | — |
| **Total Monthly** | **$0** | **~$6.50/mo with domains** |

### 9.2 Revenue Projections

| Timeline | Traffic | Ad Revenue | Net Profit |
|----------|---------|------------|------------|
| Month 1 | ~100 visits/site | $0 (AdSense approval) | -$6.50 |
| Month 2 | ~300 visits/site | $10-20 | +$3-14 |
| Month 3 | ~800 visits/site | $30-60 | +$24-54 |
| Month 6 | ~2,000 visits/site | $100-200 | +$94-194 |
| Month 12 | ~5,000 visits/site | $300-600 | +$294-594 |

**Break-even:** Month 2-3 (with domains)

---

## 10. Execution Checklist

### Phase 1: Immediate (Today)
- [ ] Push all 8 sites to GitHub (`DBOT-DC/guidestack-pseo`)
- [ ] Create Cloudflare account (if not existing)
- [ ] Connect GitHub to Cloudflare Pages
- [ ] Create 8 CF Pages projects (one per site, root directory = site name)
- [ ] Deploy all sites to `*.pages.dev` URLs
- [ ] Verify all sites load correctly

### Phase 2: This Week
- [ ] Purchase 8 domains (Cloudflare Registrar recommended)
- [ ] Configure custom domains in CF Pages
- [ ] Add `robots.txt` with correct sitemap URL for each site
- [ ] Update `astro.config.mjs` `site` field with real domain for each site
- [ ] Rebuild and redeploy all sites

### Phase 3: Week 2
- [ ] Set up Google Search Console for all 8 domains
- [ ] Submit sitemaps
- [ ] Request indexing for top articles
- [ ] Apply for Google AdSense

### Phase 4: Ongoing
- [ ] Monitor GSC for indexing status
- [ ] Add AdSense code once approved
- [ ] Set up Cloudflare Web Analytics
- [ ] Configure cache rules and performance optimizations
- [ ] Continue content generation (4x daily bursts)
- [ ] Monthly traffic and revenue review

---

## 11. Automation Script (Quick Deploy)

Save as `deploy-all.sh`:

```bash
#!/bin/bash
# GuideStack — Deploy all sites to Cloudflare Pages
# Usage: ./deploy-all.sh

set -e
SITES_DIR="/Users/penny/Documents/Penny/pseo-network/output/sites"

for site in ai-tools-hub bitcoin-beginners budget-travel-tips \
  crypto-investing-guide crypto-trading-strategies defi-yield-guide \
  personal-finance-tips smart-emergency-fund; do
  
  echo "🚀 Building ${site}..."
  cd "${SITES_DIR}/${site}"
  
  # Install deps
  npm install --quiet
  
  # Build static site
  npm run build
  
  # Deploy to Cloudflare Pages
  echo "📦 Deploying ${site}..."
  npx wrangler pages deploy dist --project-name=gs-${site}
  
  echo "✅ ${site} deployed!"
  echo ""
done

echo "🎉 All 8 sites deployed!"
```

---

## 12. Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails on CF Pages | Check Node.js version (set to 20), run `npm run build` locally first |
| Domain not resolving | Check CNAME records point to CF Pages URL, wait for DNS propagation |
| Sitemap 404 | Ensure `@astrojs/sitemap` is in `astro.config.mjs` integrations |
| AdSense rejected | Ensure privacy policy, about page, and 15+ quality articles exist |
| Slow indexing | Submit sitemap, use URL inspection, build backlinks via social sharing |
| CF Pages build timeout | Sites are small (~2.5 MB), should build in <60 sec. Check for large assets |

---

*Document version: 1.0 | Created: 2026-05-12 | Author: Senior Developer Agent*
