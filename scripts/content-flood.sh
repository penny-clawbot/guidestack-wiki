#!/bin/bash
# content-flood.sh — Aggressive content generation for all PennyPress sites
# Generates articles and places them in the correct Astro content directory
set -euo pipefail

PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
DATA_DIR="$PROJECT_DIR/data/content"
OUTPUT_DIR="$PROJECT_DIR/output/sites"
GENERATOR="$PROJECT_DIR/writer.py"

generate_for_site() {
  local SITE_NAME="$1"
  local NICHE="$2"
  local COUNT="${3:-10}"
  
  local SITE_DIR="$OUTPUT_DIR/$SITE_NAME"
  local CONTENT_DIR="$SITE_DIR/src/content/articles"
  local DATA_SITE_DIR="$DATA_DIR/$SITE_NAME"
  
  mkdir -p "$CONTENT_DIR" "$DATA_SITE_DIR"
  
  echo "  Generating $COUNT articles for $SITE_NAME ($NICHE)..."
  
  # Use the existing writer.py to generate content
  cd "$PROJECT_DIR"
  python3 "$GENERATOR" \
    --site "$SITE_NAME" \
    --niche "$NICHE" \
    --count "$COUNT" \
    --output "$CONTENT_DIR" \
    --data-output "$DATA_SITE_DIR" \
    2>&1 | tail -3
}

echo "=== PennyPress Content Flood === ($(date +%Y-%m-%d %H:%M))"

# Sites with existing content — expand them
generate_for_site "budget-travel-tips" "budget travel tips and affordable destinations" 10
generate_for_site "crypto-investing-guide" "cryptocurrency investing strategies and market analysis" 10
generate_for_site "ai-tools-hub" "best AI tools and software reviews" 10
generate_for_site "personal-finance-tips" "personal finance money management tips" 10

# Sites with NO content — prime them
generate_for_site "bitcoin-beginners" "bitcoin basics beginner guide" 10
generate_for_site "crypto-trading-strategies" "cryptocurrency trading strategies and technical analysis" 10
generate_for_site "defi-yield-guide" "decentralized finance yield farming DeFi guide" 10

echo "=== Flood Complete ==="
