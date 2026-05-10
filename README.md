# PennyPress — Autonomous Programmatic SEO Network

An AI-powered content network that generates, builds, and deploys SEO-optimized niche websites autonomously. Built with Python content generation + Astro static sites + Cloudflare Pages.

## 🚀 Architecture

```
pseo-network/
├── data/
│   ├── content/          # Generated articles (Markdown with frontmatter)
│   │   ├── budget-travel-tips/
│   │   ├── crypto-investing-guide/
│   │   ├── ai-tools-hub/
│   │   └── personal-finance-tips/
│   └── sites.json        # Site registry
├── src/
│   └── agents/
│       └── writer.py     # LLM-powered content generation (MiniMax M2.7)
├── templates/
│   └── base/             # Astro template (Tailwind CSS, dark mode, TOC, schema)
├── output/
│   └── sites/            # Built static sites (one per niche)
├── scripts/
│   ├── pennypress.sh     # Main operations controller
│   ├── build-site.sh     # Astro build pipeline
│   ├── content-batch.py  # Batch article generation
│   ├── niche-content.py  # Targeted niche content generation
│   └── generate-sitemap.py  # Post-build sitemap generator
└── OPERATIONS.md         # Operations runbook
```

## 🤖 Content Generation

- **Engine:** MiniMax M2.7 via Anthropic-compatible API
- **Types:** pillar, standard, faq, howto, listicle, comparison
- **Quality:** Expert-level prompts producing 1,500-4,000+ word articles
- **Frontmatter:** Auto-generated title, description, date, category, tags, reading time

## 🌐 Sites

| Site | Niche | Articles | Status |
|------|-------|----------|--------|
| Budget Travel Tips | Budget travel | 36 | Active |
| Crypto Investing Guide | Crypto investing | 15 | Active |
| AI Tools Hub | AI tools & productivity | 15 | Active |
| Personal Finance Tips | Personal finance | 15 | Active |

## ⚡ Quick Start

```bash
# Register a new niche site
bash scripts/pennypress.sh register my-niche "my niche topic"

# Generate articles
bash scripts/pennypress.sh generate my-niche "my niche topic" 15

# Build the site
bash scripts/pennypress.sh build my-niche "my niche topic"

# Full pipeline (register + generate + build)
bash scripts/pennypress.sh full-run my-niche "my niche topic" 15

# Build all sites
bash scripts/pennypress.sh build-all
```

## 🔄 Autonomous Operations

Designed to run 24/7 via cron jobs:
- Daily content generation (new articles per niche)
- Automatic site rebuilding
- Sitemap regeneration
- Content quality monitoring

## 📊 SEO Features

- Auto-generated sitemap.xml
- robots.txt with sitemap reference
- JSON-LD structured data (Article, BreadcrumbList, Organization)
- Open Graph + Twitter Card metadata
- Internal linking system ([LINK: topic] placeholders)
- Reading time estimates
- Category-based content organization

## 🎨 Template Features

- Dark/light mode with system preference detection
- Reading progress bar
- Table of contents (auto-generated from headings)
- Related articles
- Responsive design (mobile-first)
- Tailwind CSS + @tailwindcss/typography
- Astro static site generator (SSG)

## 📜 License

Private — All rights reserved.
