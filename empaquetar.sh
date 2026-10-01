#!/usr/bin/env bash
# Crea dist/<skill>.zip de cada skill para subirla a claude.ai (sin PDF ni SVG de ejemplo, para aligerar).
set -euo pipefail
cd "$(dirname "$0")/.claude/skills"
mkdir -p ../../dist
for skill in */; do
  nombre="${skill%/}"
  rm -f "../../dist/$nombre.zip"
  find "$nombre" -name __pycache__ -prune -o -type f \
       \( -path "*/ejemplos/*" -a \( -name "*.svg" -o -name "*.pdf" \) \) -prune -o -type f -print \
    | zip -q "../../dist/$nombre.zip" -@
  echo "dist/$nombre.zip"
done
