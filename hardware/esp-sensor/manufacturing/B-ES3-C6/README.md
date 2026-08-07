# B-ES3-C6 – JLCPCB order package

This is the 130 x 80 mm, four-layer engineering-sample release with push-in
field terminals. It adds two parallel 1-Wire terminals, two protected dry
contact inputs, a protected 0-10 V input, user-switchable RS-485 termination,
diagnostic LEDs and a service button.

## Upload to JLCPCB

1. Upload `IDM-RoomSensor-ESP-B-ES3-C6-fabrication.zip` as the PCB file.
2. Select four layers, 1.6 mm thickness and 1 oz outer copper.
3. Enable Standard PCBA, top-side SMT and through-hole/wave assembly.
4. Upload `JLCPCB/JLCPCB_BOM.csv` and `JLCPCB/JLCPCB_CPL.csv`.
5. Verify all orientations and especially U2-U7, D1-D4, TVS1-TVS5, LEDs,
   USB-C, SW3 and every push-in terminal in the placement preview.
6. Do not accept substitutions for the ESP32-C6-N16, SHT45, isolated RS-485
   transceiver, 0-10 V amplifier or field-protection devices without review.

The MAX MX205R push-in terminals are through-hole parts and require JLCPCB's
THT/wave assembly option. Stock is dynamic; resolve every pre-order or sourcing
message before payment.

## Mandatory first-unit validation

- Power from USB only, 24 V only, and both together using a current limit.
- Verify 24 V, 5 V and 3.3 V rails and both diagnostic LEDs.
- Flash and test the service button without affecting boot mode.
- Calibrate and load-test the humidity 0-10 V output.
- Calibrate the protected 0-10 V input at 0 V, 5 V and 10 V.
- Test open/closed states and cable faults on both dry-contact inputs.
- Test one, two and four powered DS18B20 sensors, disconnection and hot-plug.
- Test isolated RS-485 with SW3 termination both off and on.
- Verify every J1 terminal against the exact IDM installation documentation
  before connecting a heat pump.

## Verification status

- KiCad 10 ERC errors: 0 (`ERC-KICAD10.txt`)
- KiCad 10 DRC errors: 0; unconnected items: 0 (`DRC-KICAD10.txt`)
- Schematic/PCB netlist: 252 connected pins matched
- Complete BOM: 53 lines / 80 fitted placements

The `*-all.txt` reports retain documentation-only warnings such as silkscreen
clearance and the embedded custom ESP32-C6 module footprint.
