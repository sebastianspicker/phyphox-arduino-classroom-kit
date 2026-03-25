#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$repo_root"

echo "== xmllint --noout =="
shopt -s nullglob

any=0
while IFS= read -r -d '' f; do
  any=1
  xmllint --noout "$f"
done < <(find . -type f \( -name '*.phyphox' -o -name '*.xml' \) -not -path './.git/*' -print0)

if (( any == 0 )); then
  echo "No *.phyphox or *.xml files found."
  exit 0
fi

echo "== xmllint --xinclude (sources) =="
while IFS= read -r -d '' f; do
  xmllint --xinclude --noout "$f"
done < <(find . -type f -name '*.phyphox.xml' -not -path './.git/*' -print0)

echo "== phyphox plausibility checks =="
while IFS= read -r -d '' f; do
  python3 tools/phyphox_validate.py "$f"
done < <(find . -type f -name '*.phyphox' -not -path './.git/*' -print0)

while IFS= read -r -d '' f; do
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT
  xmllint --xinclude "$f" | python3 tools/postprocess_phyphox_xml.py >"$tmp"
  python3 tools/phyphox_validate.py "$tmp"
  rm -f "$tmp"
  trap - EXIT
done < <(find . -type f -name '*.phyphox.xml' -not -path './.git/*' -print0)

echo "OK"
