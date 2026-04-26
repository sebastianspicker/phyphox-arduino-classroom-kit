#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

require_cmd xmllint "Install libxml2 utilities first." || exit 2
require_cmd python3 || exit 2

# Optional: output directory for *.phyphox (default: experiments/)
PHYPHOX_OUTDIR="${PHYPHOX_OUTDIR:-$repo_root/experiments}"
if [[ -n "${1:-}" ]]; then
  PHYPHOX_OUTDIR="$1"
fi
mkdir -p "$PHYPHOX_OUTDIR"

shopt -s nullglob

src_files=(src/phyphox/*.phyphox.xml)
if ((${#src_files[@]} == 0)); then
  echo "No source files found at src/phyphox/*.phyphox.xml"
  exit 0
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

for src in "${src_files[@]}"; do
  out="${src##*/}"
  out="${out%.xml}" # foo.phyphox.xml -> foo.phyphox
  outpath="$PHYPHOX_OUTDIR/$out"

  xmllint --xinclude "$src" | python3 tools/postprocess_phyphox_xml.py >"$tmp"
  cp "$tmp" "$outpath"
done

echo "Built ${#src_files[@]} phyphox files."
if [[ "$PHYPHOX_OUTDIR" != "$repo_root/experiments" ]]; then
  echo "Output: $PHYPHOX_OUTDIR"
fi
