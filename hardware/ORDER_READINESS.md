# PCB order readiness

Audit date: 2026-08-07
Tool: KiCad CLI 10.0.5

## Decision

The three **B-ES1 engineering-sample PCBs** are released for fabrication in the
smallest prototype quantity. Upload only the fabrication ZIP from each B-ES1
directory:

| Board | Fabrication package | BOM | ERC | DRC / unrouted |
|---|---|---|---:|---:|
| Classic room sensor | `classic-sensor/manufacturing/B-ES1/IDM-RoomSensor-Classic-B-ES1-fabrication.zip` | `classic-sensor/manufacturing/B-ES1/B-ES1-BOM.csv` | 0 | 0 / 0 |
| ESP room sensor | `esp-sensor/manufacturing/B-ES1/IDM-RoomSensor-ESP-B-ES1-fabrication.zip` | `esp-sensor/manufacturing/B-ES1/B-ES1-BOM.csv` | 0 | 0 / 0 |
| ESP fake sensor | `fake-sensor/manufacturing/B-ES1/IDM-FakeSensor-ESP-B-ES1-fabrication.zip` | `fake-sensor/manufacturing/B-ES1/B-ES1-BOM.csv` | 0 | 0 / 0 |

Do **not** order the original Rev-A placeholder PCB files. They remain in the
repository only as design-history material and are unrouted/incomplete.

## Scope of the release

These are bench-test engineering samples, not production-qualified hardware.
Assemble and power the first board from a current-limited 24 V bench supply.
Validate the 0-10 V output into a dummy load before connecting any board to an
IDM heat pump.

- The Classic board requires ATtiny1616 firmware through the UPDI header before
  it can operate. Firmware release and functional validation are separate from
  this PCB fabrication release.
- The ESP room-sensor board uses an ESP32-C3-DevKitM-1 and must be flashed and
  calibrated before use.
- The fake-sensor B-ES1 is a humidity-output bench sample. Its TEMP/KTY terminal
  is deliberately DNP and must not be connected.
- The passive KTY81/210 paths on the room-sensor samples must be validated
  against the exact IDM model and configured input before system connection.
  The original NXP `KTY81/210,112` is obsolete; buy only verified old stock or
  qualify a characteristic-compatible replacement before assembly.

## Checks completed

- Native KiCad 10 schematics and matching two-layer PCBs.
- Exact order BOMs with manufacturer part numbers.
- ERC: zero errors and zero warnings on all three designs.
- DRC: zero violations and zero unconnected items on all three designs.
- Schematic-to-PCB pin/net comparison completed.
- Gerber copper, mask, silkscreen, outline, plated/non-plated drill files,
  placement CSV, drill report and board statistics generated from each frozen
  B-ES1 PCB.
- PCB renders visually reviewed.

## Bring-up gates before an IDM connection

1. Confirm the exact IDM heat-pump model, input configuration and terminal
   assignment.
2. Measure the original sensor interface and verify KTY resistance/temperature
   behavior and humidity-output transfer function.
3. Check input current, reverse-polarity protection and regulator rails on a
   current-limited supply.
4. Calibrate and test the 0-10 V output with a dummy load, including startup and
   fault behavior.
5. Record results and only then authorize a real-IDM test.
