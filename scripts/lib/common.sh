#!/usr/bin/env bash

# Shared shell helpers for repository scripts.

repo_root_from_script() {
  local script_path="$1"
  (cd "$(dirname "$script_path")/.." && pwd)
}

require_cmd() {
  local cmd="$1"
  local hint="${2:-Install it and retry.}"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd not found. $hint" >&2
    return 2
  fi
  return 0
}
