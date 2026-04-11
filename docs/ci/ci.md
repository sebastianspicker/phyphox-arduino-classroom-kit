# CI Overview

This repository uses a single workflow (`.github/workflows/ci.yml`) to validate XML/phyphox files, compile the Arduino sketch, and run a minimal security baseline.

## Workflows & Triggers
- `ci`:
  - `push`
  - `pull_request`
  - `workflow_dispatch`

## Jobs
- **XML + phyphox validation**
  - Installs `xmllint`
  - Validates all `*.phyphox` and `*.xml`
  - Rebuilds `*.phyphox` from `src/phyphox/*.phyphox.xml`
  - Fails if generated files are out of date
- **Arduino compile**
  - Installs pinned Arduino CLI
  - Restores cache for Arduino core + libraries
  - Compiles the sketch for `arduino:mbed_nano:nano33ble`
- **Security baseline**
  - Secret scan (tight patterns)
  - Dependency pin check for Arduino core/libs
  - Minimal SAST (bash + python syntax)

## Local Reproduction
The Makefile mirrors CI steps.

```sh
make validate
make build
make compile
make security
```

Or run the full CI sequence:

```sh
make ci
```

## Dependencies
- `bash`
- `python3`
- `xmllint` (libxml2)
- `arduino-cli` (for `make compile` only)

Note: the compile step downloads Arduino core and library indexes, so it needs outbound network access.

## Caching
The CI caches Arduino CLI data and libraries:
- `~/.arduino15`
- `~/Arduino/libraries`
- `~/.cache/arduino`

This speeds up repeated runs and keeps the compile job stable.

## Secrets & Permissions
- No secrets are required.
- `GITHUB_TOKEN` is read-only (`contents: read`) with cache access.

## Extending CI
- Add a new script in `scripts/` and wire it into the Makefile.
- Add a job or step in `.github/workflows/ci.yml` with a clear name and timeout.
- Prefer pinned versions for tools and dependencies.

## Releasing
To publish a release, tag a version (e.g. `v1.2.0`) and create a GitHub Release. Optionally attach `phyphox-experiments.zip` from `make bundle` so users can download all experiments in one file.

## Optional: act
If you use `act` locally, prefer `make ci` for parity and keep runtime images minimal. Avoid adding secrets to local runs unless required by new jobs.
