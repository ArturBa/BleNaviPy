"""This is a module for floor geometry for indoorGML """
from __future__ import annotations

import logging
from typing import List

import numpy as np
from scipy.optimize import minimize

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.user import User
from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class FloorGeometry:
    """
    Class Floor
    Contains information about cells, transitions on a floor
    """

    def __init__(
        self,
        cells: List[CellGeometry],
        transitions: List[TransitionGeometry],
        beacons: List[Beacon] = None,
    ) -> None:
        """Constructor

        Args:
            cells (List[CellGeometry]): List of cells on floor
            transitions (List[TransitionGeometry]): List of transition on floor
            beacons (List[Beacon], optional): [description]. Defaults to None.
        """
        self.cells: List[CellGeometry] = cells
        self.transitions: List[TransitionGeometry] = transitions
        self.beacons: List[Beacon] = [] if beacons is None else beacons
        self.users: List[User] = []
        self.scale = 1

    def __str__(self) -> str:
        return f"Floor. Cells: {len(self.cells)}"

    def setScale(self, scale: float) -> None:
        """Set scale according to a json file (to match a json units to meters)

        Args:
            scale (float): Scale factor
        """
        self.scale = scale

    def addUser(self, user: User) -> None:
        """Add user to a floor

        Args:
            user (User): User to add
        """
        self.users.append(user)

    def getUserLocation(
        self, user_id: int = 0, get_on_transition: bool = False
    ) -> Point:
        """Get user location based on beacons
        Returns:
            Location: User location
        """
        assert user_id < len(self.users), "User out of users table"
        assert user_id >= 0, "User out of users table"
        assert type(user_id) == int, "Incorrect input of user_id"

        location = self._gpsSolve(self.users[user_id])
        logging.info(f"User location for {self.users[user_id]} found: {location}")
        if not get_on_transition:
            return location

        return self._getPointOnClosestTransition(location)

    def _gpsSolve(self, user: User) -> Point:
        def _error(x, c, r):
            return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

        [centers, distances] = self._getCentersAndDistances(user)

        if not self._isEnoughBeacons(centers):
            return Point(0, 0)

        length = len(centers)
        distances_sum = sum(distances)

        # compute weight vector for initial guess
        weight_vector: List[float] = [
            ((length - 1) * distances_sum) / (distances_sum - d) for d in distances
        ]
        # get initial guess of point location
        x0: List[float] = [
            sum([weight_vector[i] * centers[i].x for i in range(length)]),
            sum([weight_vector[i] * centers[i].y for i in range(length)]),
        ]
        centers_f: List[List[float]] = []
        for c in centers:
            centers_f.append([c.x, c.y])
        # optimize distance from signal origin to border of spheres
        found_location = minimize(
            _error, np.array(x0), args=(centers_f, distances), method="Nelder-Mead"
        ).x
        return Point(found_location[0], found_location[1])

    def _getCentersAndDistances(self, user: User) -> [List[Point], Point[float]]:
        centers: List[Point] = []
        distances: List[float] = []
        for b in self.beacons:
            rssi: float = b.getRSSI(user.location, self.scale)
            logging.debug(
                f"Checking {b}; RSSI: {round(rssi, 2)}, "
                + f"is available: {rssi>=user.minRSSI!s:>5}, "
                + f"distance: {round(b.location.distance(user.location, self.scale), 2)}"
            )
            if rssi >= user.minRSSI:
                centers.append(b.location)
                distances.append(b.getDistanceByRSSI(rssi, self.scale))
        return [centers, distances]

    def _isEnoughBeacons(self, centers: List[Point]) -> bool:
        if len(centers) == 1:
            logging.warning(
                f"Using {len(centers)} for location estimation."
                + "Cannot estimate user location."
            )
            return False
        elif len(centers) == 2:
            logging.warning(
                f"Using {len(centers)} for location estimation."
                + "This estimate will be uncertain."
            )
        return True

    def _getPointOnClosestTransition(self, point: Point) -> Point:
        distance = float("inf")
        p = point
        for transition in self.transitions:
            d = transition.getDistance(point)
            if d < distance:
                distance = d
                p = transition.getClosestPoint(point)

        if distance == float("inf"):
            logging.error(
                f"Cannot adopt {point} to any known transition. Please check configuration"
            )
        return p

    def getCellByLocation(self, location: Point) -> CellGeometry:
        """Get a cell by given location

        Args:
            location (Point):

        Returns:
            CellGeometry: found cell
        """
        for cell in self.cells:
            if cell.isPointInside(location):
                return cell
