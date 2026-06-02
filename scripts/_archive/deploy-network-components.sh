#!/bin/bash
# deploy-network-components.sh
# Copies NetworkFooter, CrossSiteLinks, and NetworkSchema Astro components
# to all 8 GuideStack sites and patches BaseLayout.astro to include them.
#
# Usage: bash scripts/deploy-network-components.sh
# FREE — no paid tools.

set -e

SITES_DIR="/Users/penny/Documents/Penny/pseo-network/output/sites"
COMPONENTS_SRC="/Users/penny/Documents/Penny/pseo-network/output/sites/bitcoin-beginners/src/components"
COMPONENTS=("NetworkFooter.astro" "CrossSiteLinks.astro" "NetworkSchema.astro")

SITES=("ai-tools-hub" "bitcoin-beginners" "budget-travel-tips" "crypto-investing-guide" 
       "crypto-trading-strategies" "defi-yield-guide" "personal-finance-tips" "smart-emergency-fund")

echo "🚀 Deploying network components to all GuideStack sites..."
echo "═══════════════════════════════════════════════════"

for SITE in "${SITES[@]}"; do
  SITE_DIR="$SITES_DIR/$SITE"
  COMP_DIR="$SITE_DIR/src/components"
  LAYOUT="$SITE_DIR/src/layouts/BaseLayout.astro"
  
  if [ ! -d "$SITE_DIR" ]; then
    echo "⚠️  $SITE: Directory not found, skipping"
    continue
  fi

  echo ""
  echo "📦 Processing: $SITE"
  echo "─────────────────────────────────────"
  
  # Ensure components directory exists
  mkdir -p "$COMP_DIR"
  
  # Copy network components
  for COMP in "${COMPONENTS[@]}"; do
    if [ -f "$COMP_DIR/$COMP" ]; then
      echo "  ✓ $COMP already exists (updating)"
    fi
    cp "$COMPONENTS_SRC/$COMP" "$COMP_DIR/$COMP"
    echo "  ✅ Copied $COMP"
  done

  # Patch BaseLayout.astro to include NetworkFooter and NetworkSchema
  if [ -f "$LAYOUT" ]; then
    # Check if already patched
    if grep -q "NetworkFooter" "$LAYOUT"; then
      echo "  ✓ BaseLayout already includes NetworkFooter"
    else
      # Add imports after the existing imports in the frontmatter
      # We need to add: import NetworkFooter from '../components/NetworkFooter.astro';
      # and: import NetworkSchema from '../components/NetworkSchema.astro';
      
      # Insert imports after the last existing import line
      sed -i '' "/^import/a\\
import NetworkFooter from '../components/NetworkFooter.astro';\\
import CrossSiteLinks from '../components/CrossSiteLinks.astro';\\
import NetworkSchema from '../components/NetworkSchema.astro';
" "$LAYOUT"
      
      echo "  ✅ Added component imports to BaseLayout"
      
      # Insert NetworkSchema in <head> before closing </head>
      if ! grep -q "NetworkSchema" "$LAYOUT" || true; then
        sed -i '' 's|</head>|<NetworkSchema currentSiteId="'"$SITE"'" />\n  </head>|' "$LAYOUT"
        echo "  ✅ Added NetworkSchema to <head>"
      fi

      # Insert NetworkFooter before the footer's closing </div>
      # Find the newsletter section in footer and add NetworkFooter after it
      if ! grep -q "NetworkFooter" "$LAYOUT" || true; then
        sed -i '' 's|<p class="text-xs text-\[var(--color-text-muted)\]">Built with|<NetworkFooter currentSiteId="'"$SITE"'" />\n        <p class="text-xs text-\[var(--color-text-muted)\]">Built with|' "$LAYOUT"
        echo "  ✅ Added NetworkFooter to footer"
      fi
    fi
  else
    echo "  ⚠️ No BaseLayout.astro found in $SITE"
  fi

  echo "  ✅ $SITE done"
done

echo ""
echo "═══════════════════════════════════════════════════"
echo "🎉 Network components deployed to all sites!"
echo ""
echo "📋 Next steps:"
echo "  1. Run: node scripts/generate-sitemap-index.js"
echo "  2. Rebuild all sites: bash scripts/pennypress.sh build-all"
echo "  3. Deploy to Cloudflare Pages"
echo "  4. Submit sitemap-index.xml to Google Search Console"
