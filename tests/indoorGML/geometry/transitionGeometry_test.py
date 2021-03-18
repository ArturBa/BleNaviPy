import unittest

from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class LocationTest(unittest.TestCase):
    transitionPoints = [Point(0, 0), Point(0, 1)]
    transitionGeometry = TransitionGeometry(transitionPoints)

    def testInit(self):
        self.assertEqual(self.transitionPoints, self.transitionGeometry.points)

    def testStringify(self):
        self.assertEqual(
            f"Transition: [{self.transitionPoints[0].x}, {self.transitionPoints[0].y}][{self.transitionPoints[1].x}, {self.transitionPoints[1].y}]",
            self.transitionGeometry.__str__(),
        )

    def testDistance(self):
        testPoint = Point(0.3, 0.5)
        self.assertEqual(0.3, self.transitionGeometry.getDistance(testPoint))

    def testClosestPoint(self):
        testPoint = Point(0.3, 0.5)
        closesPoint = Point(0, 0.5)
        self.assertEqual(
            closesPoint, self.transitionGeometry.getTheClosestPoint(testPoint)
        )


if __name__ == "__main__":
    unittest.main()
