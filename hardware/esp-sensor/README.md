# IDM Room Sensor ESP

The newest manufacturing revision is **B-ES2-C6**, a four-layer engineering
sample using an ESP32-C6-WROOM-1-N16, native USB-C, SHT45, MCP4725/OPA197
0-10 V output and isolated ADM2587E RS-485. It accepts protected 24 V field
power and USB power simultaneously through separate Schottky OR-ing diodes.

Revision **B-ES1** remains the simpler ESP32-C3-DevKitM-1 bench-test version.

## Order files

- B-ES2-C6 order instructions: `manufacturing/B-ES2-C6/README.md`
- B-ES2-C6 PCB source: `IDM-RoomSensor-ESP-B-ES2-C6.kicad_pcb`
- B-ES2-C6 schematic: `IDM-RoomSensor-ESP-B-ES2-C6.kicad_sch`
- B-ES2-C6 pin map: `B-ES2-C6-PINMAP.md`
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
