import logging
import unittest

import pytest

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.user import User
from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry
from bleNaviPy.indoorGML.parserJSONKeys import ParserJsonKeys

LOGGER = logging.getLogger(__name__)


class FloorGeometrySub(FloorGeometry):
    pass


class FloorGeometryTest(unittest.TestCase):
    cellName = "cellName"
    cellPoints = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
    cellGeometry = [CellGeometry("C1", cellName, cellPoints)]
    beaconPoints = [Point(0, 0), Point(0, 2), Point(2, 0), Point(2, 2)]

    transitionPoints = [Point(0.1, 0.1), Point(0.5, 0.5)]
    transitionGeometry = [TransitionGeometry(transitionPoints)]

    user = User(Point(0.2, 0.3))

    floor: FloorGeometry
    floorScale = 0.5

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.floor = FloorGeometry(self.cellGeometry, self.transitionGeometry)
        for p in self.beaconPoints:
            self.floor.addBeacon(Beacon(p))
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

    def testSetWallDetection(self):
        self.assertFalse(self.floor.wall_detection)
        self.floor.setWallDetection(True)
        self.assertTrue(self.floor.wall_detection)

    def testSetNoise(self):
        self.assertFalse(self.floor.noise)
        self.floor.setNoise(True)
        self.assertTrue(self.floor.noise)

    def testUserLocation(self):
        location = self.floor.getUserLocation()
        self.assertAlmostEqual(0.2, location.x, places=4)
        self.assertAlmostEqual(0.3, location.y, places=4)

    def testUserLocationWithWalls(self):
        self.floor.setWallDetection(True)
        self.floor.cells[0].points = [
            Point(-1, -1),
            Point(3, -1),
            Point(3, 3),
            Point(-1, 3),
        ]
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
        self.floor.transitions = []

        with self._caplog.at_level(logging.INFO):
            location = self.floor.getUserLocation(get_on_transition=True)
            assert "Cannot adopt Point" in self._caplog.text
            self.assertAlmostEqual(0.2, location.x, places=4)
            self.assertAlmostEqual(0.3, location.y, places=4)

    def testUserLocation1Beacon(self):
        self.floor.transitions = []
        self.floor.beacons = [Beacon(Point(2, 2))]

        with self._caplog.at_level(logging.WARNING):
            location = self.floor.getUserLocation()
            assert "Cannot estimate user location" in self._caplog.text
            self.assertEqual(Point(0, 0), location)

    def testUserLocation2Beacon(self):
        self.floor.transitions = []
        self.floor.beacons = [Beacon(Point(2, 2)), Beacon(Point(0, 2))]

        with self._caplog.at_level(logging.WARNING):
            location = self.floor.getUserLocation()
            assert "This estimate will be uncertain." in self._caplog.text

    def testCellByLocation(self):
        point: Point = Point(0.3, 0.3)
        self.assertEqual(self.cellGeometry[0], self.floor.getCellByLocation(point))

    def testIntersection(self):
        floor: FloorGeometrySub = FloorGeometrySub(
            self.cellGeometry, self.transitionGeometry
        )
        self.assertTrue(floor._isWallOnPath(Point(0.5, 0.5), Point(1.5, 0.5)))
        self.assertFalse(floor._isWallOnPath(Point(0.5, 0.5), Point(0.7, 0.5)))

    def testBeaconAdd(self):
        init_beacons_len = len(self.floor.beacons)
        self.floor.addBeacon(Beacon(Point(0, 0)))
        self.assertEqual(init_beacons_len + 1, len(self.floor.beacons))

    def testPropertiesDict(self):
        floor_prop_dict = {
            "scale": 1,
            "wall_detection": False,
            "noise": False,
        }

        self.assertDictEqual(floor_prop_dict, self.floor.getPropertiesDict())

    def testDict(self):
        floor_dict = {
            ParserJsonKeys.property_container.value: {
                ParserJsonKeys.cell_properties.value: [
                    c.getPropertiesDict() for c in self.floor.cells
                ],
                ParserJsonKeys.floor_properties.value: [self.floor.getPropertiesDict()],
            },
            ParserJsonKeys.geometry_container.value: {
                ParserJsonKeys.cell_geometry.value: [
                    c.getDict() for c in self.floor.cells
                ],
                ParserJsonKeys.transition_geometry.value: [
                    t.getDict() for t in self.floor.transitions
                ],
                ParserJsonKeys.beacon_geometry.value: [
                    b.getDict() for b in self.floor.beacons
                ],
                ParserJsonKeys.hole_geometry.value: [
                    c.getHolesDict() for c in self.floor.cells
                ],
            },
        }

        self.assertDictEqual(floor_dict, self.floor.getDict())


if __name__ == "__main__":
    unittest.main()
