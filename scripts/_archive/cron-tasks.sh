#!/bin/bash
#
# PennyPress Cron Tasks
# Run periodic monitoring and reporting tasks
#
# Usage:
#   bash cron-tasks.sh daily    # Rank monitoring for all sites
#   bash cron-tasks.sh weekly   # Performance reports
#   bash cron-tasks.sh monthly  # Content freshness check
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_DIR/data"
SITES_DIR="$DATA_DIR/sites"
ANALYTICS_DIR="$DATA_DIR/analytics"
LOG_DIR="$PROJECT_DIR/logs"
KEYWORDS_DIR="$DATA_DIR/keywords"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$ANALYTICS_DIR"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

# Get all registered domains
get_registered_domains() {
    local registry="$SITES_DIR/registry.json"
    if [ ! -f "$registry" ]; then
        echo ""
        return
    fi
    # Extract domains from JSON (simple grep approach, no jq needed)
    grep -o '"domain"[[:space:]]*:[[:space:]]*"[^"]*"' "$registry" 2>/dev/null | sed 's/.*: *"\([^"]*\)"/\1/' || true
}

# Daily: Rank monitoring for all sites
run_daily() {
    log "=== Running DAILY rank monitoring ==="
    
    local domains=$(get_registered_domains)
    local count=0
    
    if [ -z "$domains" ]; then
        log "No sites registered. Run site-registry.py register first."
        return
    fi
    
    for domain in $domains; do
        count=$((count + 1))
        log "Checking rankings for: $domain"
        
        # Find keywords file for this domain
        local kw_file="$KEYWORDS_DIR/${domain}-keywords.json"
        
        if [ -f "$kw_file" ]; then
            python3 "$SCRIPT_DIR/rank-monitor.py" \
                --keywords "$kw_file" \
                --domain "$domain" \
                >> "$LOG_DIR/daily-$(date '+%Y-%m-%d').log" 2>&1
            log "  ✓ Completed: $domain"
        else
            log "  ⚠ No keywords file found: $kw_file"
        fi
    done
    
    log "Daily rank monitoring complete. Checked $count sites."
}

# Weekly: Performance reports
run_weekly() {
    log "=== Running WEEKLY performance report ==="
    
    local report_file="$ANALYTICS_DIR/weekly-report-$(date '+%Y-%m-%d').json"
    
    python3 "$SCRIPT_DIR/performance-report.py" \
        --period weekly \
        --json \
        --output "$report_file"
    
    log "Weekly report saved: $report_file"
    
    # Also generate text version for quick viewing
    python3 "$SCRIPT_DIR/performance-report.py" \
        --period weekly \
        --output "$ANALYTICS_DIR/weekly-report-$(date '+%Y-%m-%d').txt"
    
    log "Text report saved."
}

# Monthly: Content freshness check
run_monthly() {
    log "=== Running MONTHLY content freshness check ==="
    
    local registry="$SITES_DIR/registry.json"
    
    if [ ! -f "$registry" ]; then
        log_error "Registry not found: $registry"
        return
    fi
    
    # Simple check: look for recent content updates
    local stale_sites=()
    local cutoff_date=$(date -d "30 days ago" '+%Y-%m-%d')
    
    for content_dir in "$DATA_DIR/content"/*/; do
        if [ -d "$content_dir" ]; then
            local latest=$(ls -t "$content_dir"*.md 2>/dev/null | head -1)
            if [ -n "$latest" ]; then
                local file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$latest" 2>/dev/null || stat -c "%y" "$latest" 2>/dev/null | cut -d' ' -f1)
                if [[ "$file_date" < "$cutoff_date" ]]; then
                    stale_sites+=("$(basename "$content_dir")")
                fi
            fi
        fi
    done
    
    if [ ${#stale_sites[@]} -eq 0 ]; then
        log "✓ All sites have recent content (within 30 days)"
    else
        log "⚠ Stale sites detected (no content in 30+ days):"
        for site in "${stale_sites[@]}"; do
            log "  - $site"
        done
        
        # Create alert file
        echo "Stale sites as of $(date '+%Y-%m-%d'):" > "$LOG_DIR/stale-sites-$(date '+%Y-%m').txt"
        for site in "${stale_sites[@]}"; do
            echo "  - $site" >> "$LOG_DIR/stale-sites-$(date '+%Y-%m').txt"
        done
    fi
    
    log "Monthly content freshness check complete."
}

# Show usage
usage() {
    echo "PennyPress Cron Tasks"
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  daily    Run daily rank monitoring for all registered sites"
    echo "  weekly   Generate weekly performance report"
    echo "  monthly  Check content freshness (flag sites with no new content in 30+ days)"
    echo ""
    echo "Examples:"
    echo "  $0 daily"
    echo "  $0 weekly"
    echo "  $0 monthly"
}

# Main
case "${1:-}" in
    daily)
        run_daily
        ;;
    weekly)
        run_weekly
        ;;
    monthly)
        run_monthly
        ;;
    *)
        usage
        exit 1
        ;;
esac