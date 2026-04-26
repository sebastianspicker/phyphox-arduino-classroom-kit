#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$script_dir/lib/common.sh"

repo_root="$(repo_root_from_script "${BASH_SOURCE[0]}")"
cd "$repo_root"

require_cmd arduino-cli "Install it first (see README.md)." || exit 2

arduino-cli core update-index

# Target derived from the supported hardware in these experiments:
# Arduino Nano 33 BLE Sense uses the Arduino Mbed OS Nano Boards platform.
arduino-cli core install arduino:mbed_nano@4.5.0

# Library versions are pinned on purpose for reproducible builds; do not upgrade
# without testing all phyphox experiments.
arduino-cli lib install \
  ArduinoBLE@1.5.0 \
  Arduino_LSM9DS1@1.1.1 \
  Arduino_HTS221@1.0.0 \
  Arduino_LPS22HB@1.0.2 \
  Arduino_APDS9960@1.0.4

arduino-cli compile --fqbn arduino:mbed_nano:nano33ble arduino/phyphox_ble_sense

echo "OK"
