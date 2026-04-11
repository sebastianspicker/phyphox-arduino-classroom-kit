# phyphox BLE sense sketch

This sketch implements a Bluetooth LE peripheral compatible with the `*.phyphox` files in this repo.

## BLE UUIDs

- Service: `cddf0001-30f7-4671-8b43-5e40ba53514a`
- Data characteristic (notify, 20 bytes): `cddf1002-30f7-4671-8b43-5e40ba53514a`
- Config characteristic (read/write, float32 LE): `cddf1003-30f7-4671-8b43-5e40ba53514a`

## Data layout

The data characteristic payload is 5x `float32` little-endian:

- **CH0** (phyphox): time channel with `extra="time"`; maps to the same value as CH1.
- **CH1**: time `t` in seconds since boot (first float, offset 0).
- **CH2..CH5**: mode-dependent values.

## Mode mapping

The app writes a float value to the config characteristic. Rounded to the nearest int:

- `1` acceleration: `x,y,z,|a|`
- `2` gyroscope: `x,y,z,|ω|`
- `3` magnetometer: `x,y,z,|B|`
- `4` pressure: `kPa` (converted to `hPa` in the phyphox experiment)
- `5` temperature/humidity: `°C,%rH`
- `6` light/color: `C,R,G,B` from `Arduino_APDS9960`
- `7`, `8` reserved for future experiments (e.g. combined IMU or other sensors)
- `9` analog inputs: `A0,A1,A2` raw ADC readings (converted to mV in the phyphox experiment)

## Behaviour on failure

If `BLE.begin()` fails in `setup()`, the sketch blocks in an infinite loop with no LED or Serial output. Ensure the board supports BLE and that no other sketch is holding the radio; power-cycle and re-flash if the device does not advertise.
