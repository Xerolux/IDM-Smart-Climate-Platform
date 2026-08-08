#!/usr/bin/env python3
"""Finish the two deterministic ground connections left by Freerouting."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def footprint(board: pcbnew.BOARD, reference: str):
    return next(item for item in board.GetFootprints() if item.GetReference() == reference)


def pad(board: pcbnew.BOARD, reference: str, number: str):
    return next(item for item in footprint(board, reference).Pads() if item.GetNumber() == number)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))
    ground = board.FindNet("GND")
    c10 = pad(board, "C10", "2").GetPosition()

    def xy(position):
        return (round(pcbnew.ToMM(position.x), 4), round(pcbnew.ToMM(position.y), 4))

    generated_segments = {
        frozenset((xy(c10), (77.4, 18.4))),
        frozenset(((71.7, 43.0), (78.7, 43.0))),
        frozenset(((71.7, 43.0), (71.7, 48.0))),
        frozenset(((71.7, 48.0), (78.7, 48.0))),
        frozenset(((78.7, 48.0), (78.7, 43.0))),
    }
    for item in list(board.GetTracks()):
        if isinstance(item, pcbnew.PCB_VIA) and xy(item.GetPosition()) in {(71.7, 43.0), (78.7, 43.0)}:
            board.RemoveNative(item)
        elif isinstance(item, pcbnew.PCB_TRACK):
            segment = frozenset((xy(item.GetStart()), xy(item.GetEnd())))
            if segment in generated_segments:
                board.RemoveNative(item)

    # SHT45 local decoupling joins the deterministic sensor escape via.
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(c10)
    track.SetEnd(point(77.4, 18.4))
    track.SetLayer(pcbnew.F_Cu)
    track.SetWidth(mm(0.2))
    track.SetNet(ground)
    board.Add(track)

    # Join the two nearby ground fanout branches on the component layer.
    route = ((71.7, 43.0), (71.7, 48.0), (78.7, 48.0), (78.7, 43.0))
    for start, end in zip(route, route[1:]):
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(point(*start))
        track.SetEnd(point(*end))
        track.SetLayer(pcbnew.F_Cu)
        track.SetWidth(mm(0.2))
        track.SetNet(ground)
        board.Add(track)

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.board), board)
    print("Finalized B-ES4-AIR-R2 ground connections")


if __name__ == "__main__":
    main()
