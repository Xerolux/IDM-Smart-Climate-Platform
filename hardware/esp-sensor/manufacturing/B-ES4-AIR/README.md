# B-ES4-AIR Ultimate – JLCPCB order package

This is the 130 x 100 mm, four-layer engineering-sample release. It combines
SHT45 temperature/humidity, SCD41 CO2, SGP41 VOC/NOx and BMP390 pressure with
ESP32-C6-N16, USB-C, 24-V input, isolated RS-485, calibrated 0-10-V output,
protected 0-10-V input, two parallel 1-Wire terminals and two dry contacts.

## JLCPCB upload

1. Upload `IDM-RoomSensor-ESP-B-ES4-AIR-fabrication.zip` as the PCB file.
2. Select 4 layers, 1.6 mm FR-4, 1 oz outer copper and quantity 5.
3. Enable Standard PCBA, top-side SMT and THT/wave soldering.
4. Upload `JLCPCB/JLCPCB_BOM.csv` and `JLCPCB/JLCPCB_CPL.csv`.
5. Inspect every red placement marker. Check polarity/orientation particularly
   for U1-U11, D1-D4, TVS1-TVS5, LED1-LED3, C30, J3 and all switches.
6. Do not accept automatic substitutions for U3/U4/U7-U11 or protection and
   power components without review.

The MAX MX205R push-in terminals are THT parts and require the wave-soldering
option. Stock, sourcing and Extended-part charges are dynamic and must be
confirmed in the JLCPCB viewer immediately before payment.

## Verified CAD status

- KiCad 10 ERC: 0 errors
- KiCad 10 PCB DRC: 0 errors, 0 unconnected pads
- schematic/PCB parity: 300 connected reference/pin/net tuples
- extended DRC: only 53 silkscreen/text warnings, retained in
  `DRC-KICAD10-all.txt`
- 64 BOM lines and 94 fitted placements
- three manifold enclosure STLs; 310 x 120 mm S5 plate plus 5 mm brim fits
  the 330 x 240 mm build area
- ESPHome commissioning configuration validated with ESPHome 2026.7.4

This is an engineering-sample release, not a field-certified product. Build
five first articles and complete `RELEASE-VERIFICATION.md` before connection
to HVAC equipment or ordering a larger batch.
