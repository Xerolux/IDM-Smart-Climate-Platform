# B-ES1 humidity engineering sample

This package is the first electrically complete KiCad 10 engineering sample in
the repository. It is intended for a current-limited **24 V bench supply** and a
dummy high-impedance 0-10 V load.

## Implemented

- fused and reverse-polarity-protected 24 V bench input;
- Traco TSR 1-2450 5 V supply;
- ESP32-C3-DevKitM-1 using GPIO8/GPIO9 for I2C;
- MCP4725 DAC;
- OPA197 non-inverting 3.03 gain stage;
- 220 ohm protected humidity output;
- test points, mounting holes and explicit terminal markings;
- native KiCad 10 schematic with zero ERC violations;
- routed two-layer board with zero DRC violations and zero unconnected pads.

## Deliberately not implemented

J1 pin 1 (IDM terminal 43 / KTY temperature emulation) is electrically
unconnected. Do not bridge or populate this path. The IDM excitation voltage,
current and accepted resistance range still require real measurement.

## Before powering

1. Inspect polarity and shorts without A1, U1, U2 and U3 fitted.
2. Power from a current-limited 24 V bench supply, initially limited to 50 mA.
3. Verify `+5V` and `+3V3` test points before fitting the ICs/module.
4. Verify DAC output into a meter, then the 0-10 V stage into a 100 kohm dummy
   load. Do not connect terminal 40 to the heat pump during this test.
5. Confirm startup, full-scale and fault-state voltage with an oscilloscope.

Passing ERC/DRC proves file consistency and geometry only. It is not electrical,
thermal, EMC or real-IDM validation.
