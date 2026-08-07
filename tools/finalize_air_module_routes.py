#!/usr/bin/env python3
"""Close the two deterministic autorouter leftovers on AIR modules."""

from __future__ import annotations
import argparse
from pathlib import Path
import pcbnew

def p(x,y): return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
def seg(b,net,a,c,layer,width=.2):
    t=pcbnew.PCB_TRACK(b); t.SetStart(p(*a)); t.SetEnd(p(*c)); t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(width)); t.SetNet(net); b.Add(t)
def via(b,net,xy):
    v=pcbnew.PCB_VIA(b); v.SetPosition(p(*xy)); v.SetWidth(pcbnew.FromMM(.7)); v.SetDrill(pcbnew.FromMM(.3)); v.SetNet(net); b.Add(v)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('board',type=Path); ap.add_argument('--variant',required=True,choices=('VOCNOX','PRESSURE'))
    a=ap.parse_args(); b=pcbnew.LoadBoard(str(a.board))
    if a.variant=='VOCNOX':
        net=b.FindNet('SLOT_5V')
        seg(b,net,(19.05,14.1375),(18.3,13.92),pcbnew.F_Cu)
        seg(b,net,(17.54,13.92),(18.3,13.92),pcbnew.In2_Cu)
        via(b,net,(18.3,13.92))
    else:
        net=b.FindNet('I2C_SDA')
        seg(b,net,(10.78,18),(11.5,18),pcbnew.F_Cu,.12)
        for a0,a1 in (((11.5,18),(3,18)),((3,18),(3,6.54)),((3,6.54),(8,6.54))):
            seg(b,net,a0,a1,pcbnew.In1_Cu)
        seg(b,net,(8,6.54),(10.8,6.54),pcbnew.F_Cu)
        via(b,net,(11.5,18)); via(b,net,(8,6.54))
    pcbnew.SaveBoard(str(a.board),b)
if __name__=='__main__': main()
