# IDM Room Sensor ESP

The newest manufacturing revision is **B-ES5-MODULAR**, a 130 x 100 mm
four-layer engineering sample. It keeps ESP32-C6-N16, SHT45, USB-C, 24 V,
isolated RS-485, 0-10 V input/output, 1-Wire and contact inputs on the base and
moves CO2, VOC/NOx and pressure onto three universal 25 x 25 mm AIR-SLOT
modules. The symmetric 2x4 connector is electrically safe after 180-degree
rotation and each module has its own 3.3 V regulator.

**B-ES4-AIR-R2 Ultimate** is the all-sensors-fitted revision. It adds a
protected 6-32 VDC input rating, individually switchable LEDs and a
potential-free COM/NO/NC signal relay while retaining USB-C power/programming.
USB and external DC may be connected simultaneously through separate
Schottky OR-ing diodes. **B-ES5-MODULAR** remains intended for product tiers,
later upgrades and field-replaceable sensor modules.

Revision **B-ES2-C6** is the smaller baseline engineering
sample using an ESP32-C6-WROOM-1-N16, native USB-C, SHT45, MCP4725/OPA197
0-10 V output and isolated CA-IS3092W RS-485. It accepts protected 24 V field
power and USB power simultaneously through separate Schottky OR-ing diodes.

Revision **B-ES1** remains the simpler ESP32-C3-DevKitM-1 bench-test version.

## Order files

- B-ES5 complete package: `manufacturing/B-ES5-MODULAR/`
- B-ES5 PCB/schematic: `IDM-RoomSensor-ESP-B-ES5-MODULAR.kicad_pcb` and
  `IDM-RoomSensor-ESP-B-ES5-MODULAR.kicad_sch`
- B-ES5 AIR modules: `modules/`
- B-ES5 printable enclosure: `enclosure/B-ES5-MODULAR-PRINTING.md`
- B-ES4 Ultimate package: `manufacturing/B-ES4-AIR/`
- B-ES4 Ultimate R2 package: `manufacturing/B-ES4-AIR-R2/`
- B-ES3-C6 order instructions: `manufacturing/B-ES3-C6/README.md`
- B-ES3-C6 PCB source: `IDM-RoomSensor-ESP-B-ES3-C6.kicad_pcb`
- B-ES3-C6 schematic: `IDM-RoomSensor-ESP-B-ES3-C6.kicad_sch`
- B-ES3-C6 pin map: `B-ES3-C6-PINMAP.md`
- B-ES3-C6 printable enclosure: `enclosure/B-ES3-C6-PRINTING.md`
- B-ES2-C6 order instructions: `manufacturing/B-ES2-C6/README.md`
- B-ES2-C6 PCB source: `IDM-RoomSensor-ESP-B-ES2-C6.kicad_pcb`
- B-ES2-C6 schematic: `IDM-RoomSensor-ESP-B-ES2-C6.kicad_sch`
- B-ES2-C6 pin map: `B-ES2-C6-PINMAP.md`
- Next-revision hardware requirements: `B-ES3-TODO.md`
- B-ES1 legacy order package: `manufacturing/B-ES1/`

The original Rev-A files are incomplete design-history artifacts and must not
be sent to fabrication.

## Bring-up warning

These PCBs are not production-qualified. Flash and calibrate the ESP32 before
use. Start with a current-limited bench supply and dummy output load. Validate
all interface paths against the exact IDM model before connecting a heat pump.

IDM terminal assumption: 43 = KTY temperature signal, 42 = +14-32 V DC,
41 = common GND/KTY return and 40 = humidity 0-10 V. This assignment must be
confirmed on the target installation.
