import math
import unittest

from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class PointTest(unittest.TestCase):
    point = Point(1, 2)

    def testInit(self):
        self.assertEqual(1, self.point.x)
        self.assertEqual(2, self.point.y)

    def testEquability(self):
        point2: Point = Point(1, 2)
        self.assertTrue(point2, self.point)

    def testString(self):
        self.assertTrue(self.point.__str__(), "Point [1; 2]")

    def testAdd(self):
        point2: Point = Point(2, 1)
        point2 = point2 + self.point
        self.assertEqual(3, point2.x)
        self.assertEqual(3, point2.y)

    def testAddOneArg(self):
        point2: Point = Point(2, 1)
        point2 += self.point
        self.assertEqual(3, point2.x)
        self.assertEqual(3, point2.y)

    def testSub(self):
        point2: Point = Point(2, 1)
        point2 = point2 - self.point
        self.assertEqual(1, point2.x)
        self.assertEqual(-1, point2.y)

    def testSubOneArg(self):
        point2: Point = Point(2, 1)
        point2 -= self.point
        self.assertEqual(1, point2.x)
        self.assertEqual(-1, point2.y)

    def testDistance(self):
        point2: Point = Point(1, 1)
        point3: Point = Point(0, 1)
        self.assertEqual(1, self.point.distance(point2))
        self.assertEqual(math.sqrt(2), self.point.distance(point3))


if __name__ == "__main__":
    unittest.main()
