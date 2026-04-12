# Contributing

This repository is the survivor of the phyphox classroom-kit consolidation. Keep changes aligned with the final scope:

- one canonical Arduino sketch in `arduino/phyphox_ble_sense/`
- source phyphox XML in `src/phyphox/`
- generated importable experiments in `experiments/`

## Before opening a PR

Run the same checks as CI:

```sh
ruff check .
ruff format --check .
pytest
bash scripts/validate-xml.sh
bash scripts/build-phyphox.sh
bash scripts/compile-arduino.sh
bash scripts/secret-scan.sh
bash scripts/deps-scan.sh
bash scripts/sast-minimal.sh
```

Or run the full local entrypoint:

```sh
bash scripts/ci-local.sh
```

## Contribution rules

- Edit `src/phyphox/*.phyphox.xml` and rebuild `experiments/*.phyphox`. Do not hand-edit generated experiments unless you are fixing the generator.
- Keep BLE UUIDs aligned between `experiments/phyphox_constants.json`, `src/phyphox/*.phyphox.xml`, and `arduino/phyphox_ble_sense/phyphox_ble_sense.ino`.
- Keep the single mode-switched sketch as the primary teaching path. Add secondary Arduino examples only if there is a clear classroom need.
- Keep docs focused on classroom use with exoplanet transit work treated as one example, not the repo boundary.
