from __future__ import annotations

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class FloorGeometry:
    def __init__(
        self, cells: list[CellGeometry], transitions: list[TransitionGeometry]
    ) -> FloorGeometry:
        self.cells: list[CellGeometry] = cells
        self.transitions: list[TransitionGeometry] = transitions
