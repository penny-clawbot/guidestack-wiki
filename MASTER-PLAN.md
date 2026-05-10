# Programmatic SEO Content Network — Master Plan

## Project Codename: **PennyPress**

### Executive Summary
Autonomous AI-powered content network generating passive revenue through display ads and affiliate commissions. AI agents handle everything: keyword research, content creation, site generation, deployment, SEO optimization, and growth.

### Why This Model
- **100% passive** — no clients, no sales, no churn
- **Zero marginal cost** — AI generates unlimited content
- **Compounding returns** — SEO content appreciates over time
- **Exit value** — portfolios sell for 30-40× monthly profit
- **Diversified risk** — hundreds of niches, no single point of failure

### Revenue Targets
| Timeline | Sites | Pages/Site | Est. Traffic | Est. RPM | Monthly Revenue |
|----------|-------|-----------|-------------|---------|----------------|
| Month 1-3 | 5 | 50 | 500/mo each | $10 | $250 |
| Month 3-6 | 15 | 100 | 2,000/mo each | $12 | $3,600 |
| Month 6-12 | 30 | 150 | 5,000/mo each | $15 | $33,750 |
| Month 12+ | 50 | 200 | 10,000/mo each | $18 | $180,000 |

### Tech Stack
| Layer | Tool | Purpose |
|-------|------|---------|
| **AI/LLM** | Ollama (local) | Content generation, analysis |
| **Site Gen** | Astro + Tailwind | Fast, SEO-optimized static sites |
| **Templates** | Jinja2-style Astro components | Programmatic page generation |
| **Images** | Stable Diffusion (local) or OpenAI DALL-E | Featured images |
| **SEO** | Custom schema generator | Structured data, meta tags, sitemaps |
| **Hosting** | Cloudflare Pages | Free CDN, SSL, global distribution |
| **Deploy** | GitHub Actions | Auto-deploy on content push |
| **Analytics** | Cloudflare Web Analytics + Umami | Privacy-compliant, free |
| **Ads** | Mediane (Carbon Ads) / AdSense | Display monetization |
| **Affiliates** | Amazon Associates + niche programs | Commission revenue |
| **Monitoring** | Custom rank tracker | Daily SERP position checks |
| **Orchestration** | OpenClaw multi-agent | Agency management, task distribution |

---

## Agency Structure

### Agency: **PennyPress Operations**

#### Agent 1: **Scout** — Keyword Research & Opportunity Discovery
- Scans Google Autocomplete, People Also Ask, Related Searches
- Analyzes SERP competition (DA, backlinks, content quality)
- Scores opportunities: Volume × Low Competition × Monetization Potential
- Output: Prioritized keyword clusters with content calendars

#### Agent 2: **Architect** — Site Generator & Template Builder
- Creates complete Astro sites from templates
- Generates navigation, taxonomy, internal linking structure
- Handles deployment configuration (Cloudflare Pages)
- Maintains template library across niches

#### Agent 3: **Writer** — Content Generation Engine
- Writes SEO-optimized articles (1,500-5,000 words)
- Generates pillar content, supporting articles, FAQs, comparisons
- Creates location-specific landing pages
- Optimizes for featured snippets, People Also Ask boxes

#### Agent 4: **Artist** — Visual Content Generator
- Creates featured images, infographics, custom graphics
- Generates alt text and image SEO metadata
- Maintains visual consistency per site/niche

#### Agent 5: **Optimizer** — SEO & Growth Agent
- Generates schema markup (Article, FAQ, HowTo, Product)
- Builds internal link networks
- Monitors rankings, identifies optimization opportunities
- Generates fresh content for declining pages

#### Agent 6: **Deployer** — Deployment & Operations Agent
- Manages GitHub repos and Cloudflare Pages projects
- Handles CI/CD pipelines
- Monitors uptime and performance
- Manages monetization integration (ads, affiliates)

#### Agent 7: **Analyst** — Performance & Revenue Agent
- Tracks traffic, rankings, revenue across all sites
- Identifies high-performing content patterns
- Recommends new niches based on performance data
- Generates weekly/monthly performance reports

---

## Phase Breakdown

### Phase 1: Foundation (Week 1)
- [ ] Set up project directory structure
- [ ] Create Astro base template with Tailwind CSS
- [ ] Build content generation pipeline (LLM → Markdown → Astro)
- [ ] Set up GitHub organization for site repos
- [ ] Configure Cloudflare Pages deployment
- [ ] Build keyword research pipeline (SERP scraping + scoring)
- [ ] Create first niche site template (home, article, category, about, contact)

### Phase 2: First Sites (Week 2-3)
- [ ] Run Scout agent: identify top 5 niche opportunities
- [ ] Generate 50 articles for first site
- [ ] Deploy Site #1 to Cloudflare Pages
- [ ] Apply for AdSense / Carbon Ads
- [ ] Set up analytics (Umami self-hosted)
- [ ] Generate 30 articles for Site #2
- [ ] Deploy Site #2
- [ ] Set up rank monitoring for both sites

### Phase 3: Scale Pipeline (Week 4-6)
- [ ] Parallelize: build 3-5 sites simultaneously
- [ ] Implement automated content refresh pipeline
- [ ] Add affiliate link integration
- [ ] Build internal linking agent
- [ ] Create backlink outreach automation
- [ ] Set up automated performance reporting
- [ ] Target: 10 sites live with 50+ pages each

### Phase 4: Growth & Optimization (Month 2-3)
- [ ] Analyze performance data, double down on winning niches
- [ ] Add location-specific landing pages to high performers
- [ ] Implement A/B testing for ad placements
- [ ] Build content freshness automation
- [ ] Expand to 20-30 sites
- [ ] Apply for premium ad networks (Ezoic, Mediavine)

### Phase 5: Autonomous Operation (Month 4+)
- [ ] Full autonomous pipeline: Scout → Build → Deploy → Monitor → Optimize
- [ ] Daily: New content generation + publishing
- [ ] Weekly: Rank monitoring + optimization
- [ ] Monthly: Performance reports + new niche exploration
- [ ] Quarterly: Template updates + infrastructure maintenance

---

## Niche Selection Criteria

### High-Priority Niches (High RPM, Low Competition)
1. **Personal finance** (credit cards, loans, investing) — $25-50 RPM
2. **Health & wellness** (supplements, fitness, mental health) — $20-40 RPM
3. **Technology** (software reviews, how-tos, comparisons) — $15-30 RPM
4. **Home & garden** (DIY, tools, renovation) — $12-25 RPM
5. **Travel** (destinations, gear, budget tips) — $10-20 RPM
6. **Pet care** (products, training, health) — $10-18 RPM
7. **Food & cooking** (recipes, equipment, nutrition) — $8-15 RPM
8. **Education** (online courses, study tips, career) — $12-20 RPM
9. **Legal** (small business law, personal rights) — $30-60 RPM
10. **Insurance** (types, comparisons, guides) — $40-80 RPM

### Site Naming Convention
`{niche}-{sub-niche}.com` or `{sub-niche}-{niche}.com`
Examples: `smart-home-gadgets.com`, `budget-travel-tips.com`, `dog-training-pro.com`

---

## Monetization Strategy

### Phase 1: Display Ads (Month 1-3)
- Apply for Google AdSense on each site
- Alternative: Carbon Ads (tech niches), Mediavine (50K sessions/mo)
- Target: $5-15 RPM initially

### Phase 2: Affiliate Links (Month 2+)
- Amazon Associates for product-focused sites
- Niche affiliate programs (ShareASale, Impact, CJ)
- Target: $5-20 per conversion

### Phase 3: Premium Networks (Month 6+)
- Ezoic (optimizes ad placement with AI)
- Raptive (formerly AdThrive, requires 100K sessions/mo)
- Target: $20-50 RPM

### Phase 4: Direct Sponsorships (Month 12+)
- AI-powered sponsorship outreach
- Target: $500-2,000 per sponsored placement

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Google AI content penalty | Use unique data, original analysis, human-like writing; mix content types |
| Algorithm updates | Focus on low-competition long-tail keywords; diversify across 100+ niches |
| Low traffic initially | Expect 3-6 month ramp; focus on content quality and volume |
| Ad account rejection | Ensure substantial content (50+ pages) before applying |
| Hosting costs | Cloudflare Pages free tier; GitHub Pages as backup |
| Content quality | Multi-pass generation: draft → review → optimize → publish |

---

## Success Metrics

### 30 Days
- 5 sites live
- 250+ pages published
- 50+ articles indexed by Google
- Analytics tracking operational

### 90 Days
- 15 sites live
- 1,500+ pages published
- 500+ pages indexed
- First ad revenue

### 180 Days
- 30 sites live
- 4,500+ pages published
- 5,000+ monthly sessions total
- $500+ monthly revenue

### 365 Days
- 50+ sites live
- 10,000+ pages published
- 100,000+ monthly sessions
- $5,000-10,000+ monthly revenue

---

_Created: 2026-05-10_
_Status: Planning → Building_
