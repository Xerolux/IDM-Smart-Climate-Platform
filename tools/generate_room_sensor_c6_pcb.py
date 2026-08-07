#!/usr/bin/env python3
"""Generate the placed four-layer B-ES2-C6 PCB for routing."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


FP_ROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")


def mm(v): return pcbnew.FromMM(v)
def point(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))


def load(lib,name):
    fp=pcbnew.FootprintLoad(str(FP_ROOT/f"{lib}.pretty"),name)
    if fp is None: raise RuntimeError(f"missing footprint {lib}:{name}")
    return fp


def add_outline(board):
    for a,b in zip(((10,10),(120,10),(120,80),(10,80)),((120,10),(120,80),(10,80),(10,10))):
        s=pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(point(*a)); s.SetEnd(point(*b)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(.15)); board.Add(s)


def custom_c6(board):
    fp=pcbnew.FOOTPRINT(board); fp.SetReference("U3"); fp.SetValue("ESP32-C6-WROOM-1-N16")
    fp.SetFPID(pcbnew.LIB_ID("Custom","ESP32-C6-WROOM-1"))
    def smd(num,x,y,w=1.5,h=.9):
        p=pcbnew.PAD(fp); p.SetNumber(str(num)); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetShape(pcbnew.PAD_SHAPE_RECT)
        layers=pcbnew.LSET(); layers.AddLayer(pcbnew.F_Cu); layers.AddLayer(pcbnew.F_Mask); layers.AddLayer(pcbnew.F_Paste)
        p.SetSize(point(w,h)); p.SetLayerSet(layers); p.SetFPRelativePosition(point(x,y)); fp.Add(p)
    y0=-5.255
    for n in range(1,15): smd(n,-8.75,y0+(n-1)*1.27)
    for n in range(15,29): smd(n,8.75,y0+(28-n)*1.27)
    smd(29,0,3.255,3.3,3.3)
    for x in (-1.1,0,1.1):
        for y in (2.155,3.255,4.355):
            p=pcbnew.PAD(fp); p.SetNumber("29"); p.SetAttribute(pcbnew.PAD_ATTRIB_PTH); p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            layers=pcbnew.LSET.AllCuMask(); layers.AddLayer(pcbnew.F_Mask); layers.AddLayer(pcbnew.B_Mask)
            p.SetSize(point(.6,.6)); p.SetDrillSize(point(.3,.3)); p.SetLayerSet(layers); p.SetFPRelativePosition(point(x,y)); fp.Add(p)
    for layer in (pcbnew.F_Fab,pcbnew.F_CrtYd):
        for a,b in zip(((-9,-12.75),(9,-12.75),(9,12.75),(-9,12.75)),((9,-12.75),(9,12.75),(-9,12.75),(-9,-12.75))):
            s=pcbnew.PCB_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(point(*a)); s.SetEnd(point(*b)); s.SetLayer(layer); s.SetWidth(mm(.1)); fp.Add(s)
    return fp


def add_part(board,nets,spec):
    ref,val,lib,name,x,y,rot,pmap=spec
    fp=custom_c6(board) if lib=="Custom" else load(lib,name)
    fp.SetReference(ref); fp.SetValue(val); fp.SetPosition(point(x,y)); fp.SetOrientationDegrees(rot)
    for pad in fp.Pads():
        net=pmap.get(pad.GetNumber())
        if net: pad.SetNet(nets[net])
    board.Add(fp); return fp


def text(board,value,x,y,size=.8,layer=pcbnew.F_SilkS):
    t=pcbnew.PCB_TEXT(board); t.SetText(value); t.SetPosition(point(x,y)); t.SetLayer(layer); t.SetTextSize(point(size,size)); t.SetTextThickness(mm(.12)); board.Add(t)


def keepout(board,layer,coords):
    z=pcbnew.ZONE(board); z.SetLayer(layer); z.SetIsRuleArea(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowZoneFills(True)
    o=z.Outline(); o.NewOutline()
    for x,y in coords: o.Append(point(x,y))
    board.Add(z)


def build():
    b=pcbnew.BOARD(); b.SetCopperLayerCount(4); add_outline(b)
    names=["GND","24V_RAW","24V_FUSED","24V_PROT","PWR_GOOD","BUCK_FB","VCC_BYP","BOOT","SW","5V_BUCK","USB_5V","SYS_5V","+3V3",
           "TEMP_KTY","RH_OUT","DAC_RAW","OPAMP_OUT","OPAMP_FB","I2C_SDA","I2C_SCL","C6_EN","C6_BOOT","USB_D-","USB_D+","USB_CC1","USB_CC2",
           "STATUS_LED","STATUS_LED_R","ONEWIRE","EXP_GPIO4","EXP_GPIO5","RS485_RX","RS485_TX","RS485_DE","VISO","RS485_A","RS485_B","RS485_COM","RS485_SHIELD","RS485_TERM"]
    nets={}
    for n in names:
        ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni); nets[n]=ni
    P=[]
    def p(ref,val,lib,name,x,y,r,pins): P.append((ref,val,lib,name,x,y,r,{str(k):v for k,v in pins.items()}))
    p("J1","43/42/41/40","TerminalBlock_Phoenix","TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",16,62,90,{1:"TEMP_KTY",2:"24V_RAW",3:"GND",4:"RH_OUT"})
    p("RTH1","KTY81/210,112","Package_TO_SOT_THT","TO-92_Inline",18,46,0,{1:"TEMP_KTY",2:"GND"})
    p("F1","1812L050/30PR","Fuse","Fuse_1812_4532Metric",29,66,0,{1:"24V_RAW",2:"24V_FUSED"})
    p("D1","SS16","Diode_SMD","D_SMA",38,66,0,{1:"24V_PROT",2:"24V_FUSED"}); p("TVS1","SMBJ33A","Diode_SMD","D_SMB",38,73,90,{1:"GND",2:"24V_PROT"})
    p("U1","LMR36510ADDAR","Package_SO","TI_SO-PowerPAD-8_ThermalVias",49,65,0,{1:"GND",2:"24V_PROT",3:"24V_PROT",4:"PWR_GOOD",5:"BUCK_FB",6:"VCC_BYP",7:"BOOT",8:"SW",9:"GND"})
    p("L1","SRP1038A-330M","Inductor_SMD","L_10.4x10.4_H4.8",61,65,0,{1:"SW",2:"5V_BUCK"})
    p("R1","100k","Resistor_SMD","R_0603_1608Metric",55,73,0,{1:"5V_BUCK",2:"BUCK_FB"}); p("R2","24.9k","Resistor_SMD","R_0603_1608Metric",55,76,0,{1:"BUCK_FB",2:"GND"}); p("R3","100k","Resistor_SMD","R_0603_1608Metric",50,57,90,{1:"PWR_GOOD",2:"5V_BUCK"})
    for ref,val,fp,x,y,pins in [
        ("C1","4.7u 100V","C_1210_3225Metric",41,56,{1:"24V_PROT",2:"GND"}),("C2","220n 100V","C_0805_2012Metric",45,53,{1:"24V_PROT",2:"GND"}),
        ("C3","1u","C_0805_2012Metric",47,72,{1:"VCC_BYP",2:"GND"}),("C4","100n","C_0603_1608Metric",54,58,{1:"BOOT",2:"SW"}),
        ("C5","47u","C_1206_3216Metric",71,59,{1:"5V_BUCK",2:"GND"}),("C6","47u","C_1206_3216Metric",71,64,{1:"5V_BUCK",2:"GND"})]: p(ref,val,"Capacitor_SMD",fp,x,y,0,pins)
    p("D2","SS14","Diode_SMD","D_SMA",74,54,0,{1:"SYS_5V",2:"5V_BUCK"}); p("D3","SS14","Diode_SMD","D_SMA",61,75,0,{1:"SYS_5V",2:"USB_5V"})
    p("U2","AP2112K-3.3","Package_TO_SOT_SMD","SOT-23-5",80,64,0,{1:"SYS_5V",2:"GND",3:"SYS_5V",5:"+3V3"})
    p("C7","10u","Capacitor_SMD","C_0805_2012Metric",77,59,0,{1:"SYS_5V",2:"GND"}); p("C8","22u","Capacitor_SMD","C_0805_2012Metric",84,59,0,{1:"+3V3",2:"GND"})
    c6={1:"GND",2:"+3V3",3:"C6_EN",4:"EXP_GPIO4",5:"EXP_GPIO5",6:"I2C_SDA",7:"I2C_SCL",10:"STATUS_LED",13:"USB_D-",14:"USB_D+",15:"C6_BOOT",21:"ONEWIRE",24:"RS485_RX",25:"RS485_TX",27:"RS485_DE",28:"GND",29:"GND"}
    p("U3","ESP32-C6-WROOM-1-N16","Custom","ESP32-C6-WROOM-1",55,22.75,0,c6)
    p("J3","USB-C","Connector_USB","USB_C_Receptacle_HRO_TYPE-C-31-M-12",75,77.2,0,{"A1":"GND","A4":"USB_5V","A5":"USB_CC1","A6":"USB_D+","A7":"USB_D-","A9":"USB_5V","A12":"GND","B1":"GND","B4":"USB_5V","B5":"USB_CC2","B6":"USB_D+","B7":"USB_D-","B9":"USB_5V","B12":"GND","SH":"GND"})
    p("ESD1","USBLC6-2SC6","Package_TO_SOT_SMD","SOT-23-6",75,68,0,{1:"USB_D-",2:"GND",3:"USB_D+",4:"USB_D+",5:"USB_5V",6:"USB_D-"})
    p("R4","5.1k","Resistor_SMD","R_0603_1608Metric",68,67,90,{1:"USB_CC1",2:"GND"}); p("R5","5.1k","Resistor_SMD","R_0603_1608Metric",70.5,67,90,{1:"USB_CC2",2:"GND"})
    p("R6","10k","Resistor_SMD","R_0603_1608Metric",65,43,0,{1:"+3V3",2:"C6_EN"}); p("C9","1u","Capacitor_SMD","C_0603_1608Metric",65,46,0,{1:"C6_EN",2:"GND"})
    p("SW1","RESET","Button_Switch_SMD","SW_SPST_B3U-1000P",70,43,0,{1:"C6_EN",2:"GND"}); p("SW2","BOOT","Button_Switch_SMD","SW_SPST_B3U-1000P",77,43,0,{1:"C6_BOOT",2:"GND"})
    p("U4","SHT45","Sensor_Humidity","Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad",108,20,0,{1:"I2C_SDA",2:"I2C_SCL",3:"+3V3",4:"GND"})
    p("R7","4.7k","Resistor_SMD","R_0603_1608Metric",103,18,0,{1:"+3V3",2:"I2C_SDA"}); p("R8","4.7k","Resistor_SMD","R_0603_1608Metric",103,21,0,{1:"+3V3",2:"I2C_SCL"}); p("C10","100n","Capacitor_SMD","C_0603_1608Metric",112,20,90,{1:"+3V3",2:"GND"})
    p("U5","MCP4725A0T","Package_TO_SOT_SMD","SOT-23-6",83,46,0,{1:"DAC_RAW",2:"GND",3:"+3V3",4:"I2C_SDA",5:"I2C_SCL",6:"GND"})
    p("U6","OPA197IDBVR","Package_TO_SOT_SMD","SOT-23-5",92,46,0,{1:"OPAMP_OUT",2:"GND",3:"DAC_RAW",4:"OPAMP_FB",5:"24V_PROT"})
    p("R9","21k 1% CAL","Resistor_SMD","R_0603_1608Metric",96,50,0,{1:"OPAMP_OUT",2:"OPAMP_FB"}); p("R10","10k","Resistor_SMD","R_0603_1608Metric",91,52,0,{1:"OPAMP_FB",2:"GND"}); p("R11","220R","Resistor_SMD","R_0603_1608Metric",99,46,0,{1:"OPAMP_OUT",2:"RH_OUT"})
    p("C11","100n","Capacitor_SMD","C_0603_1608Metric",81,50,0,{1:"+3V3",2:"GND"}); p("C12","100n 50V","Capacitor_SMD","C_0603_1608Metric",94,42,0,{1:"24V_PROT",2:"GND"}); p("C13","100n 50V","Capacitor_SMD","C_0603_1608Metric",102,46,90,{1:"RH_OUT",2:"GND"})
    p("U7","CA-IS3092W","Package_SO","SOIC-16W_7.5x10.3mm_P1.27mm",105,60,0,{1:"+3V3",2:"GND",3:"RS485_RX",4:"RS485_DE",5:"RS485_DE",6:"RS485_TX",8:"GND",9:"RS485_COM",10:"RS485_COM",12:"RS485_A",13:"RS485_B",15:"RS485_COM",16:"VISO"})
    for ref,val,x,y,pins in [("C14","100n",96,55.5,{1:"+3V3",2:"GND"}),("C16","10u",96,52.5,{1:"+3V3",2:"GND"}),("C17","100n",113,54,{1:"VISO",2:"RS485_COM"}),("C18","10u",113,57,{1:"VISO",2:"RS485_COM"})]: p(ref,val,"Capacitor_SMD","C_0805_2012Metric",x,y,0,pins)
    p("J2","RS485 A/B/COM/SH","TerminalBlock_Phoenix","TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",115,43,90,{1:"RS485_A",2:"RS485_B",3:"RS485_COM",4:"RS485_SHIELD"})
    p("R12","120R","Resistor_SMD","R_1206_3216Metric",113,63,90,{1:"RS485_A",2:"RS485_TERM"}); p("JP1","TERM","Jumper","SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm",116,63,90,{1:"RS485_TERM",2:"RS485_B"})
    p("J4","EXPANSION","Connector_JST","JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal",88,76.5,0,{1:"+3V3",2:"GND",3:"I2C_SDA",4:"I2C_SCL",5:"ONEWIRE",6:"EXP_GPIO4",7:"EXP_GPIO5",8:"SYS_5V"})
    p("LED1","STATUS","LED_SMD","LED_0603_1608Metric",82,40,0,{1:"STATUS_LED_R",2:"GND"}); p("R13","1k","Resistor_SMD","R_0603_1608Metric",78,40,0,{1:"STATUS_LED",2:"STATUS_LED_R"})
    for spec in P: add_part(b,nets,spec)
    tp_positions=((22,38),(30,38),(38,38),(46,39),(54,40),(62,40),(70,38),(83,35),(86,31),(94,31),(102,31),(110,28))
    for idx,(net,(x,y)) in enumerate(zip(("24V_RAW","24V_PROT","SYS_5V","+3V3","I2C_SDA","I2C_SCL","RH_OUT","TEMP_KTY","RS485_A","RS485_B","RS485_COM","GND"),tp_positions),1):
        add_part(b,nets,(f"TP{idx}",net,"TestPoint","TestPoint_Plated_Hole_D2.0mm",x,y,0,{"1":net}))
    for ref,x,y in (("H1",14,14),("H2",116,14),("H3",14,76),("H4",116,76)):
        fp=load("MountingHole","MountingHole_3.2mm_M3"); fp.SetReference(ref); fp.SetPosition(point(x,y)); b.Add(fp)
    for layer in (pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu): keepout(b,layer,((45.7,10.1),(64.3,10.1),(64.3,17.0),(45.7,17.0)))
    text(b,"SMART CLIMATE SENSOR",83,12,1.1); text(b,"by Xerolux | xerolux.de | REV B-ES2-C6 | 2026",83,14.5,.65)
    text(b,"USB-C FLASH / POWER",72,75,.65); text(b,"RS485 ISOLATED",105,77,.65)
    text(b,"43 TEMP | 42 +24V | 41 GND | 40 RH",37,78,.65); text(b,"ENGINEERING SAMPLE - BENCH TEST FIRST",57,33,.7)
    d=b.GetDesignSettings(); d.m_MinClearance=mm(.2); d.SetCustomTrackWidth(mm(.25)); d.SetCustomViaSize(mm(.7)); d.SetCustomViaDrill(mm(.3))
    return b


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("output",type=Path); a=ap.parse_args(); a.output.parent.mkdir(parents=True,exist_ok=True); pcbnew.SaveBoard(str(a.output),build())


if __name__=="__main__": main()
