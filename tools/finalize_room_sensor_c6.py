#!/usr/bin/env python3
"""Finish B-ES2-C6 SHT45 escape routing and normalize router output."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def pad(board, reference: str, number: str):
    footprint = next(fp for fp in board.GetFootprints() if fp.GetReference() == reference)
    return next(item for item in footprint.Pads() if item.GetNumber() == number)


def add_track(board, net, start, end, layer=pcbnew.F_Cu) -> None:
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetLayer(layer)
    track.SetWidth(mm(0.2))
    track.SetNet(net)
    board.Add(track)


def add_via(board, net, position) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(position)
    via.SetWidth(mm(0.8))
    via.SetDrill(mm(0.4))
    via.SetNet(net)
    board.Add(via)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))

    for item in board.GetTracks():
        if isinstance(item, pcbnew.PCB_TRACK) and not isinstance(item, pcbnew.PCB_VIA):
            if item.GetWidth() < mm(0.2):
                item.SetWidth(mm(0.2))

    # Freerouting cannot enter all four 0.35 x 0.50 mm SHT45 lands.  Escape
    # each pad on F.Cu, then join the already-routed net on the indicated layer.
    routes = [
        ("4", (109.7, 19.6), pcbnew.In1_Cu, (111.2453, 18.4703)),
        ("1", (106.2, 19.6), pcbnew.In1_Cu, (104.5633, 17.2617)),
        ("2", (106.2, 20.8), pcbnew.In1_Cu, (98.0001, 28.3073)),
    ]
    for pin, via_xy, layer, target_xy in routes:
        source = pad(board, "U4", pin)
        via_pos = point(*via_xy)
        add_track(board, source.GetNet(), source.GetPosition(), via_pos)
        add_via(board, source.GetNet(), via_pos)
        add_track(board, source.GetNet(), via_pos, point(*target_xy), layer)

    vdd = pad(board, "U4", "3")
    add_track(board, vdd.GetNet(), vdd.GetPosition(), point(110.0, 21.0))
    add_track(board, vdd.GetNet(), point(110.0, 21.0), point(111.2383, 21.5367))

    # Remove optimizer escape vias which DRC identifies as connected on only
    # one layer. They are not part of any completed connection.
    dangling = {
        (52.9963, 62.8754),
        (74.6426, 55.3574),
        (52.9846, 67.1129),
        (108.8477, 66.5173),
    }
    for item in list(board.GetTracks()):
        if not isinstance(item, pcbnew.PCB_VIA):
            continue
        x = round(pcbnew.ToMM(item.GetPosition().x), 4)
        y = round(pcbnew.ToMM(item.GetPosition().y), 4)
        if (x, y) in dangling:
            board.RemoveNative(item)

    pcbnew.SaveBoard(str(args.board), board)
    print("Finalized B-ES2-C6 routing")


if __name__ == "__main__":
    main()
