"""This is a module for hole geometry for indoorGML """
from __future__ import annotations

from typing import List

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class HoleGeometry:
    """
    Class hole
    Contains information about hole in cells
    """

    def __init__(self, boundary: List[Point], member_of: str) -> None:
        """Constructor

        Args:
            boundary (List[Point]): Boundary of hole
            member_of (str): Cell id
        """
        self.boundary: List[Point] = boundary
        self.memberOf: str = member_of

    def __str__(self) -> str:
        return f"Hole in {self.memberOf}"
