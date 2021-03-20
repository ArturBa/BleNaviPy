from __future__ import annotations

import math

import numpy as np
from numpy.linalg import norm

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

        p3 = np.asarray([point.x, point.y])
        distance = float("inf")
        for i in range(1, len(self.points)):
            p1 = np.asarray([self.points[i - 1].x, self.points[i - 1].y])
            p2 = np.asarray([self.points[i].x, self.points[i].y])
            d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
            if d < distance:
                distance = d
        return round(distance, 4)

    def getTheClosestPoint(self, point: Point) -> Point:
        return Point(0, 0.5)
