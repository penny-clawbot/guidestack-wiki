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
    """Build the LLM prompt for world-class content."""
    type_instructions = {
        "pillar": f"""Write a comprehensive, authoritative pillar article: "{topic}"

Target length: {target_words}+ words of pure substance.

Structure:
1. Start with # "{topic.title()}" (compelling, click-worthy title)
2. Hook paragraph — open with a surprising statistic, relatable scenario, or counterintuitive insight. NO generic "In today's world" or "Understanding X is important" openings.
3. 6-8 ## sections, each with ### subsections where appropriate
4. End with a "## Frequently Asked Questions" section (5 Q&As)
5. Final section: "## Final Thoughts" — concise summary with a clear takeaway

Content rules:
- Write like a seasoned {niche} journalist with 10 years of experience
- Include realistic, specific numbers and data points (dollar amounts, percentages, timeframes)
- Reference real destinations, brands, tools, or strategies by name
- Use first-person plural ("we") and second-person ("you") naturally
- Mix short punchy sentences with longer explanatory ones
- Include at least one comparison table
- Add 3-5 [LINK: specific-related-topic] placeholders for internal linking
- Every section must deliver actionable value — zero filler

Formatting:
- Proper markdown: ## H2, ### H3, **bold key terms**, - bullet lists, | tables |
- NO frontmatter, NO YAML, NO meta commentary""",

        "standard": f"""Write a detailed, engaging article: "{topic}"

Target length: {target_words}+ words.

Structure:
1. # "{topic.title()}" (compelling title)
2. Hook — open with something unexpected or relatable, NOT "In this article we'll explore"
3. 4-6 ## sections with real substance
4. "## Key Takeaways" bullet list before the conclusion
5. Brief conclusion

Content rules:
- Write like an experienced {niche} blogger who actually practices what they write about
- Include specific examples, real numbers, and practical advice
- Use a conversational but authoritative tone
- Vary paragraph length — short for emphasis, longer for explanation
- Add 2-3 [LINK: related-topic] internal link placeholders
- NO fluff, NO repetition, NO "in conclusion let's wrap up"

Formatting: Proper markdown. NO frontmatter.""",

        "faq": f"""Write an expert FAQ article: "{topic}"

Target length: {target_words}+ words.

Structure:
1. # "{topic.title()}" 
2. Brief intro (2-3 sentences setting context)
3. 10-15 questions, each with a detailed 100-200 word answer
4. Questions should range from beginner to advanced
5. Brief closing

Content rules:
- Each answer must be genuinely helpful — include specific advice, not vague generalities
- Mix practical tips with explanations of WHY something works
- Include dollar amounts, timeframes, and specific recommendations
- Add [LINK: topic] placeholders where cross-referencing makes sense
- Write like you're answering a friend who's about to make a real decision

Formatting: ## for each question, proper markdown. NO frontmatter.""",

        "howto": f"""Write a step-by-step how-to guide: "{topic}"

Target length: {target_words}+ words.

Structure:
1. # "{topic.title()}" 
2. Hook — why this matters right now, what the reader will gain
3. "## What You'll Need" — prerequisites checklist
4. "## Step-by-Step Instructions" — 8-15 numbered steps, grouped under ## headings
5. "## Pro Tips" section — 5 insider tips
6. "## Common Mistakes" — what to watch out for
7. Brief FAQ (3 questions)
8. Short conclusion

Content rules:
- Each step must be specific and actionable — "Do X by using Y to achieve Z"
- Include realistic time estimates and difficulty levels
- Mention specific tools, services, or resources by name
- Add screenshots/placeholders where visual aids would help
- Add [LINK: related-topic] placeholders

Formatting: Numbered steps, proper markdown. NO frontmatter.""",

        "listicle": f"""Write an engaging listicle: "{topic}"

Target length: {target_words}+ words.

Structure:
1. # "{topic.title()}" (number in title like "10 Best..." or "Top 15...")
2. Hook — why this list matters, what makes it different
3. Each item gets its own ## heading with:
   - What it is (1-2 sentences)
   - Why it's great (specific reasons)
   - Best for / Who should use it
   - Potential drawbacks
4. "## How We Chose" methodology section
5. "## Quick Comparison" summary table
6. Conclusion with top pick recommendation

Content rules:
- Each item must be DISTINCT — no overlap or redundancy
- Include specific prices, ratings, or metrics where applicable
- Write like a reviewer who's actually tested everything
- Order items from best to worst (or beginner to advanced)
- Add [LINK: related-topic] placeholders

Formatting: ## for each item, proper markdown, include a comparison table. NO frontmatter.""",

        "comparison": f"""Write a thorough comparison article: "{topic}"

Target length: {target_words}+ words.

Structure:
1. # "{topic.title()}"
2. Hook — the decision the reader is trying to make
3. Quick summary: "## At a Glance" — one paragraph per option
4. "## Feature Comparison" — detailed markdown table
5. ## section for each option covering: pros, cons, best for, pricing
6. "## Which Should You Choose?" — decision matrix based on use case
7. "## Our Verdict" — clear recommendation

Content rules:
- Be genuinely objective — acknowledge trade-offs
- Include specific numbers for comparison (prices, speeds, ratings, etc.)
- Write for someone making a real purchase decision
- Add [LINK: related-topic] placeholders

Formatting: Tables, proper markdown. NO frontmatter.""",
    }

    instructions = type_instructions.get(article_type, type_instructions["standard"])

    return f"""You are an expert content writer for a leading {niche} publication. You write articles that rank #1 on Google because they're genuinely the best resource on the topic.

{instructions}

CRITICAL RULES:
- Output ONLY the article markdown. No frontmatter, no YAML, no explanations, no meta-commentary.
- Start immediately with the # title line.
- Every paragraph must earn its place. If it doesn't add value, cut it.
- Write for a smart, curious reader who values their time.
- Use specific, concrete details — not vague abstractions.
- Sound like a real human expert, not an AI assistant."""


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
