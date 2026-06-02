#!/bin/bash
# Staged Deployment Pipeline for PennyPress
# Moves articles from queued content to live content based on deployment tier
# Usage: bash scripts/staged-deploy.sh [tier]
#   tier: "launch" (15-20 per site), "month1" (5-10 more), "month2" (remaining), "all"

set -euo pipefail

PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
CONTENT_DIR="$PROJECT_DIR/data/content"
TIERS_FILE="$PROJECT_DIR/data/deployment-tiers.json"
QUEUED_DIR="$PROJECT_DIR/data/content-queued"

TIER="${1:-launch}"

mkdir -p "$QUEUED_DIR"

# Step 1: Move all current content to queued (first run only)
if [ ! -f "$PROJECT_DIR/data/.staged-init" ]; then
    echo "📦 First run: moving all content to staged queue..."
    for SITE_DIR in "$CONTENT_DIR"/*/; do
        SITE_NAME=$(basename "$SITE_DIR")
        if [ "$SITE_NAME" = "*" ]; then continue; fi
        Q_SITE="$QUEUED_DIR/$SITE_NAME"
        mkdir -p "$Q_SITE"
        # Move all except legal pages
        for FILE in "$SITE_DIR"*.md; do
            [ -f "$FILE" ] || continue
            FNAME=$(basename "$FILE")
            if echo "$FNAME" | grep -qi "privacy\|terms\|legal\|disclaimer"; then
                echo "  Keeping legal: $SITE_NAME/$FNAME"
            else
                mv "$FILE" "$Q_SITE/"
                echo "  Queued: $SITE_NAME/$FNAME"
            fi
        done
    done
    touch "$PROJECT_DIR/data/.staged-init"
    echo "✅ All articles queued"
fi

# Step 2: Deploy based on tier
echo ""
echo "🚀 Deploying tier: $TIER"

if [ "$TIER" = "launch" ]; then
    echo "Deploying S-Tier articles (15-20 per site)..."
    python3 -c "
import json, os, shutil

with open('$TIERS_FILE') as f:
    tiers = json.load(f)

# Group by site, take top N per site
site_articles = {}
for a in tiers['s_tier_launch']:
    site = a['site']
    if site not in site_articles:
        site_articles[site] = []
    site_articles[site].append(a['file'])

for site, files in site_articles.items():
    deploy = sorted(files)[:20]  # Max 20 per site at launch
    for fname in deploy:
        src = '$QUEUED_DIR/' + site + '/' + fname
        dst = '$CONTENT_DIR/' + site + '/' + fname
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print(f'  ✅ {site}/{fname}')

    count = len([f for f in os.listdir('$CONTENT_DIR/' + site) if f.endswith('.md')])
    print(f'  📊 {site}: {count} articles live')
"

elif [ "$TIER" = "month1" ]; then
    echo "Deploying A-Tier articles..."
    python3 -c "
import json, os, shutil

with open('$TIERS_FILE') as f:
    tiers = json.load(f)

site_articles = {}
for a in tiers['a_tier_month1']:
    site = a['site']
    if site not in site_articles:
        site_articles[site] = []
    site_articles[site].append(a['file'])

for site, files in site_articles.items():
    deploy = sorted(files)[:10]
    for fname in deploy:
        src = '$QUEUED_DIR/' + site + '/' + fname
        dst = '$CONTENT_DIR/' + site + '/' + fname
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print(f'  ✅ {site}/{fname}')
    count = len([f for f in os.listdir('$CONTENT_DIR/' + site) if f.endswith('.md')])
    print(f'  📊 {site}: {count} articles live')
"

elif [ "$TIER" = "month2" ]; then
    echo "Deploying B-Tier articles..."
    python3 -c "
import json, os, shutil

with open('$TIERS_FILE') as f:
    tiers = json.load(f)

for a in tiers['b_tier_month2']:
    src = '$QUEUED_DIR/' + a['site'] + '/' + a['file']
    dst = '$CONTENT_DIR/' + a['site'] + '/' + a['file']
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f'  ✅ {a[\"site\"]}/{a[\"file\"]}')

# Count per site
for site_dir in sorted(os.listdir('$CONTENT_DIR')):
    sp = os.path.join('$CONTENT_DIR', site_dir)
    if os.path.isdir(sp):
        count = len([f for f in os.listdir(sp) if f.endswith('.md')])
        print(f'  📊 {site_dir}: {count} articles live')
"

elif [ "$TIER" = "all" ]; then
    echo "Deploying ALL remaining articles..."
    for SITE_DIR in "$QUEUED_DIR"/*/; do
        SITE_NAME=$(basename "$SITE_DIR")
        if [ "$SITE_NAME" = "*" ]; then continue; fi
        DEST="$CONTENT_DIR/$SITE_NAME"
        mkdir -p "$DEST"
        for FILE in "$SITE_DIR"*.md; do
            [ -f "$FILE" ] || continue
            mv "$FILE" "$DEST/"
            echo "  ✅ $SITE_NAME/$(basename $FILE)"
        done
    done
fi

echo ""
echo "═══════════════════════════════════════"
echo "FINAL COUNTS:"
for SITE_DIR in "$CONTENT_DIR"/*/; do
    SITE_NAME=$(basename "$SITE_DIR")
    if [ "$SITE_NAME" = "*" ]; then continue; fi
    COUNT=$(ls "$SITE_DIR"*.md 2>/dev/null | wc -l | tr -d ' ')
    QUEUED=$(ls "$QUEUED_DIR/$SITE_NAME/"*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "  $SITE_NAME: $COUNT live, $QUEUED queued"
done
echo "═══════════════════════════════════════"
