#!/usr/bin/env python3
"""Apply deterministic post-router cleanup to B-ES3."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def add_text(board, value: str, x: float, y: float, size: float = 0.55) -> None:
    if any(item.GetText() == value for item in board.GetDrawings() if isinstance(item, pcbnew.PCB_TEXT)):
        return
    item = pcbnew.PCB_TEXT(board)
    item.SetText(value)
    item.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    item.SetLayer(pcbnew.F_SilkS)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(0.12))
    board.Add(item)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))

    # Keep the upper mounting hole clear of the enlarged push-in RS-485 block.
    hole = next(fp for fp in board.GetFootprints() if fp.GetReference() == "H2")
    hole.SetPosition(pcbnew.VECTOR2I(mm(115), mm(35)))

    # Freerouting sometimes leaves a via where both connected segments are on
    # F.Cu. Removing these DRC-confirmed no-op vias does not alter connectivity.
    dangling = {(117.4037, 61.8812), (53.0043, 62.8674),
                (52.9773, 67.1033), (89.6654, 47.0292)}
    for item in list(board.GetTracks()):
        if not isinstance(item, pcbnew.PCB_VIA):
            continue
        pos = item.GetPosition()
        xy = (round(pcbnew.ToMM(pos.x), 4), round(pcbnew.ToMM(pos.y), 4))
        if xy in dangling:
            board.RemoveNative(item)

    for value, x, y in (
        ("1W-A: 3V DQ GND", 84, 22.5), ("1W-B: 3V DQ GND", 104, 22.5),
        ("DI1 COM DI2", 126, 22.5), ("A B COM SH", 128, 61),
        ("0-10V IN | GND", 127, 84), ("SERVICE", 108, 80.5), ("TERM", 122, 69),
    ):
        add_text(board, value, x, y)

    for item in board.GetDrawings():
        if not isinstance(item, pcbnew.PCB_TEXT):
            continue
        positions = {
            "SMART CLIMATE SENSOR": (35, 20),
            "by Xerolux | xerolux.de | REV B-ES3-C6 | 2026": (35, 22.5),
            "USB-C FLASH / POWER": (75, 82),
            "43 TEMP | 42 +24V | 41 GND | 40 RH": (40, 84),
            "RS485 ISOLATED": (130, 68),
            "SERVICE": (108, 80.5),
        }
        if item.GetText() in positions:
            item.SetPosition(pcbnew.VECTOR2I(*(mm(value) for value in positions[item.GetText()])))

    pcbnew.SaveBoard(str(args.board), board)
    print("Finalized B-ES3 routing")


if __name__ == "__main__":
    main()
