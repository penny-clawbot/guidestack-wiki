---
name: geo-research
description: "Research and knowledge base for GEO/SEO/agentic web optimization"
created: 2026-05-14
last_updated: 2026-06-01
status: active
---

# GEO & Agentic Web Research

## What is GEO?
Generative Engine Optimization (GEO) — optimizing content to be cited by AI engines (ChatGPT, Gemini, Perplexity, Google AI Overviews). Unlike traditional SEO that targets SERP positions, GEO targets being the **source AI cites in its answer**.

## Key Statistics (2026)
- Sites with llms.txt see 800-1000% YoY increase in AI referrals
- AI crawler activity expected to increase 300% through 2026
- Average LLM search visitor worth **5.2x more** than traditional organic
- ChatGPT citations: 87% match Bing top organic results
- YouTube is #1 cited domain in Google AI ecosystem (23.3%)
- Sites cited in AI Overviews see 35% CTR increase
- Post-llms.txt attribution improvement: 18-32% → 61-74%

## The Three Layers of AI Visibility

### Layer 1: Traditional SEO (Foundation)
- Still required — AI engines index via Bing/Google
- Fast load times, mobile-first, clean HTML
- Proper heading hierarchy (H1→H2→H3)
- Internal linking structure

### Layer 2: GEO (AI Citation Optimization)
- **FAQPage schema** — highest-impact schema type for AI visibility
- **Direct answers in first 100-150 words** — AI extracts from opening paragraphs
- **Data tables** — most-extracted format by AI engines
- **Question-style H2 headings** — "How to...", "What is...", "Why..."
- **Cited sources/statistics** — AI favors content with verifiable data
- **Numbered lists** — step-by-step content favored for HowTo
- **Expert bylines** — named experts with credentials
- **Freshness signals** — dateModified, regular updates (every 3-6 months)

### Layer 3: llms.txt, WebMCP & Agentic Web
**llms.txt** — Business-to-Agent (B2A) routing file. Tells IDE agents (Cursor, Claude Code, Copilot, Windsurf) and MCP servers what content exists on your domain. **NOT** an AI search ranking signal — search crawlers (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended) crawl HTML directly and ignore llms.txt. ~10.13% of domains have it. Real value: B2A routing, not AI search.

**WebMCP** (Chrome 146+ Canary) — Browser API co-authored by Google + Microsoft that lets sites expose structured, agent-accessible actions via declarative HTML or imperative JS. Agents call structured JSON tools (e.g. `make_reservation`, `check_inventory`) directly instead of parsing DOM. Currently behind a flag in Chrome 146 Canary.
- **Action:** Flag WebMCP-readiness for site templates targeting e-commerce, bookings, or services

**robots.txt AI directives** — Explicit allow rules for GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended.

**Crawl budget management** — rate limiting for AI crawlers.

**Citation policy** — declare attribution requirements.

## Implementation Checklist

### Technical (Week 1)
- [x] llms.txt at root domain
- [x] llms-full.txt with full article corpus
- [x] FAQPage JSON-LD on articles with FAQ sections
- [x] Organization schema with knowsAbout
- [x] Article/BlogPosting schema with author, dateModified, articleSection
- [x] BreadcrumbList schema on all pages
- [x] WebSite schema with SearchAction
- [x] CollectionPage + ItemList schema on category pages
- [x] RSS feed with auto-discovery link
- [x] robots.txt with AI crawler allow rules

### Content Structure (Ongoing)
- [ ] Question-style H2 headings in all new articles
- [ ] Direct answer in first 150 words with data
- [ ] At least one comparison/data table per article
- [ ] Numbered step-by-step lists where applicable
- [ ] Cited sources for all statistics
- [ ] Expert bylines with niche expertise labels
- [ ] Content freshness: update cycle every 3-6 months

### Build-Time Validation
- [x] Quality gate scoring (GEO checks integrated)
- [x] Alt text enforcement
- [x] FAQ section presence check
- [x] First-150-words direct answer check
- [x] Data table presence check
- [x] Question-heading check
- [x] Cited sources check

## Comparison: SEO vs GEO

| Aspect | Traditional SEO | GEO |
|--------|----------------|-----|
| Goal | Rank in link list | Be cited in AI answer |
| Metric | SERP position | AI citation presence |
| Content | Keyword-optimized text | Direct answers, tables, structured data |
| Key signals | Backlinks, keywords | Brand authority, semantic structure |
| Result | List of links | Direct answer with source |

## Sources
- Oltre AI: llms.txt Practical Guide (March 2026)
- Growth Terminal: llms.txt Implementation (2026)
- ELM Labs: GEO Guide 2026
- Magna: GEO Checklist 2026
- Seer Interactive: SearchGPT citations analysis
- Surfer AI Tracker: Google AI citation data
- Search Engine Land: FAQ rich results decoverage (May 8, 2026)
- TechCrunch: Google AI Mode side-by-side browsing (Apr 16, 2026)
- Limy AI: llms.txt in 2026: The Full Guide (May 12, 2026)
- VentureBeat: Google Chrome ships WebMCP (Feb 2026)
- Business Insider: AI crawler traffic analysis (Jan, May 2026)

---
_Updated by Penny — 2026-05-14_

---

## Weekly Updates — May 25-31, 2026

### Critical Changes This Week

#### 1. Google I/O 2026: AI Mode Now Default Search Experience
Google announced the biggest change to Search in 25+ years at I/O 2026. AI Mode is now the global default with Gemini 3.5 Flash as the new model, officially ending the era of "ten blue links".
- **Key Stats:** 1B+ monthly users with queries doubling quarterly; 93% zero-click rate in AI Mode
- **New Features:** Expandable "intelligent search box", multi-modal inputs, information agents
- **Impact:** Traditional SEO traffic patterns are fundamentally changing; focus shifts to AI citation optimization
- **Action Required:** Update all template documentation to reflect AI Mode as primary context

#### 2. FAQ Rich Results OFFICIALLY RETIRED (May 7, 2026)
Google officially retired FAQ rich results after a 9-year run. This is a confirmed breaking change.
- **Impact:** FAQPage JSON-LD produces zero SERP lift in Google
- **Status:** Schema.org still validates FAQPage — remains valuable for AI readability
- **Action Required:** Remove FAQPage schema from template implementations

#### 3. WebMCP Ships in Chrome 146 Canary (Feb 2026)
Google shipped WebMCP — a browser API co-authored with Microsoft — that lets websites expose structured, agent-accessible actions.
- **Status:** Chrome 146 Canary (behind a flag)
- **Impact:** Changes what "agent-ready" means for sites with bookable actions, e-commerce, B2B services
- **Action:** Add documentation section for future WebMCP implementation

#### 4. llms.txt: B2A Routing Protocol, Not SEO Factor
Analysis of 515M+ AI bot events confirms llms.txt is almost never fetched by major search/answer crawlers.
- **Real Value:** B2A (Business-to-Agent) routing for IDE agents (Cursor, Claude Code, Copilot) and MCP servers
- **NOT a Ranking Factor:** No major AI engine uses llms.txt for search rankings or citation decisions
- **Adoption:** Stalled at ~10% of domains
- **Action Required:** Remove any SEO ranking claims; position as agentic web infrastructure only

#### 5. Zero-Click Rate Now 93% in AI Mode (Apr 2026)
Google AI Mode expanded with side-by-side web browsing now sees ~93% zero-click rate.
- **Implication:** Attribution models must shift from direct traffic to AI cited references
- **Impact:** Traditional organic CTR metrics becoming less relevant
- **Action Required:** Update success metrics to prioritize "AI citation rate" over "organic CTR"

### Agentic Web Evolution

#### Current State (May 31, 2026)
- ✅ llms.txt implemented (as B2A routing for IDE agents)
- ✅ AI crawlers allowed in robots.txt
- ✅ Organization + WebSite + Article schema implemented
- ⚠️ FAQPage schema implemented but deprecated for rich results
- ❌ WebMCP not yet implemented
- ❌ HowTo schema not implemented as FAQ alternative
- ❌ Universal Cart integration not implemented

#### Future-Proofing Checklist
- [ ] Add WebMCP endpoint for agent-accessible actions
- [ ] Implement HowTo schema for step-by-step content
- [ ] Create "Agent-ready site" documentation section
- [ ] Update attribution measurement for zero-click AI queries
- [ ] Monitor WebMCP adoption curve for implementation timing

### Updated Implementation Checklist

#### Technical (Week 1)
- [x] llms.txt at root domain
- [x] llms-full.txt with full article corpus
- [x] **FAQPage JSON-LD on articles with FAQ sections** (still valid for AI readability)
- [x] Organization schema with knowsAbout
- [x] Article/BlogPosting schema with author, dateModified, articleSection
- [x] BreadcrumbList schema on all pages
- [x] WebSite schema with SearchAction
- [x] CollectionPage + ItemList schema on category pages
- [x] RSS feed with auto-discovery link
- [x] robots.txt with AI crawler allow rules
- [ ] WebMCP endpoint planning

#### Content Structure (Ongoing)
- [ ] Question-style H2 headings in all new articles
- [ ] Direct answer in first 150 words with data
- [ ] At least one comparison/data table per article
- [ ] Numbered step-by-step lists where applicable
- [ ] Cited sources for all statistics
- [ ] Expert bylines with niche expertise labels
- [ ] Content freshness: update cycle every 3-6 months

#### Build-Time Validation
- [x] Quality gate scoring (GEO checks integrated)
- [x] Alt text enforcement
- [x] FAQ section presence check
- [x] First-150-words direct answer check
- [x] Data table presence check
- [x] Question-heading check
- [x] Cited sources check

### Weekly Template TODOs

#### High Priority (Immediate Action Required)
1. **Update FAQPage schema documentation**
   - Clarify it's still valid for AI readability but no longer drives Google rich results
   - Update template to reflect this distinction

2. **Add WebMCP documentation section**
   - Explain client-side vs server-side (MCP) distinction
   - Include Chrome 146 status and implementation timeline
   - Position for future bookable-action verticals

3. **Reframe llms.txt positioning**
   - Remove any implication it improves AI search citations
   - Clarify it's B2A routing for IDE agents
   - Update documentation with practical guidance

#### Medium Priority
4. **Create "Agent-ready site" checklist**
   - Combine llms.txt + structured data + WebMCP-readiness
   - Include e-commerce/bookable action verticals guidance
   - Provide clear implementation steps

5. **Update zero-click impact section**
   - Add 93% zero-click stat for AI Mode
   - Discuss attribution model implications
   - Prepare for measurement gaps

#### Low Priority
6. **Consider HowTo schema addition**
   - Evaluate replacing FAQ schema with HowTo for step-by-step content
   - Add as alternative structured data format

---

## Historical Updates (for reference)

### Update — 2026-05-31 (Recent)

#### Universal Cart: New E-Commerce Gate (May 19, 2026)
Google I/O 2026 introduced Universal Cart, a feed-layer eligibility model where native commerce via Merchant Center attributes gates the Buy button.
- **Two-pipeline architecture:** Schema.org Product markup (necessary) + Merchant Center `native_commerce` feed + capability server at `/.well-known/ucp`
- **Impact:** Product schema alone is no longer sufficient for e-commerce AI visibility
- **Action Required:** Update e-commerce templates with Merchant Center integration guidance

#### May 2026 Core Update Targeting Programmatic SEO (May 21, 2026)
Google's latest core update is specifically targeting automated, ad-bloated content.
- **Impact:** Programmatic pages are being deindexed within days
- **Signal:** Scaled content without differentiation is being penalized
- **Action Required:** Add quality gates for programmatic content in template

### Update — 2026-05-18 (Previous)

### Critical: WebMCP Ships in Chrome 146 Canary (Feb 2026)
Google Chrome shipped **WebMCP** — a browser API co-authored with Microsoft — that lets websites expose structured, agent-accessible actions via declarative HTML or imperative JS. Instead of agents parsing DOM or screenshots, they call structured JSON tools (e.g., `make_reservation`, `check_inventory`) directly.
- **Status:** Chrome 146 Canary, behind a flag
- **Impact:** Changes what "agent-ready" means for sites with bookable actions, e-commerce, B2B services
- **Action:** No production urgency yet, but flag WebMCP-readiness for future site template updates

### Critical: llms.txt — AI Search Crawlers Ignore It, IDE Agents Use It
llms.txt is almost never touched by search/answer crawlers (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended all crawl HTML directly). Gary Illyes confirmed Google doesn't/won't support it (Feb 2026). The file's real value: **B2A (Business-to-Agent) routing** — IDE agents (Cursor, Claude Code, Copilot, Windsurf) and MCP servers DO fetch it routinely.
- **Reframe:** llms.txt = B2A routing protocol for IDE agents, NOT an AI search ranking factor
- **Adoption:** ~10.13% of domains

### Updated: Zero-Click Now 93% in AI Mode (Apr 2026)
Google AI Mode (expanded April 16, 2026 with side-by-side web browsing) now sees ~93% zero-click rate. Strategy must account for attribution shifting from direct traffic to AI cited references.

### Action Items (May 18)
- [x] **Add WebMCP section to GEO pillar** — declarative vs imperative API, Chrome 146 status
- [x] **Reframe llms.txt** — remove any implication it improves AI search citations; clarify as B2A routing for IDE agents/MCP
- [ ] **Add "Agent-ready site" checklist** — llms.txt + structured data + WebMCP-readiness for e-commerce/bookable verticals
- [ ] **Update zero-click / AI Mode impact section** — 93% zero-click stat; implications for attribution
- [ ] **Test AI search visibility for one deployed PSEO article**
- [ ] **Monitor llms.txt crawler access logs**
- [ ] **Check if FAQPage schema drives citations even without rich results**

---

## Update — 2026-05-17

### Recent Infrastructure Changes
- Updated template robots.txt to include:
  - `Google-Extended` (new 2026 Google AI crawler)
  - `PerplexityBot` 
  - `OAI-SearchBot`
- FAQPage schema confirmed still active (not deprecated by Schema.org — only Google's rich results display was killed)
- llms.txt link tag confirmed present in BaseLayout.astro `<head>`

### GEO Performance Data (2026)
- Sites with llms.txt: 800-1000% YoY increase in AI referrals
- Average LLM search visitor worth 5.2x more than traditional organic
- Post-llms.txt attribution improvement: 18-32% → 61-74%
- Sites cited in AI Overviews see 35% CTR increase

### Action Items
- [ ] Test AI search visibility for one deployed PSEO article
- [ ] Monitor llms.txt crawler access logs
- [ ] Check if FAQPage schema drives citations even without rich results

---

## Update — 2026-05-19

### May 19 Search Results (from SearXNG)
- **llmrefs.com** — "The 2026 Guide" to GEO — good comprehensive reference
- **almcorp.com** — "Generative Engine Optimization (GEO): Complete Guide 2026" (Feb 12, 2026)
- **reddit.com/r/LLM** — "GEO + SEO for AI search in 2026 what's actually working" (Jan 20, 2026) — 19 research papers reviewed
- **controlaltdigital.com** — "AI Search in 2026: The Complete Guide to SEO and GEO"
- **YouTube: Statista + Seer Interactive** — "State of AI Search for a Data-Driven 2026" (Dec 10, 2025)

### Key Takeaways from Today's Search
1. **GEO is maturing fast** — 2026 is the year it moves from theory to standard practice
2. **Content structure > keywords** — direct answers, data tables, and cited sources dominate AI citations
3. **Brand authority matters** — AI engines favor well-known sources over content-only quality
4. **Question-style headings** confirmed as highest-impact tactic

### Action Items
- [ ] Pull full text from llmrefs.com and almcorp.com GEO guides for detailed tactics
- [ ] Cross-reference Reddit's 19-paper GEO summary for what actually works
- [ ] Test AI search visibility for one deployed PSEO article
- [ ] Monitor llms.txt crawler access logs
- [ ] Check if FAQPage schema drives citations even without rich results
