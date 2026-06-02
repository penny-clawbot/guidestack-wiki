#!/bin/bash
# PennyPress - Project Setup Script
# Creates the full project structure for the Programmatic SEO Content Network

set -e

BASE_DIR="$HOME/Documents/Penny/Penny-AI/projects/pseo-network"

echo "🚀 Setting up PennyPress project structure..."

# Core directories
mkdir -p "$BASE_DIR"/{src,templates,data,scripts,output,logs}
mkdir -p "$BASE_DIR"/src/{agents,pipeline,templates,utils}
mkdir -p "$BASE_DIR"/data/{keywords,sites,content,analytics}
mkdir -p "$BASE_DIR"/templates/{base,niches}
mkdir -p "$BASE_DIR"/output/sites
mkdir -p "$BASE_DIR"/logs/{agents,pipeline}

# Site output directories (will be populated per-site)
mkdir -p "$BASE_DIR/output/sites"

echo "✅ Directory structure created"

# Initialize git repo if not exists
if [ ! -d "$BASE_DIR/.git" ]; then
    cd "$BASE_DIR"
    git init
    echo "✅ Git repo initialized"
fi

echo "📁 Project structure:"
find "$BASE_DIR" -type d | head -30 | sed 's|'"$BASE_DIR"'|pseo-network|'
