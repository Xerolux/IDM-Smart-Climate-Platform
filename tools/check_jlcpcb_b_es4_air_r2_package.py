#!/usr/bin/env python3
"""Validate the B-ES4-AIR-R2 JLCPCB, firmware and enclosure package."""

from __future__ import annotations

import csv
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "hardware" / "esp-sensor" / "manufacturing" / "B-ES4-AIR-R2"


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str):
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> None:
    bom = rows(RELEASE / "JLCPCB/JLCPCB_BOM.csv")
    cpl = rows(RELEASE / "JLCPCB/JLCPCB_CPL.csv")
    positions = {row["Ref"]: row for row in rows(
        RELEASE / "IDM-RoomSensor-ESP-B-ES4-AIR-R2-positions.csv"
    )}
    bom_refs = set()
    for row in bom:
        bom_refs |= refs(row["Designator"])
        assert row["JLCPCB Part #"].startswith("C") and "TBD" not in str(row).upper()
    cpl_refs = {row["Designator"] for row in cpl}
    assert len(bom) == 69, len(bom)
    assert len(cpl) == 102, len(cpl)
    assert bom_refs == cpl_refs == set(positions)
    for row in cpl:
        source = positions[row["Designator"]]
        assert row["Mid X"] == source["PosX"]
        assert row["Mid Y"] == source["PosY"]
        assert row["Rotation"] == source["Rot"]
        assert row["Layer"].lower() == source["Side"].lower()

    part = {row["Designator"]: row["JLCPCB Part #"] for row in bom}
    expected = {
        "C1": "C694475", "C2": "C2167405", "C14,C17": "C83055",
        "C22,C26,C27": "C83055", "C30": "C401791", "R9": "C209071",
        "TVS5": "C2687119", "F1": "C883142", "U3": "C5366877", "U4": "C5221601",
        "U7": "C2890051", "U8": "C3659362", "U9": "C3659325",
        "U10": "C779278", "K1": "C23510", "Q1,Q2": "C8545",
        "D5": "C2128", "J5,J6,J7": "C5188435", "J9": "C5188435",
        "R13,R16,R17,R22,R25": "C21190",
    }
    for designators, number in expected.items():
        assert part[designators] == number, (designators, part[designators])

    drc = (RELEASE / "DRC-KICAD10.txt").read_text(encoding="utf-8")
    erc = (RELEASE / "ERC-KICAD10.txt").read_text(encoding="utf-8")
    assert "Found 0 DRC violations" in drc
    assert "Found 0 unconnected pads" in drc
    assert "Errors 0" in erc

    fabrication = RELEASE / "IDM-RoomSensor-ESP-B-ES4-AIR-R2-fabrication.zip"
    with zipfile.ZipFile(fabrication) as handle:
        names = set(handle.namelist())
    for suffix in ("F_Cu.gbr", "In1_Cu.gbr", "In2_Cu.gbr", "B_Cu.gbr",
                   "F_Mask.gbr", "B_Mask.gbr", "F_Silkscreen.gbr",
                   "Edge_Cuts.gbr", "PTH.drl"):
        assert any(name.endswith(suffix) for name in names), suffix

    complete = RELEASE / "IDM-RoomSensor-B-ES4-AIR-R2-KOMPLETTPAKET.zip"
    with zipfile.ZipFile(complete) as handle:
        complete_names = set(handle.namelist())
    assert not any(name.endswith("Firmware/secrets.yaml") for name in complete_names)
    for suffix in ("_base.stl", "_lid.stl", "_S5-print-plate.stl",
                   "b-es4-air-r2-esphome.yaml", "JLCPCB_BOM.csv", "JLCPCB_CPL.csv"):
        assert any(name.endswith(suffix) for name in complete_names), suffix
    print(f"B-ES4-AIR-R2 package valid: {len(bom)} BOM lines, {len(cpl)} placements, {len(names)} fabrication files")


if __name__ == "__main__":
    main()
