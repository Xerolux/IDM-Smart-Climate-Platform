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
    ("R2", "UNI-ROYAL", "0603WAF2492T5E", "24.9 kohm 1%", "0603", "C25881"),
    ("C1", "JLCPCB Assembly", "4.7uF/100V", "4.7 uF 100 V MLCC", "1210", "C9900085220"),
    ("C2", "KEMET", "C0805C224J1RECAUTO7210", "220 nF 100 V X7R 5%", "0805", "C2222187"),
    ("C3", "Samsung Electro-Mechanics", "CL21B105KBFNNNE", "1 uF 50 V X7R", "0805", "C28323"),
    ("C4,C10,C11,C12,C13", "Murata", "GRM188R71H104KA93D", "100 nF 50 V X7R", "0603", "C77055"),
    ("C5,C6", "Samsung Electro-Mechanics", "CL31A476MPHNNNE", "47 uF 10 V X5R", "1206", "C96123"),
    ("D2,D3", "JSMSEMI", "SS14", "1 A 40 V Schottky power OR diode", "SMA", "C2837270"),
    ("U2", "TECH PUBLIC", "AP2112K-3.3TRG1", "3.3 V 600 mA LDO", "SOT-23-5", "C23380830"),
    ("C7,C16,C18", "Murata", "GRM21BR71A106KE51L", "10 uF 10 V X7R", "0805", "C86038"),
    ("C8", "TDK", "C2012X7S0J226MT000E", "22 uF 6.3 V X7S", "0805", "C342680"),
    ("U3", "Espressif Systems", "ESP32-C6-WROOM-1-N16", "Wi-Fi 6/BLE/Thread module 16 MB flash", "LCC-LGA 18x25.5 mm", "C5445014"),
    ("J3", "Korean Hroparts", "TYPE-C-31-M-12", "USB-C USB2 receptacle", "SMD/THT shield", "C165948"),
    ("ESD1", "TECH PUBLIC", "USBLC6-2SC6", "USB dual-line ESD protection", "SOT-23-6", "C2827654"),
    ("R4,R5", "UNI-ROYAL", "0603WAF5101T5E", "5.1 kohm 1% USB-C CC", "0603", "C23186"),
    ("R6", "UNI-ROYAL", "0603WAF1002T5E", "10 kohm 1%", "0603", "C25804"),
    ("C9", "Samsung Electro-Mechanics", "CL10A105KB8NNNC", "1 uF 50 V X5R", "0603", "C15849"),
    ("SW1,SW2", "Omron", "B3U-1000P", "momentary tactile switch", "SMD", "C271754"),
    ("U4", "Sensirion", "SHT45-AD1B-R2", "temperature and humidity sensor", "DFN-4 1.5x1.5 mm", "C5221601"),
    ("R7,R8", "Yageo", "RC0603FR-074K7L", "4.7 kohm 1%", "0603", "C99782"),
    ("U5", "Microchip", "MCP4725A0T-E/CH", "12-bit I2C DAC", "SOT-23-6", "C144198"),
    ("U6", "Texas Instruments", "OPA197IDBVR", "36 V precision rail-to-rail op amp", "SOT-23-5", "C221351"),
    ("R9", "KOA Speer", "RN73R1JTTD2102B25", "21 kohm 0.1% thin film; gain headroom", "0603", "C4064934"),
    ("R10", "Yageo", "RT0603BRD0710KL", "10 kohm 0.1% thin film", "0603", "C95204"),
    ("R11", "Yageo", "RC0603FR-07220RL", "220 ohm 1%", "0603", "C107696"),
    ("U7", "Analog Devices", "ADM2587EBRWZ", "isolated 500 kbps RS-485 with isoPower", "SOIC-20W", "C5119494"),
    ("FB1", "Murata", "BLM21PG601SN1D", "600 ohm at 100 MHz ferrite", "0805", "C41556732"),
    ("C14,C17", "Samsung Electro-Mechanics", "CL21B104KBCNNNC", "100 nF 50 V X7R", "0805", "C49678"),
    ("C15", "Fenghua", "0805B103K500NT", "10 nF 50 V X7R", "0805", "C1710"),
    ("R12", "Yageo", "RC1206FR-07120RL", "120 ohm 1% RS-485 termination", "1206", "C17953"),
    ("J4", "JST", "SM08B-SRSS-TB(LF)(SN)", "8-way 1 mm expansion connector", "SMD right angle", "C160407"),
    ("LED1", "Everlight", "19-217/GHC-YR1S2/3T", "green status LED", "0603", "C72043"),
    ("R13", "Yageo", "RC0603FR-071KL", "1 kohm 1%", "0603", "C21190"),
]


def refs(text: str) -> list[str]:
    return [item.strip() for item in text.split(",")]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_archives(release: Path) -> None:
    gerbers = release / "gerbers"
    fabrication = release / "IDM-RoomSensor-ESP-B-ES2-C6-fabrication.zip"
    if gerbers.is_dir() and any(gerbers.iterdir()):
        with zipfile.ZipFile(fabrication, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(gerbers.iterdir()):
                if path.is_file():
                    archive.write(path, path.name)

    order = release / "IDM-RoomSensor-ESP-B-ES2-C6-JLCPCB-order-package.zip"
    package_files = [
        fabrication,
        release / "JLCPCB/JLCPCB_BOM.csv",
        release / "JLCPCB/JLCPCB_CPL.csv",
        release / "README.md",
        release / "B-ES2-C6-BOM.csv",
        release / "IDM-RoomSensor-ESP-B-ES2-C6-schematic.pdf",
    ]
    if all(path.is_file() for path in package_files):
        with zipfile.ZipFile(order, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in package_files:
                archive.write(path, path.relative_to(release).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("positions", type=Path)
    parser.add_argument("release", type=Path)
    args = parser.parse_args()
    with args.positions.open(newline="", encoding="utf-8-sig") as handle:
        positions = {row["Ref"]: row for row in csv.DictReader(handle)}

    all_refs = [ref for row in PARTS for ref in refs(row[0])]
    missing = sorted(set(all_refs) - set(positions))
    if missing:
        raise SystemExit(f"Missing placement rows: {missing}")

    full_rows = []
    bom_rows = []
    for designators, maker, mpn, description, footprint, lcsc in PARTS:
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

    write_csv(args.release / "B-ES2-C6-BOM.csv",
              ["Designator", "Quantity", "Manufacturer", "Manufacturer Part Number",
               "Description", "Footprint", "LCSC Part Number", "Assembly"], full_rows)
    jlc = args.release / "JLCPCB"
    write_csv(jlc / "JLCPCB_BOM.csv",
              ["Comment", "Designator", "Footprint", "JLCPCB Part #"], bom_rows)
    write_csv(jlc / "JLCPCB_CPL.csv",
              ["Designator", "Mid X", "Mid Y", "Rotation", "Layer"], cpl_rows)
    write_archives(args.release)
    print(f"Generated {len(full_rows)} BOM lines and {len(cpl_rows)} placed parts")


if __name__ == "__main__":
    main()
