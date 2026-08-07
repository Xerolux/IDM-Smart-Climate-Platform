#!/usr/bin/env python3
"""Generate the placed KiCad 10 B-ES1 humidity test PCB.

Run with the Python shipped with KiCad 10 so the pcbnew module is available.
The generated board intentionally leaves the KTY pin unconnected.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


FP_ROOT = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def load_footprint(lib: str, name: str):
    footprint = pcbnew.FootprintLoad(str(FP_ROOT / f"{lib}.pretty"), name)
    if footprint is None:
        raise RuntimeError(f"Cannot load footprint {lib}:{name}")
    return footprint


def add_outline(board: pcbnew.BOARD) -> None:
    corners = [(10, 10), (155, 10), (155, 88), (10, 88), (10, 10)]
    for start, end in zip(corners, corners[1:]):
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(point(*start))
        line.SetEnd(point(*end))
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(mm(0.2))
        board.Add(line)


def add_text(board: pcbnew.BOARD, text: str, x: float, y: float, size=1.0) -> None:
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(point(x, y))
    item.SetLayer(pcbnew.F_SilkS)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(0.15))
    board.Add(item)


def add_track(board, net, start, end, layer, width) -> None:
    if start == end:
        return
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetLayer(layer)
    track.SetWidth(mm(width))
    track.SetNet(net)
    board.Add(track)


def add_via(board, net, position) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(position)
    via.SetWidth(mm(0.8))
    via.SetDrill(mm(0.4))
    via.SetNet(net)
    board.Add(via)


def add_ground_zone(board, net, layer) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(net)
    zone.SetLocalClearance(mm(0.3))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetMinThickness(mm(0.2))
    zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((10.5, 10.5), (154.5, 10.5), (154.5, 87.5), (10.5, 87.5)):
        outline.Append(point(x, y))
    board.Add(zone)


def route_non_ground_nets(board, nets) -> None:
    """Create deterministic two-layer Manhattan routes.

    Vertical access is on F.Cu and each point-to-point connection receives its
    own horizontal channel on B.Cu. This is intentionally conservative and
    reproducible so DRC can audit every generated connection.
    """
    pads_by_net = {name: [] for name in nets}
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            name = pad.GetNetname()
            if name and name != "GND":
                key = (pad.GetPosition().x, pad.GetPosition().y)
                if all((p.GetPosition().x, p.GetPosition().y) != key for p in pads_by_net[name]):
                    pads_by_net[name].append(pad)

    channel_index = 0
    widths = {"24V_RAW": 0.8, "24V_FUSED": 0.8, "24V_PROT": 0.8, "+5V": 0.6, "+3V3": 0.5, "RH_OUT": 0.5}
    for net_name, pads in pads_by_net.items():
        if len(pads) < 2:
            continue
        pads.sort(key=lambda pad: (pad.GetPosition().x, pad.GetPosition().y))
        for first, second in zip(pads, pads[1:]):
            y_channel = 12.0 + channel_index * 1.35
            channel_index += 1
            if y_channel > 84.0:
                raise RuntimeError("Routing channel budget exhausted")
            offset_a = ((channel_index % 5) - 2) * 0.45
            offset_b = (((channel_index + 2) % 5) - 2) * 0.45
            a = first.GetPosition()
            b = second.GetPosition()
            ax = a.x + mm(offset_a)
            bx = b.x + mm(offset_b)
            a_access = pcbnew.VECTOR2I(ax, a.y)
            b_access = pcbnew.VECTOR2I(bx, b.y)
            a_via = pcbnew.VECTOR2I(ax, mm(y_channel))
            b_via = pcbnew.VECTOR2I(bx, mm(y_channel))
            width = widths.get(net_name, 0.3)
            net = nets[net_name]
            add_track(board, net, a, a_access, pcbnew.F_Cu, width)
            add_track(board, net, a_access, a_via, pcbnew.F_Cu, width)
            add_via(board, net, a_via)
            add_track(board, net, a_via, b_via, pcbnew.B_Cu, width)
            add_via(board, net, b_via)
            add_track(board, net, b_via, b_access, pcbnew.F_Cu, width)
            add_track(board, net, b_access, b, pcbnew.F_Cu, width)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)
    add_outline(board)

    net_names = [
        "GND", "24V_RAW", "24V_FUSED", "24V_PROT", "+5V", "+3V3",
        "I2C_SDA", "I2C_SCL", "DAC_RAW", "OPAMP_FB", "OPAMP_OUT", "RH_OUT",
    ]
    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    parts = [
        ("J1", "IDM / BENCH", "TerminalBlock_Phoenix", "TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal", 16, 40, 0, {2: "24V_RAW", 3: "GND", 4: "RH_OUT"}),
        ("F1", "500mA 5x20mm", "Fuse", "Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal", 29, 22, 0, {1: "24V_RAW", 2: "24V_FUSED"}),
        ("D1", "SS16-E3/61T", "Diode_SMD", "D_SMA", 57, 22, 0, {1: "24V_PROT", 2: "24V_FUSED"}),
        ("U1", "TSR 1-2450", "Converter_DCDC", "Converter_DCDC_TRACO_TSR-1_THT", 69, 22, 0, {1: "24V_PROT", 2: "GND", 3: "+5V"}),
        ("C1", "22u 50V", "Capacitor_SMD", "C_1210_3225Metric", 57, 31, 0, {1: "24V_PROT", 2: "GND"}),
        ("C2", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 63, 31, 0, {1: "24V_PROT", 2: "GND"}),
        ("C3", "10u 10V", "Capacitor_SMD", "C_0805_2012Metric", 72, 31, 0, {1: "+5V", 2: "GND"}),
        ("A1", "ESP32-C3-DevKitM-1", "RF_Module", "ESP32-C3-DevKitM-1", 80, 36, 0, {1: "GND", 2: "+3V3", 3: "+3V3", 6: "GND", 8: "GND", 12: "GND", 13: "+5V", 14: "+5V", 15: "GND", 16: "GND", 19: "GND", 24: "GND", 25: "I2C_SDA", 26: "I2C_SCL", 27: "GND", 30: "GND"}),
        ("U2", "MCP4725A0T-E/CH", "Package_TO_SOT_SMD", "SOT-23-6", 115, 40, 0, {1: "DAC_RAW", 2: "GND", 3: "+3V3", 4: "I2C_SDA", 5: "I2C_SCL", 6: "GND"}),
        ("R1", "4.7k", "Resistor_SMD", "R_0603_1608Metric", 108, 30, 90, {1: "+3V3", 2: "I2C_SDA"}),
        ("R2", "4.7k", "Resistor_SMD", "R_0603_1608Metric", 112, 30, 90, {1: "+3V3", 2: "I2C_SCL"}),
        ("C4", "100n 16V", "Capacitor_SMD", "C_0603_1608Metric", 116, 30, 90, {1: "+3V3", 2: "GND"}),
        ("U3", "OPA197IDBVR", "Package_TO_SOT_SMD", "SOT-23-5", 132, 40, 0, {1: "OPAMP_OUT", 2: "GND", 3: "DAC_RAW", 4: "OPAMP_FB", 5: "24V_PROT"}),
        ("R3", "20.3k 0.1%", "Resistor_SMD", "R_0603_1608Metric", 134, 49, 0, {1: "OPAMP_OUT", 2: "OPAMP_FB"}),
        ("R4", "10k 0.1%", "Resistor_SMD", "R_0603_1608Metric", 128, 54, 90, {1: "OPAMP_FB", 2: "GND"}),
        ("R5", "220R", "Resistor_SMD", "R_0603_1608Metric", 144, 40, 0, {1: "OPAMP_OUT", 2: "RH_OUT"}),
        ("C5", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 128, 30, 90, {1: "24V_PROT", 2: "GND"}),
        ("C6", "100n 50V", "Capacitor_SMD", "C_0603_1608Metric", 145, 49, 90, {1: "RH_OUT", 2: "GND"}),
    ]

    footprints = {}
    for reference, value, lib, name, x, y, angle, pin_nets in parts:
        fp = load_footprint(lib, name)
        fp.SetReference(reference)
        fp.SetValue(value)
        fp.SetPosition(point(x, y))
        fp.SetOrientationDegrees(angle)
        board.Add(fp)
        footprints[reference] = fp
        for pad_number, net_name in pin_nets.items():
            matching = [pad for pad in fp.Pads() if pad.GetNumber() == str(pad_number)]
            if not matching:
                raise RuntimeError(f"{reference}: footprint has no pad {pad_number}")
            for pad in matching:
                pad.SetNet(nets[net_name])

    for index, (net_name, x) in enumerate(zip(("24V_RAW", "24V_PROT", "+5V", "+3V3", "DAC_RAW", "RH_OUT", "GND"), (24, 44, 64, 84, 108, 128, 140)), start=1):
        fp = load_footprint("TestPoint", "TestPoint_Plated_Hole_D2.0mm")
        fp.SetReference(f"TP{index}")
        fp.SetValue(net_name)
        fp.SetPosition(point(x, 79))
        board.Add(fp)
        fp.FindPadByNumber("1").SetNet(nets[net_name])

    for reference, x in (("H1", 16), ("H2", 149)):
        fp = load_footprint("MountingHole", "MountingHole_3.2mm_M3")
        fp.SetReference(reference)
        fp.SetPosition(point(x, 82))
        board.Add(fp)

    add_text(board, "IDM FAKE SENSOR B-ES1 / HUMIDITY TEST ONLY", 82, 13, 1.2)
    add_text(board, "TEMP/KTY PIN 1: DNP - DO NOT CONNECT", 34, 68, 1.0)
    add_text(board, "24 V BENCH SUPPLY ONLY", 35, 72, 1.0)
    add_text(board, "43 TEMP", 16, 31, 0.8)
    add_text(board, "42 +24V", 16, 34, 0.8)
    add_text(board, "41 GND", 16, 46, 0.8)
    add_text(board, "40 RH", 16, 49, 0.8)

    design = board.GetDesignSettings()
    design.m_MinClearance = mm(0.2)
    design.SetCustomTrackWidth(mm(0.25))
    design.SetCustomViaSize(mm(0.8))
    design.SetCustomViaDrill(mm(0.4))

    add_ground_zone(board, nets["GND"], pcbnew.F_Cu)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(args.output), board)


if __name__ == "__main__":
    main()
