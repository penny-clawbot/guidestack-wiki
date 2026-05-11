# PennyPress SEO Tools

Free, open-source SEO tooling for the PennyPress PSEO network.

## Tools

### 1. Lighthouse CI — Automated Performance & SEO Testing

**What:** Google Lighthouse in CI mode — scores performance, accessibility, best practices, and SEO automatically.

**Install:** Already installed via npm (`npx lhci`)

**Usage:**
```bash
# Run against a built site's dist/ directory
cd pseo-network/crypto-investing-guide
npx lhci collect --config=../tools/lhcirc.json
npx lhci assert --config=../tools/lhcirc.json

# Authenticated mode (for live URLs, requires Google API key)
npx lhci collect --url=https://crypto-investing-guide.com --config=../tools/lhcirc.json
```

**Config:** `lhcirc.json` — SEO assertions enforce score ≥ 0.9, LCP < 2.5s, CLS < 0.1, plus meta description, canonical, title, and structured data checks.

**Output:** JSON reports in `lhci-reports/` directory.

**Cost:** FREE (open source, Apache 2.0)
**Paid alternatives:** Sitebulb ($199/yr), Screaming Frog (£259/yr), Semrush Audit ($119/mo)

---

### 2. Site Crawler — Local HTML SEO Scanner

**What:** Python script that crawls built site HTML files and reports SEO issues (titles, meta descriptions, H1s, canonical URLs, Open Graph tags, schema markup, image alt text, internal/external links, reading level).

**Usage:**
```bash
# Crawl a specific site's dist/ directory
python3 tools/site-crawler.py pseo-network/crypto-investing-guide

# Limit pages
python3 tools/site-crawler.py pseo-network/crypto-investing-guide --max-pages 50
```

**Checks:**
- ✅ `<title>` presence and length (30-60 chars)
- ✅ Meta description presence and length (120-160 chars)
- ✅ Single `<h1>` per page
- ✅ Canonical URL
- ✅ Open Graph tags (title, description, image)
- ✅ Structured data (JSON-LD)
- ✅ Image alt text
- ✅ Internal & external link counts
- ✅ Reading level (Flesch-Kincaid, target 8th-10th grade)
- ✅ Meta robots (noindex detection)

**Cost:** FREE (Python 3, zero dependencies)

---

### 3. SEO Analyzer — Markdown Content Auditor

**What:** Analyzes source markdown articles for SEO quality before build. Checks frontmatter, headings, FAQ sections, word count, reading level, internal links, and content structure.

**Usage:**
```bash
# Analyze specific articles
python3 tools/seo-analyzer.py content/crypto-investing-guide/best-crypto-wallets.md

# Analyze all articles in a directory
python3 tools/seo-analyzer.py --dir content/crypto-investing-guide/

# Analyze all sites
for site in pseo-network/*/; do
  python3 tools/seo-analyzer.py --dir "$site/content/"
done
```

**Scoring (100-point scale):**
- Meta description (150-160 chars): -15 if missing, -10 if wrong length
- H1 title (30-70 chars): -15 if missing, -5 if wrong length
- Heading structure (H2/H3 depth): -5 to -8
- Internal links (3-5 ideal): -5 if few
- FAQ section (5-10 questions): -5 to -10
- Word count (1500+ ideal): -5 to -20
- Reading level (sentence length): -3
- Bold terms, lists, tables: -2 each

**Cost:** FREE (Python 3, zero dependencies)

---

## Cost Analysis

| Tool | Free Option | Paid Alternative | Annual Savings |
|------|------------|-----------------|----------------|
| Performance/SEO Audit | Lighthouse CI (free) | Semrush Site Audit ($1,428/yr) | **$1,428/yr** |
| Site Crawler | site-crawler.py (free) | Screaming Frog (£259/yr ≈ $440) | **$440/yr** |
| Content Analysis | seo-analyzer.py (free) | Surfer SEO ($89/mo = $1,068/yr) | **$1,068/yr** |
| **Total** | **$0/yr** | | **$2,936/yr saved** |

All tools use only free, open-source software. No API keys or subscriptions required.

## Integration with PennyPress Pipeline

These tools integrate with the PennyPress content generation workflow:

1. **Before build:** Run `seo-analyzer.py` on new markdown articles to catch issues early
2. **After build:** Run `site-crawler.py` on `dist/` to verify rendered HTML
3. **Before deploy:** Run `lhci` to get Google's SEO/performance scores
4. **Cron integration:** Can be scheduled to run daily via OpenClaw cron jobs

## File Locations

```
pseo-network/tools/
├── README.md           # This file
├── lhcirc.json         # Lighthouse CI configuration
├── seo-analyzer.py     # Markdown content SEO auditor
└── site-crawler.py     # Built HTML site crawler
```
