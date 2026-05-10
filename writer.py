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


def generate_with_minimax(prompt: str, max_tokens: int = 4096, timeout: int = 300) -> Optional[str]:
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
        print(f"  ⚠️ MiniMax API error: {e}", file=sys.stderr)
        return None


def generate_article(topic: str, article_type: str, target_words: int = 1500, niche: str = "general") -> str:
    """Generate an article using MiniMax M2.7, with template fallback."""

    prompt = _build_prompt(topic, article_type, target_words, niche)
    print(f"  🤖 Generating with MiniMax M2.7...", file=sys.stderr)

    result = generate_with_minimax(prompt, max_tokens=min(16384, target_words * 2))

    if result and len(result.split()) > 200:
        print(f"  ✅ MiniMax generated {len(result.split())} words", file=sys.stderr)
        return result

    # Fallback to template
    print(f"  📝 Using template fallback", file=sys.stderr)
    return generate_template_article(topic, article_type, target_words, niche)


def _build_prompt(topic: str, article_type: str, target_words: int, niche: str) -> str:
    """Build the LLM prompt."""
    type_instructions = {
        "pillar": f"""Write a COMPREHENSIVE pillar article about "{topic}".
- Target: {target_words}+ words
- Structure: H1 title → compelling hook intro → 5-8 H2 sections with H3 subsections → FAQ section (5+ Q&As) → conclusion with CTA
- Include: real statistics (make them realistic), expert insights, actionable tips
- Add [LINK: related-topic] placeholders for internal linking (3-5)
- Use markdown formatting (headers, bold, lists, tables where appropriate)
- Tone: authoritative but accessible, like an experienced guide""",

        "standard": f"""Write a detailed article about "{topic}".
- Target: {target_words}+ words
- Structure: H1 → hook intro → 3-5 H2 sections with substance → conclusion
- Add 2-3 [LINK: related-topic] internal link placeholders
- Use markdown formatting
- Tone: informative, engaging, practical""",

        "faq": f"""Write an FAQ article: "{topic}".
- Target: {target_words}+ words
- Structure: H1 → brief intro → 8-12 questions with detailed answers (100-200 words each) → conclusion
- Each answer should be genuinely helpful and thorough
- Add [LINK: topic] placeholders where relevant""",

        "howto": f"""Write a step-by-step how-to guide: "{topic}".
- Target: {target_words}+ words
- Structure: H1 → intro → prerequisites → numbered steps (8-15) with H2 headings → tips section → FAQ (3 questions) → conclusion
- Be specific and actionable in each step
- Add [LINK: related-topic] placeholders""",

        "listicle": f"""Write a listicle article: "{topic}".
- Target: {target_words}+ words
- Structure: H1 → intro → 10+ items with H2 headings (100-200 words each with pros/cons) → comparison/takeaway section → conclusion
- Make each item distinct and valuable
- Add [LINK: topic] placeholders""",

        "comparison": f"""Write a detailed comparison article: "{topic}".
- Target: {target_words}+ words
- Structure: H1 → intro → overview of each option → feature-by-feature comparison (markdown table) → who should choose what → winner/verdict → conclusion
- Be objective and data-driven
- Add [LINK: topic] placeholders""",
    }

    instructions = type_instructions.get(article_type, type_instructions["standard"])

    return f"""You are an expert SEO content writer specializing in {niche}. {instructions}

IMPORTANT RULES:
- Output ONLY the article content in markdown format (no frontmatter, no YAML)
- Start with the H1 title line (# Title)
- Use proper markdown: ## headers, **bold**, - bullet lists, | tables |
- Write naturally for humans, not for search engines
- Include specific examples, data points, and actionable advice
- Never use filler content or repetitive statements

Write the complete article now:"""


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

- **Foundation matters** — A strong understanding of basics prevents costly mistakes
- **Consistency beats intensity** — Regular, focused effort outperforms sporadic bursts
- **Measure and iterate** — Track your progress and adjust based on results
- **Learn from others** — The community has valuable experience to share

[LINK: {topic.lower().replace(' ', '-')}-guide]

## Practical Strategies

### Getting Started

The most important step is the first one. Here's how to begin effectively:

1. **Research thoroughly** — Understand the landscape before committing resources
2. **Set clear goals** — Define what success looks like for your specific situation
3. **Start small** — Test your approach on a small scale before expanding
4. **Document everything** — Future you will thank present you for keeping records

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

For most people, yes. The potential benefits — including time savings, improved outcomes, and new capabilities — typically justify the initial learning investment.

## Conclusion

{topic} offers genuine value when approached with the right mindset and strategies. By following the guidance in this article — researching thoroughly, starting small, measuring results, and iterating based on data — you'll be well-positioned for success.

The key is to start today and stay consistent. Progress compounds over time, and every expert was once a beginner.

---

*Last updated: {today} | Part of our {niche} coverage. [LINK: {niche}]*
"""
    return content


# Convenience functions
def generate_pillar_article(topic, target_word_count=3500, niche="general"):
    return generate_article(topic, "pillar", target_word_count, niche)

def generate_standard_article(topic, target_word_count=1800, niche="general"):
    return generate_article(topic, "standard", target_word_count, niche)

def generate_faq_article(topic, target_word_count=1200, niche="general"):
    return generate_article(topic, "faq", target_word_count, niche)

def generate_howto_article(topic, target_word_count=1500, niche="general"):
    return generate_article(topic, "howto", target_word_count, niche)

def generate_listicle_article(topic, target_word_count=2000, niche="general"):
    return generate_article(topic, "listicle", target_word_count, niche)

def generate_comparison_article(topic, target_word_count=2000, niche="general"):
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
