#!/usr/bin/env python3
"""Validate the B-ES4-AIR JLCPCB and enclosure package."""

from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> int:
    release = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "hardware/esp-sensor/manufacturing/B-ES4-AIR"
    )
    bom = rows(release / "JLCPCB/JLCPCB_BOM.csv")
    cpl = rows(release / "JLCPCB/JLCPCB_CPL.csv")
    positions = {row["Ref"]: row for row in rows(
        release / "IDM-RoomSensor-ESP-B-ES4-AIR-positions.csv"
    )}
    bom_refs: set[str] = set()
    for row in bom:
        bom_refs |= refs(row["Designator"])
        assert row["JLCPCB Part #"].startswith("C"), row
        assert "TBD" not in ",".join(row.values()).upper(), row
    cpl_refs = {row["Designator"] for row in cpl}
    assert len(bom) == 64, len(bom)
    assert len(cpl) == 94, len(cpl)
    assert bom_refs == cpl_refs
    for row in cpl:
        source = positions[row["Designator"]]
        assert row["Mid X"] == source["PosX"]
        assert row["Mid Y"] == source["PosY"]
        assert row["Rotation"] == source["Rot"]
        assert row["Layer"].lower() == source["Side"].lower()

    critical = {row["Designator"]: row["JLCPCB Part #"] for row in bom}
    expected = {
        "U3": "C5445014", "U4": "C5221601", "U7": "C2890051",
        "U8": "C3659362", "U9": "C3659325", "U10": "C5124834",
        "U11": "C23380830", "C30": "C963255",
        "J1,J2": "C7471336", "J5,J6,J7": "C7471335", "J8": "C7471334",
    }
    for designators, part in expected.items():
        assert critical[designators] == part, (designators, critical[designators])

    drc = (release / "DRC-KICAD10.txt").read_text(encoding="utf-8")
    erc = (release / "ERC-KICAD10.txt").read_text(encoding="utf-8")
    assert "Found 0 DRC violations" in drc
    assert "Found 0 unconnected pads" in drc
    assert "Errors 0" in erc

    fabrication = release / "IDM-RoomSensor-ESP-B-ES4-AIR-fabrication.zip"
    with zipfile.ZipFile(fabrication) as handle:
        names = set(handle.namelist())
    required = ("F_Cu.gbr", "In1_Cu.gbr", "In2_Cu.gbr", "B_Cu.gbr",
                "F_Mask.gbr", "B_Mask.gbr", "F_Silkscreen.gbr",
                "Edge_Cuts.gbr", "PTH.drl")
    for suffix in required:
        assert any(name.endswith(suffix) for name in names), suffix
    for mesh in ("base.stl", "lid.stl", "S5-print-plate.stl"):
        assert any(path.name.endswith(mesh) for path in (release / "Gehaeuse").iterdir()), mesh
    assert (release / "IDM-RoomSensor-B-ES4-AIR-KOMPLETTPAKET.zip").is_file()
    print(f"B-ES4-AIR package valid: {len(bom)} BOM lines, {len(cpl)} placements, {len(names)} fabrication files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
