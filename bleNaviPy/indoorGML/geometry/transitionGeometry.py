"""This is a module for transition geometry for indoorGML """
from __future__ import annotations

from typing import List

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


def getClosestPointOnSegment(point: Point, segment: List[Point]) -> Point:
    """Get point closest on segment

    Args:
        point (Point):
        segment (List[List[Point]]): Transition segment

    Returns:
        Point: Point on segment
    """
    point0 = segment[0]
    point1 = segment[1]

    a = point.x - point0.x
    b = point.y - point0.y
    c = point1.x - point0.x
    d = point1.y - point0.y

    dot = a * c + b * d
    len_sq = c * c + d * d
    param = -1
    if len_sq != 0:  # in case of 0 length line
        param = dot / len_sq

    if param < 0:
        xx = point0.x
        yy = point0.y
    elif param > 1:
        xx = point1.x
        yy = point1.y
    else:
        xx = point0.x + param * c
        yy = point0.y + param * d

    return Point(xx, yy)


class TransitionGeometry:
    """
    Class transition
    Contains information about paths
    """

    def __init__(self, points: List[Point]) -> None:
        """Constructor

        Args:
            points (List[Point]): Path to move by points

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
    def segments(self) -> List[List[Point]]:
        """Get line segments of transition

        Returns:
            List[List[Point]]: Line segments
        """
        return [
            [self.points[i - 1], self.points[i]] for i in range(1, len(self.points))
        ]

    def getDistance(self, point: Point, precision: int = 4, scale: float = 1) -> float:
        """Get distance of a point to the closest segment of transition

        Args:
            point (Point): Point to check
            precision (int, optional): [Return value precision]. Defaults to 4.
            scale (float, optional): Floor scale. Defaults to 1.

        Returns:
            float: Distance to the segment rounded to (precision) decimal places
        """
        closest_point: Point = self.getClosestPoint(point)
        distance: float = point.distance(closest_point, scale)
        return round(distance, precision)

    def _getClosestSegmentId(self, point: Point) -> int:
        """Get id of the closes segment to point

        Args:
            point (Point):

        Returns:
            int: Id of closest segment
        """
        segment_id = 0
        distance: float = float("inf")
        for i in range(len(self.segments)):
            dist: float = point.distance(
                getClosestPointOnSegment(point, self.segments[i])
            )
            if dist < distance:
                distance = dist
                segment_id = i
        return segment_id

    def getClosestPoint(self, point: Point) -> Point:
        """Get the closest point on any segment

        Args:
            point (Point): Test point

        Returns:
            Point: Closest Point
        """

        closest_segment: int = self._getClosestSegmentId(point)
        closest_point: Point = getClosestPointOnSegment(
            point, self.segments[closest_segment]
        )
        return closest_point

    def getDict(self) -> dict:
        return {"points": [p.getDict() for p in self.points]}
