#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
cd "$repo_root"

bash scripts/check-prereqs.sh ci

echo "== Ruff =="
ruff check .
ruff format --check .

echo
echo "== Pytest =="
pytest

echo
echo "== XML + phyphox validation =="
bash scripts/validate-xml.sh

echo
echo "== Rebuild generated experiments =="
bash scripts/build-phyphox.sh
bash scripts/check-generated-clean.sh

echo
echo "== Arduino compile =="
bash scripts/compile-arduino.sh

echo
echo "== Security baseline =="
bash scripts/secret-scan.sh
bash scripts/deps-scan.sh
bash scripts/sast-minimal.sh

echo
echo "OK"
