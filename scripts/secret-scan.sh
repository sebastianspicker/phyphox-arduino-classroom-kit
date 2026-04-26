#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

require_cmd git || exit 2
require_cmd rg "Install ripgrep to run the secret scan." || exit 2

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

rg_args=(--null --line-number --with-filename)
for pat in "${patterns[@]}"; do
  rg_args+=(-e "$pat")
done

if git ls-files -z --cached --others --exclude-standard -- . \
  | xargs -0r rg "${rg_args[@]}" -- >>"$matches"; then
  :
fi

if [[ -s "$matches" ]]; then
  while IFS= read -r -d '' file && IFS= read -r line; do
    lineno="${line%%:*}"
    echo "Potential secret match: ${file}:${lineno}"
  done <"$matches"
  echo "Secret scan failed. Remove secrets or add safe handling before proceeding." >&2
  exit 1
fi

echo "OK"
