#!/usr/bin/env python3
"""Remove DRC-confirmed no-op router vias from B-ES4-AIR."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))

    # Freerouting can insert a via even when both attached tracks remain on
    # F.Cu. KiCad reports these exact vias as dangling; removing them preserves
    # every copper connection and gives the production DRC a clean error pass.
    dangling = {
        (39.1411, 99.9554),
        (92.4275, 45.8631),
        (54.7750, 59.0082),
        (121.1037, 65.9137),
        (119.9126, 71.2624),
    }
    removed = 0
    for item in list(board.GetTracks()):
        if not isinstance(item, pcbnew.PCB_VIA):
            continue
        pos = item.GetPosition()
        xy = (round(pcbnew.ToMM(pos.x), 4), round(pcbnew.ToMM(pos.y), 4))
        if xy in dangling:
            board.RemoveNative(item)
            removed += 1

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.board), board)
    print(f"Finalized B-ES4-AIR routing; removed {removed} no-op vias")


if __name__ == "__main__":
    main()
