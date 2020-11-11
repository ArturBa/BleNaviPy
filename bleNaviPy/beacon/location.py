from __future__ import annotations

import math


class Location:
    """
    Location class
    Contains 2D point location in meters
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, location: Location) -> float:
        """Calculate distance between 2 locations

        Args:
            location (Location):

        Returns:
            float: distance between locations
        """
        x_distance = math.pow(self.x - location.x, 2)
        y_distance = math.pow(self.y - location.y, 2)
        distance = math.sqrt(x_distance + y_distance)
        return distance

    def __eq__(self, location: Location):
        return self.x == location.x and self.y == location.y

    def __str__(self):
        return f"Location x: {self.x}\ty: {self.y}"

    def __add__(self, location: Location):
        self.x += location.x
        self.y += location.y
        return self

    def __sub__(self, location: Location):
        print(self, location)
        self.x -= location.x
        self.y -= location.y
        return self
