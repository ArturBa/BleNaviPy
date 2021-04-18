"""This is a module for user geometry for indoorGML """
from __future__ import annotations

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class User:
    """
    User
    Contains information about user location and min signal strength
    """

    def __init__(self, location: Point, minRSSI: float = -95):
        """Constructor

        Args:
            location (Point): User location
            minRSSI (float, optional): Min RSSI detected by user. Defaults to -95.
        """
        self.location = location
        self.minRSSI = minRSSI

    def __str__(self):
        """Stringify

        Returns:
            [type]: Self description string
        """
        return f"User: {self.location}"
