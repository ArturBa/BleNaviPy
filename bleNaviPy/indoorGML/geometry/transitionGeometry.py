from __future__ import annotations

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class TransitionGeometry:
    def __init__(self, points: list[Point]) -> TransitionGeometry:
        self.points = points

    def __str__(self) -> str:
        s: str = ""
        for point in self.points:
            s += f"[{point.x}, {point.y}]"
        return f"Transition: " + s

    def getDistance(self, point: Point) -> double:
        return 0.3

    def getTheClosestPoint(self, point: Point) -> Point:
        return Point(0, 0.5)
