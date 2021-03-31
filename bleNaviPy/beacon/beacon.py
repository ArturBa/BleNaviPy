from __future__ import annotations

import math
from enum import Enum
from enum import unique
from typing import Union

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


@unique
class BeaconTypeEnum(Enum):
    GENERIC = "generic"


class BeaconType:
    def __init__(self, rssi_1: int, n: float):
        """
        Args:
            rssi_1 (int): Value of rssi in 1m distance
            n (float): Medium resistance factor
        """
        self.RSSI_1 = rssi_1
        self.N = n


class Beacon:
    beaconType = {
        "generic": BeaconType(-80, 2),
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

    def getRSSI(self, location: Point) -> float:
        """Calculate RSSI on given location

        Args:
            location (Location):

        Returns:
            float: RSSI in dB
        """
        # Distance = 10 ^ ((Measured Power — RSSI) / (10 * N))
        distance = location.distance(self.location)
        return -10 * self.N * math.log10(distance) + self.RSSI_1

    def getDistanceByRSSI(self, rss):  # calculate the dist given rss
        return 10 ** ((self.RSSI_1 - rss) / 10.0 / self.N)
