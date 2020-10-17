import unittest

from bleNaviPy.beacon.location import Location


class LocationTest(unittest.TestCase):
    location = Location(1, 2)

    def testInit(self):
        self.assertEqual(self.location.x, 1)
        self.assertEqual(self.location.y, 2)

    def testEquability(self):
        location2: Location = Location(1, 2)
        self.assertTrue(self.location, location2)

    def testString(self):
        self.assertTrue(self.location.__str__(), "Location x: 1\ty: 2")

    def testAdd(self):
        location2: Location = Location(2, 1)
        location2 = location2 + self.location
        self.assertEqual(location2.x, 3)
        self.assertEqual(location2.y, 3)

    def testAddOneArg(self):
        location2: Location = Location(2, 1)
        location2 += self.location
        self.assertEqual(location2.x, 3)
        self.assertEqual(location2.y, 3)

    def testSub(self):
        location2: Location = Location(2, 1)
        location2 = location2 - self.location
        self.assertEqual(location2.x, 1)
        self.assertEqual(location2.y, -1)

    def testSubOneArg(self):
        location2: Location = Location(2, 1)
        location2 -= self.location
        self.assertEqual(location2.x, 1)
        self.assertEqual(location2.y, -1)


if __name__ == "__main__":
    unittest.main()
