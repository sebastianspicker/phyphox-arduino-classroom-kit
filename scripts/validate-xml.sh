#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

require_cmd xmllint "Install libxml2 utilities first." || exit 2
require_cmd python3 || exit 2

shopt -s nullglob

source_files=(src/phyphox/*.phyphox.xml)
include_files=(src/phyphox/includes/*.xml)
generated_files=(experiments/*.phyphox)

if ((${#source_files[@]} == 0)); then
  echo "No source files found at src/phyphox/*.phyphox.xml." >&2
  exit 1
fi

echo "== xmllint --noout =="
for f in "${include_files[@]}" "${source_files[@]}" "${generated_files[@]}"; do
  [[ -e "$f" ]] || continue
  xmllint --noout "$f"
done

echo "== xmllint --xinclude =="
for f in "${source_files[@]}"; do
  xmllint --xinclude --noout "$f"
done

if ((${#generated_files[@]} == 0)); then
  echo "No generated experiments found at experiments/*.phyphox." >&2
  exit 1
fi

echo "== phyphox plausibility checks (generated) =="
python3 tools/validate_phyphox.py "${generated_files[@]}"

echo "== phyphox plausibility checks (expanded sources) =="
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
for f in "${source_files[@]}"; do
  out="${f##*/}"
  out="${out%.xml}"
  outpath="$tmpdir/$out"
  xmllint --xinclude "$f" | python3 tools/postprocess_phyphox_xml.py >"$outpath"
  python3 tools/validate_phyphox.py "$outpath"
done

echo "OK"
