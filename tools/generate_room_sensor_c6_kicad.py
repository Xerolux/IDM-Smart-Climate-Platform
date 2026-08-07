#!/usr/bin/env python3
"""Generate the B-ES2-C6 native KiCad schematic."""

from __future__ import annotations

import argparse
from pathlib import Path

from kiutils.items.common import Effects, Font, Position, TitleBlock
from kiutils.items.schitems import LocalLabel, Text

from generate_fake_sensor_kicad import Builder, uid


GRID = 1.27


class C6Builder(Builder):
    """Place every connection on-grid and attach labels directly to pins.

    Direct labels avoid the crossing label stubs that can silently merge nets in
    a dense generated schematic.
    """

    def add_label(self, net: str, point: tuple[float, float], pin_angle: float) -> None:
        key = (net, point[0], point[1])
        if key in self._labels:
            return
        self._labels.add(key)
        self.sch.labels.append(
            LocalLabel(
                text=net,
                position=Position(point[0], point[1], int(pin_angle or 0) % 360),
                effects=Effects(font=Font(height=1.0, width=1.0)),
                uuid=uid(),
            )
        )

    def add(self, **kwargs) -> None:
        x, y = kwargs["center"]
        kwargs["center"] = (round(x / GRID) * GRID, round(y / GRID) * GRID)
        super().add(**kwargs)


def title(builder: Builder, text: str, x: float, y: float, size: float = 1.4) -> None:
    builder.sch.texts.append(Text(text=text, position=Position(x, y, 0),
        effects=Effects(font=Font(height=size, width=size, bold=True)), uuid=uid()))


def add_passive(builder: Builder, ref: str, kind: str, center, value: str,
                footprint: str, nets: dict[str, str], datasheet: str = "~") -> None:
    builder.add(reference=ref, nickname="Device", entry=kind, center=center,
        value=value, footprint=footprint, datasheet=datasheet, nets=nets)


def build():
    b = C6Builder()
    b.sch.titleBlock = TitleBlock(
        title="IDM Room Sensor B-ES2-C6 - USB-C / RS-485 / 0-10 V",
        date="2026-08-07", revision="B-ES2-C6",
        company="IDM Smart Climate Platform",
        comments={
            1: "ENGINEERING SAMPLE - BENCH VALIDATION REQUIRED BEFORE IDM CONNECTION",
            2: "ESP32-C6-WROOM-1-N16; USB-C; isolated Modbus RS-485",
            3: "SHT45 room sensing; passive KTY81/210; active 0-10 V humidity output",
        },
    )
    title(b, "B-ES2-C6 MULTIPROTOCOL ROOM SENSOR", 90, 17, 2.0)
    title(b, "24 V / IDM interface and protected 5 V supply", 35, 35)
    title(b, "ESP32-C6, USB-C and local sensing", 145, 35)
    title(b, "0-10 V and isolated RS-485", 245, 35)

    b.add(reference="J1", nickname="Connector_Generic", entry="Conn_01x04",
        center=(25, 58), value="1-2834011-4 / IDM 43 TEMP / 42 +24V / 41 GND / 40 RH",
        footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",
        datasheet="https://www.te.com/usa-en/product-1-2834011-4.html",
        nets={"1":"TEMP_KTY", "2":"24V_RAW", "3":"GND", "4":"RH_OUT"})
    b.add(reference="RTH1", nickname="Sensor_Temperature", entry="KTY81",
        center=(25, 82), value="KTY81/210,112", footprint="Package_TO_SOT_THT:TO-92_Inline",
        datasheet="https://www.nxp.com/docs/en/data-sheet/KTY81_SER.pdf",
        nets={"1":"TEMP_KTY", "2":"GND"})
    add_passive(b, "F1", "Polyfuse", (50,58), "1812L050/30PR 500mA", "Fuse:Fuse_1812_4532Metric", {"1":"24V_RAW","2":"24V_FUSED"})
    add_passive(b, "D1", "D_Schottky", (70,58), "SS16 60V", "Diode_SMD:D_SMA", {"1":"24V_PROT","2":"24V_FUSED"})
    add_passive(b, "TVS1", "D_TVS", (70,82), "SMBJ33A", "Diode_SMD:D_SMB", {"1":"GND","2":"24V_PROT"})
    b.add(reference="U1", nickname="Regulator_Switching", entry="LMR36510ADDA",
        center=(100,58), value="LMR36510ADDAR 24V-to-5V", footprint="Package_SO:TI_SO-PowerPAD-8_ThermalVias",
        datasheet="https://www.ti.com/lit/ds/symlink/lmr36510.pdf",
        nets={"1":"GND","2":"24V_PROT","3":"24V_PROT","4":"PWR_GOOD","5":"BUCK_FB","6":"VCC_BYP","7":"BOOT","8":"SW","9":"GND"})
    add_passive(b,"L1","L",(125,58),"SRP1038A-330M 33uH","Inductor_SMD:L_10.4x10.4_H4.8",{"1":"SW","2":"5V_BUCK"})
    for spec in [
        ("R1",(110,82),"100k 1%",{"1":"5V_BUCK","2":"BUCK_FB"}),
        ("R2",(125,82),"24.9k 1%",{"1":"BUCK_FB","2":"GND"}),
        ("R3",(140,82),"100k",{"1":"PWR_GOOD","2":"5V_BUCK"}),
    ]: add_passive(b,spec[0],"R",spec[1],spec[2],"Resistor_SMD:R_0603_1608Metric",spec[3])
    for ref,center,value,fp,nets in [
        ("C1",(82,82),"4.7u 100V","Capacitor_SMD:C_1210_3225Metric",{"1":"24V_PROT","2":"GND"}),
        ("C2",(92,82),"220n 100V","Capacitor_SMD:C_0805_2012Metric",{"1":"24V_PROT","2":"GND"}),
        ("C3",(100,82),"1u 16V","Capacitor_SMD:C_0805_2012Metric",{"1":"VCC_BYP","2":"GND"}),
        ("C4",(115,95),"100n 16V","Capacitor_SMD:C_0603_1608Metric",{"1":"BOOT","2":"SW"}),
        ("C5",(130,95),"47u 10V","Capacitor_SMD:C_1206_3216Metric",{"1":"5V_BUCK","2":"GND"}),
        ("C6",(145,95),"47u 10V","Capacitor_SMD:C_1206_3216Metric",{"1":"5V_BUCK","2":"GND"}),
    ]: add_passive(b,ref,"C",center,value,fp,nets)
    add_passive(b,"D2","D_Schottky",(155,58),"SS14","Diode_SMD:D_SMA",{"1":"SYS_5V","2":"5V_BUCK"})
    add_passive(b,"D3","D_Schottky",(155,72),"SS14","Diode_SMD:D_SMA",{"1":"SYS_5V","2":"USB_5V"})
    b.add(reference="U2", nickname="Regulator_Linear", entry="AP2112K-3.3",
        center=(180,58), value="AP2112K-3.3TRG1", footprint="Package_TO_SOT_SMD:SOT-23-5",
        datasheet="https://www.diodes.com/assets/Datasheets/AP2112.pdf",
        nets={"1":"SYS_5V","2":"GND","3":"SYS_5V","5":"+3V3"}, no_connect={"4"})
    add_passive(b,"C7","C",(175,82),"10u 10V","Capacitor_SMD:C_0805_2012Metric",{"1":"SYS_5V","2":"GND"})
    add_passive(b,"C8","C",(190,82),"22u 6.3V","Capacitor_SMD:C_0805_2012Metric",{"1":"+3V3","2":"GND"})

    c6_nets={"1":"GND","2":"+3V3","3":"C6_EN","4":"EXP_GPIO4","5":"EXP_GPIO5",
        "6":"I2C_SDA","7":"I2C_SCL","10":"STATUS_LED","13":"USB_D-","14":"USB_D+",
        "15":"C6_BOOT","21":"ONEWIRE","24":"RS485_RX","25":"RS485_TX","27":"RS485_DE",
        "28":"GND","29":"GND"}
    c6_nc={str(n) for n in range(1,31)}-set(c6_nets)
    b.add(reference="U3", nickname="Connector_Generic", entry="Conn_02x15_Odd_Even",
        center=(150,125), value="ESP32-C6-WROOM-1-N16 (pins per Espressif datasheet)",
        footprint="Custom:ESP32-C6-WROOM-1", datasheet="https://documentation.espressif.com/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf",
        nets=c6_nets, no_connect=c6_nc)
    b.add(reference="J3", nickname="Connector", entry="USB_C_Receptacle_USB2.0_16P",
        center=(95,125), value="TYPE-C-31-M-12", footprint="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
        datasheet="https://jlcpcb.com/partdetail/C165948",
        nets={"A1":"GND","A4":"USB_5V","A5":"USB_CC1","A6":"USB_D+","A7":"USB_D-","A9":"USB_5V","A12":"GND",
              "B1":"GND","B4":"USB_5V","B5":"USB_CC2","B6":"USB_D+","B7":"USB_D-","B9":"USB_5V","B12":"GND","SH":"GND"},
        no_connect={"A8","B8"})
    b.add(reference="ESD1", nickname="Power_Protection", entry="USBLC6-2SC6", center=(95,155),
        value="USBLC6-2SC6", footprint="Package_TO_SOT_SMD:SOT-23-6", datasheet="https://jlcpcb.com/partdetail/USBLC6-2SC6/C2827654",
        nets={"1":"USB_D-","2":"GND","3":"USB_D+","4":"USB_D+","5":"USB_5V","6":"USB_D-"})
    for ref,y,net in [("R4",125,"USB_CC1"),("R5",137,"USB_CC2")]:
        add_passive(b,ref,"R",(70,y),"5.1k 1%","Resistor_SMD:R_0603_1608Metric",{"1":net,"2":"GND"})
    add_passive(b,"R6","R",(175,115),"10k","Resistor_SMD:R_0603_1608Metric",{"1":"+3V3","2":"C6_EN"})
    add_passive(b,"C9","C",(185,115),"1u","Capacitor_SMD:C_0603_1608Metric",{"1":"C6_EN","2":"GND"})
    for ref,center,value,net in [("SW1",(180,135),"RESET","C6_EN"),("SW2",(180,150),"BOOT","C6_BOOT")]:
        b.add(reference=ref,nickname="Switch",entry="SW_Push",center=center,value=value,
            footprint="Button_Switch_SMD:SW_SPST_B3U-1000P",datasheet="~",nets={"1":net,"2":"GND"})

    b.add(reference="U4", nickname="Sensor_Humidity", entry="SHT4x", center=(220,125),
        value="SHT45-AD1B-R2", footprint="Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad",
        datasheet="https://sensirion.com/media/documents/33FD6951/662A593A/Datasheet_SHT4x.pdf",
        nets={"1":"I2C_SDA","2":"I2C_SCL","3":"+3V3","4":"GND"})
    for ref,y,net in [("R7",120,"I2C_SDA"),("R8",132,"I2C_SCL")]:
        add_passive(b,ref,"R",(245,y),"4.7k","Resistor_SMD:R_0603_1608Metric",{"1":"+3V3","2":net})
    add_passive(b,"C10","C",(220,150),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"+3V3","2":"GND"})

    b.add(reference="U5",nickname="Analog_DAC",entry="MCP4725xxx-xCH",center=(220,58),value="MCP4725A0T-E/CH",
        footprint="Package_TO_SOT_SMD:SOT-23-6",datasheet="https://ww1.microchip.com/downloads/en/DeviceDoc/MCP4725-Data-Sheet-20002039E.pdf",
        nets={"1":"DAC_RAW","2":"GND","3":"+3V3","4":"I2C_SDA","5":"I2C_SCL","6":"GND"})
    b.add(reference="U6",nickname="Amplifier_Operational",entry="OPA197xDBV",center=(255,58),value="OPA197IDBVR",
        footprint="Package_TO_SOT_SMD:SOT-23-5",datasheet="https://www.ti.com/lit/ds/symlink/opa197.pdf",
        nets={"1":"OPAMP_OUT","2":"GND","3":"DAC_RAW","4":"OPAMP_FB","5":"24V_PROT"})
    for ref,center,value,nets in [
        ("R9",(270,78),"21k 1% CAL",{"1":"OPAMP_OUT","2":"OPAMP_FB"}),
        ("R10",(250,90),"10k 0.1%",{"1":"OPAMP_FB","2":"GND"}),
        ("R11",(285,58),"220R",{"1":"OPAMP_OUT","2":"RH_OUT"}),
    ]: add_passive(b,ref,"R",center,value,"Resistor_SMD:R_0603_1608Metric",nets)
    add_passive(b,"C11","C",(230,82),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"+3V3","2":"GND"})
    add_passive(b,"C12","C",(270,95),"100n 50V","Capacitor_SMD:C_0603_1608Metric",{"1":"24V_PROT","2":"GND"})
    add_passive(b,"C13","C",(290,82),"100n 50V","Capacitor_SMD:C_0603_1608Metric",{"1":"RH_OUT","2":"GND"})

    b.add(reference="U7",nickname="Connector_Generic",entry="Conn_02x08_Odd_Even",center=(245,130),value="CA-IS3092W",
        footprint="Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm",datasheet="https://e.chipanalog.com/Public/Uploads/uploadfile/files/20250818/CAIS30923098datasheetVersion1.13en202412162.pdf",
        nets={"1":"+3V3","2":"GND","3":"RS485_RX","4":"RS485_DE","5":"RS485_DE","6":"RS485_TX","8":"GND",
              "9":"RS485_COM","10":"RS485_COM","12":"RS485_A","13":"RS485_B","15":"RS485_COM","16":"VISO"},
        no_connect={"7","11","14"})
    for ref,center,value,nets in [
        ("C14",(235,160),"100n",{"1":"+3V3","2":"GND"}),
        ("C16",(255,160),"10u",{"1":"+3V3","2":"GND"}),
        ("C17",(270,145),"100n",{"1":"VISO","2":"RS485_COM"}),
        ("C18",(285,145),"10u",{"1":"VISO","2":"RS485_COM"}),
    ]: add_passive(b,ref,"C",center,value,"Capacitor_SMD:C_0805_2012Metric",nets)
    b.add(reference="J2",nickname="Connector_Generic",entry="Conn_01x04",center=(305,130),value="1-2834011-4 / RS485 A / B / COM / SHIELD",
        footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",datasheet="https://www.te.com/usa-en/product-1-2834011-4.html",
        nets={"1":"RS485_A","2":"RS485_B","3":"RS485_COM","4":"RS485_SHIELD"})
    add_passive(b,"R12","R",(300,155),"120R termination","Resistor_SMD:R_1206_3216Metric",{"1":"RS485_A","2":"RS485_TERM"})
    b.add(reference="JP1",nickname="Jumper",entry="Jumper_2_Open",center=(315,155),value="RS485 TERM ENABLE",
        footprint="Jumper:SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm",datasheet="~",nets={"1":"RS485_TERM","2":"RS485_B"})

    b.add(reference="J4",nickname="Connector_Generic",entry="Conn_01x08",center=(145,180),value="EXPANSION",
        footprint="Connector_JST:JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal",datasheet="~",
        nets={"1":"+3V3","2":"GND","3":"I2C_SDA","4":"I2C_SCL","5":"ONEWIRE","6":"EXP_GPIO4","7":"EXP_GPIO5","8":"SYS_5V"})
    add_passive(b,"LED1","LED",(195,180),"STATUS GREEN","LED_SMD:LED_0603_1608Metric",{"1":"STATUS_LED_R","2":"GND"})
    add_passive(b,"R13","R",(180,180),"1k","Resistor_SMD:R_0603_1608Metric",{"1":"STATUS_LED","2":"STATUS_LED_R"})

    for idx,net in enumerate(("24V_RAW","24V_PROT","SYS_5V","+3V3","I2C_SDA","I2C_SCL","RH_OUT","TEMP_KTY","RS485_A","RS485_B","RS485_COM","GND"),1):
        b.add(reference=f"TP{idx}",nickname="Connector_Generic",entry="Conn_01x01",center=(20+idx*22,205),value=net,
            footprint="TestPoint:TestPoint_Plated_Hole_D2.0mm",datasheet="~",nets={"1":net})
    for idx,net in enumerate(("24V_PROT","SYS_5V","GND","RS485_COM"),1):
        b.add(reference=f"#FLG0{idx}",nickname="power",entry="PWR_FLAG",center=(40+idx*18,220),value="PWR_FLAG",
            footprint="",datasheet="~",nets={"1":net},in_bom=False,on_board=False)
    return b.sch


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("output",type=Path); args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True); build().to_file(args.output,encoding="utf-8")


if __name__ == "__main__": main()
