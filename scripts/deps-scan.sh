#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

file="scripts/compile-arduino.sh"
req_file="requirements-test.txt"

if [[ ! -f "$file" ]]; then
  echo "Missing file: $file" >&2
  exit 1
fi

if [[ ! -f "$req_file" ]]; then
  echo "Missing file: $req_file" >&2
  exit 1
fi

if ! grep -q "arduino-cli core install" "$file"; then
  echo "No 'arduino-cli core install' found in $file" >&2
  exit 1
fi

if ! grep -q "arduino-cli core install .*@" "$file"; then
  echo "Arduino core install is not version-pinned in $file" >&2
  exit 1
fi

in_lib_block=0
unpinned=0

while IFS= read -r line; do
  if [[ "$line" == arduino-cli\ lib\ install* ]]; then
    in_lib_block=1
  fi

  if (( in_lib_block == 1 )); then
    # Strip comments and trailing backslashes.
    line_no_comment="${line%%#*}"
    line_no_comment="${line_no_comment%\\}"

    for token in $line_no_comment; do
      case "$token" in
        arduino-cli|lib|install) continue ;;
      esac
      if [[ -n "$token" && "$token" != "\\" && "$token" != *@* ]]; then
        echo "Unpinned Arduino library: $token" >&2
        unpinned=1
      fi
    done

    if [[ "$line" != *"\\" ]]; then
      in_lib_block=0
    fi
  fi
done <"$file"

if (( unpinned == 1 )); then
  exit 1
fi

# Check that every Python dependency in requirements-test.txt carries a version constraint.
py_unconstrained=0
while IFS= read -r line; do
  # Skip blank lines and comments.
  [[ -z "$line" || "$line" == \#* ]] && continue
  # Strip inline comments and surrounding whitespace.
  pkg="${line%%#*}"
  pkg="${pkg%%[[:space:]]*}"
  [[ -z "$pkg" ]] && continue

  # A version constraint contains one of: >= <= == != ~= > <
  if ! grep -qE "[><=!~]" <<<"$pkg"; then
    echo "Unconstrained Python dependency: $pkg (in $req_file)" >&2
    py_unconstrained=1
  fi
done <"$req_file"

if (( py_unconstrained == 1 )); then
  exit 1
fi

echo "OK"
