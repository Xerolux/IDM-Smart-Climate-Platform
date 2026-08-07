#!/usr/bin/env python3
"""Validate the B-ES3-C6 enclosure STL meshes and prepared S5 G-code."""

from collections import Counter
from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[1]
ENC = ROOT / "hardware" / "esp-sensor" / "enclosure"


def triangles(path: Path):
    data = path.read_bytes()
    if data[:5].lower() == b"solid":
        values = [tuple(map(float, match)) for match in re.findall(
            rb"vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)", data
        )]
        if len(values) % 3:
            raise AssertionError(f"invalid ASCII STL: {path}")
        return [tuple(values[index:index + 3]) for index in range(0, len(values), 3)]

    count = struct.unpack_from("<I", data, 80)[0]
    result = []
    offset = 84
    for _ in range(count):
        vertices = struct.unpack_from("<9f", data, offset + 12)
        result.append(tuple(tuple(vertices[i:i + 3]) for i in range(0, 9, 3)))
        offset += 50
    return result


def validate_mesh(filename: str, expected_min, expected_max):
    path = ENC / filename
    tris = triangles(path)
    points = [point for tri in tris for point in tri]
    actual_min = tuple(min(point[axis] for point in points) for axis in range(3))
    actual_max = tuple(max(point[axis] for point in points) for axis in range(3))
    for actual, expected in zip(actual_min + actual_max, expected_min + expected_max):
        assert abs(actual - expected) < 0.011, (path, actual_min, actual_max)

    edges = Counter()
    for tri in tris:
        rounded = [tuple(round(value, 5) for value in point) for point in tri]
        for first, second in ((0, 1), (1, 2), (2, 0)):
            edges[tuple(sorted((rounded[first], rounded[second])))] += 1
    bad_edges = [edge for edge, count in edges.items() if count != 2]
    assert not bad_edges, f"{path}: {len(bad_edges)} non-manifold edges"
    print(f"PASS {filename}: {len(tris)} triangles, manifold, bounds OK")


def validate_gcode():
    path = ENC / "IDM-RoomSensor-B-ES3-C6-S5-AA04-Ultimaker-PLA.gcode"
    text = path.read_text(encoding="utf-8", errors="replace")
    required = (
        ";TARGET_MACHINE.NAME:Ultimaker S5",
        ";EXTRUDER_TRAIN.0.NOZZLE.NAME:AA 0.4",
        ";BUILD_PLATE.INITIAL_TEMPERATURE:60",
        ";PRINT.TIME:54517",
        ";LAYER_COUNT:90",
        "M190 S60",
        "M104 S200",
        "M109 S200",
    )
    for marker in required:
        assert marker in text, f"missing G-code marker: {marker}"
    assert ";TYPE:SUPPORT" not in text, "unexpected support toolpaths"

    # 310 x 100 mm model plus a 5 mm brim on each side fits 330 x 240 mm.
    assert 310 + 2 * 5 <= 330
    assert 100 + 2 * 5 <= 240
    print("PASS S5 G-code: AA0.4/PLA profile, 90 layers, no support, bed fit OK")


if __name__ == "__main__":
    validate_mesh("idm-roomsensor-b-es3-c6_base.stl", (0, 0, 0), (150, 100, 11))
    validate_mesh("idm-roomsensor-b-es3-c6_lid.stl", (0, 0, 0), (150, 100, 17.95))
    validate_mesh(
        "idm-roomsensor-b-es3-c6_S5-print-plate.stl",
        (-155, -50, 0),
        (155, 50, 17.95),
    )
    validate_gcode()
