#!/usr/bin/env python3
"""Regenerate short bitcoin-beginners articles to meet 2500+ word requirement."""
import json, os, sys, urllib.request, time
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
OUTPUT_DIR = "/Users/penny/Documents/Penny/pseo-network/data/content/bitcoin-beginners"

# Articles to regenerate with expanded topics
REGEN = [
    ("Bitcoin Transaction Fees Explained: How Much Does It Cost to Send Bitcoin", "bitcoin-transaction-fees-explained"),
    ("Bitcoin Taxes Explained: A Beginner's Complete Guide to Crypto Tax Reporting in 2026", "bitcoin-taxes-explained-a-beginners-guide-to-crypto-tax-reporting"),
    ("Bitcoin ATMs Near Me: How to Buy Bitcoin With Cash in 2026", "bitcoin-atms-near-me-how-to-buy-bitcoin-with-cash-in-2026"),
    ("What Is Bitcoin: A Complete Beginner's Guide to Understanding Digital Currency", "what-is-bitcoin-a-complete-beginners-guide"),
    ("What Is the Bitcoin Lightning Network: The Future of Fast Bitcoin Payments", "what-is-the-bitcoin-lightning-network"),
    ("Bitcoin vs Ethereum: Key Differences Explained for Beginners", "bitcoin-vs-ethereum-key-differences-explained"),
    ("How to Buy Bitcoin for the First Time: A Step-by-Step Beginner's Guide", "how-to-buy-bitcoin-for-the-first-time"),
    ("Understanding Bitcoin Halving Cycles: What They Mean for Price and Supply", "understanding-bitcoin-halving-cycles"),
]

def generate_article(topic: str) -> str:
    prompt = f"""Write a VERY comprehensive, SEO-optimized article about: {topic}

CRITICAL REQUIREMENT: This article MUST be at least 2,500 words. Do NOT stop early. Be thorough and detailed.

Niche: bitcoin-beginners (targeting complete beginners)
Target audience: People who are new to Bitcoin and cryptocurrency

Structure:
- Compelling H1 title with the primary keyword
- Engaging introduction (3-4 paragraphs) with statistics and a strong hook
- 7-10 detailed H2 sections
- Include H3 subheadings within H2 sections for deeper coverage
- Use bullet points, numbered lists, tables, and blockquotes for readability
- Include a comprehensive FAQ section at the end with 6-8 common questions
- Conclusion with actionable next steps

Content requirements:
- Real-world examples and case studies
- Statistics and data points where relevant
- Step-by-step instructions where applicable
- Common mistakes to avoid
- Pro tips and expert insights
- Comparison tables where appropriate
- No jargon without clear explanation
- Authoritative but friendly, accessible tone

Write at least 2,500 words. Be thorough — every section should be detailed with multiple paragraphs.

Output ONLY the article in markdown format starting with # Title."""

    body = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
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
                if block.get("type") == "text" and block.get("text", "").strip().startswith("#"):
                    return block["text"]
            for block in data.get("content", []):
                if block.get("type") == "text" and len(block["text"]) > 500:
                    return block["text"]
            return ""
    except Exception as e:
        return f"ERROR: {e}"

def add_frontmatter(content: str, title: str, slug: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = content.split("\n\n")
    desc = ""
    for line in lines[1:]:
        clean = line.strip().replace("#", "").replace("*", "").replace('"', "'")
        if len(clean) > 50:
            desc = clean[:160]
            break
    if not desc:
        desc = title[:160]

    return f"""---
title: "{title.replace('"', '\\"')}"
slug: "{slug}"
date: "{today}"
description: "{desc.replace('"', '\\"')}"
category: "bitcoin-beginners"
tags: ["bitcoin", "beginners", "{slug.split('-')[0]}"]
---

{content}"""

def main():
    generated = 0
    failed = 0
    
    for i, (topic, slug) in enumerate(REGEN):
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        print(f"📝 [{i+1}/{len(REGEN)}] Regenerating: {topic}...")
        sys.stdout.flush()
        
        article = generate_article(topic)
        
        if article and not article.startswith("ERROR"):
            word_count = len(article.split())
            final = add_frontmatter(article, topic, slug)
            with open(filepath, "w") as f:
                f.write(final)
            status = "✅" if word_count >= 2500 else "⚠️"
            print(f"{status} {filename} ({word_count} words)")
            generated += 1
        else:
            print(f"❌ Failed: {topic} — {article[:200]}")
            failed += 1
        sys.stdout.flush()
        
        if i < len(REGEN) - 1:
            time.sleep(2)
    
    print(f"\nRegenerated: {generated} | Failed: {failed}")
    
    # Final count
    files = os.listdir(OUTPUT_DIR)
    print(f"Total articles in bitcoin-beginners: {len(files)}")

if __name__ == "__main__":
    main()
