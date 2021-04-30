import unittest

import numpy

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class BeaconTest(unittest.TestCase):

    beacon = Beacon(Point(1, 1))

    def testInit(self):
        self.assertEqual(Point(1, 1), self.beacon.location)

    def testRSSI_1m(self):
        location = Point(1, 2)
        self.assertEqual(self.beacon.RSSI_1, self.beacon.getRSSI(location))

    def testRSSI_2m(self):
        location = Point(1, 3)
        self.beacon.RSSI_1 = -69
        self.assertAlmostEqual(-75, self.beacon.getRSSI(location), 1)

    def testRSSI_2mWall(self):
        location = Point(1, 3)
        self.beacon.RSSI_1 = -69
        self.assertGreater(-75, self.beacon.getRSSI(location, is_wall=True))

    def testRSSI_2mNoise(self):
        location = Point(1, 3)
        numpy.random.seed(0)
        self.beacon.RSSI_1 = -69
        self.assertLess(-75 - self.beacon.getRSSI(location, noise=True), 10)

    def testLocationByRSSI(self):
        location = Point(1, 3)
        self.assertAlmostEqual(
            location.distance(self.beacon.location),
            self.beacon.getDistanceByRSSI(self.beacon.getRSSI(location)),
            1,
        )


if __name__ == "__main__":
    unittest.main()
