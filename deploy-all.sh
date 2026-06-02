#!/bin/bash
# GuideStack — Deploy all sites to Cloudflare Pages
# Usage: ./deploy-all.sh
# Prerequisites: wrangler CLI installed, logged in (wrangler login)

set -e
SITES_DIR="/Users/penny/Documents/Penny/pseo-network/output/sites"
SITES="ai-tools-hub bitcoin-beginners budget-travel-tips crypto-investing-guide crypto-trading-strategies defi-yield-guide personal-finance-tips smart-emergency-fund"

DEPLOYED=0
FAILED=0

for site in $SITES; do
  echo "🚀 Building ${site}..."
  cd "${SITES_DIR}/${site}"
  
  # Install deps (quiet, only if needed)
  if [ ! -d "node_modules" ]; then
    npm install --quiet 2>/dev/null
  fi
  
  # Build static site
  if npm run build 2>&1; then
    # Deploy to Cloudflare Pages
    echo "📦 Deploying ${site}..."
    if npx wrangler pages deploy dist --project-name=gs-${site} 2>&1; then
      echo "✅ ${site} deployed!"
      DEPLOYED=$((DEPLOYED + 1))
    else
      echo "❌ ${site} deploy failed!"
      FAILED=$((FAILED + 1))
    fi
  else
    echo "❌ ${site} build failed!"
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

echo "================================"
echo "🎉 Deployed: ${DEPLOYED}/8"
if [ $FAILED -gt 0 ]; then
  echo "⚠️  Failed: ${FAILED}/8"
fi
echo "================================"
