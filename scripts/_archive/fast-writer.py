#!/usr/bin/env python3
"""Fast content generator using MiniMax M2.7 API directly."""
import json, os, sys, urllib.request, urllib.error, re
from datetime import datetime

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not API_KEY:
    try:
        with open(os.path.expanduser("~/.zshrc")) as f:
            for line in f:
                if "MINIMAX_API_KEY" in line and "export" in line:
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    except: pass

BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2.7"

def generate_article(topic: str, niche: str, words: int = 1200) -> str:
    prompt = f"""Write a comprehensive, SEO-optimized article about: {topic}

Niche: {niche}
Target length: ~{words} words

Requirements:
- Compelling H1 title with the main keyword
- Engaging introduction with a hook
- 4-6 H2 sections with subheadings
- Practical tips, examples, or data throughout
- Conclusion with a call-to-action
- Natural keyword usage (don't stuff)
- Write in an authoritative but approachable tone

Output ONLY the article in markdown format. No preamble, no thinking, just the article starting with # Title"""

    body = json.dumps({
        "model": MODEL,
        "max_tokens": min(max(words * 3, 4000), 8192),
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).encode()

    req = urllib.request.Request(BASE_URL, data=body, headers={
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    })

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            for block in data.get("content", []):
                if block.get("type") == "text" and block.get("text", "").strip():
                    text = block["text"].strip()
                    # Skip thinking blocks (no markdown headers)
                    if len(text) > 200:
                        return text
            # Fallback: return any text content
            for block in data.get("content", []):
                if block.get("type") == "text" and len(block["text"]) > 100:
                    return block["text"]
            return ""
    except Exception as e:
        return f"ERROR: {e}"

def make_slug(title: str) -> str:
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug).strip('-')
    return slug[:80]

def add_frontmatter(content: str, title: str, niche: str, topic: str) -> str:
    slug = make_slug(title)
    today = datetime.now().strftime("%Y-%m-%d")
    desc = content.split("\n\n")[1][:160] if len(content.split("\n\n")) > 1 else topic[:160]
    return f"""---
title: "{title.replace('"', '\\"')}"
slug: "{slug}"
date: "{today}"
description: "{desc.replace('"', '\\"')}"
category: "{niche}"
tags: ["{niche}", "{slug.split('-')[0]}"]
---

{content}"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: fast-writer.py <topic> <niche> [output_dir] [words]")
        sys.exit(1)

    topic = sys.argv[1]
    niche = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
    words = int(sys.argv[4]) if len(sys.argv) > 4 else 1200

    os.makedirs(output_dir, exist_ok=True)
    article = generate_article(topic, niche, words)
    
    if article and not article.startswith("ERROR"):
        title = article.split("\n")[0].lstrip("# ").strip()
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{make_slug(topic)}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(add_frontmatter(article, title, niche, topic))
        print(f"✅ {filename} ({len(article)} chars)")
    else:
        print(f"❌ Failed: {topic} — {article[:100]}")
