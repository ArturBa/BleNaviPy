import unittest

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.location import Location


class BeaconTest(unittest.TestCase):

    beacon = Beacon(Location(1, 1))

    def testInit(self):
        self.assertEqual(Location(1, 1), self.beacon.location)

    def testRSSI(self):
        location = Location(1, 2)
        self.assertEqual(self.beacon.RSSI_0, self.beacon.getRSSI(location))


if __name__ == "__main__":
    unittest.main()
