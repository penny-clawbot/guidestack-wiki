#!/bin/bash
# PennyPress — Autonomous Operations Controller
# Runs all periodic tasks for the PSEO content network
# Designed to be called by OpenClaw cron jobs

set -e

PROJECT_DIR="/Users/penny/Documents/Penny/pseo-network"
LOG_DIR="$PROJECT_DIR/logs"
SITE_REGISTRY="$PROJECT_DIR/data/sites.json"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
LOG="$LOG_DIR/operations_$TIMESTAMP.log"

log() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$LOG"
}

# ── Registry Management ──────────────────────────────────────

ensure_registry() {
    if [ ! -f "$SITE_REGISTRY" ]; then
        cat > "$SITE_REGISTRY" << 'EOF'
{
  "sites": [],
  "settings": {
    "articles_per_batch": 5,
    "min_articles_before_deploy": 15,
    "max_articles_per_site": 100,
    "content_types": ["pillar", "standard", "faq", "howto", "listicle", "comparison"],
    "build_on_new_content": true
  }
}
EOF
        log "Created site registry"
    fi
}

register_site() {
    local name="$1" niche="$2"
    # Check if already registered
    if python3 -c "
import json, sys
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['name'] == '$name':
        sys.exit(0)
sys.exit(1)
"; then
        log "Site '$name' already registered"
        return
    fi
    python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
data['sites'].append({
    'name': '$name',
    'niche': '$niche',
    'status': 'active',
    'created': '$(date -Iseconds)',
    'last_build': None,
    'last_deploy': None,
    'article_count': 0
})
with open('$SITE_REGISTRY', 'w') as f:
    json.dump(data, f, indent=2)
"
    log "Registered site: $name"
}

# ── Content Generation ──────────────────────────────────────

generate_content() {
    local site_name="$1" niche="$2" count="${3:-5}"
    local script="$PROJECT_DIR/scripts/content-batch.py"
    
    log "Generating $count articles for '$site_name' ($niche)"
    PYTHONUNBUFFERED=1 python3 "$script" "$site_name" "$niche" "$count" 2>&1 | tee -a "$LOG"
    
    # Update article count in registry
    local art_count=$(ls "$PROJECT_DIR/data/content/$site_name/"*.md 2>/dev/null | wc -l | tr -d ' ')
    python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['name'] == '$site_name':
        s['article_count'] = $art_count
        break
with open('$SITE_REGISTRY', 'w') as f:
    json.dump(data, f, indent=2)
"
    log "Article count for $site_name: $art_count"
}

# ── Site Build ──────────────────────────────────────────────

build_site() {
    local site_name="$1" niche="$2"
    local build_script="$PROJECT_DIR/scripts/build-site.sh"
    
    log "Building site: $site_name"
    bash "$build_script" "$site_name" "$niche" 2>&1 | tee -a "$LOG"
    
    # Update last build time
    python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['name'] == '$site_name':
        s['last_build'] = '$(date -Iseconds)'
        break
with open('$SITE_REGISTRY', 'w') as f:
    json.dump(data, f, indent=2)
"
}

# ── Main ────────────────────────────────────────────────────

ensure_registry

case "${1:-status}" in
    status)
        echo "═══ PennyPress Status ═══"
        if [ -f "$SITE_REGISTRY" ]; then
            python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    print(f\"  {s['name']:30} | {s['niche']:25} | {s['article_count']} articles | {s['status']}\")
print(f\"\\n  Total sites: {len(data['sites'])}\")
"
        else
            echo "  No sites registered yet"
        fi
        echo "═════════════════════════"
        ;;
    
    register)
        register_site "$2" "$3"
        ;;
    
    generate)
        generate_content "$2" "$3" "${4:-5}"
        ;;
    
    build)
        build_site "$2" "$3"
        ;;
    
    full-run)
        # Generate + build for a site
        site="$2"; niche="$3"; count="${4:-5}"
        register_site "$site" "$niche"
        generate_content "$site" "$niche" "$count"
        build_site "$site" "$niche"
        ;;
    
    update)
        # Update article count for a site
        site="$2"; count="$3"
        python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['name'] == '$site':
        s['article_count'] = $count
        break
with open('$SITE_REGISTRY', 'w') as f:
    json.dump(data, f, indent=2)
"
        log "Updated: $count articles"
        ;;

    build-all)
        # Build all registered sites
        python3 -c "
import json
with open('$SITE_REGISTRY') as f:
    data = json.load(f)
for s in data['sites']:
    if s['status'] == 'active':
        print(f\"{s['name']}|{s['niche']}\")
" | while IFS='|' read -r name niche; do
            build_site "$name" "$niche"
        done
        ;;
    
    *)
        echo "Usage: $0 {status|register|generate|build|full-run|build-all}"
        echo ""
        echo "Commands:"
        echo "  status                    Show all registered sites"
        echo "  register <name> <niche>   Register a new site"
        echo "  generate <name> <niche> [count]  Generate articles"
        echo "  build <name> <niche>      Build a site"
        echo "  full-run <name> <niche> [count]  Register + generate + build"
        echo "  build-all                 Build all active sites"
        ;;
esac
