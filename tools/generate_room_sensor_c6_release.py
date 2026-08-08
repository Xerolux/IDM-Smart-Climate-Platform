#!/usr/bin/env python3
"""Generate complete B-ES2-C6 engineering BOM and JLCPCB BOM/CPL files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import zipfile


# designators, manufacturer, MPN, description, footprint, LCSC/JLCPCB number
PARTS = [
    ("J1,J2", "TE Connectivity", "1-2834011-4", "4-way 3.5 mm screw terminal", "THT P3.50mm 1x04", "C589905"),
    ("RTH1", "NXP", "KTY81/210,112", "2 kohm silicon temperature sensor", "TO-92 inline", "C481813"),
    ("F1", "Littelfuse", "1812L050/30PR", "500 mA hold 30 V resettable fuse", "1812", "C151168"),
    ("D1", "Zhengxin", "SS16", "1 A 60 V Schottky", "SMA", "C5262487"),
    ("TVS1", "MDD", "SMBJ33A", "33 V 600 W unidirectional TVS", "SMB", "C173526"),
    ("U1", "Texas Instruments", "LMR36510ADDAR", "65 V 1 A synchronous buck", "SOP-8-EP", "C1858393"),
    ("L1", "Bourns", "SRP1038A-330M", "33 uH 3.5 A shielded inductor", "11x10 mm SMD", "C2041318"),
    ("R1,R3", "UNI-ROYAL", "0603WAF1003T5E", "100 kohm 1%", "0603", "C25803"),
    ("R2", "UNI-ROYAL", "0603WAF2492T5E", "24.9 kohm 1%", "0603", "C25962"),
    ("C1", "JLCPCB Assembly", "4.7uF/100V", "4.7 uF 100 V MLCC", "1210", "C9900085220"),
    ("C2", "CCTC", "TCC0805X7R224K101FT", "220 nF 100 V X7R 10%", "0805", "C2994652"),
    ("C3", "Samsung Electro-Mechanics", "CL21B105KBFNNNE", "1 uF 50 V X7R", "0805", "C28323"),
    ("C4,C10,C11,C12,C13", "Murata", "GRM188R71H104KA93D", "100 nF 50 V X7R", "0603", "C77055"),
    ("C5,C6", "Samsung Electro-Mechanics", "CL31A476MPHNNNE", "47 uF 10 V X5R", "1206", "C96123"),
    ("D2,D3", "JSMSEMI", "SS14", "1 A 40 V Schottky power OR diode", "SMA", "C2837270"),
    ("U2", "TECH PUBLIC", "AP2112K-3.3TRG1", "3.3 V 600 mA LDO", "SOT-23-5", "C23380830"),
    ("C7,C16,C18", "Murata", "GRM21BR71A106KE51L", "10 uF 10 V X7R", "0805", "C86038"),
    ("C8", "TDK", "C2012X5R1A226MT0J0E", "22 uF 10 V X5R", "0805", "C361180"),
    ("U3", "Espressif Systems", "ESP32-C6-WROOM-1-N16", "Wi-Fi 6/BLE/Thread module 16 MB flash", "LCC-LGA 18x25.5 mm", "C5445014"),
    ("J3", "Korean Hroparts", "TYPE-C-31-M-12", "USB-C USB2 receptacle", "SMD/THT shield", "C165948"),
    ("ESD1", "TECH PUBLIC", "USBLC6-2SC6", "USB dual-line ESD protection", "SOT-23-6", "C2827654"),
    ("R4,R5", "UNI-ROYAL", "0603WAF5101T5E", "5.1 kohm 1% USB-C CC", "0603", "C23186"),
    ("R6", "UNI-ROYAL", "0603WAF1002T5E", "10 kohm 1%", "0603", "C25804"),
    ("C9", "Samsung Electro-Mechanics", "CL10A105KB8NNNC", "1 uF 50 V X5R", "0603", "C15849"),
    ("SW1,SW2", "Omron", "B3U-1000P", "momentary tactile switch", "SMD", "C231329"),
    ("U4", "Sensirion", "SHT45-AD1B-R2", "temperature and humidity sensor", "DFN-4 1.5x1.5 mm", "C5221601"),
    ("R7,R8", "Yageo", "RC0603FR-074K7L", "4.7 kohm 1%", "0603", "C99782"),
    ("U5", "Microchip", "MCP4725A0T-E/CH", "12-bit I2C DAC", "SOT-23-6", "C144198"),
    ("U6", "Texas Instruments", "OPA197IDBVR", "36 V precision rail-to-rail op amp", "SOT-23-5", "C221351"),
    ("R9", "TyoHM", "RMC060321K1%N", "21 kohm 1%; calibrated gain headroom", "0603", "C269418"),
    ("R10", "Yageo", "RT0603BRD0710KL", "10 kohm 0.1% thin film", "0603", "C95204"),
    ("R11", "Yageo", "RC0603FR-07220RL", "220 ohm 1%", "0603", "C107696"),
    ("U7", "Chipanalog", "CA-IS3092W", "isolated 500 kbps RS-485 with integrated isolated power", "SOIC-16W", "C2890051"),
    ("C14,C17", "Samsung Electro-Mechanics", "CL21B104KBCNNNC", "100 nF 50 V X7R", "0805", "C49678"),
    ("R12", "Yageo", "RC1206FR-07120RL", "120 ohm 1% RS-485 termination", "1206", "C114928"),
    ("J4", "JST", "SM08B-SRSS-TB(LF)(SN)", "8-way 1 mm expansion connector", "SMD right angle", "C160407"),
    ("LED1", "MEIHUA", "MHT192CGCT", "green status LED", "0603", "C389518"),
    ("R13", "Yageo", "RC0603FR-071KL", "1 kohm 1%", "0603", "C21190"),
]

ES3_PARTS = [
    ("SW3", "BIWIN", "SOP01", "user-accessible RS-485 termination switch", "SMD DIP SPST", "C3294660"),
    ("J5,J6,J7", "MAX", "MX205R-5.0-03P-GN01-Cu-A", "3-way push-in spring terminal", "THT P5.00mm 1x03", "C7471335"),
    ("J8", "MAX", "MX205R-5.0-02P-GN01-Cu-A", "2-way push-in spring terminal", "THT P5.00mm 1x02", "C7471334"),
    ("R14", "UNI-ROYAL", "0603WAF1000T5E", "100 ohm 1% 1-Wire series resistor", "0603", "C22775"),
    ("R15", "Yageo", "RC0603FR-074K7L", "4.7 kohm 1% 1-Wire pull-up", "0603", "C99782"),
    ("TVS2,TVS3,TVS4", "TECH PUBLIC", "PCESD3V3D3", "3.3 V field-interface ESD protection", "SOD-323", "C2928727"),
    ("R16,R17,R22,R25", "UNI-ROYAL", "0603WAF1001T5E", "1 kohm 1%", "0603", "C21190"),
    ("R18,R19,R21,R23", "UNI-ROYAL", "0603WAF1002T5E", "10 kohm 1%", "0603", "C25804"),
    ("C19,C20,C21", "Murata", "GRM188R71H104KA93D", "100 nF 50 V X7R", "0603", "C77055"),
    ("TVS5", "ElecSuper", "PESD12VL1BA-ES", "12 V bidirectional 0-10 V input protection", "SOD-323", "C5180221"),
    ("R20", "UNI-ROYAL", "0603WAF3302T5E", "33 kohm 1% 0-10 V divider", "0603", "C4216"),
    ("D4", "IDCHIP", "BAT54S", "dual Schottky ADC rail clamp", "SOT-23", "C2848194"),
    ("SW4", "Omron", "B3U-1000P", "service and identify button", "SMD", "C231329"),
    ("R24", "UNI-ROYAL", "0603WAF1202T5E", "12 kohm 1% 24 V LED resistor", "0603", "C22790"),
    ("LED2,LED3", "MEIHUA", "MHT192CGCT", "green diagnostic LED", "0603", "C389518"),
]

AIR_PARTS = [
    ("U8", "Sensirion", "SCD41-D-R1", "photoacoustic CO2 sensor", "SCD4x 10.1x10.1 mm", "C3659362"),
    ("U9", "Sensirion", "SGP41-D-R4", "VOC and NOx index sensor", "DFN-6 2.4x2.4 mm", "C3659325"),
    ("U10", "Bosch Sensortec", "BMP390", "barometric pressure sensor", "LGA-10 2x2 mm", "C5124834"),
    ("U11", "TECH PUBLIC", "AP2112K-3.3TRG1", "dedicated 3.3 V 600 mA AIR LDO", "SOT-23-5", "C23380830"),
    ("C22,C26,C27", "Murata", "GRM21BR71H104KA01L", "100 nF 50 V X7R", "0805", "C49678"),
    ("C23", "CCTC", "TCC0805X7R475K100FTM", "4.7 uF 10 V X7R", "0805", "C51912533"),
    ("C24,C25", "Samsung Electro-Mechanics", "CL21B105KBFNNNE", "1 uF 50 V X7R", "0805", "C28323"),
    ("C28", "Murata", "GRM21BR71A106KE51L", "10 uF 10 V X7R", "0805", "C86038"),
    ("C29", "TDK", "C2012X5R1A226MT0J0E", "22 uF 10 V X5R", "0805", "C361180"),
    ("R26", "Yageo", "RC0603FR-0710RL", "10 ohm 1% SGP41 VDD filter", "0603", "C109318"),
    ("C30", "KS", "UT1A221M0810VG", "220 uF 10 V USB peak-current reservoir", "SMD D8x10.2 mm", "C963255"),
]

AIR_R2_PARTS = [
    ("Q1,Q2", "Yangzhou Yangjie Electronic Technology", "2N7002", "60 V N-channel MOSFET for LED and relay switching", "SOT-23", "C8545"),
    ("R27,R29", "UNI-ROYAL", "0603WAF1003T5E", "100 kohm gate pull-down", "0603", "C25803"),
    ("R28", "UNI-ROYAL", "0603WAF1000T5E", "100 ohm relay gate resistor", "0603", "C22775"),
    ("D5", "Jiangsu Changjing Electronics Technology", "1N4148WS", "100 V relay-coil flyback diode", "SOD-323", "C2128"),
    ("K1", "Hongfa", "HFD4/5", "5 V DPDT potential-free signal relay; one changeover contact used", "DIP 10x6.5 mm", "C23510"),
    ("J9", "MAX", "MX205R-5.0-03P-GN01-Cu-A", "COM/NO/NC push-in spring terminal", "THT P5.00mm 1x03", "C7471335"),
]

MODULAR_PARTS = [
    ("J9,J10,J11", "CJT", "A2541WV-2x4P", "2x4 2.54 mm vertical AIR-SLOT male header", "THT P2.54mm 2x04", "C225519"),
    ("C30", "KS", "UT1A221M0810VG", "220 uF 10 V AIR-SLOT reservoir", "SMD D8x10.2 mm", "C963255"),
]


def refs(text: str) -> list[str]:
    return [item.strip() for item in text.split(",")]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_archives(release: Path, revision: str) -> None:
    gerbers = release / "gerbers"
    fabrication = release / f"IDM-RoomSensor-ESP-{revision}-fabrication.zip"
    if gerbers.is_dir() and any(gerbers.iterdir()):
        with zipfile.ZipFile(fabrication, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(gerbers.iterdir()):
                if path.is_file():
                    archive.write(path, path.name)

    order = release / f"IDM-RoomSensor-ESP-{revision}-JLCPCB-order-package.zip"
    package_files = [
        fabrication,
        release / "JLCPCB/JLCPCB_BOM.csv",
        release / "JLCPCB/JLCPCB_CPL.csv",
        release / "README.md",
        release / f"{revision}-BOM.csv",
        release / f"IDM-RoomSensor-ESP-{revision}-schematic.pdf",
        release / f"IDM-RoomSensor-ESP-{revision}-top.png",
    ]
    if revision in {"B-ES3-C6", "B-ES4-AIR", "B-ES4-AIR-R2", "B-ES5-MODULAR"}:
        package_files.extend([
            release / "START-HIER-BESTELLUNG.md",
            release / f"{revision}-MECHANIK-BOM.csv",
            release / "RELEASE-VERIFICATION.md",
        ])
    if all(path.is_file() for path in package_files):
        with zipfile.ZipFile(order, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in package_files:
                archive.write(path, path.relative_to(release).as_posix())

    if revision in {"B-ES4-AIR", "B-ES4-AIR-R2", "B-ES5-MODULAR"} and (release / "Gehaeuse").is_dir() and order.is_file():
        complete = release / f"IDM-RoomSensor-{revision}-KOMPLETTPAKET.zip"
        excluded = {complete, release / "DRC.txt"}
        with zipfile.ZipFile(complete, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(release.rglob("*")):
                if path.is_file() and path not in excluded and "gerbers" not in path.parts:
                    archive.write(path, path.relative_to(release).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("positions", type=Path)
    parser.add_argument("release", type=Path)
    parser.add_argument("--revision", choices=("B-ES2-C6", "B-ES3-C6", "B-ES4-AIR", "B-ES4-AIR-R2", "B-ES5-MODULAR"), default="B-ES2-C6")
    args = parser.parse_args()
    with args.positions.open(newline="", encoding="utf-8-sig") as handle:
        positions = {row["Ref"]: row for row in csv.DictReader(handle)}

    parts = list(PARTS)
    if args.revision in {"B-ES3-C6", "B-ES4-AIR", "B-ES4-AIR-R2", "B-ES5-MODULAR"}:
        parts[0] = ("J1,J2", "MAX", "MX205R-5.0-04P-GN01-Cu-A", "4-way push-in spring terminal", "THT P5.00mm 1x04", "C7471336")
        parts.extend(ES3_PARTS)
    if args.revision in {"B-ES4-AIR", "B-ES4-AIR-R2"}:
        parts.extend(AIR_PARTS)
    if args.revision == "B-ES4-AIR-R2":
        parts[2] = ("F1", "BHFUSE", "BSMD1812-050-60V", "500 mA hold 60 V resettable fuse", "1812", "C883142")
        parts.extend(AIR_R2_PARTS)
        # Stock snapshot 2026-08-08: drop-in alternatives selected after a
        # complete JLCPCB BOM review. C5188435 matches the existing 5.00 mm
        # three-pin THT footprint; it uses screws instead of push-in springs.
        r2_overrides = {
            "C1": ("C1", "TDK", "C3225X7S2A475KT003S", "4.7 uF 100 V X7S 10% MLCC", "1210", "C694475"),
            "C2": ("C2", "KEMET", "C0805C224K1RACTU", "220 nF 100 V X7R 10%", "0805", "C2167405"),
            "R9": ("R9", "TA-I Tech", "RMS06FT2102", "21 kohm 1%; calibrated gain headroom", "0603", "C209071"),
            "C14,C17": ("C14,C17", "Walsin", "0805B104K500CT", "100 nF 50 V X7R 10%", "0805", "C83055"),
            "R24": ("R24", "UNI-ROYAL", "0603WAF1802T5E", "18 kohm 1% switchable VIN LED resistor", "0603", "C25810"),
            "TVS5": ("TVS5", "UMW", "PESD12VL1BA", "12 V bidirectional 0-10 V input protection", "SOD-323", "C2687119"),
            "C22,C26,C27": ("C22,C26,C27", "Walsin", "0805B104K500CT", "100 nF 50 V X7R 10%", "0805", "C83055"),
            "C30": ("C30", "Panasonic", "EEEHB1A221AP", "220 uF 10 V USB peak-current reservoir", "SMD D8x10.2 mm", "C401791"),
            "J5,J6,J7": ("J5,J6,J7", "MAX", "MX126-5.0-03P-GN01-Cu-S-A", "3-way screw terminal", "THT P5.00mm 1x03", "C5188435"),
            "J9": ("J9", "MAX", "MX126-5.0-03P-GN01-Cu-S-A", "COM/NO/NC screw terminal", "THT P5.00mm 1x03", "C5188435"),
        }
        parts = [r2_overrides.get(row[0], row) for row in parts]
    if args.revision == "B-ES5-MODULAR":
        parts.extend(MODULAR_PARTS)
    all_refs = [ref for row in parts for ref in refs(row[0])]
    missing = sorted(set(all_refs) - set(positions))
    if missing:
        raise SystemExit(f"Missing placement rows: {missing}")

    full_rows = []
    bom_rows = []
    for designators, maker, mpn, description, footprint, lcsc in parts:
        full_rows.append({
            "Designator": designators,
            "Quantity": str(len(refs(designators))),
            "Manufacturer": maker,
            "Manufacturer Part Number": mpn,
            "Description": description,
            "Footprint": footprint,
            "LCSC Part Number": lcsc,
            "Assembly": "JLCPCB Standard PCBA",
        })
        bom_rows.append({
            "Comment": mpn,
            "Designator": designators,
            "Footprint": footprint,
            "JLCPCB Part #": lcsc,
        })

    cpl_rows = []
    for reference in all_refs:
        row = positions[reference]
        cpl_rows.append({
            "Designator": reference,
            "Mid X": row["PosX"],
            "Mid Y": row["PosY"],
            "Rotation": row["Rot"],
            "Layer": row["Side"].title(),
        })

    write_csv(args.release / f"{args.revision}-BOM.csv",
              ["Designator", "Quantity", "Manufacturer", "Manufacturer Part Number",
               "Description", "Footprint", "LCSC Part Number", "Assembly"], full_rows)
    jlc = args.release / "JLCPCB"
    write_csv(jlc / "JLCPCB_BOM.csv",
              ["Comment", "Designator", "Footprint", "JLCPCB Part #"], bom_rows)
    write_csv(jlc / "JLCPCB_CPL.csv",
              ["Designator", "Mid X", "Mid Y", "Rotation", "Layer"], cpl_rows)
    write_archives(args.release, args.revision)
    print(f"Generated {len(full_rows)} BOM lines and {len(cpl_rows)} placed parts")


if __name__ == "__main__":
    main()
