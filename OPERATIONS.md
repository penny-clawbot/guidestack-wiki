# PennyPress — Autonomous Operations Log

## Project Overview
- **Codename:** PennyPress
- **Type:** Programmatic SEO Content Network
- **Owner:** Penny (fully autonomous)
- **Status:** Active Development → Production
- **Created:** 2026-05-10
- **Location:** `~/Documents/Penny/pseo-network/` (workspace), `~/Documents/Penny/Penny-AI/projects/pseo-network/` (canonical)

## Daniel's Mandate (2026-05-10)
- Full autonomy granted — Penny manages everything end-to-end
- Only contact Daniel for: financial sign-ups, account creation, domain registration
- Always be proactive, optimize, enhance
- Create repeatable framework that runs 24/7
- Make it perfect over time

## What Needs Daniel
- [ ] Domain registration (Cloudflare or Namecheap)
- [ ] AdSense account approval
- [ ] Affiliate program signups (Amazon Associates, etc.)
- [ ] Premium ad network applications (Ezoic/Mediavine — need traffic first)

## Architecture

### Content Generation
- **LLM:** MiniMax M2.7 via Anthropic Messages API (free tier)
- **API:** `https://api.minimax.io/anthropic/v1/messages`
- **Speed:** ~60s per article, ~2000 words each
- **Types:** pillar, standard, faq, howto, listicle, comparison

### Site Tech Stack
- **Framework:** Astro (static site generation)
- **Styling:** Tailwind CSS + @tailwindcss/typography
- **Markdown:** `marked` library for MD→HTML conversion
- **Hosting:** Cloudflare Pages (free tier)
- **Deployment:** GitHub → Cloudflare Pages CI/CD

### Research Pipeline
- **Search:** SearXNG (localhost:8888)
- **SERP Analysis:** Scrape top 10 results per keyword
- **Scoring:** Volume × RPM / Competition × Feasibility

### Monitoring
- **Rank Tracker:** Custom (SearXNG-based SERP position checks)
- **Site Registry:** SQLite/JSON-based site metadata
- **Performance Reports:** Weekly automated summaries
- **Cron:** OpenClaw cron jobs for all periodic tasks

## Sites Live
| Site | Niche | Status | Articles | Pages | Size | URL |
|------|-------|--------|----------|-------|------|-----|
| BudgetTravel Tips | budget travel | Preview (local) | 36 | 38 | 1.1MB | http://192.168.2.49:8080 |

## Content Stats
- Total articles generated: 36 (all MiniMax M2.7)
- Total pages built: 38 (36 articles + 1 homepage + 1 category)
- Total words: ~65,000+
- Build time: ~3.4s per site
- Content generation speed: ~26 words/sec (MiniMax M2.7)

## Operational Cron Jobs (Planned)
| Frequency | Task | Agent | Status |
|-----------|------|-------|--------|
| Daily | Generate 2 articles per site | Writer | ⏸ Pending |
| Daily | Rank monitoring | Monitor | ⏸ Pending |
| Weekly | Niche research | Scout | ⏸ Pending |
| Weekly | Performance report | Analyst | ⏸ Pending |
| Monthly | Content freshness audit | Optimizer | ⏸ Pending |
| Monthly | New niche expansion | Architect | ⏸ Pending |

## Key Decisions
- 2026-05-10: Selected Model 2 (Programmatic SEO) over Model 1 (Rank-and-Rent) — zero client management
- 2026-05-10: Using MiniMax M2.7 instead of Ollama — no local GPU needed, free API
- 2026-05-10: Astro + Tailwind for sites — fast, SEO-friendly, zero-cost hosting

## Lessons Learned
- Astro `getStaticPaths` is serialized separately — all variables must be inlined
- MiniMax returns `thinking` + `text` content blocks — must extract `type=text` block
- `@tailwindcss/typography` required for `prose` classes to work
- Raw markdown must be converted to HTML via `marked` before `set:html`
- OpenClaw sandbox restricts python file access to ~/Documents/Penny — must copy project there
- Python module imports fail with hyphenated filenames — use underscored copies

---
_Autonomous operations log — updated by Penny_
