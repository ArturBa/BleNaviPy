import math
import unittest

from bleNaviPy.indoorGML.geometry.point import Point


class PointTest(unittest.TestCase):
    location = Point(1, 2)

    def testInit(self):
        self.assertEqual(1, self.location.x)
        self.assertEqual(2, self.location.y)

    def testEquability(self):
        location2: Location = Point(1, 2)
        self.assertTrue(location2, self.location)

    def testString(self):
        self.assertTrue(self.location.__str__(), "Location x: 1\ty: 2")

    def testAdd(self):
        location2: Location = Point(2, 1)
        location2 = location2 + self.location
        self.assertEqual(3, location2.x)
        self.assertEqual(3, location2.y)

    def testAddOneArg(self):
        location2: Location = Point(2, 1)
        location2 += self.location
        self.assertEqual(3, location2.x)
        self.assertEqual(3, location2.y)

    def testSub(self):
        location2: Location = Point(2, 1)
        location2 = location2 - self.location
        self.assertEqual(1, location2.x)
        self.assertEqual(-1, location2.y)

    def testSubOneArg(self):
        location2: Location = Point(2, 1)
        location2 -= self.location
        self.assertEqual(1, location2.x)
        self.assertEqual(-1, location2.y)

    def testDistance(self):
        location2: Location = Point(1, 1)
        location3: Location = Point(0, 1)
        self.assertEqual(1, self.location.distance(location2))
        self.assertEqual(math.sqrt(2), self.location.distance(location3))


if __name__ == "__main__":
    unittest.main()
