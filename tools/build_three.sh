#!/bin/sh
# Rebuild the three.js bundle embedded in the HTML viewer (only when moving to another three.js version;
# the result is committed):
#   tools/build_three.sh
# Installs the pinned three.js (MIT) from npm, bundles the parts listed in tools/three-entry.js into one
# IIFE (window.THREE) with esbuild, and copies the three.js licence next to it.
set -eu
THREE_VERSION=0.187.0
ESBUILD_VERSION=0.25.10
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/skills/fdm-minimal-design/scripts/viewer"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
npm init -y >/dev/null
npm install --no-fund --no-audit "three@$THREE_VERSION" "esbuild@$ESBUILD_VERSION" >/dev/null
npm audit --audit-level=moderate   # stop instead of bundling a version with a known advisory
cp "$ROOT/tools/three-entry.js" entry.js
npx esbuild entry.js --bundle --minify --format=iife --global-name=THREE --legal-comments=none --outfile=bundle.js
{
  printf '/* three.js %s (MIT) https://github.com/mrdoob/three.js - licence text in three-LICENSE.txt */\n' "$THREE_VERSION"
  cat bundle.js
} > "$OUT/three.min.js"
cp node_modules/three/LICENSE "$OUT/three-LICENSE.txt"
echo "$OUT/three.min.js $(wc -c < "$OUT/three.min.js") bytes"
