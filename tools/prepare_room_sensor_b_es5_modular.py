#!/usr/bin/env python3
"""Pre-route the four symmetric AIR-SLOT pin pairs before autorouting."""

from __future__ import annotations

import argparse
from pathlib import Path
import pcbnew


def segment(board, net, start, end, layer, width=0.25):
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(start); track.SetEnd(end); track.SetLayer(layer)
    track.SetWidth(pcbnew.FromMM(width)); track.SetNet(net); board.Add(track)
    track.SetLocked(True)


def route(board, net, points, layer):
    for start, end in zip(points, points[1:]):
        segment(board, net, start, end, layer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("board", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))
    for ref in ("J9", "J10", "J11"):
        fp = board.FindFootprintByReference(ref)
        pads = {p.GetNumber(): p for p in fp.Pads()}
        x0 = pcbnew.ToMM(pads["1"].GetPosition().x); x1 = pcbnew.ToMM(pads["2"].GetPosition().x)
        y0 = pcbnew.ToMM(pads["1"].GetPosition().y); y3 = pcbnew.ToMM(pads["7"].GetPosition().y)
        p = lambda x,y: pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
        # Perimeter approaches avoid every intervening plated-through pad.
        route(board,pads["1"].GetNet(),[pads["1"].GetPosition(),p(x0-2,y0),p(x0-2,y3+2.9),p(x1+2,y3+2.9),p(x1+2,y3),pads["8"].GetPosition()],pcbnew.In1_Cu)
        route(board,pads["2"].GetNet(),[pads["2"].GetPosition(),p(x1+2.5,y0),p(x1+2.5,y3+2.3),p(x0-2.5,y3+2.3),p(x0-2.5,y3),pads["7"].GetPosition()],pcbnew.In2_Cu)
        mid = y0 + 6.35
        route(board,pads["3"].GetNet(),[pads["3"].GetPosition(),p(x0-1.7,y0+2.54),p(x0-1.7,mid),p(x1+1.7,mid),p(x1+1.7,y0+5.08),pads["6"].GetPosition()],pcbnew.F_Cu)
        route(board,pads["4"].GetNet(),[pads["4"].GetPosition(),p(x1+2.2,y0+2.54),p(x1+2.2,mid),p(x0-2.2,mid),p(x0-2.2,y0+5.08),pads["5"].GetPosition()],pcbnew.B_Cu)
    pcbnew.SaveBoard(str(args.board), board)


if __name__ == "__main__":
    main()
