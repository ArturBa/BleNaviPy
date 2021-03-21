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

    def getDistance(self, point: Point, precistion: int = 4) -> float:
        """Get distance of a point to the closest segment of transition

        Args:
            point (Point): Point to check
            precistion (int, optional): [Return value precistion]. Defaults to 4.

        Returns:
            float: Distance to the segment rounded to (precision) decimal places
        """
        distance = float("inf")
        for i in range(1, len(self.points)):
            d = self.__getSegmentDistance(point, [self.points[i - 1], self.points[i]])
            if d < distance:
                distance = d
        return round(distance, precistion)

    def __getSegmentDistance(self, point: Point, segment: list[Point]) -> float:
        point0 = segment[0]
        point1 = segment[1]

        A = point.x - point0.x
        B = point.y - point0.y
        C = point1.x - point0.x
        D = point1.y - point0.y

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1
        if len_sq != 0:  # in case of 0 length line
            param = dot / len_sq

        xx = 0
        yy = 0

        if param < 0:
            xx = point0.x
            yy = point0.y
        elif param > 1:
            xx = point1.x
            yy = point1.y
        else:
            xx = point0.x + param * C
            yy = point0.y + param * D

        dx = point.x - xx
        dy = point.y - yy
        return math.sqrt(dx * dx + dy * dy)

    def getTheClosestPoint(self, point: Point) -> Point:
        """Get the closest point on any segment

        Args:
            point (Point): [description]

        Returns:
            Point: [description]
        """
        return Point(0, 0.5)
