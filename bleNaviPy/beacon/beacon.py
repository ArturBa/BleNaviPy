"""This is a module for beacon geometry"""
from __future__ import annotations

import logging
import math
from enum import Enum
from enum import unique
from typing import Union

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


@unique
class BeaconTypeEnum(Enum):
    """Beacon types enum

    Args:
        Enum:
    """

    GENERIC = "generic"


class BeaconType:
    """Beacon type with default data"""

    def __init__(self, rssi_1: int, n: float, n_wall: float) -> None:
        """
        Args:
            rssi_1 (int): Value of rssi in 1m distance
            n (float): Medium (air) resistance factor
            n_wall (float): Medium (air+wall) resistance factor
        """
        self.RSSI_1 = rssi_1
        self.N = n
        self.N_wall = n_wall


class Beacon:
    """
    Class beacon
    Contains information about location of beacon
    """

    beaconType = {
        "generic": BeaconType(-80, 2, 3),
    }

    def __init__(
        self,
        location: Point,
        beacon_type: Union[BeaconTypeEnum, BeaconType] = BeaconTypeEnum.GENERIC,
    ) -> None:
        """Constructor

        Args:
            location (Point): Location of the beacon
        """
        if isinstance(beacon_type, BeaconTypeEnum):
            beacon_type = self.beaconType.get(beacon_type.value)

        self.location = location
        self.RSSI_1 = beacon_type.RSSI_1
        self.N = beacon_type.N
        self.N_wall = beacon_type.N_wall

    def __str__(self):
        return f"Beacon: [{self.location}]"

    def getRSSI(
        self, location: Point, scale: float = 1, is_wall: bool = False
    ) -> float:
        """Calculate RSSI on given location

        Args:
            location (Location):
            scale (float, optional): Floor scale. Defaults to 1.
            is_wall (bool, optional): Is wall on a way. Defaults to False.

        Returns:
            float: RSSI in dB
        """
        # Distance = 10 ^ ((Measured Power — RSSI) / (10 * N))
        distance = location.distance(self.location, scale)
        if is_wall:
            signal_strength: float = (
                -10 * self.N_wall * math.log10(distance) + self.RSSI_1
            )
        else:
            signal_strength: float = -10 * self.N * math.log10(distance) + self.RSSI_1
        logging.debug(f"{self} for {location} RSSI: {round(signal_strength, 2)}")
        return signal_strength

    def getDistanceByRSSI(self, rssi: float, scale: float = 1) -> float:
        """Get distance from a beacon by rssi

        Args:
            rssi (float): Signal strength
            scale (float, optional): Floor scale. Defaults to 1.

        Returns:
            float: Distance from beacon using a map units
        """
        distance: float = 10 ** ((self.RSSI_1 - rssi) / 10.0 / self.N) * 1 / scale
        logging.debug(
            f"{self} for {round(rssi, 2)} Distance: {round(distance, 2)} on scale {scale}"
        )
        return distance
