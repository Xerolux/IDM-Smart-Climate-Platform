#!/usr/bin/env python3
"""Validate the B-ES3-C6 JLCPCB upload package."""

from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(text: str) -> set[str]:
    return {item.strip() for item in text.split(",") if item.strip()}


def main() -> int:
    release = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "hardware/esp-sensor/manufacturing/B-ES3-C6"
    )
    bom = rows(release / "JLCPCB/JLCPCB_BOM.csv")
    cpl = rows(release / "JLCPCB/JLCPCB_CPL.csv")
    positions = {row["Ref"]: row for row in rows(
        release / "IDM-RoomSensor-ESP-B-ES3-C6-positions.csv"
    )}

    bom_refs: set[str] = set()
    for row in bom:
        bom_refs |= refs(row["Designator"])
        assert row["JLCPCB Part #"].startswith("C"), row
        assert "TBD" not in ",".join(row.values()).upper(), row
    cpl_refs = {row["Designator"] for row in cpl}
    assert len(bom) == 53, len(bom)
    assert len(cpl) == 80, len(cpl)
    assert bom_refs == cpl_refs, (sorted(bom_refs - cpl_refs), sorted(cpl_refs - bom_refs))

    for row in cpl:
        source = positions[row["Designator"]]
        assert row["Mid X"] == source["PosX"]
        assert row["Mid Y"] == source["PosY"]
        assert row["Rotation"] == source["Rot"]
        assert row["Layer"].lower() == source["Side"].lower()

    critical = {row["Designator"]: row["JLCPCB Part #"] for row in bom}
    expected = {
        "U3": "C5445014", "U4": "C5221601", "U7": "C2890051",
        "J1,J2": "C7471336", "J5,J6,J7": "C7471335", "J8": "C7471334",
        "SW3": "C3294660", "TVS2,TVS3,TVS4": "C2928727",
        "TVS5": "C5180221", "D4": "C2848194",
    }
    for designators, part in expected.items():
        assert critical[designators] == part, (designators, critical[designators])

    drc = (release / "DRC-KICAD10.txt").read_text(encoding="utf-8")
    erc = (release / "ERC-KICAD10.txt").read_text(encoding="utf-8")
    assert "Found 0 DRC violations" in drc
    assert "Found 0 unconnected pads" in drc
    assert "Errors 0" in erc

    archive = release / "IDM-RoomSensor-ESP-B-ES3-C6-fabrication.zip"
    with zipfile.ZipFile(archive) as handle:
        names = set(handle.namelist())
    for suffix in (".gtl", ".g1", ".g2", ".gbl", ".gts", ".gbs", ".gto", ".gm1", "PTH.drl"):
        assert any(name.endswith(suffix) for name in names), suffix

    print(f"B-ES3-C6 package valid: {len(bom)} BOM lines, {len(cpl)} placements, {len(names)} fabrication files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
