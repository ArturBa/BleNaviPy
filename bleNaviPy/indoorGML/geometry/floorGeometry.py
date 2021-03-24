from __future__ import annotations

import logging
from typing import List

import numpy as np
from scipy.optimize import minimize

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class FloorGeometry:
    """
    Class Floor
    Contains information about cells, transitions on a floor
    """

    def __init__(
        self, cells: List[CellGeometry], transitions: List[TransitionGeometry]
    ) -> None:
        """Constructor

        Args:
            cells (List[CellGeometry]): List of cells on floor
            transitions (List[TransitionGeometry]): List of transition on floor
        """
        self.cells: List[CellGeometry] = cells
        self.transitions: List[TransitionGeometry] = transitions
        self.beacons: List[Beacon] = []
        self.users: List[Point] = []

    def __str__(self) -> str:
        return f"Floor. Cells: {len(self.cells)}"

    def getUserLocation(
        self, user_id: int = 0, get_on_transition: bool = False
    ) -> Point:
        """Get user location based on beacons
        Returns:
            Location: User location
        """
        location = self._gpsSolve(self.users[user_id])
        if not get_on_transition:
            return location

        return self._getPointOnClosestTransition(location)

    def _gpsSolve(self, user_location: Point) -> Point:
        def error(x, c, r):
            return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

        centers: List[Point] = [b.location for b in self.beacons]
        distances: List[float] = [
            user_location.distance(b.location) for b in self.beacons
        ]
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
            error, np.array(x0), args=(centers_f, distances), method="Nelder-Mead"
        ).x
        return Point(found_location[0], found_location[1])

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
        for cell in self.cells:
            if cell.isPointInside(location):
                return cell
