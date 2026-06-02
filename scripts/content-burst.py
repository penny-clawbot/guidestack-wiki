#!/usr/bin/env python3
"""Content Burst — Batch article generation for PennyPress sites.
Calls writer.py directly with specific topics to avoid duplication."""
import json, os, sys, re, time
from datetime import datetime

PROJECT_DIR = "/Users/penny/Documents/Penny/pseo-network"
CONTENT_DIR = f"{PROJECT_DIR}/data/content"
sys.path.insert(0, PROJECT_DIR)
from writer import generate_article

SITES = {
    "budget-travel-tips": {
        "niche": "budget travel tips and affordable destinations",
        "topics": [
            "cheapest countries to visit in 2026", "how to find cheap flights last minute",
            "best budget hostels in europe", "affordable honeymoon destinations under 3000",
            "budget travel packing list essentials", "how to travel southeast asia on 30 a day",
            "best budget travel apps 2026", "how to use credit card points for free flights",
            "affordable beach destinations caribbean", "budget travel tips for solo travelers",
            "cheapest cities to live in europe 2026", "how to find cheap accommodation anywhere",
            "budget safari tours in africa", "best budget airlines for international travel",
            "how to travel japan on a budget", "affordable road trip routes in usa",
            "budget travel insurance worth it", "how to save money on food while traveling",
            "best budget travel destinations for families", "off season travel deals and tips",
            "how to plan a budget trip to mexico", "cheapest ways to travel between cities",
            "budget travel mistakes to avoid", "best travel hacks for saving money 2026",
            "how to get cheap hotel upgrades", "budget friendly national parks to visit",
            "how to travel full time on a budget", "affordable adventure travel activities",
            "best budget travel gear essentials", "how to find hidden gem destinations",
            "budget travel for digital nomads", "cheapest time to fly to europe",
            "how to use airline miles effectively", "budget travel tips for students",
        ]
    },
    "crypto-investing-guide": {
        "niche": "cryptocurrency investing strategies and market analysis",
        "topics": [
            "best cryptocurrencies to invest in 2026", "how to start investing in crypto",
            "bitcoin vs ethereum investment comparison", "crypto dollar cost averaging strategy",
            "how to read crypto charts for beginners", "best crypto wallets for investors",
            "understanding crypto market cycles", "how to build a crypto portfolio",
            "defi investing opportunities 2026", "crypto etf explained for beginners",
            "risk management in crypto investing", "how to spot crypto bull runs early",
            "best crypto exchanges for beginners", "understanding crypto market cap",
            "how to invest in crypto safely", "crypto investing mistakes to avoid",
            "passive income with crypto staking", "crypto investing for retirement",
            "how to research altcoins before investing", "understanding crypto tokenomics",
            "best long term crypto holds 2026", "crypto investing tax implications",
            "how to diversify crypto portfolio", "crypto investing vs stock market",
            "understanding bitcoin halving impact", "how to set crypto price alerts",
            "best crypto analytics tools", "institutional crypto investing trends",
            "how to invest in layer 2 tokens", "crypto investing during bear markets",
            "understanding crypto on chain analysis", "best crypto books for investors",
            "how to create a crypto investment plan", "crypto investing with small amounts",
        ]
    },
    "ai-tools-hub": {
        "niche": "best AI tools and software reviews",
        "topics": [
            "best ai writing tools 2026", "ai tools for content creators",
            "best free ai tools for students", "ai coding assistants comparison",
            "best ai image generators", "ai tools for small business owners",
            "best ai video editing tools", "ai tools for social media management",
            "best ai chatbots compared", "ai productivity tools for remote workers",
            "best ai tools for marketers", "free ai tools for designers",
            "ai tools for email marketing", "best ai seo tools 2026",
            "ai tools for podcast creators", "best ai presentation makers",
            "ai tools for data analysis", "free ai alternatives to paid tools",
            "best ai tools for teachers", "ai customer service tools",
            "best ai music generation tools", "ai tools for website building",
            "best ai transcription tools", "ai tools for project management",
            "free ai tools for startups", "best ai research tools",
            "ai tools for hr and recruiting", "best ai translation tools",
            "ai tools for ecommerce stores", "best ai scheduling assistants",
            "free ai tools for nonprofits", "ai tools for legal professionals",
            "best ai note taking apps", "ai tools for financial planning",
            "best ai voice over tools", "ai tools for fitness and health tracking",
            "best ai recipe and meal planning tools", "ai tools for real estate agents",
            "best ai interior design tools", "ai tools for personal shoppers",
            "best ai tools for accountants", "ai tools for lawyers",
            "best ai tools for doctors", "ai tools for mental health support",
            "best ai tools for customer support", "ai tools for influencer marketing",
            "best ai tools for affiliate marketing", "ai tools for dropshippers",
            "ai tools for crypto traders", "best ai tools for forex trading",
            "best ai tools for stock market analysis", "ai tools for business intelligence",
            "best ai tools for supply chain management", "ai tools for inventory tracking",
            "best ai tools for fraud detection", "ai tools for cybersecurity",
            "best ai tools for email automation", "ai tools for lead generation",
            "best ai tools for sales forecasting", "ai tools for customer retention",
            "best ai tools for brand monitoring", "ai tools for competitive analysis",
            "best ai tools for market research", "ai tools for product development",
            "best ai tools for ux design", "ai tools for graphic design",
            "best ai tools for video production", "ai tools for animation",
            "best ai tools for game development", "ai tools for app development",
            "best ai tools for qa testing", "ai tools for devops automation",
            "best ai tools for cloud infrastructure", "ai tools for data engineering",
            "best ai tools for machine learning", "ai tools for deep learning",
            "best ai tools for natural language processing", "ai tools for computer vision",
            "best ai tools for robotics", "ai tools for autonomous vehicles",
            "best ai tools for healthcare diagnosis", "ai tools for drug discovery",
            "best ai tools for agricultural monitoring", "ai tools for environmental monitoring",
        ]
    },
    "personal-finance-tips": {
        "niche": "personal finance money management tips",
        "topics": [
            "how to create a budget that works", "best budgeting apps 2026",
            "how to save money every month", "emergency fund how much to save",
            "best high yield savings accounts", "how to pay off credit card debt fast",
            "investing for beginners guide", "best index funds for beginners",
            "how to improve credit score fast", "side hustle ideas to make extra money",
            "how to negotiate salary effectively", "best money saving tips 2026",
            "how to start investing with 100 dollars", "understanding 401k and retirement",
            "best budgeting methods compared", "how to stop living paycheck to paycheck",
            "tax saving strategies for individuals", "best cashback credit cards 2026",
            "how to build multiple income streams", "financial independence retire early fire",
            "best personal finance books", "how to teach kids about money",
            "best investment apps for beginners", "how to refinance student loans",
            "understanding compound interest", "best ways to invest 1000 dollars",
            "how to create a financial plan", "best budget travel destinations under 500",
            "money mistakes to avoid in your 20s", "how to automate your finances",
            "best checking accounts 2026", "how to build an emergency fund fast",
            "real estate investing for beginners", "best financial podcasts to follow",
            "how to negotiate bills down", "best side hustles for passive income",
            "how to start a sole proprietorship", "best savings bonds for beginners",
            "how to reduce monthly expenses", "best bank accounts for teens",
            "how to teach teenagers about credit", "best money management for couples",
            "how to handle debt collectors", "best debt payoff methods snowball vs avalanche",
            "how to read your credit report", "best credit monitoring services",
            "how to dispute credit report errors", "best identity theft protection",
        ]
    },
    "bitcoin-beginners": {
        "niche": "bitcoin basics beginner guide",
        "topics": [
            "what is bitcoin explained simply", "how to buy bitcoin for beginners",
            "bitcoin wallet types explained", "how bitcoin mining works",
            "bitcoin vs traditional money", "is bitcoin a good investment 2026",
            "how to store bitcoin safely", "bitcoin transaction fees explained",
            "understanding bitcoin halving", "how to accept bitcoin payments",
            "bitcoin history and timeline", "bitcoin vs ethereum differences",
            "how to send and receive bitcoin", "bitcoin security best practices",
            "what is a bitcoin hardware wallet", "bitcoin atm how to use",
            "bitcoin price prediction 2026", "how to read bitcoin charts",
            "bitcoin regulations by country", "bitcoin and taxes what you need to know",
            "lightning network explained simply", "bitcoin scalability solutions",
            "how to avoid bitcoin scams", "bitcoin for small business owners",
            "best bitcoin apps for beginners", "understanding bitcoin addresses",
            "bitcoin vs gold comparison", "how to earn bitcoin without buying",
            "bitcoin and environmental impact", "best bitcoin podcasts to follow",
            "bitcoin forks explained simply", "how to create a bitcoin wallet",
            "bitcoin debit cards compared", "central bank digital currencies vs bitcoin",
            "bitcoin node setup guide", "bitcoin private keys explained",
            "bitcoin multisig wallets guide", "bitcoin cold storage best practices",
            "bitcoin soft fork vs hard fork", "bitcoin witness segwit explained",
            "bitcoin lightning network channels", "bitcoin refund policies explained",
            "bitcoin mixers and privacy", "bitcoin paper wallet guide",
            "bitcoin brain wallet risks", "bitcoin key generation methods",
            "bitcoin fee estimation guide", "bitcoin replace by fee rbf",
            "bitcoin child pays for parent cpfp", "bitcoin raw transaction guide",
            "bitcoin sign message verify", "bitcoin coin control features",
            "bitcoin etf vs direct ownership", "bitcoin yield farming DeFi",
            "bitcoinDAO explained", "bitcoin maxis culture",
            "bitcoin recurring buys dollar cost averaging", "bitcoin darknet myth",
            "bitcoin wire transfer guide", "bitcoin cash price comparison",
            "bitcoin segwit2x controversy", "bitcoin institutional adoption 2026",
            "bitcoin mining difficulty adjustment", "bitcoin ETF tax treatment",
            "bitcoin hard drive disposal risk", "bitcoin whitepaper explained simply",
            "bitcoin futures and derivatives basics", "bitcoin options trading guide",
            "bitcoin collar strategy hedging", "bitcoin merkle tree explained",
        ]
    },
    "crypto-trading-strategies": {
        "niche": "cryptocurrency trading strategies and technical analysis",
        "topics": [
            "crypto day trading for beginners", "best crypto trading strategies 2026",
            "how to read crypto candlestick charts", "crypto swing trading guide",
            "best crypto trading indicators", "risk management in crypto trading",
            "how to set stop losses crypto", "crypto scalping strategies explained",
            "best crypto trading bots", "support and resistance levels crypto",
            "moving averages crypto trading", "rsi trading strategy crypto",
            "fibonacci retracement crypto", "best crypto trading platforms 2026",
            "crypto trading psychology", "how to paper trade crypto",
            "best timeframes for crypto trading", "crypto breakout trading strategy",
            "volume analysis in crypto", "crypto market order types explained",
            "how to build a trading plan", "crypto trading journal template",
            "best crypto trading tools free", "understanding crypto order books",
            "crypto correlation trading", "how to trade crypto futures",
            "best crypto pairs to trade", "crypto trading mistakes beginners make",
            "position sizing in crypto trading", "how to trade crypto news events",
            "crypto range trading strategy", "best crypto trading communities",
            "how to backtest crypto strategies", "crypto margin trading risks",
            "best crypto trading books", "how to start crypto trading with 100",
            "macd crypto trading strategy", "bollinger bands crypto strategy",
            "vwap crypto trading strategy", "supertrend crypto strategy",
            "ichimoku cloud crypto trading", "elliott wave crypto analysis",
            "crypto options trading for beginners", "crypto perpetual futures guide",
            "crypto funding rate arbitrage", "crypto basis trading strategies",
            "crypto grid trading bots", "crypto DCA vs lump sum",
            "crypto portfoliorebalancing guide", "crypto tax loss harvesting",
        ]
    },
        "smart-emergency-fund": {
            "niche": "smart emergency fund management and savings strategies",
            "topics": [
                "best high yield savings accounts for emergency funds 2026",
                "how much emergency fund do you really need",
                "automated emergency fund savings strategies",
                "best banks for emergency fund savings",
                "how to build emergency fund fast on low income",
                "emergency fund vs investing which comes first",
                "best emergency fund calculators and tools",
                "how to keep emergency fund accessible but earning interest",
                "emergency fund for self employed and freelancers",
                "best money market accounts for emergency funds",
                "how to rebuild emergency fund after using it",
                "emergency fund vs credit line which is better",
                "best cd accounts for emergency fund ladder",
                "how to save for emergency fund while paying debt",
                "emergency fund milestones and benchmarks",
                "best checking accounts for emergency fund parking",
                "how to automate emergency fund contributions",
                "emergency fund for new parents guide",
                "best savings apps for emergency fund building",
                "how to handle emergency fund during job loss",
                "emergency fund for small business owners",
                "best treasury bills for emergency fund yields",
                "how to prioritize emergency fund vs retirement",
                "emergency fund for recent graduates",
                "best HYSA for emergency funds compared 2026",
                "how to start emergency fund from zero",
                "emergency fund for homeowners unexpected repairs",
                "best savings strategies for irregular income",
                "how to build 3 month emergency fund fast",
                "emergency fund for medical expenses and health crises",
                "best places to keep emergency fund accessible",
                "how to save emergency fund while supporting family",
                "emergency fund benchmarks by age and income",
                "best ways to grow emergency fund balance",
            ],
        },
    "defi-yield-guide": {
        "niche": "decentralized finance yield farming DeFi guide",
        "topics": [
            "what is defi explained simply", "best defi yield farming platforms 2026",
            "how to start yield farming", "defi liquidity pools explained",
            "best defi staking rewards", "impermanent loss explained simply",
            "top defi protocols compared", "how to use uniswap step by step",
            "defi lending platforms compared", "best defi wallets 2026",
            "how to earn passive income defi", "defi risks and how to mitigate them",
            "understanding defi governance tokens", "best defi aggregators",
            "how to bridge crypto to defi", "defi insurance protocols",
            "best defi analytics tools", "cross chain defi explained",
            "defi vs cefi comparison", "how to audit defi protocols",
            "best yield farming strategies", "defi flash loans explained",
            "understanding total value locked tvl", "best defi tokens to watch 2026",
            "how to provide liquidity on defi", "defi composability explained",
            "best defi platforms for beginners", "how to calculate apy vs apr defi",
            "defi security best practices", "best defi podcasts and resources",
            "layer 2 defi opportunities", "real yield vs inflationary yield defi",
            "how to build a defi portfolio", "defi regulation update 2026",
            "best defi education resources", "how to spot defi rug pulls",
            "how to use aave for borrowing", "best defi year in review 2025",
            "defi mining vs staking comparison", "how to calculate defi portfolio value",
            "best defi dashboards and trackers", "defi arbitrage opportunities 2026",
            "how to use curve finance", "best stablecoin defi strategies",
            "defi options and derivatives explained", "how to earn btc yield on defi",
            "best defi leverage farming strategies", "how to use balancer lp",
            "defi token price prediction methods", "best defi risk management tools",
            "how to provide liquidity on curve", "yearn finance vs curve finance vs defi farming compared",
            "best defi crypto index funds", "how to use sushiswap farming",
            "defi impermanent loss calculator tools", "best defi compounding strategies",
            "how to use aave flash loans", "defi lending vs liquidity mining",
            "best defi yield optimizer protocols", "how to track defi tvl trends",
            "defi profit taking strategies", "best defi auto compound tools",
            "how to start defi with 100 dollars", "defi portfolio rebalancing guide",
            "best defi gas optimization tips", "how to use yearn vault strategies",
            "defi cross chain bridges compared", "best defi sustainable apy range",
            "how to evaluate defi project fundamentals", "defi hack prevention guide",
            "best defi yield hunting strategies", "how to use convex finance for boosted apy",
            "defi smart contract risk assessment", "best defi savings account alternatives",
            "how to use makerdao for dai generation", "defi portfolio diversification guide",
            "best defi analytics platforms compared", "how to use 1inch aggregator",
            "defi liquidity provision for beginners", "best defi insurance coverage options",
            "how to calculate net apy in defi", "defi farming tax reporting guide",
            "best defi strategies for bear markets", "how to use paraswap swap aggregation",
        ]
    },
    "memecoin-trading": {
        "niche": "memecoin trading strategies and portfolio building",
        "topics": [
            "best memecoins to buy 2026", "how to trade memecoins for beginners",
            "memecoin portfolio strategy 2026", "solana memecoins to watch",
            "how to find new memecoins early", "dogecoin alternatives 2026",
            "best wallets for memecoin storage", "how to buy memecoins on raydium",
            "memecoin risk management strategies", "top performing memecoins 2026",
            "how to analyze memecoin tokenomics", "memecoin vs altcoin comparison",
            "best dex for memecoin trading", "how to bridge sol for memecoin purchases",
            "memecoin trading signals and indicators", " safest memecoin investment strategies",
            "how to set up memecoin trading dashboard", "memecoin tax implications 2026",
            "best memecoin trackers and tools", "when to sell memecoin profits",
            "memecoin market cycle analysis", "how to avoid memecoin rug pulls",
            "best memecoin communities to join", "memecoin airdrop farming strategies",
            "solana memecoin ecosystem guide", "how to participate in memecoin presales",
            "memecoin volatility trading strategies", "best hardware wallets for memecoins",
            "how to build a diversified memecoin portfolio", "memecoin vs bitcoin comparison",
            "best time to buy memecoins 2026", "memecoin fundamental analysis guide",
            "how to read memecoin charts like a pro", "memecoin liquidity pool strategies",
        ]
    }
}

# Article types to cycle through
ARTICLE_TYPES = ["standard", "listicle", "howto", "faq", "comparison", "pillar"]


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def topic_exists(topic, output_dir):
    """Check if a topic has already been written (by exact slug match in any existing file)."""
    slug = slugify(topic)
    if not os.path.isdir(output_dir):
        return False
    for f in os.listdir(output_dir):
        if f.endswith('.md') and f.startswith(f'{slug}.md'):
            return True
    return False


def save_article(topic, content, article_type, niche, output_dir):
    """Save article with frontmatter to data/content/."""
    os.makedirs(output_dir, exist_ok=True)
    slug = slugify(topic)
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{output_dir}/{date}-ai-{slug}.md'

    # Strip any existing frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)

    words = len(content.split())
    descriptions = {
        'pillar': f'Comprehensive guide to {topic.lower()}',
        'standard': f'Expert insights on {topic.lower()}',
        'faq': f'Answers to your questions about {topic.lower()}',
        'howto': f'Step-by-step: {topic.lower()}',
        'listicle': f'Curated picks for {topic.lower()}',
        'comparison': f'Compare your options for {topic.lower()}',
    }

    frontmatter = f'''---
title: "{topic}"
description: "{descriptions.get(article_type, topic.lower())}"
date: "{date}"
category: "{niche.lower().replace(' ', '-')}"
tags:
  - {niche.lower().replace(' ', '-')}
  - {slug}
draft: false
readingTime: "{max(1, words // 200)} min"
---

'''
    with open(filename, 'w') as f:
        f.write(frontmatter + content)

    return filename


def generate_for_site(site_name, config, max_articles):
    """Generate articles for a single site."""
    niche = config["niche"]
    topics = config["topics"]
    output_dir = f"{CONTENT_DIR}/{site_name}"
    os.makedirs(output_dir, exist_ok=True)

    existing = len([f for f in os.listdir(output_dir) if f.endswith('.md')])
    needed = max(0, max_articles - existing)

    if needed == 0:
        print(f"\n📦 {site_name}: {existing}/{max_articles} ✅ (skipping)")
        return 0, 0

    generated = 0
    failed = 0

    print(f"\n📦 {site_name}: {existing} existing → need {needed} more")

    for i, topic in enumerate(topics):
        if generated + failed >= needed:
            break

        if topic_exists(topic, output_dir):
            continue

        article_type = ARTICLE_TYPES[i % len(ARTICLE_TYPES)]
        print(f"  [{generated + failed + 1}/{needed}] {article_type}: {topic[:55]}...", end=" ", flush=True)

        t0 = time.time()
        try:
            content = generate_article(topic, article_type, target_words=800, niche=niche)
            elapsed = time.time() - t0

            if content and len(content.split()) > 100:
                save_article(topic, content, article_type, niche, output_dir)
                words = len(content.split())
                print(f"✅ {words} words ({elapsed:.0f}s)")
                generated += 1
            else:
                print(f"⚠️ too short ({len(content.split()) if content else 0} words)")
                failed += 1
        except Exception as e:
            elapsed = time.time() - t0
            print(f"❌ {elapsed:.0f}s: {str(e)[:50]}")
            failed += 1

    return generated, failed


if __name__ == "__main__":
    target_site = sys.argv[1] if len(sys.argv) > 1 else "all"
    articles_per_site = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    total_gen = 0
    total_fail = 0
    t0 = time.time()

    print(f"{'='*55}")
    print(f"  Content Burst — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Target: {articles_per_site} articles/site")
    print(f"  Output: {CONTENT_DIR}/")
    print(f"{'='*55}")

    for site_name, config in SITES.items():
        if target_site != "all" and site_name != target_site:
            continue

        gen, fail = generate_for_site(site_name, config, articles_per_site)
        total_gen += gen
        total_fail += fail

    elapsed = time.time() - t0
    print(f"\n{'='*55}")
    print(f"  DONE: {total_gen} generated, {total_fail} failed, {elapsed:.0f}s total")
    print(f"{'='*55}")
