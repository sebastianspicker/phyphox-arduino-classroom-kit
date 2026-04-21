# REPO MAP

## Top-Level

- `README.md`: classroom-facing overview and quickstart
- `CONTRIBUTING.md`, `SECURITY.md`: maintainer policy surface
- `experiments/*.phyphox`: committed importable experiments
- `experiments/phyphox_constants.json`: BLE UUID and mode metadata
- `src/phyphox/*.phyphox.xml`: source XML with XInclude deduplication
- `src/phyphox/includes/*`: shared XML fragments
- `arduino/phyphox_ble_sense/phyphox_ble_sense.ino`: canonical Arduino sketch
- `scripts/`: build, validation, compile, and local CI entrypoints
- `tools/`: XML post-processing and phyphox plausibility validation
- `docs/`: runbook, CI notes, consolidation decisions/findings/log

## Key flows

- Build flow:
  - `scripts/build-phyphox.sh` expands XInclude via `xmllint --xinclude`, post-processes XML, and writes `experiments/*.phyphox`.
- Validation flow:
  - `scripts/validate-xml.sh` validates committed experiments and expanded source output.
  - `tools/validate_phyphox.py` enforces phyphox structure plus UUID alignment with `experiments/phyphox_constants.json` and the Arduino sketch.
- Arduino flow:
  - `scripts/compile-arduino.sh` installs pinned Arduino core/libs and compiles the sketch.
- Local CI flow:
  - `scripts/ci-local.sh` runs `ruff`, `pytest`, XML validation, rebuild freshness, Arduino compile, and the security baseline.

## Hot spots / risks

- XML generation pipeline: `scripts/build-phyphox.sh`, `tools/postprocess_phyphox_xml.py`
- BLE UUID consistency across `experiments/phyphox_constants.json`, XML sources, and Arduino firmware
- Classroom quickstart accuracy after the repo rename and consolidation

## Entrypoints

- `make ci-local`
- `bash scripts/ci-local.sh`
- `bash scripts/validate-xml.sh`
