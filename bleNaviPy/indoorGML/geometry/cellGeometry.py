from __future__ import annotations

import logging
from typing import List

from bleNaviPy.indoorGML.geometry.holeGeometry import HoleGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class CellGeometry:
    """
    CellGeometry class
    Contains information about cell shape and name

    """

    def __init__(self, id: str, name: str, points: List[Point]) -> None:
        """Constructor

        Args:
            id (str): Cell id
            name (str): Cell name
            points (List[Point]): Cell boundaries
        """
        self.id = id
        self.name: str = name
        self.points: List[Point] = points
        self.holes: List[List[Point]] = []

    def addHole(self, hole: HoleGeometry) -> None:
        if hole.memberOf is not self.id:
            logging.error(
                f"Cannot add hole {hole} to {self.name}. "
                + f"Hole is member of: {hole.memberOf} "
                + f"while cell id is: {self.id}"
            )
            return

        for point in hole.boundary:
            if not self.isPointInside(point):
                logging.error(
                    f"Cannot add hole {hole} to {self.name}. "
                    + "Please check if hole fits inside."
                )
                return
        self.holes.append(hole.boundary)

    def isPointInside(self, point: Point) -> bool:
        is_in_cell: bool = self._isInsideCell(point)
        logging.info(is_in_cell)
        for i in range(len(self.holes)):
            if self._isInsideHole(point, i):
                logging.info("In a hole")
                return False
        return is_in_cell

    def _isInsideCell(self, point: Point) -> bool:
        return isPointInsidePolynomial(self.points, point)

    def _isInsideHole(self, point: Point, hole_id: int) -> bool:
        return isPointInsidePolynomial(self.holes[hole_id], point)

    def __str__(self) -> str:
        s: str = ""
        for point in self.points:
            s += f"[{point.x}, {point.y}]"
        return f"Cell: {self.name} Points: " + s


def isPointInsidePolynomial(polynomial: List[Point], point: Point) -> bool:
    ans = False
    for i in range(len(polynomial)):
        x0 = polynomial[i].x
        y0 = polynomial[i].y
        x1 = polynomial[(i + 1) % len(polynomial)].x
        y1 = polynomial[(i + 1) % len(polynomial)].y
        if not min(y0, y1) < point.y <= max(y0, y1):
            continue
        if point.x < min(x0, x1):
            continue
        cur_x = x0 if x0 == x1 else x0 + (point.y - y0) * (x1 - x0) / (y1 - y0)
        ans ^= point.x > cur_x
    return ans
