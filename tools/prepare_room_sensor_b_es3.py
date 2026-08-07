#!/usr/bin/env python3
"""Add deterministic SHT45 escape routing before B-ES3 autorouting."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))
    footprint = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U4")
    targets = {"1": (71.8, 18.8), "2": (71.8, 21.2), "3": (76.2, 21.2), "4": (76.2, 18.8)}

    for pad in footprint.Pads():
        target = point(*targets[pad.GetNumber()])
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pad.GetPosition())
        track.SetEnd(target)
        track.SetLayer(pcbnew.F_Cu)
        track.SetWidth(mm(0.2))
        track.SetNet(pad.GetNet())
        board.Add(track)

        via = pcbnew.PCB_VIA(board)
        via.SetPosition(target)
        via.SetWidth(mm(0.8))
        via.SetDrill(mm(0.4))
        via.SetNet(pad.GetNet())
        board.Add(via)

    pcbnew.SaveBoard(str(args.board), board)
    print("Prepared B-ES3 SHT45 escape routing")


if __name__ == "__main__":
    main()
