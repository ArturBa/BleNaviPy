import unittest

from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class LocationTest(unittest.TestCase):
    transitionPoints = [Point(0, 0), Point(1, 0), Point(1, -1)]
    transitionGeometry = TransitionGeometry(transitionPoints)

    def testInit(self):
        self.assertEqual(self.transitionPoints, self.transitionGeometry.points)

    def testStringify(self):
        transitionPoints = [Point(0, 0), Point(0, 1)]
        transitionGeometry = TransitionGeometry(transitionPoints)
        self.assertEqual(
            f"Transition: [{transitionPoints[0].x}, {transitionPoints[0].y}][{transitionPoints[1].x}, {transitionPoints[1].y}]",
            transitionGeometry.__str__(),
        )

    def testDistance(self):
        testPoint = Point(0.3, 0.3)
        self.assertEqual(0.3, self.transitionGeometry.getDistance(testPoint))

        testPoint = Point(0.3, 0.5)
        self.assertEqual(0.5, self.transitionGeometry.getDistance(testPoint))

        testPoint = Point(0.9, -0.9)
        self.assertEqual(0.1, self.transitionGeometry.getDistance(testPoint))

        testPoint = Point(1.3, 0.3)
        self.assertEqual(
            round(0.3 * 2 ** 0.5, 4), self.transitionGeometry.getDistance(testPoint)
        )

    def testClosestPoint(self):
        testPoint = Point(0.3, 0.5)
        closesPoint = Point(0, 0.5)
        self.assertEqual(
            closesPoint, self.transitionGeometry.getTheClosestPoint(testPoint)
        )


if __name__ == "__main__":
    unittest.main()
