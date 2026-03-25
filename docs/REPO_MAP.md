# REPO MAP

## Top-Level
- `README.md`: High-level overview and usage.
- `Makefile`: Convenience targets for validation/build/compile.
- `*.phyphox`: Generated phyphox experiments (importable into the app).
- `src/phyphox/*.phyphox.xml`: Source XML with XInclude for deduplication.
- `src/phyphox/includes/*`: Shared XML fragments (containers + BLE channel mapping).
- `arduino/phyphox_ble_sense/phyphox_ble_sense.ino`: Arduino BLE sketch for Nano 33 BLE Sense.
- `scripts/`: Validation/build/compile scripts.
- `tools/`: Python helpers for XML post-processing and plausibility checks.

## Key Flows
- Build flow:
  - `scripts/build-phyphox.sh` expands XInclude via `xmllint --xinclude`, post-processes XML, and writes `*.phyphox`.
- Validation flow:
  - `scripts/validate-xml.sh` runs `xmllint` on all XML and `.phyphox` files.
  - `tools/phyphox_validate.py` enforces phyphox-specific structural checks.
- Arduino flow:
  - `scripts/compile-arduino.sh` installs Arduino core/libs and compiles the sketch.

## Hot Spots / Risks
- XML generation pipeline (`scripts/build-phyphox.sh`, `tools/postprocess_phyphox_xml.py`).
- Validation logic (`tools/phyphox_validate.py`) defines correctness for phyphox structure.
- BLE UUID consistency across XML sources and Arduino sketch.

## Entrypoints
- `make validate`, `make build`, `make compile`.
- Direct script execution in `scripts/`.
