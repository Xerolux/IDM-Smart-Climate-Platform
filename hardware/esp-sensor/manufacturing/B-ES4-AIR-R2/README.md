# B-ES4-AIR-R2 Ultimate – JLCPCB order package

This 130 x 100 mm four-layer engineering-sample revision retains the complete
Ultimate Air sensor set and adds a protected 6-32 VDC input rating, three
individually controllable LEDs and one GPIO-controlled potential-free COM/NO/NC
signal relay output. USB-C provides power and native programming; the DC and
USB supplies are diode-OR isolated and may be connected simultaneously.

At 0 V the unit is off. Full 0-10 V output operation requires adequate external
DC headroom and must be calibrated on the first article. The relay is intended
for SELV/signalling loads only, not uncertified mains switching.

## JLCPCB upload

1. Upload `IDM-RoomSensor-ESP-B-ES4-AIR-R2-fabrication.zip`.
2. Select 4 layers, 1.6 mm FR-4, 1 oz outer copper and quantity 5.
3. Select Standard PCBA, top SMT and THT/wave soldering.
4. Upload `JLCPCB/JLCPCB_BOM.csv` and `JLCPCB/JLCPCB_CPL.csv`.
5. Verify every placement and all polarized parts, especially U1-U11, K1,
   Q1/Q2, D1-D5, TVS1-TVS5, LEDs, C30, USB-C and switches.
6. Do not accept automatic substitutions for sensors, power/protection,
   isolation, relay or connector parts without engineering review.

The BOM contains the verified drop-in stock alternatives selected on
2026-08-08 for C1, C2, C14/C17, C22/C26/C27, C30, R9 and TVS5. Stock remains
dynamic. U3 uses the stocked ESP32-C6-WROOM-1-N8 (C5366877); its 8 MB flash is
sufficient for the planned firmware. U10 uses the stocked BMP388 (C779278),
which is pin-compatible with BMP390 and supported by the same ESPHome bmp3xx
driver. J5/J6/J7/J9 use C5188435, a footprint-compatible 5.00 mm
three-way screw terminal. C7471335 is not a valid selectable part.
R13/R16/R17/R22/R25 are intentionally combined into one C21190 BOM row so
JLCPCB calculates the required quantity instead of flagging a duplicate match.

The field terminals and K1 are THT parts. Stock, sourcing and wave-solder charges
must be confirmed in the JLCPCB viewer immediately before payment.

## Verified release status

- KiCad 10 ERC: 0 errors
- KiCad 10 PCB DRC: 0 errors and 0 unconnected pads
- schematic/PCB parity: 324 connected reference/pin/net tuples
- 70 BOM lines and 102 fitted placements
- ESPHome 2026.7.4 configuration valid
- three manifold enclosure STLs; 310 x 120 mm S5 plate plus 5 mm brim fits
  the 330 x 240 mm build area

This is an engineering sample, not a production-qualified or mains-certified
product. Build five first articles and complete `RELEASE-VERIFICATION.md`.
