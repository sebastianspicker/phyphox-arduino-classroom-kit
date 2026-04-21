#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Optional: output directory for *.phyphox (default: experiments/)
PHYPHOX_OUTDIR="${PHYPHOX_OUTDIR:-$repo_root/experiments}"
if [[ -n "${1:-}" ]]; then
  PHYPHOX_OUTDIR="$1"
fi
mkdir -p "$PHYPHOX_OUTDIR"

shopt -s nullglob

src_files=( src/phyphox/*.phyphox.xml )
if (( ${#src_files[@]} == 0 )); then
  echo "No source files found at src/phyphox/*.phyphox.xml"
  exit 0
fi

for src in "${src_files[@]}"; do
  out="${src##*/}"
  out="${out%.xml}" # foo.phyphox.xml -> foo.phyphox
  outpath="$PHYPHOX_OUTDIR/$out"

  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT

  xmllint --xinclude "$src" | python3 tools/postprocess_phyphox_xml.py >"$tmp"
  mv "$tmp" "$outpath"
  trap - EXIT
done

echo "Built ${#src_files[@]} phyphox files."
if [[ "$PHYPHOX_OUTDIR" != "$repo_root/experiments" ]]; then
  echo "Output: $PHYPHOX_OUTDIR"
fi
