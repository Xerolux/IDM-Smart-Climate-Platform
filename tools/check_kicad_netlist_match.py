#!/usr/bin/env python3
"""Compare schematic netlist nodes with the pads in a KiCad PCB."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pcbnew


def parse_sexpr(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    tokens = re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', text)
    stack: list[list] = []
    root = None
    for token in tokens:
        if token == "(":
            item: list = []
            if stack:
                stack[-1].append(item)
            stack.append(item)
            if root is None:
                root = item
        elif token == ")":
            stack.pop()
        else:
            if token.startswith('"'):
                token = bytes(token[1:-1], "utf-8").decode("unicode_escape")
            stack[-1].append(token)
    return root


def child(items, key):
    return next(item for item in items if isinstance(item, list) and item and item[0] == key)


def children(items, key):
    return [item for item in items if isinstance(item, list) and item and item[0] == key]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schematic_netlist", type=Path)
    parser.add_argument("board", type=Path)
    args = parser.parse_args()

    data = parse_sexpr(args.schematic_netlist)
    nets = child(data, "nets")
    expected: dict[tuple[str, str], str] = {}
    for net in children(nets, "net"):
        name = child(net, "name")[1]
        if name.startswith("unconnected-("):
            continue
        name = name.removeprefix("/")
        for node in children(net, "node"):
            expected[(child(node, "ref")[1], child(node, "pin")[1])] = name

    board = pcbnew.LoadBoard(str(args.board))
    actual: dict[tuple[str, str], str] = {}
    for footprint in board.GetFootprints():
        reference = footprint.GetReference()
        for pad in footprint.Pads():
            net = pad.GetNetname()
            if net:
                actual[(reference, pad.GetNumber())] = net

    missing = [(node, net, actual.get(node)) for node, net in expected.items() if actual.get(node) != net]
    extra = [(node, net) for node, net in actual.items() if node not in expected and node[0] not in {"H1", "H2"}]
    if missing or extra:
        for node, expected_net, actual_net in missing:
            print(f"MISMATCH {node[0]}.{node[1]}: schematic={expected_net!r}, pcb={actual_net!r}")
        for node, actual_net in extra:
            print(f"EXTRA {node[0]}.{node[1]}: pcb={actual_net!r}")
        raise SystemExit(1)
    print(f"Netlist match: {len(expected)} connected schematic pins match PCB pads")


if __name__ == "__main__":
    main()
