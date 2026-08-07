# B-ES3-C6 release verification

Verified on 2026-08-07 with KiCad CLI 10.0.5 and CuraEngine 5.11.0.

## PCB and assembly data

- ERC: 0 errors
- DRC: 0 violations
- Unconnected pads: 0
- Footprint errors: 0
- Schematic/PCB parity problems: 0
- JLCPCB BOM: 53 grouped lines
- Fitted components: 80 unique references per PCB
- CPL: all 80 references match a fresh KiCad position export
- Position, rotation and board-side mismatches: 0
- Fabrication archive: 14 valid Gerber/drill/job files
- Assembly side: top

## Enclosure and S5 data

- Base, lid and combined S5 plate: closed manifold meshes
- Combined model: 310 x 100 mm before brim
- UltiMaker S5 build area: 330 x 240 mm
- Prepared slice: AA 0.4, UltiMaker PLA, 0.20 mm, 90 layers
- Support toolpaths: 0
- Estimated material: approximately 154 g
- Tallest checked terminal: 14.4 mm with approximately 2.3 mm roof clearance

## Release scope

The files are released for an initial order of five engineering samples. CAD,
electrical rules, routing, placement data and slicing have been checked. They
do not replace physical bring-up, calibration, thermal testing, EMC/surge
qualification or validation against the exact IDM installation.
