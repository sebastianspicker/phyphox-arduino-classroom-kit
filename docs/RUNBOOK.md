# RUNBOOK

Commands are written for the repository root.

## Scope

This repository packages a classroom-ready Arduino Nano 33 BLE Sense plus phyphox workflow:

- author phyphox experiments in `src/phyphox/`
- commit generated importable files in `experiments/`
- compile one canonical Arduino sketch in `arduino/phyphox_ble_sense/`

## Prereqs

- Python 3.11+
- `xmllint` from libxml2
- `arduino-cli`
- `ruff` and `pytest` from `requirements-test.txt`

Arduino compile target:

- FQBN: `arduino:mbed_nano:nano33ble`

Pinned Arduino packages:

- Core: `arduino:mbed_nano@4.5.0`
- `ArduinoBLE@1.5.0`
- `Arduino_LSM9DS1@1.1.1`
- `Arduino_HTS221@1.0.0`
- `Arduino_LPS22HB@1.0.2`
- `Arduino_APDS9960@1.0.4`

## Setup

```sh
python3 -m pip install -r requirements-test.txt
```

Install system dependencies separately:

- macOS: `brew install libxml2 arduino-cli`
- Debian/Ubuntu: `apt install libxml2-utils` plus an `arduino-cli` install path

## Fast loop

```sh
ruff check .
pytest
bash scripts/validate-xml.sh
```

## Full loop

```sh
bash scripts/ci-local.sh
```

## Manual classroom probe

1. Flash `arduino/phyphox_ble_sense/phyphox_ble_sense.ino`.
2. Import one file from `experiments/` into phyphox on a phone.
3. Start the experiment and confirm that `phyphox-sense` connects and streams values.
4. Change to a different experiment and confirm the mode switch changes the sensor payload.

## Troubleshooting

- `xmllint not found`: install libxml2 and retry.
- `ruff` or `pytest` missing: install `requirements-test.txt`.
- `arduino-cli` failures: ensure the pinned core and libraries can be installed.
- No BLE data after flashing: power-cycle the board and confirm the phone is not already paired to another session.
