#!/bin/bash
set -e
echo "🚀 Deploying WifEnglish to Cloudflare Pages..."
cd "$(dirname "$0")"

# Use wrangler (recommended)
if ! command -v wrangler &> /dev/null; then
  echo "Using npx wrangler..."
fi

npx wrangler pages deploy . --project-name=wifenglish --commit-dirty=true

echo "✅ Deployed to https://wifenglish.pages.dev"
echo "Custom domain: https://wifenglish.wordm.us (configure DNS + Pages domain if needed)"
