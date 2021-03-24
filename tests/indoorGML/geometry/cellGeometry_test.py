import logging
import unittest

import pytest

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.holeGeometry import HoleGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class LocationTest(unittest.TestCase):
    cellId = "C1"
    cellName = "cellName"
    cellPoints = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
    cellGeometry = CellGeometry(cellId, cellName, cellPoints)

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def testInit(self):
        self.assertEqual(self.cellId, self.cellGeometry.id)
        self.assertEqual(self.cellName, self.cellGeometry.name)
        self.assertEqual(self.cellPoints, self.cellGeometry.points)

    def testStringify(self):
        self.assertEqual(
            f"Cell: {self.cellName} Points: "
            + f"[{self.cellPoints[0].x}, {self.cellPoints[0].y}]"
            + f"[{self.cellPoints[1].x}, {self.cellPoints[1].y}]"
            + f"[{self.cellPoints[2].x}, {self.cellPoints[2].y}]"
            + f"[{self.cellPoints[3].x}, {self.cellPoints[3].y}]",
            self.cellGeometry.__str__(),
        )

    def testAddHole(self):
        hole_geometry = HoleGeometry(
            [Point(0.3, 0.3), Point(0.3, 0.5), Point(0.5, 0.3)], self.cellId
        )
        self.cellGeometry.addHole(hole_geometry)
        self.assertEqual(1, len(self.cellGeometry.holes))

    def testAddHoleWrongId(self):
        hole_geometry = HoleGeometry(
            [Point(0.3, 0.3), Point(0.3, 0.5), Point(0.5, 0.3)], self.cellId + "bad"
        )
        with self._caplog.at_level(logging.INFO):
            self.cellGeometry.addHole(hole_geometry)
            assert (
                f"Hole is member of: {hole_geometry.memberOf} while cell id is: {self.cellId}"
                in self._caplog.text
            )

    def testAddHoleOutsideOfCell(self):
        hole_geometry = HoleGeometry(
            [Point(2, 3), Point(3, 5), Point(5, 2)], self.cellId
        )
        with self._caplog.at_level(logging.INFO):
            self.cellGeometry.addHole(hole_geometry)
            assert f"Please check if hole fits inside." in self._caplog.text

    def testIsInside(self):
        self.assertTrue(self.cellGeometry.isPointInside(Point(0.5, 0.5)))
        self.assertFalse(self.cellGeometry.isPointInside(Point(5, 5)))
        self.assertTrue(self.cellGeometry.isPointInside(Point(0.5, 1)))
        # self.assertTrue(self.cellGeometry.isPointInside(Point(0.1, 0)))


if __name__ == "__main__":
    unittest.main()
