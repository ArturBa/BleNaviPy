from __future__ import annotations

import math


class Point:
    """
    Point class
    Contains 2D point location
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, point: Point) -> float:
        """Calculate distance between 2 locations

        Args:
            point (Point):

        Returns:
            float: distance between point
        """
        x_distance = math.pow(self.x - point.x, 2)
        y_distance = math.pow(self.y - point.y, 2)
        distance = math.sqrt(x_distance + y_distance)
        return distance

    def __eq__(self, point: Point):
        return self.x == point.x and self.y == point.y

    def __str__(self):
        return f"Location x: {self.x}\ty: {self.y}"

    def __add__(self, point: Point):
        self.x += point.x
        self.y += point.y
        return self

    def __sub__(self, point: Point):
        self.x -= point.x
        self.y -= point.y
        return self
