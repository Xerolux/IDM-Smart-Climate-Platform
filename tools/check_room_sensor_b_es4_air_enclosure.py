#!/usr/bin/env python3
"""Validate B-ES4-AIR enclosure STL meshes and S5 bed fit."""

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
        assert len(values) % 3 == 0, f"invalid ASCII STL: {path}"
        return [tuple(values[i:i + 3]) for i in range(0, len(values), 3)]
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
    actual_min = tuple(min(point[a] for point in points) for a in range(3))
    actual_max = tuple(max(point[a] for point in points) for a in range(3))
    for actual, expected in zip(actual_min + actual_max, expected_min + expected_max):
        assert abs(actual - expected) < 0.011, (path, actual_min, actual_max)
    edges = Counter()
    for tri in tris:
        rounded = [tuple(round(v, 5) for v in point) for point in tri]
        for first, second in ((0, 1), (1, 2), (2, 0)):
            edges[tuple(sorted((rounded[first], rounded[second])))] += 1
    bad = [edge for edge, count in edges.items() if count != 2]
    assert not bad, f"{path}: {len(bad)} non-manifold edges"
    print(f"PASS {filename}: {len(tris)} triangles, manifold, bounds OK")


if __name__ == "__main__":
    validate_mesh("idm-roomsensor-b-es4-air_base.stl", (0, 0, 0), (150, 120, 11))
    validate_mesh("idm-roomsensor-b-es4-air_lid.stl", (0, 0, 0), (150, 120, 17.95))
    validate_mesh(
        "idm-roomsensor-b-es4-air_S5-print-plate.stl",
        (-155, -60, 0), (155, 60, 17.95),
    )
    assert 310 + 2 * 5 <= 330
    assert 120 + 2 * 5 <= 240
    print("PASS Ultimaker S5 bed fit: 310x120 mm model plus 5 mm brim")
