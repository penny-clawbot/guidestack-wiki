# GEO Update — Google Kills llms.txt Signal (2026-05-31)

## Key Finding
Google officially retired llms.txt as a ranking signal in their May 2026 AI Optimization guide.

Source: [Weaverse — Google AI Optimization Guide 2026](https://weaverse.io/blogs/google-ai-optimization-guide-llms-txt-dead-hydrogen-seo-2026) (May 16, 2026)

## What's Dead
- `/llms.txt` as an AI search visibility lever — Google explicitly says don't bother
- Custom AI-readable files, markup, or markdown created solely for AI crawlers
- Zero fetches of llms.txt across 12,099 AI bot requests in Feb-Mar 2026 server audits
- 1 llms.txt URL out of 94,614 cited URLs in the ALLMO citation study (0.001%)

## What Still Works (Per Google)
1. **Classical SEO = AI SEO** — Rank well in normal Search → eligible for AI Overviews
2. **Query fan-out** — Related queries behind the scenes = more pages can surface
3. **Structured data** — Article, Product, FAQ, Review, Breadcrumb schema explicitly endorsed
4. **RAG grounding** — Same index powers AI Overviews and blue links

## What This Means for GuideStack
- Don't spend time on llms.txt customization — it was never a lever
- Focus on: classical SEO quality, structured data (FAQ, Article schema), internal linking
- Content quality + backlinks = AI visibility (same as old SEO)
- The GEO work already done (structured data in articles) is still valid
- Agent: directives in robots.txt are fine (crawler guidance, not ranking signal)

## Action Items
- Remove llms.txt placeholder from deployment checklist (it was a placeholder anyway)
- Focus on: schema markup in articles, internal linking, content quality
- Quality-refresh.py with new template (images, tables, FAQ sections) is the real GEO lever

_Last updated: 2026-05-31_