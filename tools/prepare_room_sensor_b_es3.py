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
    # Leave the sensor's footprint keepout horizontally, then fan out at 45°.
    # The final vias are far enough apart for 0.2 mm copper clearance.
    elbows = {"1": (71.8, 19.6), "2": (71.8, 20.4), "3": (76.2, 20.4), "4": (76.2, 19.6)}
    targets = {"1": (70.6, 18.4), "2": (70.6, 21.6), "3": (77.4, 21.6), "4": (77.4, 18.4)}

    for pad in footprint.Pads():
        elbow = point(*elbows[pad.GetNumber()])
        target = point(*targets[pad.GetNumber()])
        for start, end in ((pad.GetPosition(), elbow), (elbow, target)):
            track = pcbnew.PCB_TRACK(board)
            track.SetStart(start)
            track.SetEnd(end)
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
