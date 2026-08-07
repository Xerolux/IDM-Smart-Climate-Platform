#!/usr/bin/env python3
"""Add split logic and isolated-bus reference planes to B-ES2-C6."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_zone(board, net_name: str, coordinates: tuple[tuple[float, float], ...]) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.In2_Cu)
    zone.SetNet(board.FindNet(net_name))
    zone.SetLocalClearance(mm(0.25))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetMinThickness(mm(0.2))
    zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in coordinates:
        outline.Append(point(x, y))
    board.Add(zone)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))
    extended = pcbnew.ToMM(board.GetBoardEdgesBoundingBox().GetWidth()) > 120
    air = pcbnew.ToMM(board.GetBoardEdgesBoundingBox().GetHeight()) > 90

    # Idempotent when rerun on the released board.
    for zone in list(board.Zones()):
        if not zone.GetIsRuleArea():
            board.RemoveNative(zone)

    # Logic ground covers the board except the isolated RS-485 region.  It may
    # extend to the SHT45 at the upper-right without entering the bus island.
    logic_outline = (
        ((10.5, 10.5), (139.5, 10.5), (139.5, 34.0), (103.5, 34.0),
         (103.5, 70.0), (139.5, 70.0), (139.5, 109.5), (50.0, 109.5),
         (50.0, 89.5), (20.0, 89.5), (20.0, 109.5), (10.5, 109.5))
        if air else
        ((10.5, 10.5), (139.5, 10.5), (139.5, 34.0), (103.5, 34.0),
         (103.5, 70.0), (139.5, 70.0), (139.5, 89.5), (10.5, 89.5))
        if extended else
        ((10.5, 10.5), (119.5, 10.5), (119.5, 34.0),
         (103.5, 34.0), (103.5, 79.5), (10.5, 79.5))
    )
    add_zone(board, "GND", logic_outline)
    add_zone(
        board,
        "RS485_COM",
        ((106.5, 35.0), (139.5 if extended else 119.5, 35.0),
         (139.5 if extended else 119.5, 70.0), (106.5, 70.0)),
    )
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.board), board)
    print("Added split C6 reference planes")


if __name__ == "__main__":
    main()
