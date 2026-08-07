#!/usr/bin/env python3
"""Add filled top and bottom GND planes to a 25 mm AIR-SLOT module."""

from __future__ import annotations

import argparse
from pathlib import Path
import pcbnew


def mm(v): return pcbnew.FromMM(v)
def point(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("board",type=Path); args=parser.parse_args()
    board=pcbnew.LoadBoard(str(args.board))
    for zone in list(board.Zones()):
        if not zone.GetIsRuleArea(): board.RemoveNative(zone)
    for layer in (pcbnew.F_Cu,pcbnew.B_Cu):
        zone=pcbnew.ZONE(board); zone.SetLayer(layer); zone.SetNet(board.FindNet("GND")); zone.SetLocalClearance(mm(.25))
        zone.SetMinThickness(mm(.2)); zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
        outline=zone.Outline(); outline.NewOutline()
        for xy in ((.4,.4),(24.6,.4),(24.6,24.6),(.4,24.6)): outline.Append(point(*xy))
        board.Add(zone)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones()); pcbnew.SaveBoard(str(args.board),board)
    print("Added AIR-SLOT module ground planes")


if __name__=="__main__": main()
