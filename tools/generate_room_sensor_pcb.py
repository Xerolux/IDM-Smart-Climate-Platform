#!/usr/bin/env python3
"""Generate placed KiCad 10 B-ES1 room-sensor PCBs for routing."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew

from generate_fake_sensor_pcb import add_ground_zone, add_outline, add_text, add_track, add_via, load_footprint, mm, point


def add_part(board, nets, spec) -> None:
    reference, value, library, footprint_name, x, y, rotation, pin_nets = spec
    footprint = load_footprint(library, footprint_name)
    footprint.SetReference(reference)
    footprint.SetValue(value)
    footprint.SetPosition(point(x, y))
    footprint.SetOrientationDegrees(rotation)
    for pad in footprint.Pads():
        name = pin_nets.get(int(pad.GetNumber())) if pad.GetNumber().isdigit() else None
        if name:
            pad.SetNet(nets[name])
    board.Add(footprint)


def add_mounting_hole(board, reference, x, y) -> None:
    footprint = load_footprint("MountingHole", "MountingHole_3.2mm_M3")
    footprint.SetReference(reference)
    footprint.SetValue("M3")
    footprint.SetPosition(point(x, y))
    board.Add(footprint)


def build(variant: str) -> pcbnew.BOARD:
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)
    add_outline(board)
    names = [
        "GND", "24V_RAW", "24V_FUSED", "24V_PROT", "+5V", "+3V3",
        "I2C_SDA", "I2C_SCL", "DAC_RAW", "OPAMP_FB", "OPAMP_OUT",
        "RH_OUT", "TEMP_KTY", "UPDI",
    ]
    nets = {}
    for name in names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    parts = [
        ("J1", "IDM / BENCH", "TerminalBlock_Phoenix", "TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal", 16, 40, 0, {1: "TEMP_KTY", 2: "24V_RAW", 3: "GND", 4: "RH_OUT"}),
        ("RTH1", "KTY81/210", "Package_TO_SOT_THT", "TO-92_Inline", 24, 55, 0, {1: "TEMP_KTY", 2: "GND"}),
        ("F1", "500mA 5x20mm", "Fuse", "Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal", 29, 22, 0, {1: "24V_RAW", 2: "24V_FUSED"}),
        ("D1", "SS16-E3/61T", "Diode_SMD", "D_SMA", 57, 22, 0, {1: "24V_PROT", 2: "24V_FUSED"}),
        ("U1", "TSR 1-2450", "Converter_DCDC", "Converter_DCDC_TRACO_TSR-1_THT", 69, 22, 0, {1: "24V_PROT", 2: "GND", 3: "+5V"}),
        ("C1", "22u 50V", "Capacitor_SMD", "C_1210_3225Metric", 57, 31, 0, {1: "24V_PROT", 2: "GND"}),
        ("C2", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 63, 31, 0, {1: "24V_PROT", 2: "GND"}),
        ("C3", "10u 10V", "Capacitor_SMD", "C_0805_2012Metric", 72, 31, 0, {1: "+5V", 2: "GND"}),
        ("U3", "SHT45-AD1B-R2", "Sensor_Humidity", "Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad", 116, 60, 0, {1: "I2C_SDA", 2: "I2C_SCL", 3: "+3V3", 4: "GND"}),
        ("U4", "MCP4725A0T-E/CH", "Package_TO_SOT_SMD", "SOT-23-6", 115, 40, 0, {1: "DAC_RAW", 2: "GND", 3: "+3V3", 4: "I2C_SDA", 5: "I2C_SCL", 6: "GND"}),
        ("U5", "OPA197IDBVR", "Package_TO_SOT_SMD", "SOT-23-5", 132, 40, 0, {1: "OPAMP_OUT", 2: "GND", 3: "DAC_RAW", 4: "OPAMP_FB", 5: "24V_PROT"}),
        ("R1", "4.7k", "Resistor_SMD", "R_0603_1608Metric", 109, 52, 90, {1: "+3V3", 2: "I2C_SDA"}),
        ("R2", "4.7k", "Resistor_SMD", "R_0603_1608Metric", 113, 52, 90, {1: "+3V3", 2: "I2C_SCL"}),
        ("R3", "20.3k 0.1%", "Resistor_SMD", "R_0603_1608Metric", 136, 48, 90, {1: "OPAMP_OUT", 2: "OPAMP_FB"}),
        ("R4", "10k 0.1%", "Resistor_SMD", "R_0603_1608Metric", 128, 54, 90, {1: "OPAMP_FB", 2: "GND"}),
        ("R5", "220R 1%", "Resistor_SMD", "R_0603_1608Metric", 145, 40, 90, {1: "OPAMP_OUT", 2: "RH_OUT"}),
        ("C4", "100n 16V", "Capacitor_SMD", "C_0603_1608Metric", 121, 60, 90, {1: "+3V3", 2: "GND"}),
        ("C5", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 128, 30, 90, {1: "24V_PROT", 2: "GND"}),
        ("C6", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 145, 49, 90, {1: "RH_OUT", 2: "GND"}),
    ]
    if variant == "esp":
        parts.append(("A1", "ESP32-C3-DevKitM-1", "RF_Module", "ESP32-C3-DevKitM-1", 80, 43, 0,
                      {1: "GND", 2: "+3V3", 3: "+3V3", 6: "GND", 8: "GND", 12: "GND", 13: "+5V", 14: "+5V", 15: "GND", 16: "GND", 19: "GND", 24: "GND", 25: "I2C_SDA", 26: "I2C_SCL", 27: "GND", 30: "GND"}))
    else:
        parts.extend([
            ("U2", "ATtiny1616-SNR", "Package_SO", "SOIC-20W_7.5x12.8mm_P1.27mm", 84, 43, 0,
             {1: "+3V3", 20: "GND", 16: "UPDI", 17: "I2C_SDA", 18: "I2C_SCL"}),
            ("U6", "AP2112K-3.3TRG1", "Package_TO_SOT_SMD", "SOT-23-5", 84, 27, 0,
             {1: "+5V", 2: "GND", 3: "+5V", 5: "+3V3"}),
            ("J2", "UPDI", "Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical", 96, 62, 90,
             {1: "+3V3", 2: "UPDI", 3: "GND"}),
        ])
    for part in parts:
        add_part(board, nets, part)

    # The SHT45 footprint intentionally blocks copper between its 0.8 mm-pitch
    # pads. Escape the three active non-ground pads before handing the design to
    # the autorouter so it can route from accessible B.Cu vias.
    sht = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U3")
    sht_pads = {pad.GetNumber(): pad for pad in sht.Pads()}
    fanouts = {
        "1": [point(114.5, 59.6), point(113.5, 58.6)],
        "2": [point(114.5, 60.4), point(113.5, 61.4)],
        "3": [point(117.5, 60.4), point(118.5, 61.4)],
    }
    for number, route in fanouts.items():
        pad_item = sht_pads[number]
        positions = [pad_item.GetPosition(), *route]
        for start, end in zip(positions, positions[1:]):
            add_track(board, pad_item.GetNet(), start, end, pcbnew.F_Cu, 0.2)
        add_via(board, pad_item.GetNet(), route[-1])
    sht_gnd = sht_pads["4"]
    add_track(board, sht_gnd.GetNet(), sht_gnd.GetPosition(), point(117.5, 59.6), pcbnew.F_Cu, 0.2)
    add_track(board, sht_gnd.GetNet(), point(117.5, 59.6), point(117.5, 58.5), pcbnew.F_Cu, 0.2)
    add_track(board, sht_gnd.GetNet(), point(117.5, 58.5), point(115.5, 58.5), pcbnew.F_Cu, 0.2)
    add_via(board, sht_gnd.GetNet(), point(115.5, 58.5))
    add_via(board, sht_gnd.GetNet(), point(115.5, 55.0))
    add_track(board, sht_gnd.GetNet(), point(115.5, 58.5), point(115.5, 55.0), pcbnew.B_Cu, 0.2)

    test_nets = ["24V_RAW", "24V_PROT", "+5V", "+3V3", "I2C_SDA", "I2C_SCL", "DAC_RAW", "RH_OUT", "TEMP_KTY", "GND"]
    for index, (name, x) in enumerate(zip(test_nets, (24, 36, 48, 60, 72, 84, 96, 108, 120, 132)), start=1):
        add_part(board, nets, (f"TP{index}", name, "TestPoint", "TestPoint_Plated_Hole_D2.0mm", x, 84, 0, {1: name}))
    add_mounting_hole(board, "H1", 14, 84)
    add_mounting_hole(board, "H2", 151, 84)
    add_ground_zone(board, nets["GND"], pcbnew.F_Cu)

    label = "CLASSIC" if variant == "classic" else "ESP"
    add_text(board, f"IDM ROOM SENSOR {label} B-ES1", 82, 12, 1.2)
    add_text(board, "ENGINEERING SAMPLE / BENCH TEST FIRST", 82, 74, 0.9)
    add_text(board, "43 TEMP", 13, 33, 0.8)
    add_text(board, "42 +24V", 13, 35, 0.8)
    add_text(board, "41 GND", 13, 50, 0.8)
    add_text(board, "40 RH", 13, 52, 0.8)
    add_text(board, "KTY81/210 - VERIFY IDM INTERFACE", 42, 67, 0.8)
    add_text(board, "24 V BENCH SUPPLY FIRST", 42, 70, 0.8)
    return board


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=("classic", "esp"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    board = build(args.variant)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(args.output), board)


if __name__ == "__main__":
    main()
