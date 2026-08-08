#!/usr/bin/env python3
"""Copy generated R2 enclosure deliverables into the manufacturing release."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "hardware" / "esp-sensor" / "enclosure"
RELEASE = ROOT / "hardware" / "esp-sensor" / "manufacturing" / "B-ES4-AIR-R2"
TARGET = RELEASE / "Gehaeuse"

FILES = (
    "B-ES4-AIR-R2-PRINTING.md",
    "Xerolux-B-ES4-AIR-R2-S5-AA04-PLA.inst.cfg",
    "idm-roomsensor-b-es4-air-r2-enclosure.scad",
    "idm-roomsensor-b-es4-air-enclosure.scad",
    "idm-roomsensor-b-es4-air-r2-preview.png",
    "idm-roomsensor-b-es4-air-r2_base.stl",
    "idm-roomsensor-b-es4-air-r2_lid.stl",
    "idm-roomsensor-b-es4-air-r2_S5-print-plate.stl",
)


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        source = SOURCE / filename
        if not source.is_file():
            raise SystemExit(f"Missing enclosure artifact: {source}")
        shutil.copy2(source, TARGET / filename)
    print(f"Prepared {len(FILES)} B-ES4-AIR-R2 enclosure files")


if __name__ == "__main__":
    main()
