#!/usr/bin/env python3
"""Generate the native KiCad 10 fake-sensor engineering schematic.

This intentionally implements only the power, ESP32 and humidity 0-10 V test
path. The IDM temperature/KTY terminal is explicitly left unconnected until the
real input excitation has been measured.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from kiutils.items.common import Effects, Font, Position, TitleBlock
from kiutils.items.schitems import (
    Connection,
    LocalLabel,
    NoConnect,
    SchematicSymbol,
    SymbolProjectInstance,
    SymbolProjectPath,
    Text,
)
from kiutils.schematic import Schematic
from kiutils.symbol import Symbol, SymbolLib


KICAD_SYMBOL_DIR = Path("/mnt/c/Program Files/KiCad/10.0/share/kicad/symbols")
GRID = 1.27


def uid() -> str:
    return str(uuid4())


class Builder:
    def __init__(self) -> None:
        self.sch = Schematic(
            version="20231120",
            generator="eeschema",
            uuid=uid(),
            titleBlock=TitleBlock(
                title="IDM Fake Sensor ESP - humidity engineering sample",
                date="2026-08-07",
                revision="B-ES1",
                company="IDM Smart Climate Platform",
                comments={
                    1: "BENCH TEST ONLY - NOT RELEASED FOR CONNECTION TO IDM",
                    2: "KTY/TEMP terminal deliberately DNP pending input measurement",
                    3: "Validated design target: 24 V bench input, 0-10 V humidity output",
                },
            ),
        )
        self._libraries: dict[str, SymbolLib] = {}
        self._embedded: set[str] = set()
        self._labels: set[tuple[str, float, float]] = set()

    def library(self, nickname: str) -> SymbolLib:
        if nickname not in self._libraries:
            self._libraries[nickname] = SymbolLib().from_file(
                KICAD_SYMBOL_DIR / f"{nickname}.kicad_sym"
            )
        return self._libraries[nickname]

    def source_symbol(self, nickname: str, entry: str) -> Symbol:
        lib = self.library(nickname)
        symbol = next((item for item in lib.symbols if item.entryName == entry), None)
        if symbol is None:
            raise KeyError(f"Missing KiCad symbol {nickname}:{entry}")
        if not symbol.extends:
            return deepcopy(symbol)

        # KiCad aliases contain their ordering data in a parent symbol. Embed a
        # resolved copy so the generated schematic is self-contained.
        parent = next(item for item in lib.symbols if item.entryName == symbol.extends)
        resolved = deepcopy(parent)
        parent_name = resolved.entryName
        resolved.entryName = symbol.entryName
        resolved.extends = None
        for unit in resolved.units:
            if unit.entryName and unit.entryName.startswith(parent_name):
                unit.entryName = symbol.entryName + unit.entryName[len(parent_name) :]
        alias_properties = {prop.key: prop for prop in symbol.properties}
        for index, prop in enumerate(resolved.properties):
            if prop.key in alias_properties:
                resolved.properties[index] = deepcopy(alias_properties[prop.key])
        return resolved

    @staticmethod
    def pins(symbol: Symbol) -> dict[str, object]:
        result = {pin.number: pin for pin in symbol.pins}
        for unit in symbol.units:
            if unit.unitId in (0, 1):
                result.update({pin.number: pin for pin in unit.pins})
        return result

    @staticmethod
    def endpoint(center: tuple[float, float], pin: object) -> tuple[float, float]:
        # All generated symbols are unrotated. KiCad's symbol Y axis is opposite
        # to the page Y axis.
        return (
            round(center[0] + pin.position.X, 6),
            round(center[1] - pin.position.Y, 6),
        )

    def add_label(self, net: str, point: tuple[float, float], pin_angle: float) -> None:
        key = (net, point[0], point[1])
        if key in self._labels:
            return
        self._labels.add(key)
        offsets = {
            0: (-5.08, 0.0),
            90: (0.0, 5.08),
            180: (5.08, 0.0),
            270: (0.0, -5.08),
        }
        dx, dy = offsets.get(int(pin_angle or 0) % 360, (-5.08, 0.0))
        target = (round(point[0] + dx, 6), round(point[1] + dy, 6))
        self.sch.graphicalItems.append(
            Connection(
                type="wire",
                points=[Position(point[0], point[1]), Position(target[0], target[1])],
                uuid=uid(),
            )
        )
        label_angle = 180 if dx < 0 else 0
        self.sch.labels.append(
            LocalLabel(
                text=net,
                position=Position(target[0], target[1], label_angle),
                effects=Effects(font=Font(height=1.0, width=1.0)),
                uuid=uid(),
            )
        )

    def add(
        self,
        *,
        reference: str,
        nickname: str,
        entry: str,
        center: tuple[float, float],
        value: str,
        footprint: str,
        datasheet: str,
        nets: dict[str, str],
        no_connect: set[str] | None = None,
        in_bom: bool = True,
        on_board: bool = True,
        dnp: bool = False,
    ) -> None:
        source = self.source_symbol(nickname, entry)
        lib_id = f"{nickname}:{entry}"
        if lib_id not in self._embedded:
            embedded = deepcopy(source)
            embedded.libraryNickname = nickname
            self.sch.libSymbols.append(embedded)
            self._embedded.add(lib_id)

        pins = self.pins(source)
        unknown = (set(nets) | set(no_connect or set())) - set(pins)
        if unknown:
            raise ValueError(f"{reference}: unknown pins {sorted(unknown)}")

        properties = deepcopy(source.properties)
        overrides = {
            "Reference": reference,
            "Value": value,
            "Footprint": footprint,
            "Datasheet": datasheet,
        }
        visible_index = 0
        for prop in properties:
            if prop.key in overrides:
                prop.value = overrides[prop.key]
            prop.showName = False
            visible = prop.key in ("Reference", "Value")
            prop.position = Position(
                center[0], center[1] - 10.16 + visible_index * 2.54, 0
            )
            prop.effects = Effects(
                font=Font(height=1.27, width=1.27), hide=not visible
            )
            if visible:
                visible_index += 1

        instance = SchematicSymbol(
            libraryNickname=nickname,
            entryName=entry,
            libName=lib_id,
            position=Position(center[0], center[1], 0),
            unit=1,
            inBom=in_bom,
            onBoard=on_board,
            dnp=dnp,
            uuid=uid(),
            properties=properties,
            pins={number: uid() for number in pins},
            instances=[
                SymbolProjectInstance(
                    name="",
                    paths=[
                        SymbolProjectPath(
                            sheetInstancePath="/", reference=reference, unit=1
                        )
                    ],
                )
            ],
        )
        self.sch.schematicSymbols.append(instance)

        for number, net in nets.items():
            self.add_label(
                net, self.endpoint(center, pins[number]), pins[number].position.angle
            )
        for number in no_connect or set():
            point = self.endpoint(center, pins[number])
            self.sch.noConnects.append(
                NoConnect(position=Position(point[0], point[1]), uuid=uid())
            )


def build() -> Schematic:
    b = Builder()

    b.sch.texts.extend(
        [
            Text(
                text="REV B-ES1: HUMIDITY PATH ENGINEERING SAMPLE",
                position=Position(85.0, 20.32, 0),
                effects=Effects(font=Font(height=2.0, width=2.0, bold=True)),
                uuid=uid(),
            ),
            Text(
                text="WARNING: J1 pin 1 (TEMP/KTY) is deliberately unconnected. Bench supply only; do not attach to IDM before interface validation.",
                position=Position(85.0, 25.4, 0),
                effects=Effects(font=Font(height=1.27, width=1.27, bold=True)),
                uuid=uid(),
            ),
            Text(
                text="Input protection and 5 V power",
                position=Position(30.48, 40.64, 0),
                effects=Effects(font=Font(height=1.5, width=1.5, bold=True)),
                uuid=uid(),
            ),
            Text(
                text="ESP32-C3 DevKitM-1 and I2C DAC",
                position=Position(129.54, 40.64, 0),
                effects=Effects(font=Font(height=1.5, width=1.5, bold=True)),
                uuid=uid(),
            ),
            Text(
                text="0-10 V humidity output: gain = 1 + 20.3k/10k = 3.03",
                position=Position(210.82, 40.64, 0),
                effects=Effects(font=Font(height=1.5, width=1.5, bold=True)),
                uuid=uid(),
            ),
        ]
    )

    b.add(
        reference="J1",
        nickname="Connector_Generic",
        entry="Conn_01x04",
        center=(38.1, 63.5),
        value="IDM / BENCH INTERFACE",
        footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal",
        datasheet="https://www.phoenixcontact.com/en-de/products/pcb-terminal-block-pt-15-4-35-h-1984633",
        nets={"2": "24V_RAW", "3": "GND", "4": "RH_OUT"},
        no_connect={"1"},
    )
    b.add(
        reference="F1",
        nickname="Device",
        entry="Fuse",
        center=(58.42, 63.5),
        value="500mA 5x20mm fuse",
        footprint="Fuse:Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal",
        datasheet="https://www.littelfuse.com/assetdocs/littelfuse-5x20mm-glass-fuse-217-datasheet",
        nets={"1": "24V_RAW", "2": "24V_FUSED"},
    )
    b.add(
        reference="D1",
        nickname="Device",
        entry="D_Schottky",
        center=(86.36, 63.5),
        value="SS16-E3/61T",
        footprint="Diode_SMD:D_SMA",
        datasheet="https://www.vishay.com/docs/88746/ss12.pdf",
        # KiCad diode convention: pin 1 = cathode, pin 2 = anode.
        nets={"1": "24V_PROT", "2": "24V_FUSED"},
    )
    b.add(
        reference="U1",
        nickname="Regulator_Linear",
        entry="L7805",
        center=(114.3, 63.5),
        value="TSR 1-2450",
        footprint="Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT",
        datasheet="https://www.tracopower.com/tsr1-datasheet",
        nets={"1": "24V_PROT", "2": "GND", "3": "+5V"},
    )

    for ref, center, value, footprint, nets, datasheet in [
        ("C1", (83.82, 91.44), "22u 50V X7R", "Capacitor_SMD:C_1210_3225Metric", {"1": "24V_PROT", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71H226KE15-01.pdf"),
        ("C2", (99.06, 91.44), "100n 50V X7R", "Capacitor_SMD:C_0603_1608Metric", {"1": "24V_PROT", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf"),
        ("C3", (114.3, 91.44), "10u 10V X7R", "Capacitor_SMD:C_0805_2012Metric", {"1": "+5V", "2": "GND"}, "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71A106KE51-01.pdf"),
    ]:
        b.add(reference=ref, nickname="Device", entry="C", center=center, value=value, footprint=footprint, datasheet=datasheet, nets=nets)

    devkit_nets = {
        "1": "GND", "2": "+3V3", "3": "+3V3", "6": "GND",
        "8": "GND", "12": "GND", "13": "+5V", "14": "+5V",
        "15": "GND", "16": "GND", "19": "GND", "24": "GND",
        "25": "I2C_SDA", "26": "I2C_SCL", "27": "GND", "30": "GND",
    }
    devkit_nc = {str(number) for number in range(1, 31)} - set(devkit_nets)
    b.add(
        reference="A1",
        nickname="RF_Module",
        entry="ESP32-C3-DevKitM-1",
        center=(149.86, 68.58),
        value="ESP32-C3-DevKitM-1",
        footprint="RF_Module:ESP32-C3-DevKitM-1",
        datasheet="https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html",
        nets=devkit_nets,
        no_connect=devkit_nc,
    )
    b.add(
        reference="U2",
        nickname="Analog_DAC",
        entry="MCP4725xxx-xCH",
        center=(198.12, 68.58),
        value="MCP4725A0T-E/CH",
        footprint="Package_TO_SOT_SMD:SOT-23-6",
        datasheet="https://ww1.microchip.com/downloads/en/DeviceDoc/MCP4725-Data-Sheet-20002039E.pdf",
        nets={"1": "DAC_RAW", "2": "GND", "3": "+3V3", "4": "I2C_SDA", "5": "I2C_SCL", "6": "GND"},
    )
    for ref, center, value, nets in [
        ("R1", (175.26, 101.6), "4.7k", {"1": "+3V3", "2": "I2C_SDA"}),
        ("R2", (187.96, 101.6), "4.7k", {"1": "+3V3", "2": "I2C_SCL"}),
    ]:
        b.add(reference=ref, nickname="Device", entry="R", center=center, value=value, footprint="Resistor_SMD:R_0603_1608Metric", datasheet="https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/PYu-RC_Group_51_RoHS_L_11.pdf", nets=nets)
    b.add(reference="C4", nickname="Device", entry="C", center=(200.66, 101.6), value="100n 16V X7R", footprint="Capacitor_SMD:C_0603_1608Metric", datasheet="https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71C104KA01-01.pdf", nets={"1": "+3V3", "2": "GND"})

    b.add(
        reference="U3",
        nickname="Amplifier_Operational",
        entry="OPA197xDBV",
        center=(236.22, 68.58),
        value="OPA197IDBVR",
        footprint="Package_TO_SOT_SMD:SOT-23-5",
        datasheet="https://www.ti.com/lit/ds/symlink/opa197.pdf",
        nets={"1": "OPAMP_OUT", "2": "GND", "3": "DAC_RAW", "4": "OPAMP_FB", "5": "24V_PROT"},
    )
    for ref, center, value, nets, tolerance in [
        ("R3", (251.46, 86.36), "20.3k 0.1%", {"1": "OPAMP_OUT", "2": "OPAMP_FB"}, "0.1%"),
        ("R4", (236.22, 101.6), "10k 0.1%", {"1": "OPAMP_FB", "2": "GND"}, "0.1%"),
        ("R5", (269.24, 68.58), "220R 1%", {"1": "OPAMP_OUT", "2": "RH_OUT"}, "1%"),
    ]:
        b.add(reference=ref, nickname="Device", entry="R", center=center, value=value, footprint="Resistor_SMD:R_0603_1608Metric", datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/AOA0000C307.pdf" if tolerance == "0.1%" else "https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/PYu-RC_Group_51_RoHS_L_11.pdf", nets=nets)
    b.add(reference="C5", nickname="Device", entry="C", center=(220.98, 101.6), value="100n 50V X7R", footprint="Capacitor_SMD:C_0603_1608Metric", datasheet="https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf", nets={"1": "24V_PROT", "2": "GND"})
    b.add(reference="C6", nickname="Device", entry="C", center=(269.24, 101.6), value="100n 50V X7R", footprint="Capacitor_SMD:C_0603_1608Metric", datasheet="https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf", nets={"1": "RH_OUT", "2": "GND"})

    for index, net in enumerate(("24V_RAW", "24V_PROT", "+5V", "+3V3", "DAC_RAW", "RH_OUT", "GND"), start=1):
        b.add(
            reference=f"TP{index}",
            nickname="Connector_Generic",
            entry="Conn_01x01",
            center=(30.48 + (index - 1) * 20.32, 111.76),
            value=net,
            footprint="TestPoint:TestPoint_Plated_Hole_D2.0mm",
            datasheet="~",
            nets={"1": net},
        )

    # Passive input protection cannot satisfy ERC's power-source inference, so
    # explicitly mark the protected input and ground. +5V and +3V3 already have
    # real power-output pins and must not receive a second PWR_FLAG.
    for index, net in enumerate(("24V_PROT", "GND"), start=1):
        b.add(
            reference=f"#FLG0{index}",
            nickname="power",
            entry="PWR_FLAG",
            center=(43.18 + (index - 1) * 12.7, 124.46),
            value="PWR_FLAG",
            footprint="",
            datasheet="~",
            nets={"1": net},
            in_bom=False,
            on_board=False,
        )

    return b.sch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build().to_file(args.output, encoding="utf-8")


if __name__ == "__main__":
    main()
