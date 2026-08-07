#!/usr/bin/env python3
"""Generate native KiCad 10 schematics for Classic and ESP room sensors."""

from __future__ import annotations

import argparse
from pathlib import Path

from kiutils.items.common import Effects, Font, Position, TitleBlock
from kiutils.items.schitems import Text

from generate_fake_sensor_kicad import Builder, uid


def add_text(builder: Builder, text: str, x: float, y: float, size=1.4) -> None:
    builder.sch.texts.append(
        Text(
            text=text,
            position=Position(x, y, 0),
            effects=Effects(font=Font(height=size, width=size, bold=True)),
            uuid=uid(),
        )
    )


def add_power_input(builder: Builder) -> None:
    builder.add(
        reference="J1", nickname="Connector_Generic", entry="Conn_01x04",
        center=(30.48, 63.5), value="IDM / BENCH INTERFACE",
        footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",
        datasheet="https://www.phoenixcontact.com/en-de/products/pcb-terminal-block-pt-15-4-35-h-1984633",
        nets={"1": "TEMP_KTY", "2": "24V_RAW", "3": "GND", "4": "RH_OUT"},
    )
    builder.add(
        reference="RTH1", nickname="Sensor_Temperature", entry="KTY81",
        center=(30.48, 91.44), value="KTY81/210",
        footprint="Package_TO_SOT_THT:TO-92_Inline",
        datasheet="https://www.nxp.com/docs/en/data-sheet/KTY81_SER.pdf",
        nets={"1": "TEMP_KTY", "2": "GND"},
    )
    builder.add(
        reference="F1", nickname="Device", entry="Fuse", center=(55.88, 63.5),
        value="500mA 5x20mm fuse",
        footprint="Fuse:Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal",
        datasheet="https://www.littelfuse.com/assetdocs/littelfuse-5x20mm-glass-fuse-217-datasheet",
        nets={"1": "24V_RAW", "2": "24V_FUSED"},
    )
    builder.add(
        reference="D1", nickname="Device", entry="D_Schottky", center=(86.36, 63.5),
        value="SS16-E3/61T", footprint="Diode_SMD:D_SMA",
        datasheet="https://www.vishay.com/docs/88746/ss12.pdf",
        nets={"1": "24V_PROT", "2": "24V_FUSED"},
    )
    builder.add(
        reference="U1", nickname="Regulator_Linear", entry="L7805", center=(121.92, 63.5),
        value="TSR 1-2450", footprint="Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT",
        datasheet="https://www.tracopower.com/tsr1-datasheet",
        nets={"1": "24V_PROT", "2": "GND", "3": "+5V"},
    )
    for ref, center, value, footprint, nets, datasheet in [
        ("C1", (83.82, 91.44), "22u 50V X7R", "Capacitor_SMD:C_1210_3225Metric", {"1": "24V_PROT", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71H226KE15-01.pdf"),
        ("C2", (101.6, 91.44), "100n 50V X7R", "Capacitor_SMD:C_0603_1608Metric", {"1": "24V_PROT", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf"),
        ("C3", (121.92, 91.44), "10u 10V X7R", "Capacitor_SMD:C_0805_2012Metric", {"1": "+5V", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71A106KE51-01.pdf"),
    ]:
        builder.add(reference=ref, nickname="Device", entry="C", center=center, value=value, footprint=footprint, datasheet=datasheet, nets=nets)


def add_sht_dac_output(builder: Builder, x_offset: float = 0.0) -> None:
    builder.add(
        reference="U3", nickname="Sensor_Humidity", entry="SHT4x",
        center=(160.02 + x_offset, 91.44), value="SHT45-AD1B-R2",
        footprint="Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad",
        datasheet="https://sensirion.com/media/documents/33FD6951/662A593A/Datasheet_SHT4x.pdf",
        nets={"1": "I2C_SDA", "2": "I2C_SCL", "3": "+3V3", "4": "GND"},
    )
    builder.add(
        reference="U4", nickname="Analog_DAC", entry="MCP4725xxx-xCH",
        center=(198.12 + x_offset, 68.58), value="MCP4725A0T-E/CH",
        footprint="Package_TO_SOT_SMD:SOT-23-6",
        datasheet="https://ww1.microchip.com/downloads/en/DeviceDoc/MCP4725-Data-Sheet-20002039E.pdf",
        nets={"1": "DAC_RAW", "2": "GND", "3": "+3V3", "4": "I2C_SDA", "5": "I2C_SCL", "6": "GND"},
    )
    builder.add(
        reference="U5", nickname="Amplifier_Operational", entry="OPA197xDBV",
        center=(238.76 + x_offset, 68.58), value="OPA197IDBVR",
        footprint="Package_TO_SOT_SMD:SOT-23-5",
        datasheet="https://www.ti.com/lit/ds/symlink/opa197.pdf",
        nets={"1": "OPAMP_OUT", "2": "GND", "3": "DAC_RAW", "4": "OPAMP_FB", "5": "24V_PROT"},
    )
    for ref, center, value, nets, mpn in [
        ("R1", (175.26 + x_offset, 111.76), "4.7k", {"1": "+3V3", "2": "I2C_SDA"}, "RC0603FR-074K7L"),
        ("R2", (187.96 + x_offset, 111.76), "4.7k", {"1": "+3V3", "2": "I2C_SCL"}, "RC0603FR-074K7L"),
        ("R3", (251.46 + x_offset, 88.9), "20.3k 0.1%", {"1": "OPAMP_OUT", "2": "OPAMP_FB"}, "ERA-3AEB2032V"),
        ("R4", (238.76 + x_offset, 111.76), "10k 0.1%", {"1": "OPAMP_FB", "2": "GND"}, "ERA-3AEB103V"),
        ("R5", (274.32 + x_offset, 68.58), "220R 1%", {"1": "OPAMP_OUT", "2": "RH_OUT"}, "RC0603FR-07220RL"),
    ]:
        builder.add(reference=ref, nickname="Device", entry="R", center=center, value=value,
                    footprint="Resistor_SMD:R_0603_1608Metric", datasheet="~", nets=nets)
    for ref, center, value, nets in [
        ("C4", (160.02 + x_offset, 111.76), "100n 16V X7R", {"1": "+3V3", "2": "GND"}),
        ("C5", (223.52 + x_offset, 111.76), "100n 50V X7R", {"1": "24V_PROT", "2": "GND"}),
        ("C6", (274.32 + x_offset, 101.6), "100n 50V X7R", {"1": "RH_OUT", "2": "GND"}),
    ]:
        builder.add(reference=ref, nickname="Device", entry="C", center=center, value=value,
                    footprint="Capacitor_SMD:C_0603_1608Metric", datasheet="~", nets=nets)


def build(variant: str):
    b = Builder()
    display = "Classic" if variant == "classic" else "ESP"
    b.sch.titleBlock = TitleBlock(
        title=f"IDM Room Sensor {display} - engineering sample",
        date="2026-08-07", revision="B-ES1", company="IDM Smart Climate Platform",
        comments={
            1: "BENCH TEST FIRST - IDM CONNECTION ONLY AFTER INTERFACE VALIDATION",
            2: "KTY81/210 passive temperature path; 0-10 V active humidity path",
            3: "24 V nominal engineering sample",
        },
    )
    add_text(b, f"REV B-ES1: {display.upper()} ROOM SENSOR ENGINEERING SAMPLE", 85, 20.32, 2.0)
    add_text(b, "WARNING: validate KTY and 0-10 V interfaces on dummy loads before IDM connection", 85, 25.4, 1.1)
    add_text(b, "24 V input protection and passive KTY path", 28, 40.64)
    add_text(b, "Local humidity acquisition and 0-10 V output", 175, 40.64)
    add_power_input(b)

    if variant == "classic":
        b.add(
            reference="U2", nickname="MCU_Microchip_ATtiny", entry="ATtiny1616-S",
            center=(152.4, 63.5), value="ATtiny1616-SNR",
            footprint="Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm",
            datasheet="https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/ATtiny1614-16-17-DataSheet-DS40002204A.pdf",
            nets={"1": "+3V3", "20": "GND", "16": "UPDI", "17": "I2C_SDA", "18": "I2C_SCL"},
            no_connect={str(n) for n in range(1, 21)} - {"1", "20", "16", "17", "18"},
        )
        b.add(
            reference="U6", nickname="Regulator_Linear", entry="AP2112K-3.3",
            center=(137.16, 111.76), value="AP2112K-3.3TRG1",
            footprint="Package_TO_SOT_SMD:SOT-23-5",
            datasheet="https://www.diodes.com/assets/Datasheets/AP2112.pdf",
            nets={"1": "+5V", "2": "GND", "3": "+5V", "5": "+3V3"}, no_connect={"4"},
        )
        b.add(
            reference="J2", nickname="Connector_Generic", entry="Conn_01x03",
            center=(137.16, 134.62), value="UPDI",
            footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
            datasheet="~", nets={"1": "+3V3", "2": "UPDI", "3": "GND"},
        )
        add_sht_dac_output(b)
    else:
        esp_nets = {
            "1": "GND", "2": "+3V3", "3": "+3V3", "6": "GND", "8": "GND",
            "12": "GND", "13": "+5V", "14": "+5V", "15": "GND", "16": "GND",
            "19": "GND", "24": "GND", "25": "I2C_SDA", "26": "I2C_SCL",
            "27": "GND", "30": "GND",
        }
        b.add(
            reference="A1", nickname="RF_Module", entry="ESP32-C3-DevKitM-1",
            center=(152.4, 63.5), value="ESP32-C3-DevKitM-1",
            footprint="RF_Module:ESP32-C3-DevKitM-1",
            datasheet="https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html",
            nets=esp_nets, no_connect={str(n) for n in range(1, 31)} - set(esp_nets),
        )
        add_sht_dac_output(b)

    for index, net in enumerate(("24V_RAW", "24V_PROT", "+5V", "+3V3", "I2C_SDA", "I2C_SCL", "DAC_RAW", "RH_OUT", "TEMP_KTY", "GND"), start=1):
        b.add(
            reference=f"TP{index}", nickname="Connector_Generic", entry="Conn_01x01",
            center=(20.32 + (index - 1) * 25.4, 147.32), value=net,
            footprint="TestPoint:TestPoint_Plated_Hole_D2.0mm", datasheet="~", nets={"1": net},
        )
    for index, net in enumerate(("24V_PROT", "GND"), start=1):
        b.add(
            reference=f"#FLG0{index}", nickname="power", entry="PWR_FLAG",
            center=(43.18 + (index - 1) * 12.7, 160.02), value="PWR_FLAG",
            footprint="", datasheet="~", nets={"1": net}, in_bom=False, on_board=False,
        )
    return b.sch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=("classic", "esp"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(args.variant).to_file(args.output, encoding="utf-8")


if __name__ == "__main__":
    main()
