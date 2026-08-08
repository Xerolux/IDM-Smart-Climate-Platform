#!/usr/bin/env python3
"""Validate B-ES4-AIR-R2 enclosure meshes and Ultimaker S5 fit."""

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
        assert len(values) % 3 == 0
        return [tuple(values[index:index + 3]) for index in range(0, len(values), 3)]
    count = struct.unpack_from("<I", data, 80)[0]
    result = []
    offset = 84
    for _ in range(count):
        values = struct.unpack_from("<9f", data, offset + 12)
        result.append(tuple(tuple(values[index:index + 3]) for index in range(0, 9, 3)))
        offset += 50
    return result


def validate(filename: str, expected_min, expected_max):
    path = ENC / filename
    mesh = triangles(path)
    points = [point for triangle in mesh for point in triangle]
    actual_min = tuple(min(point[axis] for point in points) for axis in range(3))
    actual_max = tuple(max(point[axis] for point in points) for axis in range(3))
    for actual, expected in zip(actual_min + actual_max, expected_min + expected_max):
        assert abs(actual - expected) < 0.011, (path, actual_min, actual_max)
    edges = Counter()
    for triangle in mesh:
        rounded = [tuple(round(value, 5) for value in point) for point in triangle]
        for first, second in ((0, 1), (1, 2), (2, 0)):
            edges[tuple(sorted((rounded[first], rounded[second])))] += 1
    assert all(count == 2 for count in edges.values()), f"{path}: non-manifold mesh"
    print(f"PASS {filename}: {len(mesh)} triangles, manifold")


if __name__ == "__main__":
    validate("idm-roomsensor-b-es4-air-r2_base.stl", (0, 0, 0), (150, 120, 11))
    validate("idm-roomsensor-b-es4-air-r2_lid.stl", (0, 0, 0), (150, 120, 17.95))
    validate("idm-roomsensor-b-es4-air-r2_S5-print-plate.stl", (-155, -60, 0), (155, 60, 17.95))
    assert 310 + 2 * 5 <= 330 and 120 + 2 * 5 <= 240
    print("PASS Ultimaker S5: 310x120 mm plus 5 mm brim")
