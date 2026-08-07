# IDM Room Sensor Classic

The orderable PCB revision is **B-ES1**, a bench-test engineering sample using
an ATtiny1616, SHT45, MCP4725 and OPA197. It is powered from the protected 24 V
input and provides a passive KTY81/210 path plus a nominal 0-10 V humidity
output.

## Order files

- PCB source: `IDM-RoomSensor-Classic-B-ES1.kicad_pcb`
- Schematic: `IDM-RoomSensor-Classic-B-ES1.kicad_sch`
- Gerber/drill ZIP: `manufacturing/B-ES1/IDM-RoomSensor-Classic-B-ES1-fabrication.zip`
- Exact BOM: `manufacturing/B-ES1/B-ES1-BOM.csv`

The original Rev-A files are incomplete design-history artifacts and must not
be sent to fabrication.

## Bring-up warning

This PCB is not production-qualified and requires ATtiny1616 firmware through
J2 (UPDI) before it can operate. Use a current-limited 24 V bench supply and a
dummy output load first. Validate and calibrate both interface paths against the
exact IDM model before connecting the board to a heat pump.

IDM terminal assumption: 43 = KTY temperature signal, 42 = +14-32 V DC,
41 = common GND/KTY return and 40 = humidity 0-10 V. This assignment must be
confirmed on the target installation.
