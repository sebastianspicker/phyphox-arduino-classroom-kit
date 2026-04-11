#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Basic secret patterns. Keep this list tight to avoid noise.
# Note: output is parsed as file:lineno:content; filenames containing colons may be misparsed.
patterns=(
  "BEGIN (RSA|EC|OPENSSH) PRIVATE KEY"
  "AKIA[0-9A-Z]{16}"
  "ASIA[0-9A-Z]{16}"
  "xox[baprs]-[0-9A-Za-z-]{10,}"
  "ghp_[0-9A-Za-z]{36}"
  "github_pat_[0-9A-Za-z_]{20,}"
  "glpat-[0-9A-Za-z-]{20,}"
)

matches="$(mktemp)"
trap 'rm -f "$matches"' EXIT

found=0
for pat in "${patterns[@]}"; do
  if git grep -nE "$pat" -- . >>"$matches" 2>/dev/null; then
    found=1
  fi
done

if (( found == 1 )); then
  while IFS= read -r line; do
    file="${line%%:*}"
    rest="${line#*:}"
    lineno="${rest%%:*}"
    echo "Potential secret match: ${file}:${lineno}"
  done <"$matches"
  echo "Secret scan failed. Remove secrets or add safe handling before proceeding." >&2
  exit 1
fi

echo "OK"
