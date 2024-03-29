"""This is a module for point geometry in indoorGML geometry"""
from __future__ import annotations

import math


class Point:
    """
    Point class
    Contains 2D point location
    """

    def __init__(self, x: float, y: float) -> None:
        """Constructor

        Args:
            x (float):
            y (float):
        """
        self.x = x
        self.y = y

    def distance(self, point: Point, scale: float = 1) -> float:
        """Calculate distance between 2 locations

        Args:
            point (Point):
            scale (float, optional): Floor scale. Defaults to 1.

        Returns:
            float: distance between point
        """
        x_distance = math.pow(self.x - point.x, 2)
        y_distance = math.pow(self.y - point.y, 2)
        distance = math.sqrt(x_distance + y_distance)
        return distance * scale

    def __eq__(self, point: Point) -> bool:
        """Check if points are equal

        Args:
            point (Point): Point to check

        Returns:
            bool: True if points x's any y's are identical
        """
        return self.x == point.x and self.y == point.y

    def __str__(self) -> str:
        return f"Point [{self.x}; {self.y}]"

    def __add__(self, point: Point) -> Point:
        """Add 2 points

        Args:
            point (Point): Point to sum

        Returns:
            Point:
        """
        self.x += point.x
        self.y += point.y
        return self

    def __sub__(self, point: Point) -> Point:
        """Subtract 2 points

        Args:
            point (Point): Point to subtract

        Returns:
            Point:
        """
        self.x -= point.x
        self.y -= point.y
        return self

    def getDict(self) -> dict:
        """Get dictionary form of point geometry ready for a saving

        Returns:
            dict: Save ready dict form of point geometry
        """
        return {"point": {"x": self.x, "y": self.y}}
