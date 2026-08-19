# Legacy / prototype hardware archive

This directory preserves historical IDM Smart Climate hardware packages that were recovered on 2026-08-19. They are kept so the older board families, manufacturing files and PoE variants remain publicly traceable.

## Included board families

### B-SS2
- `Climate-Sensor-B-SS2-JLCPCB-PCB`: socket/carrier PCB Gerber + drill package.
- `Climate-Sensor-B-SS2-NET-JLCPCB-PCB`: Ethernet/PoE companion board Gerber + drill package.
- The recovered B-SS2-NET BOM uses the Wuerth Elektronik `7499210124A` PoE MagJack, Silvertel `Ag97005-FL` and WIZnet `W5500-io`.

### B-SU1 universal board
- PCB size: **220 x 130 mm**.
- Two preserved variants: **B-SU1-MIT-POE** and **B-SU1-OHNE-POE**.
- The package contains KiCad sources, schematics, Gerbers, JLCPCB BOM/CPL files, ESPHome examples, enclosure STL files, assembly/order docs and test plans.
- PoE option: Silvertel `Ag97005-FL`, WIZnet `W5500-io` and Wuerth `7499210124A` MagJack.
- **F1 on B-SU1:** `0.5 A resettable fuse`, rated at least `30 V`, radial THT. This value belongs to the B-SU1 BOM and must not be copied to another PCB revision unless its own BOM/schematic confirms it.

### B-ES3-C6
- Mechanical BOM.
- PCB top render.
- S5 print-plate STL.
- The normal B-ES3-C6 design/manufacturing files already live under `hardware/esp-sensor/`; this archive only preserves the recovered supplemental files together with the older board families.

## Complete recovered bundle

`IDM-Smart-Climate-Legacy-Hardware-2026-08-19.tar.xz`

The archive contains **162 files** and preserves all recovered package contents, including both B-SU1 variants, both B-SS2 Gerber sets, B-SU1 source/manufacturing data and the B-ES3-C6 mechanical/print files.

SHA-256:

```text
50ae5f7277f6cc2bf77c8e90fe586cbe4b3c3396ce5bd7abd89d14250e7a45b1  IDM-Smart-Climate-Legacy-Hardware-2026-08-19.tar.xz
```

`SOURCE_SHA256.txt` records the hashes of the original recovered upload files. `CONTENTS.txt` lists every file inside the consolidated archive.

## Status

These are **legacy/reference and engineering-sample files**, not an instruction to replace the newer supported ESP room-sensor revisions. Keep board-specific BOMs, Gerbers and assembly instructions together; do not mix parts between B-SS2, B-SU1, B-ES3-C6 and newer B-ES4/B-ES5 revisions without schematic verification.
