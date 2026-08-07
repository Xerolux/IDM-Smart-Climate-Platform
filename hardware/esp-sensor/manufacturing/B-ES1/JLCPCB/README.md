# JLCPCB SMT assembly package

This directory is an upload-ready **partial SMT assembly** package for the ESP
B-ES1 engineering sample. It deliberately keeps the electrically critical
design unchanged.

## Upload

1. Upload `../IDM-RoomSensor-ESP-B-ES1-fabrication.zip` as the Gerber archive.
2. Enable PCB assembly, top side, and select Economic or Standard PCBA.
3. Upload `JLCPCB_BOM.csv` as BOM and `JLCPCB_CPL.csv` as CPL/Pick & Place.
4. Confirm exactly 12 placed components at 12 designators.
5. In the placement preview, verify U3 pin 1, U4 pin 1 and U5 pin 1 against the
   board silkscreen/pad-1 marker. Also check that all parts are on the top side.
6. Do not accept an automatic substitute with a different package, voltage,
   tolerance or I2C address.

The LCSC/JLCPCB mappings were checked on 2026-08-07. Stock and assembly support
can change. Reconfirm every match in the order preview before payment.

## JLCPCB-installed components

- U3 SHT45: `C5221601`
- U4 MCP4725A0T-E/CH: `C144198`
- U5 OPA197IDBVR: `C221351`
- R1/R2 4.7 kohm 1%: `C99782`
- R4 10 kohm 0.1%: `C95204` (Yageo equivalent to the Panasonic BOM part)
- R5 220 ohm 1%: `C107696`
- C2/C5/C6 100 nF 50 V X7R: `C77055`
- C3 10 uF 10 V X7R: `C86038`
- C4 100 nF 16 V X7R: `C45000`

## Install after delivery

`HAND_ASSEMBLY.csv` contains C1, D1, R3 and all through-hole parts. C1, D1 and
R3 are intentionally absent from both JLCPCB upload files; do not let the order
system auto-fill them. Test points and mounting hardware are optional.

Before fitting U1 or A1, inspect the board for shorts. After hand assembly,
power the first sample from a current-limited 24 V bench supply and validate the
5 V rail, ESP module supply, DAC output and 0-10 V output into a dummy load.

The obsolete parent-directory `JLCPCB_BOM.csv` and `JLCPCB_CPL.csv` belong to
the incomplete Rev-A placeholder and must never be uploaded for B-ES1.
