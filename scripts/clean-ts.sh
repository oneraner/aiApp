#!/usr/bin/env sh
set -e

echo "🧹 Cleaning TypeScript & build caches..."

# TypeScript incremental build cache
find . -name "*.tsbuildinfo" -type f -delete

# Vite cache
rm -rf node_modules/.vite
rm -rf **/node_modules/.vite 2>/dev/null || true

# Turbo cache
rm -rf .turbo

# TanStack Start / Vite SSR cache
rm -rf .nitro
rm -rf .start

# dist / build outputs
rm -rf dist build out

# Optional: tsserver cache (safe)
rm -rf ~/.tsbuildinfo 2>/dev/null || true

echo "✅ Done. Restart VSCode + TS Server recommended."
