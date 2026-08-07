# B-ES2-C6 – JLCPCB order package

This directory contains the manufacturing release for the 110 x 70 mm,
four-layer IDM room-sensor engineering sample. It is intended for a first
bench-tested prototype run, not for an untested connection to a heat pump.

## Upload to JLCPCB

1. Upload `IDM-RoomSensor-ESP-B-ES2-C6-fabrication.zip` as the PCB file.
2. Select four copper layers, 1.6 mm thickness and 1 oz outer copper.
3. Enable Standard PCBA and top-side assembly.
4. Upload `JLCPCB/JLCPCB_BOM.csv` and `JLCPCB/JLCPCB_CPL.csv`.
5. Include through-hole assembly for J1, J2 and RTH1, or fit those three parts
   by hand if JLCPCB does not offer THT assembly for the selected order route.
6. In the component/placement preview, verify every designator and especially
   the polarity/orientation of D1-D3, TVS1, LED1, U2, U3, U7 and J3.

Part inventory and JLCPCB's assembly classification change continuously. Before
payment, resolve any stock/pre-order prompt. In particular, check KTY81/210
(legacy part), C1 (JLCPCB generic 4.7 uF/100 V), the THT terminals and the
ESP32-C6-N16 module.
Do not silently accept a functional substitute for the ESP32 module, isolated
RS-485 transceiver, KTY sensor or 0-10 V amplifier.

## Power behaviour

USB-C VBUS and the protected 24 V buck output feed `SYS_5V` through separate
Schottky diodes D3 and D2. They may therefore be connected at the same time:
neither source is directly connected to the other. Grounds on the logic/IDM
side are common by design. The RS-485 bus side uses the isolated `RS485_COM`
domain and must not be bridged to logic GND.

USB alone powers programming and the 3.3 V logic. Use 24 V for full functional
operation, particularly the 0-10 V output. The first assembled unit must pass:

- USB only: flash/debug works; no hazardous back-feed appears at the 24 V input.
- Current-limited 24 V only: verify 5 V, 3.3 V and idle current.
- USB and 24 V together: verify stable rails and no reverse current/heating.
- Sweep the humidity DAC into a dummy load and calibrate 0-10 V.
- Validate KTY characteristic and both SHT45 channels against references.
- Exercise isolated RS-485 with termination both open and closed.
- Only then verify terminals 43/42/41/40 against the exact IDM model and wire it.

## Verification status

- KiCad 10 ERC errors: 0 (`ERC-KICAD10.txt`)
- KiCad 10 DRC errors: 0; unconnected items: 0 (`DRC-KICAD10.txt`)
- Schematic/PCB netlist: 200 connected pins matched
- Complete BOM: 40 lines / 54 fitted placements

The `*-all.txt` reports retain non-electrical documentation warnings such as
silkscreen overlap, the embedded custom ESP module footprint, intentional
`GND2` naming on the isolated side and the deliberately open shield net.
