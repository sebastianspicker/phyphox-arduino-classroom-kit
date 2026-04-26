#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

require_cmd bash || exit 2
require_cmd python3 || exit 2

shopt -s nullglob

shell_files=(scripts/*.sh)
if (( ${#shell_files[@]} > 0 )); then
  echo "== bash -n (shell syntax) =="
  for f in "${shell_files[@]}"; do
    bash -n "$f"
  done

  if command -v shellcheck >/dev/null 2>&1; then
    echo "== shellcheck =="
    shellcheck "${shell_files[@]}"
  fi
fi

py_files=(tools/*.py)
if (( ${#py_files[@]} > 0 )); then
  echo "== python3 -m py_compile =="
  python3 -m py_compile "${py_files[@]}"
fi

echo "OK"
