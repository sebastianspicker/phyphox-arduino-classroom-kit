#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

profile="${1:-base}"
missing=0

check() {
  local cmd="$1"
  local hint="${2:-Install it and retry.}"
  if ! require_cmd "$cmd" "$hint"; then
    missing=1
  fi
}

check python3

case "$profile" in
  base)
    ;;
  build)
    check xmllint "Install libxml2 utilities first."
    ;;
  compile)
    check arduino-cli "Install it first (see README.md)."
    ;;
  security)
    check git
    check rg "Install ripgrep to run the secret scan."
    ;;
  ci)
    check ruff "Install test dependencies first (see requirements-test.txt)."
    check pytest "Install test dependencies first (see requirements-test.txt)."
    check xmllint "Install libxml2 utilities first."
    check arduino-cli "Install it first (see README.md)."
    check git
    check rg "Install ripgrep to run the secret scan."
    ;;
  *)
    echo "Unknown profile: $profile" >&2
    echo "Valid profiles: base, build, compile, security, ci" >&2
    exit 2
    ;;
esac

if (( missing == 1 )); then
  exit 2
fi

echo "OK"
