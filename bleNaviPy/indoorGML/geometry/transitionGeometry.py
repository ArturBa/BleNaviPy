from __future__ import annotations

import math

import numpy as np
from numpy.linalg import norm

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class TransitionGeometry:
    """
    Class transition
    Contains information about paths
    """

    def __init__(self, points: list[Point]) -> TransitionGeometry:
        """Constructor

        Args:
            points (list[Point]): Path to move by points

        Returns:
            TransitionGeometry:
        """
        self.points = points

    def __str__(self) -> str:
        s: str = ""
        for point in self.points:
            s += f"[{point.x}, {point.y}]"
        return f"Transition: " + s

    @property
    def segments(self) -> list[[Point, Point]]:
        """Get line segments of transition

        Returns:
            list[[Point, Point]]: Line segments
        """
        return [
            [self.points[i - 1], self.points[i]] for i in range(1, len(self.points))
        ]

    def getDistance(self, point: Point, precistion: int = 4) -> float:
        """Get distance of a point to the closest segment of transition

        Args:
            point (Point): Point to check
            precistion (int, optional): [Return value precistion]. Defaults to 4.

        Returns:
            float: Distance to the segment rounded to (precision) decimal places
        """
        closestPoint: Point = self.getClosestPoint(point)
        distance: float = point.distance(closestPoint)
        return round(distance, precistion)

    def _getClosestPointOnSegment(
        self, point: Point, segment: list[[Point, Point]]
    ) -> Point:
        """Get point closest on segment

        Args:
            point (Point):
            segment (list[[Point, Point]]): Transition segment

        Returns:
            Point: Point on segment
        """
        point0 = segment[0]
        point1 = segment[1]

        A = point.x - point0.x
        B = point.y - point0.y
        C = point1.x - point0.x
        D = point1.y - point0.y

        dot = A * C + B * D
        lenSq = C * C + D * D
        param = -1
        if lenSq != 0:  # in case of 0 length line
            param = dot / lenSq

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

        return Point(xx, yy)

    def _getClosestSegmentId(self, point: Point) -> int:
        """Get id of the closes segment to point

        Args:
            point (Point):

        Returns:
            int: Id of closest segment
        """
        segmentId = 0
        distance: float = float("inf")
        for i in range(len(self.segments)):
            d: float = point.distance(
                self._getClosestPointOnSegment(point, self.segments[i])
            )
            if d < distance:
                distance = d
                segmentId = i
        return segmentId

    def getClosestPoint(self, point: Point) -> Point:
        """Get the closest point on any segment

        Args:
            point (Point): Test point

        Returns:
            Point: Closest Point
        """

        closestSegment: int = self._getClosestSegmentId(point)
        closestPoint: Point = self._getClosestPointOnSegment(
            point, self.segments[closestSegment]
        )
        return closestPoint
