# Agent Guide

This repository is the `phyphox-arduino-classroom-kit` consolidation.

`reference/phyphox-wiki-core/` is an optional local, untracked adjunct. Use it
as the first phyphox reference only when it exists in the working tree. A fresh
clone on GitHub will not contain that folder.

## Canonical Reference Order

When the optional local reference exists:

1. `reference/phyphox-wiki-core/file-format.md`
2. `reference/phyphox-wiki-core/analysis-modules.md`
3. `reference/phyphox-wiki-core/commands-and-transport.md`
4. Repo docs and sources:
   - `docs/ASTRONOMY_EXPERIMENTS_COMPANION.md`
   - `docs/audit/`
   - `src/phyphox/`
   - `experiments/`
   - `arduino/phyphox_ble_sense/`
   - `tools/validate_phyphox.py`

When the optional local reference is absent, start with the tracked repo docs
and sources above.

## What To Trust

- Use the curated markdown summaries first for phyphox XML structure, module
  behavior, remote commands, network transport, and BLE syntax.
- Use the raw wiki mirror only when the summaries are not detailed enough and a
  source-level check is needed.
- If the local wiki mirror and repo sources disagree, prefer the repo sources
  for implementation reality and the curated summaries for conceptual guidance.

## Repo-Specific Focus

- `config` is the control surface for mode switching.
- BLE output and input characteristics are the key bridge between the app and
  the Arduino sketch.
- `.phyphox` files are the main experiment contract.
- Analysis modules are buffer-driven; prefer the smallest correct module chain
  or `formula` block that solves the task.

## Working Style

- Read the repo first, then the curated reference.
- Keep changes surgical and traceable to the request.
- When a follow-up question depends on phyphox behavior, answer from the
  curated core reference instead of re-scraping the wiki.
