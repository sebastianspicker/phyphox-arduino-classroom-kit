# FINDINGS

## Consolidation ledger

Date: 2026-04-12

### Which files are byte-identical duplicates

- `LICENSE`
- `.github/dependabot.yml`
- `tests/__init__.py`

These were not the deciding surfaces for the merge.

### Which files are conceptual duplicates with different implementation

- Generated experiments exist in both repos under the same filenames, but the files are not byte-identical.
- Both repos validate phyphox XML, but one uses `tools/phyphox_validate.py` plus a source build pipeline and the other uses `tools/validate_phyphox.py` with constants-based UUID checks.
- Both repos compile Arduino code, but one uses a single mode-switched sketch and the other uses one sketch per sensor.

### Which repo had the stronger subsystem

- phyphox authoring pipeline: `arduino-phyphox-experiments`
- classroom onboarding and contributor policy surface: `smartphone-based-exoplanet-detection`
- canonical firmware maintenance surface: `arduino-phyphox-experiments`

### Canonical choices applied here

- survivor repo name: `phyphox-arduino-classroom-kit`
- generated outputs move to `experiments/`
- single Arduino sketch remains canonical
- contributor/security/runbook surfaces imported into the survivor repo
