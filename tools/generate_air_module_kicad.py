#!/usr/bin/env python3
"""Generate native KiCad schematics for Xerolux AIR-SLOT sensor modules."""

from __future__ import annotations

import argparse
from pathlib import Path

from kiutils.items.common import Effects, Font, Position, TitleBlock
from kiutils.items.schitems import Text

from generate_fake_sensor_kicad import Builder, uid


def label(builder: Builder, value: str, x: float, y: float, size: float = 1.5) -> None:
    builder.sch.texts.append(Text(text=value, position=Position(x, y, 0),
        effects=Effects(font=Font(height=size, width=size, bold=True)), uuid=uid()))


def passive(builder: Builder, ref: str, kind: str, center, value: str, footprint: str, nets) -> None:
    builder.add(reference=ref, nickname="Device", entry=kind, center=center,
        value=value, footprint=footprint, datasheet="~", nets=nets)


def build(variant: str):
    names = {"CO2": "SCD41 CO2", "VOCNOX": "SGP41 VOC/NOx", "PRESSURE": "BMP390 PRESSURE"}
    b = Builder()
    b.sch.titleBlock = TitleBlock(
        title=f"Xerolux AIR-SLOT {names[variant]} module",
        date="2026-08-08", revision="A-ES1", company="Xerolux",
        comments={1: "B-ES5-MODULAR plug-in module", 2: "180-degree rotation-safe symmetric connector"},
    )
    label(b, f"XEROLUX AIR-SLOT / {names[variant]}", 90, 25, 2.0)
    slot = {"1":"GND", "2":"SLOT_5V", "3":"I2C_SDA", "4":"I2C_SCL",
            "5":"I2C_SCL", "6":"I2C_SDA", "7":"SLOT_5V", "8":"GND"}
    b.add(reference="J1", nickname="Connector_Generic", entry="Conn_02x04_Odd_Even",
        center=(45,65), value="XEROLUX AIR-SLOT / ROTATION SAFE",
        footprint="Connector_PinSocket_2.54mm:PinSocket_2x04_P2.54mm_Vertical",
        datasheet="~", nets=slot)
    power_flags = [("SLOT_5V", 25), ("GND", 225)]
    for index, (net, x) in enumerate(power_flags, 1):
        b.add(reference=f"#FLG0{index}", nickname="power", entry="PWR_FLAG",
            center=(x,130), value="PWR_FLAG", footprint="", datasheet="~",
            nets={"1":net}, in_bom=False, on_board=False)

    if variant == "CO2":
        b.add(reference="U1", nickname="Sensor_Gas", entry="SCD41-D-R2", center=(110,65),
            value="SCD41-D-R1", footprint="Xerolux-Air:SENSOR-SMD_SCD41-D-R1",
            datasheet="https://sensirion.com/resource/datasheet/scd4x",
            nets={"6":"GND","7":"MOD_3V3","9":"I2C_SCL","10":"I2C_SDA",
                  "19":"MOD_3V3","20":"GND","21":"GND"})
        b.add(reference="U2", nickname="Regulator_Linear", entry="AP2112K-3.3", center=(50,115),
            value="AP2112K-3.3TRG1", footprint="Package_TO_SOT_SMD:SOT-23-5",
            datasheet="https://www.diodes.com/assets/Datasheets/AP2112.pdf",
            nets={"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"}, no_connect={"4"})
        passive(b,"C1","C",(105,105),"10u","Capacitor_SMD:C_0805_2012Metric",{"1":"SLOT_5V","2":"GND"})
        passive(b,"C2","C",(125,105),"22u","Capacitor_SMD:C_0805_2012Metric",{"1":"MOD_3V3","2":"GND"})
        passive(b,"C3","C",(145,105),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"MOD_3V3","2":"GND"})
    elif variant == "VOCNOX":
        b.add(reference="U1", nickname="Connector_Generic", entry="Conn_01x07", center=(110,65),
            value="SGP41-D-R4", footprint="Xerolux-Air:DFN-6_L2.4-W2.4-P0.80-TL-EP",
            datasheet="https://sensirion.com/resource/datasheet/sgp41",
            nets={"1":"SGP_VDD","2":"GND","3":"I2C_SDA","4":"GND",
                  "5":"MOD_3V3","6":"I2C_SCL","7":"GND"})
        b.add(reference="U2", nickname="Regulator_Linear", entry="AP2112K-3.3", center=(50,115),
            value="AP2112K-3.3TRG1", footprint="Package_TO_SOT_SMD:SOT-23-5",
            datasheet="https://www.diodes.com/assets/Datasheets/AP2112.pdf",
            nets={"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"}, no_connect={"4"})
        passive(b,"R1","R",(85,105),"10R","Resistor_SMD:R_0603_1608Metric",{"1":"MOD_3V3","2":"SGP_VDD"})
        passive(b,"C1","C",(115,105),"1u","Capacitor_SMD:C_0805_2012Metric",{"1":"SGP_VDD","2":"GND"})
        passive(b,"C2","C",(145,105),"1u","Capacitor_SMD:C_0805_2012Metric",{"1":"MOD_3V3","2":"GND"})
        passive(b,"C3","C",(175,105),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"MOD_3V3","2":"GND"})
        passive(b,"C4","C",(100,130),"10u","Capacitor_SMD:C_0805_2012Metric",{"1":"SLOT_5V","2":"GND"})
        passive(b,"C5","C",(140,130),"22u","Capacitor_SMD:C_0805_2012Metric",{"1":"MOD_3V3","2":"GND"})
    else:
        b.add(reference="U1", nickname="Connector_Generic", entry="Conn_02x05_Odd_Even", center=(110,65),
            value="BMP390", footprint="Xerolux-Air:LGA-10_L2.0-W2.0-P0.50-BL",
            datasheet="https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp390/",
            nets={"1":"MOD_3V3","2":"I2C_SCL","3":"GND","4":"I2C_SDA","5":"GND",
                  "6":"MOD_3V3","8":"GND","9":"GND","10":"MOD_3V3"}, no_connect={"7"})
        b.add(reference="U2", nickname="Regulator_Linear", entry="AP2112K-3.3", center=(50,115),
            value="AP2112K-3.3TRG1", footprint="Package_TO_SOT_SMD:SOT-23-5",
            datasheet="https://www.diodes.com/assets/Datasheets/AP2112.pdf",
            nets={"1":"SLOT_5V","2":"GND","3":"SLOT_5V","5":"MOD_3V3"}, no_connect={"4"})
        passive(b,"C1","C",(95,105),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"MOD_3V3","2":"GND"})
        passive(b,"C2","C",(125,105),"100n","Capacitor_SMD:C_0603_1608Metric",{"1":"MOD_3V3","2":"GND"})
        passive(b,"C3","C",(155,105),"10u","Capacitor_SMD:C_0805_2012Metric",{"1":"SLOT_5V","2":"GND"})
        passive(b,"C4","C",(185,105),"22u","Capacitor_SMD:C_0805_2012Metric",{"1":"MOD_3V3","2":"GND"})
    return b.sch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--variant", choices=("CO2","VOCNOX","PRESSURE"), required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(args.variant).to_file(args.output, encoding="utf-8")


if __name__ == "__main__":
    main()
