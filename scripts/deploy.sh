#!/usr/bin/env bash
# deploy.sh — Deploy PennyPress site to GitHub + Cloudflare Pages
# Usage: ./deploy.sh <site-directory>
# Example: ./deploy.sh output/sites/smart-home-gadgets

set -e

SITE_DIR="$1"

if [ -z "$SITE_DIR" ]; then
    echo "Usage: ./deploy.sh <site-directory>"
    echo "Example: ./deploy.sh output/sites/smart-home-gadgets"
    exit 1
fi

if [ ! -d "$SITE_DIR" ]; then
    echo "❌ Site directory not found: $SITE_DIR"
    exit 1
fi

# Resolve absolute path
SITE_DIR=$(cd "$SITE_DIR" && pwd)
SITE_NAME=$(basename "$SITE_DIR")
echo "🚀 Deploying site: $SITE_NAME"
echo "📁 Directory: $SITE_DIR"

# Check GitHub CLI auth
echo ""
echo "Checking GitHub authentication..."
if ! gh auth status &>/dev/null; then
    echo ""
    echo "⚠️  GitHub CLI not authenticated!"
    echo ""
    echo "To authenticate, run:"
    echo "  gh auth login"
    echo ""
    echo "Required scope: repo (for private repos) or public_repo (for public)"
    echo ""
    exit 1
fi

echo "✅ GitHub CLI authenticated"

# Get GitHub user/org
GITHUB_USER=$(gh api user --jq .login 2>/dev/null || echo "")
if [ -z "$GITHUB_USER" ]; then
    echo "❌ Could not determine GitHub username"
    exit 1
fi

echo "✅ GitHub user: $GITHUB_USER"

# Initialize git if not already
if [ ! -d "$SITE_DIR/.git" ]; then
    echo ""
    echo "📦 Initializing git repository..."
    cd "$SITE_DIR"
    git init
    git branch -M main

    # Create .gitignore if needed
    if [ ! -f "$SITE_DIR/.gitignore" ]; then
        cat > "$SITE_DIR/.gitignore" << 'EOF'
node_modules/
dist/
.DS_Store
*.log
.env
EOF
    fi

    # Initial commit
    git add .
    git commit -m "Initial PennyPress site deployment"
else
    echo "✅ Git repo already initialized"
fi

# Check if remote exists
cd "$SITE_DIR"
HAS_REMOTE=$(git remote -v 2>/dev/null | grep origin || echo "")

if [ -z "$HAS_REMOTE" ]; then
    echo ""
    echo "🔗 Creating GitHub repository..."
    
    # Try to create under pennypress-sites org, fall back to personal
    REPO_URL=""
    
    # Try org first
    if gh api repos/pennypress-sites &>/dev/null; then
        echo "✅ Found pennypress-sites organization"
        REPO_URL="https://github.com/pennypress-sites/${SITE_NAME}.git"
        gh repo create "pennypress-sites/${SITE_NAME}" --source=. --private --push 2>/dev/null || {
            echo "⚠️ Could not create in org, trying personal..."
            REPO_URL=""
        }
    fi
    
    if [ -z "$REPO_URL" ]; then
        echo "📝 Creating personal repository: $GITHUB_USER/$SITE_NAME"
        gh repo create "${SITE_NAME}" --source=. --private --push 2>/dev/null || true
        REPO_URL="https://github.com/${GITHUB_USER}/${SITE_NAME}.git"
    fi

    if [ -n "$REPO_URL" ]; then
        echo "✅ Repository created and pushed: $REPO_URL"
    fi
else
    echo "✅ Remote already configured"
fi

# Get the repo URL for display
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "unknown")

echo ""
echo "✅ GitHub repository ready: $REPO_URL"
echo ""
echo "📋 NEXT STEPS FOR CLOUDFLARE PAGES:"
echo ""
echo "1. Go to: https://pages.cloudflare.com/"
echo "2. Click 'Create a project' → 'Import Git repository'"
echo "3. Select: $REPO_URL"
echo "4. Configure:"
echo "   - Build command: npm install && npm run build"
echo "   - Build output directory: dist"
echo "   - Environment variables (optional):"
echo "     NODE_VERSION: 20"
echo ""
echo "OR use Wrangler CLI:"
echo "  npx wrangler pages project create $SITE_NAME"
echo "  npx wrangler pages deploy dist --project-name=$SITE_NAME"
echo ""
echo "🌐 Once deployed, your site will be at:"
echo "   https://${SITE_NAME}.pages.dev"
echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "📊 Summary:"
echo "   Site: $SITE_NAME"
echo "   Repo: $REPO_URL"
echo "   Directory: $SITE_DIR"