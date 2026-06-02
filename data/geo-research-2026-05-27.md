# GEO Research — 2026-05-27

## Top Findings

1. **Google's Official AI Optimization Guide** — Google published a dedicated docs page on optimizing for generative AI features in Search. It emphasizes that traditional SEO fundamentals (helpful content, crawlability, structured data) remain the foundation, but adds AI-specific guidance on clear entity signals and concise answer formatting. — https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

2. **llms.txt as a B2A Standard** — The `llms.txt` file has matured into a "Business-to-Agent" protocol — a machine-readable surface at site root that tells AI crawlers and agents what the site offers. Described as the first standardized way for brands to publish agent-consumable content summaries. Implementation is simple: place a markdown-formatted `llms.txt` at `/llms.txt`. — https://limy.ai/blog/llms-txt-in-2026-the-full-guide

3. **AI Crawler Landscape Has Fragmented to 10+ Bots** — In 2026, robots.txt must handle a dozen AI-specific crawlers: GPTBot, OAI-SearchBot, ChatGPT-User (OpenAI), ClaudeBot, Claude-User, Claude-SearchBot (Anthropic), PerplexityBot, Perplexity-User, Google-Extended, CCBot (Common Crawl), and Bytespider (ByteDance). Key insight: **OAI-SearchBot drives ChatGPT Search citations** — blocking it removes you from ChatGPT results. Bytespider has documented non-compliance with robots.txt. — https://soar.sh/blog/ai-bots-robots-txt-guide

4. **Structured Data Is the Bridge to AI Visibility** — Schema markup (Article, FAQ, HowTo, Organization) is now explicitly recognized as critical for AI-era search. The `Speakable` schema (still in beta) marks content best suited for audio/voice playback and is gaining relevance as AI assistants consume content audibly. Mark only 2-3 key sections per page as speakable. — https://www.stackmatix.com/blog/structured-data-ai-search

5. **GEO ≠ Traditional SEO** — Best practices for 2026 converge on: entity coverage, answer blocks with concise definitions, strong internal linking, proof signals (authorship, citations, dates), and ensuring content is structured for citation by LLMs — not just ranked by keywords. — https://seotuners.com/blog/generative-engine-optimization/generative-engine-optimization-best-practices/

## Practical Implications for GuideStack

- **Add `llms.txt`** to all 8 sites — concise markdown summary of each site's purpose, content structure, and key URLs. This is low-effort, high-leverage.
- **Allow AI search crawlers explicitly** in robots.txt: OAI-SearchBot, PerplexityBot, Claude-SearchBot, Google-Extended. Block training-only crawlers (GPTBot, ClaudeBot, CCBot) if content protection matters; allow them if citation in model knowledge matters more.
- **Implement Speakable schema** on key guide pages — mark the intro/summary sections for voice/AI consumption.
- **Add FAQ and HowTo schema** to all programmatic guide pages — these are the most-cited structured data types in AI Overviews.
- **Concise answer blocks** — Each guide page should have a 2-3 sentence direct-answer paragraph near the top, matching the query intent. AI Overviews pull these directly.
- **Author/entity signals** — Add `Organization` and `Person` schema, bylines, and publication dates to build trust signals that AI models weight heavily.

## New Developments

- **Claude-SearchBot is new** — Anthropic now has a dedicated search indexer (Claude-SearchBot), distinct from training (ClaudeBot) and user-initiated (Claude-User) crawlers. This signals Claude/Amazon are building live search into Claude.
- **Perplexity-User claims "agent not bot"** — Perplexity's user-initiated fetcher claims it's not a bot and may not respect robots.txt rules. Server-level blocking may be needed if Perplexity citation isn't desired.
- **Google's official AI optimization guide** (published May 2026) is the first time Google has formally documented how to optimize specifically for AI Overviews — previously only informal guidance existed.
- **robots.txt is now a "frontline defense"** for IP protection vs. AI training — the conversation has shifted from "let crawlers in" to strategic allow/block decisions per bot.
