from __future__ import annotations

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class CellGeometry:
    """
    CellGeometry class
    Contains information about cell shape and name

    """

    def __init__(self, name: str, points: list[Point]) -> CellGeometry:
        self.name = name
        self.points = points
        self.holes = []

    def __str__(self) -> str:
        s: str = ""
        for point in self.points:
            s += f"[{point.x}, {point.y}]"
        return f"Cell: {self.name} Points: " + s
