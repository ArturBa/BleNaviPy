import logging
import unittest

import pytest

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.user import User
from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry

LOGGER = logging.getLogger(__name__)


class LocationTest(unittest.TestCase):
    cellName = "cellName"
    cellPoints = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
    cellGeometry = [CellGeometry("C1", cellName, cellPoints)]

    transitionPoints = [Point(0.1, 0.1), Point(0.5, 0.5)]
    transitionGeometry = [TransitionGeometry(transitionPoints)]

    user = User(Point(0.2, 0.3))

    floor: FloorGeometry = FloorGeometry(cellGeometry, transitionGeometry)
    floorScale = 0.5

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.floor.beacons.append(Beacon(Point(2, 2)))
        self.floor.beacons.append(Beacon(Point(0, 0)))
        self.floor.beacons.append(Beacon(Point(0, 2)))
        self.floor.beacons.append(Beacon(Point(2, 0)))
        self.floor.addUser(self.user)

    def testInit(self):
        self.assertEqual(len(self.cellGeometry), len(self.floor.cells))
        self.assertEqual(len(self.transitionGeometry), len(self.floor.transitions))

    def testSetScale(self):
        self.floor.setScale(self.floorScale)
        self.assertEqual(self.floorScale, self.floor.scale)

    def testStringify(self):
        self.assertEqual(
            f"Floor. Cells: {len(self.cellGeometry)}", self.floor.__str__()
        )

    def testUserLocation(self):
        location = self.floor.getUserLocation()
        self.assertAlmostEqual(0.2, location.x, places=4)
        self.assertAlmostEqual(0.3, location.y, places=4)

    def testUserLocationErrors(self):
        with pytest.raises(AssertionError, match=r"User out of users table"):
            self.floor.getUserLocation(-1)
        with pytest.raises(AssertionError, match=r"User out of users table"):
            self.floor.getUserLocation(100)
        with pytest.raises(AssertionError, match=r"Incorrect input *"):
            self.floor.getUserLocation(0.1)

    def testUserLocationOnTransition(self):
        location = self.floor.getUserLocation(get_on_transition=True)
        self.assertAlmostEqual(0.25, location.x, places=4)
        self.assertAlmostEqual(0.25, location.y, places=4)

    def testUserLocationNoTransitionAdded(self):
        floor: FloorGeometry = FloorGeometry(self.cellGeometry, [])
        floor.beacons.append(Beacon(Point(2, 2)))
        floor.beacons.append(Beacon(Point(0, 0)))
        floor.beacons.append(Beacon(Point(0, 2)))
        floor.beacons.append(Beacon(Point(2, 0)))
        floor.addUser(self.user)

        with self._caplog.at_level(logging.INFO):
            location = floor.getUserLocation(get_on_transition=True)
            assert "Cannot adopt Point" in self._caplog.text
            self.assertAlmostEqual(0.2, location.x, places=4)
            self.assertAlmostEqual(0.3, location.y, places=4)

    def testUserLocation1Beacon(self):
        floor: FloorGeometry = FloorGeometry(self.cellGeometry, [])
        floor.beacons.append(Beacon(Point(2, 2)))
        floor.addUser(self.user)

        with self._caplog.at_level(logging.WARNING):
            location = floor.getUserLocation()
            assert "Cannot estimate user location" in self._caplog.text
            self.assertEqual(Point(0, 0), location)

    def testUserLocation2Beacon(self):
        floor: FloorGeometry = FloorGeometry(self.cellGeometry, [])
        floor.beacons.append(Beacon(Point(2, 2)))
        floor.beacons.append(Beacon(Point(0, 2)))
        floor.addUser(self.user)

        with self._caplog.at_level(logging.WARNING):
            location = floor.getUserLocation()
            assert "This estimate will be uncertain." in self._caplog.text

    def testCellByLocation(self):
        point: Point = Point(0.3, 0.3)
        self.assertEqual(self.cellGeometry[0], self.floor.getCellByLocation(point))


if __name__ == "__main__":
    unittest.main()
