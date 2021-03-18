import unittest

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class BeaconTest(unittest.TestCase):

    beacon = Beacon(Point(1, 1))

    def testInit(self):
        self.assertEqual(Point(1, 1), self.beacon.location)

    def testRSSI(self):
        location = Point(1, 2)
        self.assertEqual(self.beacon.RSSI_0, self.beacon.getRSSI(location))


if __name__ == "__main__":
    unittest.main()
