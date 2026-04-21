# DECISIONS

## 2026-04-12

### Survivor and public name

- Keep `arduino-phyphox-experiments` as the technical survivor.
- Rename the consolidated project to `phyphox-arduino-classroom-kit`.

### Canonical repo layout

- Keep `src/phyphox/` as the only authoring source.
- Store committed importable artifacts in `experiments/` instead of the repository root.
- Keep BLE constants in `experiments/phyphox_constants.json` as the documentation bridge between XML and firmware.

### Canonical firmware strategy

- Keep `arduino/phyphox_ble_sense/phyphox_ble_sense.ino` as the primary firmware surface.
- Do not import the per-sensor sketch layout as a second first-class architecture.

### Validation strategy

- Use one canonical validator entrypoint: `tools/validate_phyphox.py`.
- Run one documented local CI entrypoint: `scripts/ci-local.sh`.
