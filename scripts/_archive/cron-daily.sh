#!/bin/bash
# PennyPress Cron — Daily content generation and rebuild
# Designed to run via OpenClaw cron (isolated session, MiniMax M2.7)
# Run: bash /Users/penny/Documents/Penny/pseo-network/scripts/cron-daily.sh

set -e

PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
SITE_REGISTRY="$PROJECT_DIR/data/sites.json"
LOG="$PROJECT_DIR/logs/cron-$(date +%Y-%m-%d).log"
mkdir -p "$PROJECT_DIR/logs"

log() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$LOG"
}

log "═══ PennyPress Daily Cron ═══"

# Read all active sites and their niches
python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['status'] == 'active':
        print(f\"{s['name']}|{s['niche']}|{s['article_count']}\")
" | while IFS='|' read -r name niche count; do
    log "Site: $name ($count articles)"

    # Only generate if under max
    if [ "$count" -lt 50 ]; then
        log "  Generating 2 new articles for $name..."

        # Generate targeted content using the niche-content.py script
        # Topics are auto-selected based on niche
        TOPICS=$(python3 -c "
import random

niche = '$niche'
name = '$name'

# Topic pools per niche
topic_pools = {
    'budget travel': [
        ('Best Budget Airlines for 2026 Compared', 'comparison', 1000),
        ('How to Find Hidden Gem Destinations on a Budget', 'standard', 900),
        ('Budget Travel Packing List: The Ultimate Guide', 'listicle', 1000),
        ('How to Travel Southeast Asia on $30 a Day', 'howto', 1000),
        ('Credit Card Points for Travel: Complete Beginner Guide', 'pillar', 1200),
        ('Budget Travel Mistakes That Could Ruin Your Trip', 'listicle', 900),
        ('How to Find Cheap Hotels: Insider Strategies', 'howto', 1000),
        ('Budget Travel Photography Tips for Amazing Photos', 'standard', 800),
        ('How to Travel During Peak Season Without Breaking the Bank', 'howto', 1000),
        ('Best Budget Travel Insurance Options Compared', 'comparison', 1000),
    ],
    'crypto investing': [
        ('What Is Blockchain: Complete Beginner Explanation', 'standard', 1000),
        ('Top DeFi Protocols You Should Know in 2026', 'listicle', 1000),
        ('Crypto Portfolio Diversification Strategies', 'standard', 1000),
        ('How to Spot Crypto Scams: Red Flags to Watch', 'howto', 1000),
        ('Solana vs Ethereum: Which Blockchain Wins?', 'comparison', 1000),
        ('How to Use Decentralized Exchanges (DEX)', 'howto', 1000),
        ('Crypto Market Cap Explained: What It Really Means', 'standard', 800),
        ('Best Hardware Wallets Compared for 2026', 'comparison', 1000),
        ('How to Read Crypto Whitepapers', 'howto', 1000),
        ('Layer 2 Scaling Solutions Explained Simply', 'standard', 1000),
    ],
    'AI tools': [
        ('Best AI Video Editors in 2026 Compared', 'comparison', 1000),
        ('How to Use AI for Social Media Management', 'howto', 1000),
        ('AI Automation Tools That Save 10+ Hours a Week', 'listicle', 1000),
        ('Claude vs ChatGPT vs Gemini: Which AI Is Best?', 'comparison', 1000),
        ('How to Build an AI Chatbot for Your Business', 'howto', 1000),
        ('Best AI Presentation Makers Compared', 'comparison', 900),
        ('AI-Powered SEO Tools: Complete Guide', 'standard', 1000),
        ('How to Use AI for Email Marketing', 'howto', 1000),
        ('AI Music Generators: Create Original Music with AI', 'standard', 900),
        ('Best AI Tools for Students: Complete Guide', 'listicle', 1000),
    ],
    'personal finance': [
        ('How to Build an Emergency Fund from Zero', 'howto', 1000),
        ('Best Side Hustles for 2026: Complete Guide', 'listicle', 1000),
        ('How to Start Investing with Just $100', 'howto', 1000),
        ('Tax-Loss Harvesting: Complete Strategy Guide', 'pillar', 1200),
        ('Best Robo-Advisors Compared for 2026', 'comparison', 1000),
        ('How to Negotiate Bills and Save Thousands', 'howto', 900),
        ('Financial Independence Retire Early (FIRE) Guide', 'pillar', 1200),
        ('Best Cashback Credit Cards Compared', 'comparison', 1000),
        ('How to Create Multiple Income Streams', 'standard', 1000),
        ('Money Mistakes to Avoid in Your 20s and 30s', 'listicle', 1000),
    ]
}

pool = topic_pools.get(niche, topic_pools.get('budget travel', []))
selected = random.sample(pool, min(2, len(pool)))
import json
print(json.dumps(selected))
")

        cd "$PROJECT_DIR"
        PYTHONUNBUFFERED=1 python3 scripts/niche-content.py "$name" "$niche" "$TOPICS" 2>&1 | tail -5 | tee -a "$LOG"

        # Update article count
        NEW_COUNT=$(ls "$PROJECT_DIR/data/content/$name/"*.md 2>/dev/null | wc -l | tr -d ' ')
        python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['name'] == '$name':
        s['article_count'] = $NEW_COUNT
        break
with open('$SITE_REGISTRY', 'w') as f:
    json.dump(data, f, indent=2)
"
        log "  Now at $NEW_COUNT articles"
    else
        log "  Skipping (at $count articles, max 80)"
    fi

    # Rebuild the site
    log "  Rebuilding $name..."
    cd "$PROJECT_DIR"
    bash scripts/build-site.sh "$name" "$niche" 2>&1 | grep -E "page|Complete|Error|PAGES|Sitemap" | tee -a "$LOG"
    log "  Done"
done

# Git commit and push
cd "$PROJECT_DIR"
git add -A data/content/ data/sites.json
CHANGES=$(git diff --cached --stat 2>/dev/null | wc -l | tr -d ' ')
if [ "$CHANGES" -gt 0 ]; then
    git commit -m "Daily content update: $(date +%Y-%m-%d)" 2>&1 | tail -1 | tee -a "$LOG"
    git push 2>&1 | tail -1 | tee -a "$LOG"
    log "Pushed to GitHub"
else
    log "No changes to push"
fi

log "═══ Daily Cron Complete ═══"
