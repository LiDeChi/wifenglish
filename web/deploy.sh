#!/bin/bash
set -e
echo "🚀 Deploying WifEnglish to Vercel..."
cd "$(dirname "$0")"
if ! command -v vercel &> /dev/null; then
  echo "Installing Vercel CLI..."
  npm i -g vercel
fi
echo "Please run 'vercel login' if you haven't already (one-time)."
vercel --prod --yes
echo "✅ Deployed!"
