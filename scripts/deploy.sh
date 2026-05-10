#!/bin/bash
# PennyPress Deploy — Build and prepare all sites for Cloudflare Pages
# Each site deploys as a separate Cloudflare Pages project

set -e

PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
SITE_REGISTRY="$PROJECT_DIR/data/sites.json"

echo "🏗️  PennyPress Deploy Pipeline"
echo "   $(date)"
echo ""

# Read all active sites
python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['status'] == 'active':
        print(f\"{s['name']}|{s['niche']}\")
" | while IFS='|' read -r name niche; do
    echo "═══ Deploying: $name ═══"
    
    SITE_DIR="$PROJECT_DIR/output/sites/$name"
    
    # Build if dist doesn't exist or is stale
    if [ ! -d "$SITE_DIR/dist" ] || [ "$(find $SITE_DIR/dist -name '*.html' 2>/dev/null | wc -l)" -lt 5 ]; then
        echo "   Building site..."
        bash "$PROJECT_DIR/scripts/build-site.sh" "$name" "$niche"
    fi
    
    # Count pages
    PAGES=$(find "$SITE_DIR/dist" -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
    SIZE=$(du -sh "$SITE_DIR/dist" 2>/dev/null | cut -f1)
    
    echo "   ✅ $PAGES pages ($SIZE)"
    echo ""
done

echo "═══════════════════════════════════════"
echo " ✅ ALL SITES BUILT AND READY"
echo ""
echo " Deploy to Cloudflare Pages:"
for name in $(python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['status'] == 'active':
        print(s['name'])
"); do
    echo "   npx wrangler pages deploy output/sites/$name/dist --project-name=$name"
done
echo "═══════════════════════════════════════"
