from __future__ import annotations

from typing import List

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class CellGeometry:
    """
    CellGeometry class
    Contains information about cell shape and name

    """

    def __init__(self, name: str, points: List[Point]) -> None:
        """Constructor

        Args:
            name (str): Cell name
            points (List[Point]): Cell boundaries

        Returns:
            CellGeometry: Cell Geometry
        """
        self.name: str = name
        self.points: List[Point] = points
        self.holes = []

    def __str__(self) -> str:
        s: str = ""
        for point in self.points:
            s += f"[{point.x}, {point.y}]"
        return f"Cell: {self.name} Points: " + s
