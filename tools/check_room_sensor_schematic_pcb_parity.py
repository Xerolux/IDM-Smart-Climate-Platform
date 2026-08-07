#!/usr/bin/env python3
"""Compare connected schematic pins with PCB pad nets, ignoring root '/' prefix."""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

import pcbnew


def normalize(net: str) -> str:
    return net.removeprefix("/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    parser.add_argument("xml_netlist", type=Path)
    args = parser.parse_args()

    root = ET.parse(args.xml_netlist).getroot()
    schematic = set()
    for net in root.findall("./nets/net"):
        name = normalize(net.attrib["name"])
        if name.startswith("unconnected-("):
            continue
        for node in net.findall("node"):
            schematic.add((node.attrib["ref"], node.attrib["pin"], name))

    board = pcbnew.LoadBoard(str(args.board))
    pcb = set()
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            if pad.GetNetname():
                pcb.add((footprint.GetReference(), pad.GetNumber(), normalize(pad.GetNetname())))

    missing_pcb = sorted(schematic - pcb)
    missing_schematic = sorted(pcb - schematic)
    assert not missing_pcb, f"schematic-only connected pins: {missing_pcb}"
    assert not missing_schematic, f"PCB-only connected pads: {missing_schematic}"
    print(f"PASS schematic/PCB parity: {len(schematic)} connected ref/pin/net tuples")


if __name__ == "__main__":
    main()
