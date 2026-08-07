#!/usr/bin/env python3
"""Validate the B-ES2-C6 JLCPCB upload package and generated release reports."""

from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def split_refs(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> int:
    release = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "hardware/esp-sensor/manufacturing/B-ES2-C6"
    )
    bom = read_csv(release / "JLCPCB/JLCPCB_BOM.csv")
    cpl = read_csv(release / "JLCPCB/JLCPCB_CPL.csv")
    positions = {row["Ref"]: row for row in read_csv(
        release / "IDM-RoomSensor-ESP-B-ES2-C6-positions.csv"
    )}

    bom_refs: set[str] = set()
    for row in bom:
        bom_refs |= split_refs(row["Designator"])
        assert row["JLCPCB Part #"].startswith("C"), row
        assert "TBD" not in ",".join(row.values()).upper(), row
    cpl_refs = {row["Designator"] for row in cpl}
    assert len(bom) == 40, len(bom)
    assert len(cpl) == 54, len(cpl)
    assert bom_refs == cpl_refs, (sorted(bom_refs - cpl_refs), sorted(cpl_refs - bom_refs))

    for row in cpl:
        source = positions[row["Designator"]]
        assert row["Mid X"] == source["PosX"], row
        assert row["Mid Y"] == source["PosY"], row
        assert row["Rotation"] == source["Rot"], row
        assert row["Layer"].lower() == source["Side"].lower(), row

    critical = {row["Designator"]: row["JLCPCB Part #"] for row in bom}
    expected = {
        "U3": "C5445014", "U7": "C5119494", "U4": "C5221601",
        "U1": "C1858393", "J3": "C165948", "J1,J2": "C589905",
    }
    for designator, part in expected.items():
        assert critical[designator] == part, (designator, critical[designator])

    drc_text = (release / "DRC-KICAD10.txt").read_text(encoding="utf-8")
    erc_text = (release / "ERC-KICAD10.txt").read_text(encoding="utf-8")
    assert "Found 0 DRC violations" in drc_text, drc_text[-500:]
    assert "Found 0 unconnected pads" in drc_text, drc_text[-500:]
    assert "Errors 0" in erc_text, erc_text[-500:]

    archive = release / "IDM-RoomSensor-ESP-B-ES2-C6-fabrication.zip"
    with zipfile.ZipFile(archive) as handle:
        names = set(handle.namelist())
    required_suffixes = (".gtl", ".g1", ".g2", ".gbl", ".gts", ".gbs", ".gto", ".gm1", "PTH.drl")
    for suffix in required_suffixes:
        assert any(name.endswith(suffix) for name in names), suffix

    print(f"JLCPCB package valid: {len(bom)} BOM lines, {len(cpl)} placements, {len(names)} fabrication files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
