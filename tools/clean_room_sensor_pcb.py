#!/usr/bin/env python3
"""Clean router artifacts and connect copper planes on room-sensor boards."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_ground_zone(board, net, layer) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(net)
    zone.SetLocalClearance(mm(0.3))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetMinThickness(mm(0.2))
    zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((10.5, 10.5), (154.5, 10.5), (154.5, 87.5), (10.5, 87.5)):
        outline.Append(point(x, y))
    board.Add(zone)


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
    parser.add_argument("variant", choices=("classic", "esp"))
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))

    for item in board.GetTracks():
        if not isinstance(item, pcbnew.PCB_VIA) and item.GetWidth() < mm(0.2):
            item.SetWidth(mm(0.2))

    for item in list(board.GetTracks()):
        if not isinstance(item, pcbnew.PCB_VIA) or item.GetNetname() != "+3V3":
            continue
        position = item.GetPosition()
        if abs(pcbnew.ToMM(position.x) - 118.5) < 0.02 and abs(pcbnew.ToMM(position.y) - 61.4) < 0.02:
            board.RemoveNative(item)
            break

    if args.variant == "esp":
        for drawing in board.GetDrawings():
            if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() == "ENGINEERING SAMPLE / BENCH TEST FIRST":
                drawing.SetPosition(point(127, 74))

    if args.variant == "classic":
        zones = list(board.Zones())
        for duplicate in zones[1:]:
            board.RemoveNative(duplicate)
        sht = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U3")
        gnd_pad = next(pad for pad in sht.Pads() if pad.GetNumber() == "4")
        for item in list(board.GetTracks()):
            if item.GetNetname() != "GND":
                continue
            if isinstance(item, pcbnew.PCB_VIA):
                position = item.GetPosition()
                if (abs(pcbnew.ToMM(position.x) - 121.0) < 0.02 and abs(pcbnew.ToMM(position.y) - 58.0) < 0.02) or (abs(pcbnew.ToMM(position.x) - 125.0) < 0.02 and abs(pcbnew.ToMM(position.y) - 55.0) < 0.02):
                    board.RemoveNative(item)
                continue
            positions = (item.GetStart(), item.GetEnd())
            old_bridge = {(round(pcbnew.ToMM(position.x), 3), round(pcbnew.ToMM(position.y), 3)) for position in positions}
            if old_bridge == {(121.0, 58.0), (125.0, 55.0)}:
                board.RemoveNative(item)
                continue
            if all(116.5 <= pcbnew.ToMM(position.x) <= 123.1 and 55.5 <= pcbnew.ToMM(position.y) <= 65.1 for position in positions):
                board.RemoveNative(item)
        add_track(board, gnd_pad.GetNet(), gnd_pad.GetPosition(), point(117.5, 59.6))
        add_track(board, gnd_pad.GetNet(), point(117.5, 59.6), point(117.5, 58.5))
        add_track(board, gnd_pad.GetNet(), point(117.5, 58.5), point(115.5, 58.5))
        add_via(board, gnd_pad.GetNet(), point(115.5, 58.5))
        add_via(board, gnd_pad.GetNet(), point(115.5, 55.0))
        add_track(board, gnd_pad.GetNet(), point(115.5, 58.5), point(115.5, 55.0), pcbnew.B_Cu)

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.board), board)
    print(f"Cleaned {args.variant} board")


if __name__ == "__main__":
    main()
