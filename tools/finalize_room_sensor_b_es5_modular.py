#!/usr/bin/env python3
"""Close the deterministic B-ES5-MODULAR autorouter power-bus leftover."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def mm(value): return pcbnew.FromMM(value)
def point(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))


def add_track(board, net, a, b, layer=pcbnew.B_Cu):
    item=pcbnew.PCB_TRACK(board); item.SetStart(point(*a)); item.SetEnd(point(*b)); item.SetLayer(layer)
    item.SetWidth(mm(.25)); item.SetNet(net); board.Add(item)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("board",type=Path); args=parser.parse_args()
    board=pcbnew.LoadBoard(str(args.board))
    net=board.FindNet("SYS_5V")
    obsolete={
        ((58.04,98),(58.04,109.2)),((58.04,109.2),(86.04,109.2)),((86.04,109.2),(86.04,107.92)),
        ((58.04,98),(60,96)),((86.04,107.92),(88,109)),((60,96),(60,109.2)),
        ((60,109.2),(88,109.2)),((88,109.2),(88,109)),
    }
    for item in list(board.GetTracks()):
        if isinstance(item,pcbnew.PCB_VIA):
            q=item.GetPosition(); xy=(round(pcbnew.ToMM(q.x),2),round(pcbnew.ToMM(q.y),2))
            if xy in {(58.04,98),(86.04,107.92),(60,96),(88,109)}: board.RemoveNative(item)
            continue
        s=item.GetStart(); e=item.GetEnd()
        pair=((round(pcbnew.ToMM(s.x),2),round(pcbnew.ToMM(s.y),2)),(round(pcbnew.ToMM(e.x),2),round(pcbnew.ToMM(e.y),2)))
        if pair in obsolete or (pair[1],pair[0]) in obsolete: board.RemoveNative(item)
    for a,b in (((55.54,98),(55.54,95.5)),((55.54,95.5),(83.54,95.5)),((83.54,95.5),(83.54,98))): add_track(board,net,a,b)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.board),board)
    print("Finalized B-ES5-MODULAR AIR-SLOT 5 V bus")


if __name__=="__main__": main()
