# B-ES5-MODULAR – JLCPCB engineering-sample package

This is the modular 130 x 100 mm, four-layer Xerolux room/air sensor. The base
contains ESP32-C6-N16, SHT45 temperature/humidity, USB-C, protected 24 V input,
isolated RS-485, calibrated 0-10 V output, protected 0-10 V input, two parallel
1-Wire push-in terminals and two dry-contact inputs. Three universal AIR-SLOT
headers accept the separately orderable CO2, VOC/NOx and pressure modules.

## What to order

1. Order the base board with the files in this directory.
2. Order only the desired module directories under `Modules/`.
3. For an Ultimate set, order all three module types in the same quantity as
   the base board.
4. Print the base and lid in `Gehaeuse/`.

The base is the economical standard sensor even when no AIR module is fitted:
temperature/humidity and all field interfaces remain available. Fully fitting
all modules costs more than B-ES4-AIR because four PCBs and four assembly jobs
are involved; modularity pays for itself when many bases omit one or more
expensive sensors or when field replacement matters.

## Verified CAD status

- KiCad 10 base ERC/DRC: 0 errors, 0 unconnected pads
- AIR-CO2, AIR-VOCNOX and AIR-PRESSURE: 0 ERC/DRC errors each
- schematic/PCB parity: base 278, modules 25/31/29 connected tuples
- base size 130 x 100 mm; each module 25 x 25 mm
- symmetric rotation-safe 5 V/GND/I2C connector, local module LDOs
- enclosure outside size 150 x 120 mm, within the requested 150 x 150 mm

This is an engineering-sample release. Build five first articles and complete
`RELEASE-VERIFICATION.md` before connecting to HVAC equipment or ordering a
production quantity.

