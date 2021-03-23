from __future__ import annotations

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
        self, cells: list[CellGeometry], transitions: list[TransitionGeometry]
    ) -> FloorGeometry:
        """Constructor

        Args:
            cells (list[CellGeometry]): List of cells on floor
            transitions (list[TransitionGeometry]): List of transition on floor

        Returns:
            FloorGeometry:
        """
        self.cells: list[CellGeometry] = cells
        self.transitions: list[TransitionGeometry] = transitions
        self.beacons: list[Beacon] = []
        self.users: list[Point] = []

    def __str__(self) -> str:
        return f"Floor. Cells: {len(self.cells)}"