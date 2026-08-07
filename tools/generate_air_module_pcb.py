#!/usr/bin/env python3
"""Generate placed 25 x 25 mm Xerolux AIR-SLOT module PCBs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


FP_ROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
AIR_FP_ROOT = Path(__file__).resolve().parents[1] / "hardware" / "esp-sensor" / "B-ES4-AIR-lib" / "Xerolux-Air.pretty"


def mm(v): return pcbnew.FromMM(v)
def point(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))


def load(lib,name):
    root = AIR_FP_ROOT if lib == "Xerolux-Air" else FP_ROOT / f"{lib}.pretty"
    fp = pcbnew.FootprintLoad(str(root), name)
    if fp is None: raise RuntimeError(f"missing footprint {lib}:{name}")
    return fp


def add_part(board,nets,ref,val,lib,name,x,y,rot,pmap,layer=pcbnew.F_Cu):
    fp=load(lib,name); fp.SetReference(ref); fp.SetValue(val); fp.SetPosition(point(x,y)); fp.SetOrientationDegrees(rot)
    fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    for pad in fp.Pads():
        if pad.GetNumber() in pmap: pad.SetNet(nets[pmap[pad.GetNumber()]])
    board.Add(fp)
    if layer == pcbnew.B_Cu: fp.Flip(point(x,y), False)
    return fp


def text(board,value,x,y,size=.8,layer=pcbnew.F_SilkS):
    item=pcbnew.PCB_TEXT(board); item.SetText(value); item.SetPosition(point(x,y)); item.SetLayer(layer)
    item.SetTextSize(point(size,size)); item.SetTextThickness(mm(.12)); board.Add(item)


def track(board,net,a,b,layer=pcbnew.F_Cu,width=.25):
    item=pcbnew.PCB_TRACK(board); item.SetStart(point(*a)); item.SetEnd(point(*b)); item.SetLayer(layer)
    item.SetWidth(mm(width)); item.SetNet(nets_or(net)); board.Add(item)


def nets_or(net): return net


def build(variant: str):
    board=pcbnew.BOARD(); board.SetCopperLayerCount(4)
    for a,b in zip(((0,0),(25,0),(25,25),(0,25)),((25,0),(25,25),(0,25),(0,0))):
        s=pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(point(*a)); s.SetEnd(point(*b)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(.15)); board.Add(s)
    names=["GND","SLOT_5V","I2C_SDA","I2C_SCL","MOD_3V3"]
    if variant=="VOCNOX": names += ["SGP_VDD"]
    nets={}
    for name in names:
        net=pcbnew.NETINFO_ITEM(board,name); board.Add(net); nets[name]=net
    slot={"1":"GND","2":"SLOT_5V","3":"I2C_SDA","4":"I2C_SCL",
          "5":"I2C_SCL","6":"I2C_SDA","7":"SLOT_5V","8":"GND"}
    add_part(board,nets,"J1","AIR-SLOT","Connector_PinSocket_2.54mm","PinSocket_2x04_P2.54mm_Vertical",12.5,4,0,slot,pcbnew.B_Cu)
    if variant=="CO2":
        add_part(board,nets,"U1","SCD41-D-R1","Xerolux-Air","SENSOR-SMD_SCD41-D-R1",7.5,18.5,0,{"6":"GND","7":"MOD_3V3","9":"I2C_SCL","10":"I2C_SDA","19":"MOD_3V3","20":"GND","21":"GND"})
        add_part(board,nets,"U2","AP2112K-3.3","Package_TO_SOT_SMD","SOT-23-5",20,13,90,{"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"})
        add_part(board,nets,"C1","10u","Capacitor_SMD","C_0805_2012Metric",17.5,16.5,0,{"1":"SLOT_5V","2":"GND"})
        add_part(board,nets,"C2","22u","Capacitor_SMD","C_0805_2012Metric",20.5,18.5,0,{"1":"MOD_3V3","2":"GND"})
        add_part(board,nets,"C3","100n","Capacitor_SMD","C_0603_1608Metric",18.5,21.5,0,{"1":"MOD_3V3","2":"GND"})
    elif variant=="VOCNOX":
        add_part(board,nets,"U1","SGP41-D-R4","Xerolux-Air","DFN-6_L2.4-W2.4-P0.80-TL-EP",10,18,0,{"1":"SGP_VDD","2":"GND","3":"I2C_SDA","4":"GND","5":"MOD_3V3","6":"I2C_SCL","7":"GND"})
        add_part(board,nets,"U2","AP2112K-3.3","Package_TO_SOT_SMD","SOT-23-5",20,13,90,{"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"})
        add_part(board,nets,"R1","10R","Resistor_SMD","R_0603_1608Metric",6.5,14,0,{"1":"MOD_3V3","2":"SGP_VDD"})
        add_part(board,nets,"C1","1u","Capacitor_SMD","C_0805_2012Metric",13,14,0,{"1":"SGP_VDD","2":"GND"})
        add_part(board,nets,"C2","1u","Capacitor_SMD","C_0805_2012Metric",6,22,0,{"1":"MOD_3V3","2":"GND"})
        add_part(board,nets,"C3","100n","Capacitor_SMD","C_0603_1608Metric",10,22,0,{"1":"MOD_3V3","2":"GND"})
        add_part(board,nets,"C4","10u","Capacitor_SMD","C_0805_2012Metric",18,17,0,{"1":"SLOT_5V","2":"GND"})
        add_part(board,nets,"C5","22u","Capacitor_SMD","C_0805_2012Metric",18,21,0,{"1":"MOD_3V3","2":"GND"})
    else:
        add_part(board,nets,"U1","BMP390","Xerolux-Air","LGA-10_L2.0-W2.0-P0.50-BL",10,18,0,{"1":"MOD_3V3","2":"I2C_SCL","3":"GND","4":"I2C_SDA","5":"GND","6":"MOD_3V3","8":"GND","9":"GND","10":"MOD_3V3"})
        add_part(board,nets,"U2","AP2112K-3.3","Package_TO_SOT_SMD","SOT-23-5",20,13,90,{"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"})
        add_part(board,nets,"C1","100n","Capacitor_SMD","C_0603_1608Metric",6,22,0,{"1":"MOD_3V3","2":"GND"})
        add_part(board,nets,"C2","100n","Capacitor_SMD","C_0603_1608Metric",10,22,0,{"1":"MOD_3V3","2":"GND"})
        add_part(board,nets,"C3","10u","Capacitor_SMD","C_0805_2012Metric",18,17,0,{"1":"SLOT_5V","2":"GND"})
        add_part(board,nets,"C4","22u","Capacitor_SMD","C_0805_2012Metric",18,21,0,{"1":"MOD_3V3","2":"GND"})
    title={"CO2":"CO2 / SCD41","VOCNOX":"VOC-NOx / SGP41","PRESSURE":"PRESSURE / BMP390"}[variant]
    text(board,f"{title} | XEROLUX",12.5,1,.55)
    text(board,"REV A-ES1 | 2026",12.5,1,.55,pcbnew.B_SilkS)
    settings=board.GetDesignSettings(); settings.m_MinClearance=mm(.15); settings.m_TrackMinWidth=mm(.12); settings.SetCustomTrackWidth(mm(.2)); settings.SetCustomViaSize(mm(.7)); settings.SetCustomViaDrill(mm(.3))
    return board


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("output",type=Path); parser.add_argument("--variant",choices=("CO2","VOCNOX","PRESSURE"),required=True)
    args=parser.parse_args(); args.output.parent.mkdir(parents=True,exist_ok=True); pcbnew.SaveBoard(str(args.output),build(args.variant))


if __name__=="__main__": main()
