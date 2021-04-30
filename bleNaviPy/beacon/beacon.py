"""This is a module for beacon geometry"""
from __future__ import annotations

import copy
import logging
import math
from enum import Enum
from enum import unique
from typing import Union

import numpy as np

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

    def __init__(self, rssi_1: int, n: float, n_wall: float, noise_var: float) -> None:
        """
        Args:
            rssi_1 (int): Value of rssi in 1m distance
            n (float): Path loss exponent for building
            n_wall (float): Path loss exponent for obstructed in building
            noise_var (float): Variance of a singal noise
        """
        self.rssi_1 = rssi_1
        self.n = n
        self.n_wall = n_wall
        self.noise_var = noise_var


class Beacon:
    """
    Class beacon
    Contains information about location of beacon
    """

    beaconType = {
        BeaconTypeEnum.GENERIC: BeaconType(-80, 2, 5, 7.5),
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
            beacon_type = self.beaconType.get(beacon_type)

        self.location = location
        for k, v in beacon_type.__dict__.items():
            self.__dict__[k] = copy.deepcopy(v)

    def __str__(self):
        return f"Beacon: [{self.location}]"

    def getRSSI(
        self,
        location: Point,
        scale: float = 1,
        is_wall: bool = False,
        noise: bool = False,
    ) -> float:
        """Calculate RSSI on given location

        Args:
            location (Location):
            scale (float, optional): Floor scale. Defaults to 1.
            is_wall (bool, optional): Is wall on a way. Defaults to False.
            noise (bool, optional): Should noise be added to a signal. Defaults to False.

        Returns:
            float: RSSI in dB
        """
        # Distance = 10 ^ ((Measured Power — RSSI) / (10 * N))
        distance = location.distance(self.location, scale)
        if is_wall:
            n = self.n_wall
        else:
            n = self.n
        signal_strength: float = -10 * n * math.log10(distance) + self.rssi_1
        if noise:
            signal_strength += np.random.normal(0, self.noise_var)
        logging.debug(f"{self} for {location} RSSI: {signal_strength:4.2f}")
        return signal_strength

    def getDistanceByRSSI(self, rssi: float, scale: float = 1) -> float:
        """Get distance from a beacon by rssi

        Args:
            rssi (float): Signal strength
            scale (float, optional): Floor scale. Defaults to 1.

        Returns:
            float: Distance from beacon using a map units
        """
        distance: float = 10 ** ((self.rssi_1 - rssi) / 10.0 / self.n) * 1 / scale
        logging.debug(
            f"{self} for {rssi:4.2f} Distance: {distance:4.2f} on scale {scale}"
        )
        return distance

    def getDict(self) -> dict:
        """Get save ready beacon dictionary

        Returns:
            dict: save ready beacon dictionary
        """
        return {
            "points": self.location.getDict(),
            "rssi_1": self.rssi_1,
            "n": self.n,
            "n_wall": self.n_wall,
            "noise_var": self.noise_var,
        }
