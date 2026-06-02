#!/usr/bin/env python3
"""
Writer Agent - Content generation for PennyPress SEO network
Uses MiniMax M2.7 via Anthropic Messages API (free tier)
"""

import urllib.request
import json
import os
import sys
from datetime import datetime
from typing import Optional

# MiniMax M2.7 API (Anthropic-compatible)
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimax.io/anthropic"
MODEL = "MiniMax-M2.7"

# Try to load key from zshrc if not set
if not API_KEY:
    try:
        with open(os.path.expanduser("~/.zshrc")) as f:
            for line in f:
                if "MINIMAX_API_KEY" in line and "export" in line:
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    API_KEY = key
                    break
    except:
        pass


def _strip_thinking(text: str) -> str:
    """Strip chain-of-thought preamble from LLM output.
    Finds the first markdown header that looks like actual content."""
    lines = text.split('\n')
    content_start = 0

    # Skip lines that look like thinking/reasoning
    thinking_patterns = [
        'the user asks', 'the user wants', 'we need to', 'i need to',
        'plan:', 'draft:', 'let me', 'i will', 'i should', 'first, i',
        'okay, i', 'here is', 'thinking process'
    ]

    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        # Skip empty lines and thinking patterns
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in thinking_patterns):
            content_start = i + 1
            continue
        # First real content line (starts with # or is substantive)
        if stripped.startswith('#') and len(stripped) > 3:
            content_start = i
            break
        # Non-thinking paragraph
        if len(stripped) > 50 and not any(stripped.startswith(p) for p in thinking_patterns):
            content_start = i
            break

    return '\n'.join(lines[content_start:]).strip()


def generate_with_minimax(prompt: str, max_tokens: int = 4096, timeout: int = 300, retries: int = 2) -> Optional[str]:
    """Generate content using MiniMax M2.7 via Anthropic Messages API."""
    if not API_KEY:
        print("  ⚠️ MINIMAX_API_KEY not found", file=sys.stderr)
        return None

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }).encode()

    req = urllib.request.Request(
        f"{BASE_URL}/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01"
        }
    )

    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
                # Anthropic format with thinking: content may have thinking + text blocks
                # Find the actual text block (skip thinking blocks)
                text_content = ""
                for block in data.get("content", []):
                    if block.get("type") == "text" and block.get("text", "").strip():
                        text_content = block["text"].strip()
                        break

                if text_content:
                    # Strip any remaining chain-of-thought preamble
                    text_content = _strip_thinking(text_content)
                    if len(text_content.split()) > 50:
                        return text_content

                return None
        except Exception as e:
            print(f"  ⚠️ MiniMax API error (attempt {attempt}/{retries}): {e}", file=sys.stderr)
            if attempt < retries:
                import time
                time.sleep(3 * attempt)  # Backoff: 3s, 6s
            else:
                return None


def generate_article(topic: str, article_type: str, target_words: int = 800, niche: str = "general") -> str:
    """Generate an article using MiniMax M2.7, with template fallback."""

    prompt = _build_prompt(topic, article_type, target_words, niche)
    print(f"  🤖 Generating with MiniMax M2.7 ({target_words} words)...", file=sys.stderr)

    result = generate_with_minimax(prompt, max_tokens=min(4096, target_words * 3))

    if result and len(result.split()) > 200:
        print(f"  ✅ MiniMax generated {len(result.split())} words", file=sys.stderr)
        return result

    # Fallback to template
    print(f"  📝 Using template fallback", file=sys.stderr)
    return generate_template_article(topic, article_type, target_words, niche)


def _build_prompt(topic: str, article_type: str, target_words: int, niche: str) -> str:
    """Build the LLM prompt with GEO-optimized article structure."""
    type_instructions = {
        "pillar": f"""Write a comprehensive guide about \"{topic}\".
- {target_words}+ words
- STRUCTURE (strictly follow — every item is required):
  1. **First paragraph**: 2-3 sentence direct answer/summary (no intro fluff, no \"in today's world\")
  2. **## H2 headings**: MUST be question-style (\"## How to Invest in Bitcoin\", \"## What is a Hardware Wallet?\") — NOT declarative statements
  3. **5-6 H2 sections** with specific data, statistics with sources, actionable tips
  4. **IMAGE**: Include one contextual image with descriptive alt text: ![descriptive alt text describing the image content](https://example.com/image.jpg) — alt text must describe what is shown, not just \"image\"
  5. **TABLE**: At least one markdown comparison table with headers and data
  6. **FAQ**: \"## Frequently Asked Questions\" section with 5 questions as ### H3, each with a direct 1-3 sentence answer
  7. **SOURCES**: Cite specific numbers/percentages with source references (e.g., \"According to CoinMarketCap, 45% of investors...")
  8. **Conclusion**: Brief closing paragraph
- Markdown: # title, ## H2 (question-style), ### H3, **bold**, | table | columns |, numbered lists
- Output ONLY the article starting with # Title""",

        "standard": f"""Write an article about \"{topic}\".
- {target_words}+ words
- STRUCTURE (strictly follow — every item is required):
  1. **First paragraph**: 2-3 sentence direct answer/summary (no intro fluff)
  2. **## H2 headings**: MUST be question-style (\"## How to Save Money Fast\", \"## What is Compound Interest?\") — NOT declarative
  3. **3-4 H2 sections** with specific examples and data
  4. **IMAGE**: Include one contextual image with descriptive alt text: ![alt describing image content](https://example.com/image.jpg)
  5. **TABLE**: At least one markdown table with headers and data
  6. **FAQ**: \"## Frequently Asked Questions\" with 3 questions as ### H3, direct 1-3 sentence answers
  7. **SOURCES**: Cite specific numbers with source references
  8. **Conclusion**: Brief closing paragraph
- Markdown: ## headers (question-style), ### H3 for FAQ, **bold**, - lists, | table | data |
- Output ONLY the article starting with # Title""",

        "faq": f"""Write an FAQ article: \"{topic}\".
- {target_words}+ words, 8 questions with detailed answers
- Each ## heading MUST be question-style: \"## How to Invest in Crypto?\", \"## What is DeFi?\", \"## Why Does X Matter?\"
- **IMAGE**: Include one contextual image with descriptive alt text: ![alt describing image content](https://example.com/image.jpg)
- **TABLE**: At least one markdown table in the article
- Answers must be direct and factual, then expand with detail
- Include specific data and source citations
- Output ONLY the article starting with # Title""",

        "howto": f"""Write a step-by-step guide: \"{topic}\".
- {target_words}+ words
- STRUCTURE (strictly follow):
  1. **First paragraph**: 2-3 sentence summary of what this guide accomplishes
  2. **IMAGE**: Include one contextual image with descriptive alt text: ![alt describing image content](https://example.com/image.jpg)
  3. \"## Step-by-Step Instructions\" — each step as ### H3 (\"### Step 1: ...\", \"### Step 2: ...\")
  4. **TABLE**: Summary table comparing options or results
  5. **FAQ**: \"## Frequently Asked Questions\" with 4 questions as ### H3
  6. Tips section with specific actionable advice
- Include specific numbers/dates in each step and cite sources
- Output ONLY the article starting with # Title""",

        "listicle": f"""Write a listicle: \"{topic}\".
- {target_words}+ words, 8-10 items
- STRUCTURE:
  1. **First paragraph**: 2-3 sentence answer summarizing the top picks
  2. **IMAGE**: Include one contextual image with descriptive alt text: ![alt describing image content](https://example.com/image.jpg)
  3. Each item: ## H2 (numbered question-style like \"## #1: How to Choose the Best...\"), brief pros/cons, specific details
  4. **TABLE**: Comparison table across items
  5. **FAQ**: \"## Frequently Asked Questions\" with 3 questions as ### H3
- Include specific prices, ratings, or data points for each item
- Cite sources for all statistics
- Output ONLY the article starting with # Title""",

        "comparison": f"""Write a comparison: \"{topic}\".
- {target_words}+ words
- STRUCTURE:
  1. **First paragraph**: 2-3 sentence answer: which option is best for whom
  2. **IMAGE**: Include one contextual image with descriptive alt text: ![alt describing image content](https://example.com/image.jpg)
  3. Feature comparison as a markdown table with headers and data columns
  4. \"## Frequently Asked Questions\" with 4 questions as ### H3
  5. Final verdict with specific reasoning and source citations
- Include specific numbers, prices, performance data
- Output ONLY the article starting with # Title""",
    }

    instructions = type_instructions.get(article_type, type_instructions["standard"])

    return f"""You are an expert {niche} writer. {instructions}

GEO-QUALITY CHECKLIST — your article MUST contain ALL of the following:
☐ Direct answer in first paragraph (2-3 sentences, no filler intros)
☐ ## H2 headings in question-style ("How to...", "What is...", "Why...")
☐ At least 1 markdown table with headers and data
☐ At least 1 image with descriptive alt text: ![alt text](url)
☐ ## Frequently Asked Questions section with ### H3 sub-questions
☐ At least 3 data points with source citations (e.g., "According to [Source]...")
☐ Brief conclusion paragraph

Rules: Output ONLY markdown article. Start with # Title. No filler. Write now:"""


def generate_template_article(topic: str, article_type: str, target_words: int, niche: str) -> str:
    """Generate a well-structured article using templates (when API is unavailable)."""
    today = datetime.now().strftime("%B %d, %Y")

    titles = {
        "pillar": f"# The Complete Guide to {topic.title()} ({datetime.now().year})",
        "standard": f"# {topic.title()}: Everything You Need to Know",
        "faq": f"# {topic.title()}: Your Questions Answered",
        "howto": f"# How to {topic.title()}: A Step-by-Step Guide",
        "listicle": f"# {topic.title()}: The Definitive List",
        "comparison": f"# {topic.title()}: Which Option Is Right for You?",
    }

    title = titles.get(article_type, titles["standard"])

    content = f"""{title}

## Why This Matters

Understanding **{topic}** is essential for making informed decisions. Whether you're just getting started or looking to deepen your knowledge, this guide covers the key fundamentals and practical insights you need.

## Key Fundamentals

Before diving into specific strategies, let's establish the core principles:

- **Foundation matters** - A strong understanding of basics prevents costly mistakes
- **Consistency beats intensity** - Regular, focused effort outperforms sporadic bursts
- **Measure and iterate** - Track your progress and adjust based on results
- **Learn from others** - The community has valuable experience to share

[LINK: {topic.lower().replace(' ', '-')}-guide]

## Practical Strategies

### Getting Started

The most important step is the first one. Here's how to begin effectively:

1. **Research thoroughly** - Understand the landscape before committing resources
2. **Set clear goals** - Define what success looks like for your specific situation
3. **Start small** - Test your approach on a small scale before expanding
4. **Document everything** - Future you will thank present you for keeping records

### Intermediate Approaches

Once you've established a baseline, consider these strategies:

- Build systems, not just individual actions
- Focus on high-impact, low-effort wins first
- Create feedback loops to catch issues early
- Invest in tools that save time in the long run

[LINK: {topic.lower().replace(' ', '-')}-tips]

### Advanced Techniques

For those ready to level up:

- Automate repetitive processes
- Use data-driven decision making
- Build a network of knowledgeable peers
- Stay current with industry developments

## Common Mistakes to Avoid

| Mistake | Impact | Solution |
|---------|--------|----------|
| Skipping research | Wasted resources | Always validate before investing |
| Moving too fast | Errors compound | Take a measured approach |
| Ignoring feedback | Missed optimization | Actively seek and apply feedback |
| Not tracking results | Can't improve | Set up measurement from day one |
| Going it alone | Slower progress | Leverage community knowledge |

## Frequently Asked Questions

### What's the best way to get started with {topic}?

The best approach is to start with the fundamentals covered in this guide, then gradually expand your knowledge through practice and community engagement.

### How long does it take to see results?

Most people see initial results within 30-90 days, with more significant outcomes typically appearing within 3-6 months of consistent effort.

### What's the biggest misconception?

The most common misconception is that you need expensive tools or extensive prior experience. In reality, many successful approaches use freely available resources.

### Is this worth investing time in?

For most people, yes. The potential benefits - including time savings, improved outcomes, and new capabilities - typically justify the initial learning investment.

## Conclusion

{topic} offers genuine value when approached with the right mindset and strategies. By following the guidance in this article - researching thoroughly, starting small, measuring results, and iterating based on data - you'll be well-positioned for success.

The key is to start today and stay consistent. Progress compounds over time, and every expert was once a beginner.

---

*Last updated: {today} | Part of our {niche} coverage. [LINK: {niche}]*
"""
    return content


# Convenience functions
def generate_pillar_article(topic, target_word_count=2000, niche="general"):
    return generate_article(topic, "pillar", target_word_count, niche)

def generate_standard_article(topic, target_word_count=800, niche="general"):
    return generate_article(topic, "standard", target_word_count, niche)

def generate_faq_article(topic, target_word_count=800, niche="general"):
    return generate_article(topic, "faq", target_word_count, niche)

def generate_howto_article(topic, target_word_count=800, niche="general"):
    return generate_article(topic, "howto", target_word_count, niche)

def generate_listicle_article(topic, target_word_count=1000, niche="general"):
    return generate_article(topic, "listicle", target_word_count, niche)

def generate_comparison_article(topic, target_word_count=1000, niche="general"):
    return generate_article(topic, "comparison", target_word_count, niche)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: writer.py <topic> [article_type] [target_words] [niche]")
        print("Types: pillar, standard, faq, howto, listicle, comparison")
        sys.exit(1)

    topic = sys.argv[1]
    article_type = sys.argv[2] if len(sys.argv) > 2 else "standard"
    target_words = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    niche = sys.argv[4] if len(sys.argv) > 4 else "general"

    result = generate_article(topic, article_type, target_words, niche)
    print(result)
