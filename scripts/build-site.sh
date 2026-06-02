#!/bin/bash
# PennyPress — Full Site Build Pipeline
# Usage: ./build-site.sh <site-name> <niche> [article-count]
# Example: ./build-site.sh budget-travel-tips "budget travel" 20

set -e

SITE_NAME="$1"
NICHE="$2"
ARTICLE_COUNT="${3:-20}"
PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
TEMPLATE_DIR="$PROJECT_DIR/templates/base"
OUTPUT_DIR="$PROJECT_DIR/output/sites"
CONTENT_DIR="$PROJECT_DIR/data/content/$SITE_NAME"
SITE_DIR="$OUTPUT_DIR/$SITE_NAME"

if [ -z "$SITE_NAME" ] || [ -z "$NICHE" ]; then
    echo "Usage: $0 <site-name> <niche> [article-count]"
    echo "Example: $0 budget-travel-tips \"budget travel\" 20"
    exit 1
fi

echo "🏗️  PennyPress Build Pipeline"
echo "   Site: $SITE_NAME"
echo "   Niche: $NICHE"
echo "   Articles: $ARTICLE_COUNT"
echo ""

# Step 1: Create site directory from template
echo "[1/5] Setting up site directory..."
if [ ! -d "$SITE_DIR" ]; then
    cp -r "$TEMPLATE_DIR" "$SITE_DIR"
    echo "   ✅ Created from template"
else
    echo "   ✅ Site directory exists"
fi

# Step 2: Create site config
echo "[2/5] Creating site config..."
SLUG=$(echo "$NICHE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
SITE_TITLE=$(echo "$NICHE" | perl -pe 's/\b(\w)/\u$1/g')

cat > "$SITE_DIR/site-config.json" << EOF
{
  "name": "${SITE_TITLE} Guide",
  "niche": "$NICHE",
  "domain": "${SLUG}.com",
  "description": "Your comprehensive guide to $NICHE. Expert tips, reviews, and strategies.",
  "keywords": ["${SLUG}", "$NICHE"],
  "colors": {"primary": "#2563eb", "secondary": "#7c3aed", "accent": "#f59e0b"},
  "author": "PennyPress",
  "language": "en"
}
EOF
echo "   ✅ Site config created"

# Step 3: Copy content
echo "[3/5] Copying content..."
ARTICLES_SRC="$CONTENT_DIR"
ARTICLES_DEST="$SITE_DIR/src/content/articles"
mkdir -p "$ARTICLES_DEST"
COUNT=0
if [ -d "$ARTICLES_SRC" ]; then
    cp "$ARTICLES_SRC"/*.md "$ARTICLES_DEST/" 2>/dev/null || true
    COUNT=$(ls "$ARTICLES_DEST"/*.md 2>/dev/null | wc -l | tr -d ' ')
fi
echo "   ✅ $COUNT articles copied"

# Step 3.5: Validate content quality
echo "[3.5/6] Validating content quality..."
python3 "$PROJECT_DIR/scripts/validate-content.py" "$SITE_DIR" --min-score 60 || echo "   ⚠️  Some articles below quality threshold (proceeding anyway)"

# Step 4: Copy latest template pages
echo "[4/5] Updating template pages..."
mkdir -p "$SITE_DIR/src/pages/category"
mkdir -p "$SITE_DIR/src/layouts"
mkdir -p "$SITE_DIR/src/styles"
cp "$TEMPLATE_DIR/src/pages/index.astro" "$SITE_DIR/src/pages/index.astro"
cp "$TEMPLATE_DIR/src/pages/[slug].astro" "$SITE_DIR/src/pages/[slug].astro"
cp "$TEMPLATE_DIR/src/pages/category/[category].astro" "$SITE_DIR/src/pages/category/[category].astro"

# Copy new pages (legal, 404, author)
for page in about.astro privacy-policy.astro terms.astro contact.astro 404.astro; do
  cp "$TEMPLATE_DIR/src/pages/$page" "$SITE_DIR/src/pages/$page" 2>/dev/null || true
done
mkdir -p "$SITE_DIR/src/pages/about"
cp "$TEMPLATE_DIR/src/pages/about/author.astro" "$SITE_DIR/src/pages/about/author.astro" 2>/dev/null || true

# Copy new dynamic page directories
mkdir -p "$SITE_DIR/src/pages/compare" "$SITE_DIR/src/pages/best"
cp "$TEMPLATE_DIR/src/pages/compare/[...slug].astro" "$SITE_DIR/src/pages/compare/[...slug].astro" 2>/dev/null || true
cp "$TEMPLATE_DIR/src/pages/best/[category].astro" "$SITE_DIR/src/pages/best/[category].astro" 2>/dev/null || true

# Copy new components and utils
mkdir -p "$SITE_DIR/src/components" "$SITE_DIR/src/utils" "$SITE_DIR/src/data"
cp "$TEMPLATE_DIR/src/components/CrossSiteLinks.astro" "$SITE_DIR/src/components/CrossSiteLinks.astro" 2>/dev/null || true
cp "$TEMPLATE_DIR/src/components/MidArticleCTA.astro" "$SITE_DIR/src/components/MidArticleCTA.astro" 2>/dev/null || true
cp "$TEMPLATE_DIR/src/utils/marked-config.ts" "$SITE_DIR/src/utils/marked-config.ts" 2>/dev/null || true
cp "$TEMPLATE_DIR/src/data/affiliates.json" "$SITE_DIR/src/data/affiliates.json" 2>/dev/null || true

# Copy RSS feed + network config
cp "$TEMPLATE_DIR/src/pages/feed.xml.ts" "$SITE_DIR/src/pages/feed.xml.ts" 2>/dev/null || true
cp "$PROJECT_DIR/network-config.json" "$SITE_DIR/network-config.json" 2>/dev/null || true
cp "$TEMPLATE_DIR/src/layouts/BaseLayout.astro" "$SITE_DIR/src/layouts/BaseLayout.astro"
cp "$TEMPLATE_DIR/src/styles/global.css" "$SITE_DIR/src/styles/global.css"
cp "$TEMPLATE_DIR/tailwind.config.mjs" "$SITE_DIR/tailwind.config.mjs"
cp "$TEMPLATE_DIR/astro.config.mjs" "$SITE_DIR/astro.config.mjs"

# Inject correct sitemap URL into robots.txt
SITE_DOMAIN=$(python3 -c "import json; print(json.load(open('$SITE_DIR/site-config.json')).get('domain','${SLUG}.com'))")
sed "s|{{SITEMAP_URL}}|https://${SITE_DOMAIN}/sitemap.xml|" "$TEMPLATE_DIR/robots.txt" > "$SITE_DIR/public/robots.txt"
echo "   ✅ Templates updated"}, {

# Step 5: Build
echo "[5/6] Building site..."
cd "$SITE_DIR"

# Ensure dependencies
if [ ! -d "node_modules" ] || [ ! -f "node_modules/marked/package.json" ]; then
    echo "   Installing dependencies..."
    npm install --silent 2>/dev/null
fi

rm -rf dist
npx astro build 2>&1 | grep -E "page|Complete|Error|ERROR" || true

# Step 6: Generate sitemap
echo "[6/7] Generating sitemap..."
rm -rf "$SITE_DIR/dist/sitemap.xml"
python3 "$PROJECT_DIR/scripts/generate-sitemap.py" "$SITE_DIR" 2>&1 | tail -1

# Generate llms.txt for AI crawlers (GEO)
python3 "$PROJECT_DIR/scripts/generate-llms-txt.py" "$SITE_DIR"
python3 "$PROJECT_DIR/scripts/generate-llms-full.py" "$SITE_DIR"

# Count output
PAGES=$(find dist -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
SITEMAP_URLS=$(grep -c '<loc>' "$SITE_DIR/dist/sitemap.xml" 2>/dev/null || echo 0)
SIZE=$(du -sh dist 2>/dev/null | cut -f1)

echo ""
echo "═══════════════════════════════════════"
echo " ✅ BUILD COMPLETE"
echo "   Pages: $PAGES"
echo "   Sitemap URLs: $SITEMAP_URLS"
echo "   Size: $SIZE"
echo "   Output: $SITE_DIR/dist/"
echo "═══════════════════════════════════════"
