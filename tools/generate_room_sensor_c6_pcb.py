#!/usr/bin/env python3
"""Generate the placed four-layer B-ES2-C6 PCB for routing."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


FP_ROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
AIR_FP_ROOT = Path(__file__).resolve().parents[1] / "hardware" / "esp-sensor" / "B-ES4-AIR-lib" / "Xerolux-Air.pretty"


def mm(v): return pcbnew.FromMM(v)
def point(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))


def load(lib,name):
    root=AIR_FP_ROOT if lib=="Xerolux-Air" else FP_ROOT/f"{lib}.pretty"
    fp=pcbnew.FootprintLoad(str(root),name)
    if fp is None: raise RuntimeError(f"missing footprint {lib}:{name}")
    return fp


def add_outline(board, right=120, bottom=80):
    for a,b in zip(((10,10),(right,10),(right,bottom),(10,bottom)),((right,10),(right,bottom),(10,bottom),(10,10))):
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


def custom_hfd4(board):
    """Hongfa HFD4 DIP: 2.54 mm columns, 5.08 mm row spacing."""
    fp=pcbnew.FOOTPRINT(board); fp.SetReference("K1"); fp.SetValue("HFD4/5")
    fp.SetFPID(pcbnew.LIB_ID("Custom","Relay_Hongfa_HFD4_DIP"))
    positions={"1":(-3.81,-2.54),"2":(-1.27,-2.54),"3":(1.27,-2.54),"4":(3.81,-2.54),
               "8":(-3.81,2.54),"7":(-1.27,2.54),"6":(1.27,2.54),"5":(3.81,2.54)}
    for number,(x,y) in positions.items():
        pad=pcbnew.PAD(fp); pad.SetNumber(number); pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetShape(pcbnew.PAD_SHAPE_RECT if number=="1" else pcbnew.PAD_SHAPE_CIRCLE)
        layers=pcbnew.LSET.AllCuMask(); layers.AddLayer(pcbnew.F_Mask); layers.AddLayer(pcbnew.B_Mask)
        pad.SetSize(point(1.6,1.6)); pad.SetDrillSize(point(.9,.9)); pad.SetLayerSet(layers)
        pad.SetFPRelativePosition(point(x,y)); fp.Add(pad)
    for layer in (pcbnew.F_SilkS,pcbnew.F_Fab):
        for a,c in zip(((-5,-3.25),(5,-3.25),(5,3.25),(-5,3.25)),((5,-3.25),(5,3.25),(-5,3.25),(-5,-3.25))):
            line=pcbnew.PCB_SHAPE(fp); line.SetShape(pcbnew.SHAPE_T_SEGMENT); line.SetStart(point(*a)); line.SetEnd(point(*c)); line.SetLayer(layer); line.SetWidth(mm(.15)); fp.Add(line)
    return fp


def add_part(board,nets,spec):
    ref,val,lib,name,x,y,rot,pmap=spec
    fp=custom_c6(board) if lib=="Custom" else custom_hfd4(board) if lib=="Xerolux-Relay" else load(lib,name)
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


def build(revision="B-ES2-C6"):
    extended=revision in {"B-ES3-C6","B-ES4-AIR","B-ES4-AIR-R2","B-ES5-MODULAR"}
    air=revision in {"B-ES4-AIR","B-ES4-AIR-R2"}
    air_r2=revision=="B-ES4-AIR-R2"
    modular=revision=="B-ES5-MODULAR"
    tall=air or modular
    right,bottom=(140,110) if tall else ((140,90) if extended else (120,80))
    b=pcbnew.BOARD(); b.SetCopperLayerCount(4); add_outline(b,right,bottom)
    names=["GND","24V_RAW","24V_FUSED","24V_PROT","PWR_GOOD","BUCK_FB","VCC_BYP","BOOT","SW","5V_BUCK","USB_5V","SYS_5V","+3V3",
           "TEMP_KTY","RH_OUT","DAC_RAW","OPAMP_OUT","OPAMP_FB","I2C_SDA","I2C_SCL","C6_EN","C6_BOOT","USB_D-","USB_D+","USB_CC1","USB_CC2",
           "STATUS_LED","STATUS_LED_R","ONEWIRE","EXP_GPIO4","EXP_GPIO5","RS485_RX","RS485_TX","RS485_DE","VISO","RS485_A","RS485_B","RS485_COM","RS485_SHIELD","RS485_TERM"]
    if extended:
        names += ["ONEWIRE_EXT","CONTACT1","CONTACT2","CONTACT1_EXT","CONTACT2_EXT","SERVICE_BUTTON",
                  "BUS_LED","BUS_LED_R","PWR24_LED_R","AIN_0_10_RAW","AIN_DIV","ADC_0_10"]
    if air: names += ["AIR_3V3","SGP_VDD"]
    if air_r2: names += ["PWR_LED_EN","PWR_LED_K","RELAY_CTRL","RELAY_GATE","RELAY_COIL_L","RELAY_COM","RELAY_NO","RELAY_NC"]
    nets={}
    for n in names:
        ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni); nets[n]=ni
    P=[]
    def p(ref,val,lib,name,x,y,r,pins): P.append((ref,val,lib,name,x,y,r,{str(k):v for k,v in pins.items()}))
    term_lib="TerminalBlock" if extended else "TerminalBlock_Phoenix"
    term=lambda pins: (f"TerminalBlock_MaiXu_MX126-5.0-{pins:02d}P_1x{pins:02d}_P5.00mm" if extended else f"TerminalBlock_Phoenix_PT-1,5-{pins}-3.5-H_1x{pins:02d}_P3.50mm_Horizontal")
    p("J1","MX205R PUSH-IN 43/42/41/40" if extended else "43/42/41/40",term_lib,term(4),16,66,90,{1:"TEMP_KTY",2:"24V_RAW",3:"GND",4:"RH_OUT"})
    p("RTH1","KTY81/210,112","Package_TO_SOT_THT","TO-92_Inline",27 if extended else 18,46,0,{1:"TEMP_KTY",2:"GND"})
    p("F1","BSMD1812-050-60V" if air_r2 else "1812L050/30PR","Fuse","Fuse_1812_4532Metric",29,66,0,{1:"24V_RAW",2:"24V_FUSED"})
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
    if extended: c6.update({8:"ADC_0_10",16:"CONTACT1",17:"CONTACT2",18:"SERVICE_BUTTON",20:"BUS_LED"})
    if air_r2:
        c6.pop(10)
        c6.update({11:"STATUS_LED",19:"PWR_LED_EN",26:"RELAY_CTRL"})
    p("U3","ESP32-C6-WROOM-1-N16","Custom","ESP32-C6-WROOM-1",55,22.75,0,c6)
    p("J3","USB-C","Connector_USB","USB_C_Receptacle_HRO_TYPE-C-31-M-12",103 if modular else 75,107.2 if tall else (87.2 if extended else 77.2),0,{"A1":"GND","A4":"USB_5V","A5":"USB_CC1","A6":"USB_D+","A7":"USB_D-","A9":"USB_5V","A12":"GND","B1":"GND","B4":"USB_5V","B5":"USB_CC2","B6":"USB_D+","B7":"USB_D-","B9":"USB_5V","B12":"GND","SH":"GND"})
    p("ESD1","USBLC6-2SC6","Package_TO_SOT_SMD","SOT-23-6",75,68,0,{1:"USB_D-",2:"GND",3:"USB_D+",4:"USB_D+",5:"USB_5V",6:"USB_D-"})
    p("R4","5.1k","Resistor_SMD","R_0603_1608Metric",68,67,90,{1:"USB_CC1",2:"GND"}); p("R5","5.1k","Resistor_SMD","R_0603_1608Metric",70.5,67,90,{1:"USB_CC2",2:"GND"})
    p("R6","10k","Resistor_SMD","R_0603_1608Metric",65,43,0,{1:"+3V3",2:"C6_EN"}); p("C9","1u","Capacitor_SMD","C_0603_1608Metric",65,46,0,{1:"C6_EN",2:"GND"})
    p("SW1","RESET","Button_Switch_SMD","SW_SPST_B3U-1000P",70,43,0,{1:"C6_EN",2:"GND"}); p("SW2","BOOT","Button_Switch_SMD","SW_SPST_B3U-1000P",77,43,0,{1:"C6_BOOT",2:"GND"})
    sx=74 if extended else 108
    p("U4","SHT45","Sensor_Humidity","Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad",sx,20,0,{1:"I2C_SDA",2:"I2C_SCL",3:"+3V3",4:"GND"})
    p("R7","4.7k","Resistor_SMD","R_0603_1608Metric",sx-5,18,0,{1:"+3V3",2:"I2C_SDA"}); p("R8","4.7k","Resistor_SMD","R_0603_1608Metric",sx-5,21,0,{1:"+3V3",2:"I2C_SCL"}); p("C10","100n","Capacitor_SMD","C_0603_1608Metric",sx+4,20,90,{1:"+3V3",2:"GND"})
    p("U5","MCP4725A0T","Package_TO_SOT_SMD","SOT-23-6",83,46,0,{1:"DAC_RAW",2:"GND",3:"+3V3",4:"I2C_SDA",5:"I2C_SCL",6:"GND"})
    p("U6","OPA197IDBVR","Package_TO_SOT_SMD","SOT-23-5",92,46,0,{1:"OPAMP_OUT",2:"GND",3:"DAC_RAW",4:"OPAMP_FB",5:"24V_PROT"})
    p("R9","21k 1% CAL","Resistor_SMD","R_0603_1608Metric",96,50,0,{1:"OPAMP_OUT",2:"OPAMP_FB"}); p("R10","10k","Resistor_SMD","R_0603_1608Metric",91,52,0,{1:"OPAMP_FB",2:"GND"}); p("R11","220R","Resistor_SMD","R_0603_1608Metric",99,46,0,{1:"OPAMP_OUT",2:"RH_OUT"})
    p("C11","100n","Capacitor_SMD","C_0603_1608Metric",81,50,0,{1:"+3V3",2:"GND"}); p("C12","100n 50V","Capacitor_SMD","C_0603_1608Metric",94,42,0,{1:"24V_PROT",2:"GND"}); p("C13","100n 50V","Capacitor_SMD","C_0603_1608Metric",102,46,90,{1:"RH_OUT",2:"GND"})
    p("U7","CA-IS3092W","Package_SO","SOIC-16W_7.5x10.3mm_P1.27mm",105,60,0,{1:"+3V3",2:"GND",3:"RS485_RX",4:"RS485_DE",5:"RS485_DE",6:"RS485_TX",8:"GND",9:"RS485_COM",10:"RS485_COM",12:"RS485_A",13:"RS485_B",15:"RS485_COM",16:"VISO"})
    for ref,val,x,y,pins in [("C14","100n",96,55.5,{1:"+3V3",2:"GND"}),("C16","10u",96,52.5,{1:"+3V3",2:"GND"}),("C17","100n",113,54,{1:"VISO",2:"RS485_COM"}),("C18","10u",113,57,{1:"VISO",2:"RS485_COM"})]: p(ref,val,"Capacitor_SMD","C_0805_2012Metric",x,y,0,pins)
    p("J2","MX205R PUSH-IN RS485 A/B/COM/SH" if extended else "RS485 A/B/COM/SH",term_lib,term(4),135 if extended else 115,48 if extended else 43,90,{1:"RS485_A",2:"RS485_B",3:"RS485_COM",4:"RS485_SHIELD"})
    p("R12","120R","Resistor_SMD","R_1206_3216Metric",116,63,90,{1:"RS485_A",2:"RS485_TERM"})
    if extended: p("SW3","TERM ON/OFF","Button_Switch_SMD","SW_DIP_SPSTx01_Slide_Copal_CHS-01B_W7.62mm_P1.27mm",122,63,90,{1:"RS485_TERM",2:"RS485_B"})
    else: p("JP1","TERM","Jumper","SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm",116,63,90,{1:"RS485_TERM",2:"RS485_B"})
    p("J4","EXPANSION","Connector_JST","JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal",119 if modular else 88,106.5 if tall else (86.5 if extended else 76.5),0,{1:"+3V3",2:"GND",3:"I2C_SDA",4:"I2C_SCL",5:"ONEWIRE",6:"EXP_GPIO4",7:"EXP_GPIO5",8:"SYS_5V"})
    p("LED1","STATUS","LED_SMD","LED_0603_1608Metric",82,40,0,{1:"GND",2:"STATUS_LED_R"} if air_r2 else {1:"STATUS_LED_R",2:"GND"}); p("R13","1k","Resistor_SMD","R_0603_1608Metric",78,40,0,{1:"STATUS_LED",2:"STATUS_LED_R"})
    if extended:
        p("J5","1WIRE A 3V/DQ/GND",term_lib,term(3),84,15,0,{1:"+3V3",2:"ONEWIRE_EXT",3:"GND"})
        p("J6","1WIRE B 3V/DQ/GND",term_lib,term(3),104,15,0,{1:"+3V3",2:"ONEWIRE_EXT",3:"GND"})
        p("J7","CONTACT 1/COM/2",term_lib,term(3),126,15,0,{1:"CONTACT1_EXT",2:"GND",3:"CONTACT2_EXT"})
        p("J8","0-10V IN/GND",term_lib,term(2),135,75,90,{1:"AIN_0_10_RAW",2:"GND"})
        p("R14","100R","Resistor_SMD","R_0603_1608Metric",87,25,0,{1:"ONEWIRE",2:"ONEWIRE_EXT"}); p("R15","4.7k","Resistor_SMD","R_0603_1608Metric",92,25,0,{1:"+3V3",2:"ONEWIRE_EXT"}); p("TVS2","3V3 ESD","Diode_SMD","D_SOD-323",97,25,0,{1:"GND",2:"ONEWIRE_EXT"})
        p("R16","1k","Resistor_SMD","R_0603_1608Metric",112,25,0,{1:"CONTACT1_EXT",2:"CONTACT1"}); p("R17","1k","Resistor_SMD","R_0603_1608Metric",124,25,0,{1:"CONTACT2_EXT",2:"CONTACT2"})
        p("R18","10k","Resistor_SMD","R_0603_1608Metric",109,28,0,{1:"+3V3",2:"CONTACT1"}); p("R19","10k","Resistor_SMD","R_0603_1608Metric",127,28,0,{1:"+3V3",2:"CONTACT2"})
        p("C19","100n","Capacitor_SMD","C_0603_1608Metric",112,31,0,{1:"CONTACT1",2:"GND"}); p("C20","100n","Capacitor_SMD","C_0603_1608Metric",124,31,0,{1:"CONTACT2",2:"GND"})
        p("TVS3","3V3 ESD","Diode_SMD","D_SOD-323",108,25,0,{1:"GND",2:"CONTACT1_EXT"}); p("TVS4","3V3 ESD","Diode_SMD","D_SOD-323",128,25,0,{1:"GND",2:"CONTACT2_EXT"})
        p("TVS5","12V ESD","Diode_SMD","D_SOD-323",127,75,90,{1:"GND",2:"AIN_0_10_RAW"}); p("R20","33k","Resistor_SMD","R_0603_1608Metric",124,72,0,{1:"AIN_0_10_RAW",2:"AIN_DIV"}); p("R21","10k","Resistor_SMD","R_0603_1608Metric",124,75,0,{1:"AIN_DIV",2:"GND"}); p("R22","1k","Resistor_SMD","R_0603_1608Metric",120,72,0,{1:"AIN_DIV",2:"ADC_0_10"}); p("C21","100n","Capacitor_SMD","C_0603_1608Metric",120,75,0,{1:"ADC_0_10",2:"GND"}); p("D4","BAT54S","Package_TO_SOT_SMD","SOT-23",116,74,0,{1:"GND",2:"+3V3",3:"ADC_0_10"})
        p("SW4","SERVICE","Button_Switch_SMD","SW_SPST_B3U-1000P",87 if air_r2 else (116 if modular else 108),100 if air_r2 else (96 if modular else (104 if tall else 85)),0,{1:"SERVICE_BUTTON",2:"GND"}); p("R23","10k","Resistor_SMD","R_0603_1608Metric",82 if air_r2 else (111 if modular else 103),100 if air_r2 else (96 if modular else (104 if tall else 85)),0,{1:"+3V3",2:"SERVICE_BUTTON"})
        p("R24","18k" if air_r2 else "12k","Resistor_SMD","R_0603_1608Metric",91,40,0,{1:"24V_PROT",2:"PWR24_LED_R"}); p("LED2","VIN","LED_SMD","LED_0603_1608Metric",95,40,0,{1:"PWR_LED_K",2:"PWR24_LED_R"} if air_r2 else {1:"PWR24_LED_R",2:"GND"}); p("R25","1k","Resistor_SMD","R_0603_1608Metric",100,40,0,{1:"BUS_LED",2:"BUS_LED_R"}); p("LED3","BUS GREEN","LED_SMD","LED_0603_1608Metric",104,40,0,{1:"GND",2:"BUS_LED_R"} if air_r2 else {1:"BUS_LED_R",2:"GND"})
        if air_r2:
            p("Q1","2N7002 VIN LED","Package_TO_SOT_SMD","SOT-23",109,44,0,{1:"PWR_LED_EN",2:"GND",3:"PWR_LED_K"})
            p("R27","100k","Resistor_SMD","R_0603_1608Metric",113,44,0,{1:"PWR_LED_EN",2:"GND"})
            p("K1","HFD4/5","Xerolux-Relay","Relay_Hongfa_HFD4_DIP",108,97,0,{1:"SYS_5V",2:"RELAY_NC",3:"RELAY_COM",4:"RELAY_NO",8:"RELAY_COIL_L"})
            p("Q2","2N7002 RELAY","Package_TO_SOT_SMD","SOT-23",99,94,0,{1:"RELAY_GATE",2:"GND",3:"RELAY_COIL_L"})
            p("D5","1N4148WS FLYBACK","Diode_SMD","D_SOD-323",101,99,90,{1:"SYS_5V",2:"RELAY_COIL_L"})
            p("R28","100R","Resistor_SMD","R_0603_1608Metric",94,94,0,{1:"RELAY_CTRL",2:"RELAY_GATE"})
            p("R29","100k","Resistor_SMD","R_0603_1608Metric",94,98,0,{1:"RELAY_GATE",2:"GND"})
            p("J9","RELAY COM/NO/NC",term_lib,term(3),117,106.5,0,{1:"RELAY_COM",2:"RELAY_NO",3:"RELAY_NC"})
    if air:
        p("U8","SCD41-D-R1","Xerolux-Air","SENSOR-SMD_SCD41-D-R1",29,101,0,{6:"GND",7:"AIR_3V3",9:"I2C_SCL",10:"I2C_SDA",19:"AIR_3V3",20:"GND",21:"GND"})
        p("U9","SGP41-D-R4","Xerolux-Air","DFN-6_L2.4-W2.4-P0.80-TL-EP",40.5,101.5,0,{1:"SGP_VDD",2:"GND",3:"I2C_SDA",4:"GND",5:"AIR_3V3",6:"I2C_SCL",7:"GND"})
        p("U10","BMP390","Xerolux-Air","LGA-10_L2.0-W2.0-P0.50-BL",46,101.5,0,{1:"AIR_3V3",2:"I2C_SCL",3:"GND",4:"I2C_SDA",5:"GND",6:"AIR_3V3",8:"GND",9:"GND",10:"AIR_3V3"})
        p("U11","AP2112K-3.3 AIR","Package_TO_SOT_SMD","SOT-23-5",64,101,0,{1:"SYS_5V",2:"GND",3:"SYS_5V",5:"AIR_3V3"})
        for ref,val,x,y,pins in [
            ("C22","100n",35,92.5,{1:"AIR_3V3",2:"GND"}),("C23","4.7u",39,92.5,{1:"AIR_3V3",2:"GND"}),
            ("C24","1u",43,92.5,{1:"SGP_VDD",2:"GND"}),("C25","1u",47,92.5,{1:"AIR_3V3",2:"GND"}),
            ("C26","100n",51,92.5,{1:"AIR_3V3",2:"GND"}),("C27","100n",55,92.5,{1:"AIR_3V3",2:"GND"}),
            ("C28","10u",59,92.5,{1:"SYS_5V",2:"GND"}),("C29","22u",63,92.5,{1:"AIR_3V3",2:"GND"}),
        ]: p(ref,val,"Capacitor_SMD","C_0805_2012Metric",x,y,0,pins)
        p("R26","10R","Resistor_SMD","R_0603_1608Metric",38,96,90,{1:"AIR_3V3",2:"SGP_VDD"})
        p("C30","220u 10V","Capacitor_SMD","CP_Elec_8x10",77 if air_r2 else 126,92 if air_r2 else 99,0,{1:"SYS_5V",2:"GND"})
        p("TP13","AIR_3V3","TestPoint","TestPoint_Plated_Hole_D2.0mm",55,104,0,{1:"AIR_3V3"})
    if modular:
        slot_pins={1:"GND",2:"SYS_5V",3:"I2C_SDA",4:"I2C_SCL",5:"I2C_SCL",6:"I2C_SDA",7:"SYS_5V",8:"GND"}
        for ref,x,label in (("J9",25,"CO2"),("J10",53,"VOC-NOx"),("J11",81,"PRESSURE")):
            p(ref,f"AIR-SLOT {label}","Connector_PinHeader_2.54mm","PinHeader_2x04_P2.54mm_Vertical",x,98,0,slot_pins)
        p("C30","220u 10V","Capacitor_SMD","CP_Elec_8x10",128,94,0,{1:"SYS_5V",2:"GND"})
    for spec in P: add_part(b,nets,spec)
    tp_positions=((22,38),(30,38),(38,38),(46,39),(54,40),(62,40),(70,38),(83,35),(86,31),(94,31),(102,31),(91,35) if extended else (110,28))
    for idx,(net,(x,y)) in enumerate(zip(("24V_RAW","24V_PROT","SYS_5V","+3V3","I2C_SDA","I2C_SCL","RH_OUT","TEMP_KTY","RS485_A","RS485_B","RS485_COM","GND"),tp_positions),1):
        add_part(b,nets,(f"TP{idx}",net,"TestPoint","TestPoint_Plated_Hole_D2.0mm",x,y,0,{"1":net}))
    for ref,x,y in (("H1",14,14),("H2",115 if extended else right-4,35 if extended else 14),("H3",14,bottom-4),("H4",right-4,bottom-4)):
        fp=load("MountingHole","MountingHole_3.2mm_M3"); fp.SetReference(ref); fp.SetPosition(point(x,y)); b.Add(fp)
    for layer in (pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu): keepout(b,layer,((45.7,10.1),(64.3,10.1),(64.3,17.0),(45.7,17.0)))
    text(b,"SMART CLIMATE SENSOR",35 if extended else 83,20 if extended else 12,1.1); text(b,f"by Xerolux | xerolux.de | REV {revision} | 2026",35 if extended else 83,22.5 if extended else 14.5,.65)
    text(b,"USB-C FLASH / POWER",75 if extended else 72,102 if air else (82 if extended else bottom-5),.65); text(b,"RS485 ISOLATED",130 if extended else 105,68 if extended else bottom-3,.65)
    text(b,"43 TEMP | 42 +6-32V | 41 GND | 40 RH" if air_r2 else "43 TEMP | 42 +24V | 41 GND | 40 RH",40 if extended else 37,84 if extended else bottom-2,.65); text(b,"ENGINEERING SAMPLE - BENCH TEST FIRST",57,33,.7)
    if extended:
        text(b,"PUSH-IN FIELD I/O - NO USER SOLDERING",108,35,.65)
        text(b,"1W-A: 3V DQ GND",84,22.5,.55); text(b,"1W-B: 3V DQ GND",104,22.5,.55)
        text(b,"DI1 COM DI2",126,22.5,.55); text(b,"A B COM SH",128,61,.55)
        text(b,"0-10V IN | GND",127,84,.55); text(b,"SERVICE",108,82,.55); text(b,"TERM",122,69,.55)
    if air:
        text(b,"SCD41 CO2",29,108,.55); text(b,"SGP41 VOC/NOx | BMP390 hPa",44,106.8,.55)
        text(b,"ULTIMATE AIR - SENSOR ISLAND",45,89.8,.65)
    if air_r2:
        text(b,"RELAY: COM NO NC - SELV ONLY",121,101,.55)
        text(b,"GPIO21 LED ENABLE | GPIO3 RELAY",88,103.5,.48)
    if modular:
        text(b,"AIR-SLOT 1 CO2",25,88,.65); text(b,"AIR-SLOT 2 VOC/NOx",53,88,.65)
        text(b,"AIR-SLOT 3 PRESSURE",81,88,.65)
        text(b,"MODULES MAY BE ROTATED 180deg - SYMMETRIC SAFE PINOUT",53,106,.55)
    d=b.GetDesignSettings(); d.m_MinClearance=mm(.2); d.m_TrackMinWidth=mm(.15); d.SetCustomTrackWidth(mm(.25)); d.SetCustomViaSize(mm(.7)); d.SetCustomViaDrill(mm(.3))
    return b


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("output",type=Path); ap.add_argument("--revision",choices=("B-ES2-C6","B-ES3-C6","B-ES4-AIR","B-ES4-AIR-R2","B-ES5-MODULAR"),default="B-ES2-C6"); a=ap.parse_args(); a.output.parent.mkdir(parents=True,exist_ok=True); pcbnew.SaveBoard(str(a.output),build(a.revision))


if __name__=="__main__": main()
