#!/usr/bin/env python3
"""Validate the ESP B-ES1 JLCPCB BOM/CPL against KiCad placement output."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "hardware/esp-sensor/manufacturing/B-ES1"
JLC = RELEASE / "JLCPCB"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def split_designators(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    source_rows = read_csv(RELEASE / "IDM-RoomSensor-ESP-B-ES1-positions.csv")
    source = {row["Ref"]: row for row in source_rows}
    bom_rows = read_csv(JLC / "JLCPCB_BOM.csv")
    cpl_rows = read_csv(JLC / "JLCPCB_CPL.csv")
    hand_rows = read_csv(JLC / "HAND_ASSEMBLY.csv")

    assert bom_rows and cpl_rows and hand_rows
    assert all(row["JLCPCB Part #"].startswith("C") for row in bom_rows)

    bom_refs = {
        ref
        for row in bom_rows
        for ref in split_designators(row["Designator"])
    }
    cpl_refs = {row["Designator"] for row in cpl_rows}
    assert bom_refs == cpl_refs, ("BOM/CPL mismatch", bom_refs ^ cpl_refs)
    assert len(cpl_refs) == 12

    for row in cpl_rows:
        ref = row["Designator"]
        original = source[ref]
        assert row["Mid X"] == original["PosX"]
        assert row["Mid Y"] == original["PosY"]
        assert row["Rotation"] == original["Rot"]
        assert row["Layer"].lower() == original["Side"].lower() == "top"

    hand_refs = {row["Designator"] for row in hand_rows}
    assert {"C1", "D1", "R3", "J1", "U1", "A1", "RTH1"} <= hand_refs
    assert not (bom_refs & hand_refs)
    print("JLCPCB package OK: 12 SMT designators; BOM/CPL coordinates match KiCad")


if __name__ == "__main__":
    main()
