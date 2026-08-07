#!/usr/bin/env python3
"""Pre-route duplicated rotation-safe AIR-SLOT pins on four copper layers."""

from __future__ import annotations

import argparse
from pathlib import Path
import pcbnew


def point(x, y): return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def route(board, net, positions, layer):
    for a, b in zip(positions, positions[1:]):
        t = pcbnew.PCB_TRACK(board); t.SetStart(a); t.SetEnd(b); t.SetLayer(layer)
        t.SetWidth(pcbnew.FromMM(.25)); t.SetNet(net); board.Add(t)
        t.SetLocked(True)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("board", type=Path)
    args = parser.parse_args(); board = pcbnew.LoadBoard(str(args.board))
    fp = board.FindFootprintByReference("J1")
    pads = {p.GetNumber(): p for p in fp.Pads()}
    x0=pcbnew.ToMM(pads["1"].GetPosition().x); x1=pcbnew.ToMM(pads["2"].GetPosition().x)
    y0=pcbnew.ToMM(pads["1"].GetPosition().y); y3=pcbnew.ToMM(pads["7"].GetPosition().y)
    route(board,pads["1"].GetNet(),[pads["1"].GetPosition(),point(x0-2,y0),point(x0-2,y3+2.9),point(x1+2,y3+2.9),point(x1+2,y3),pads["8"].GetPosition()],pcbnew.In1_Cu)
    route(board,pads["2"].GetNet(),[pads["2"].GetPosition(),point(x1+2.5,y0),point(x1+2.5,y3+2.3),point(x0-2.5,y3+2.3),point(x0-2.5,y3),pads["7"].GetPosition()],pcbnew.In2_Cu)
    mid=y0+6.35
    route(board,pads["3"].GetNet(),[pads["3"].GetPosition(),point(x0-1.7,y0+2.54),point(x0-1.7,mid),point(x1+1.7,mid),point(x1+1.7,y0+5.08),pads["6"].GetPosition()],pcbnew.F_Cu)
    route(board,pads["4"].GetNet(),[pads["4"].GetPosition(),point(x1+2.2,y0+2.54),point(x1+2.2,mid),point(x0-2.2,mid),point(x0-2.2,y0+5.08),pads["5"].GetPosition()],pcbnew.B_Cu)
    pcbnew.SaveBoard(str(args.board), board)


if __name__ == "__main__":
    main()
