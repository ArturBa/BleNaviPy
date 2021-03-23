import unittest

from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import getClosestPointOnSegment
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class LocationTest(unittest.TestCase):
    transitionPoints = [Point(0, 0), Point(1, 0), Point(1, -1)]
    transitionGeometry = TransitionGeometry(transitionPoints)

    def testInit(self):
        self.assertEqual(self.transitionPoints, self.transitionGeometry.points)

    def testStringify(self):
        transition_points = [Point(0, 0), Point(0, 1)]
        transition_geometry = TransitionGeometry(transition_points)
        self.assertEqual(
            f"Transition: [{transition_points[0].x}, {transition_points[0].y}]"
            + f"[{transition_points[1].x}, {transition_points[1].y}]",
            transition_geometry.__str__(),
        )

    def testSegments(self):
        segments = []
        for i in range(1, len(self.transitionPoints)):
            segments.append([self.transitionPoints[i - 1], self.transitionPoints[i]])

        self.assertEqual(segments, self.transitionGeometry.segments)

    def testDistance(self):
        test_point = Point(0.3, 0.3)
        self.assertEqual(0.3, self.transitionGeometry.getDistance(test_point))

        test_point = Point(0.3, 0.5)
        self.assertEqual(0.5, self.transitionGeometry.getDistance(test_point))

        test_point = Point(0.9, -0.9)
        self.assertEqual(0.1, self.transitionGeometry.getDistance(test_point))

        test_point = Point(1.3, 0.3)
        self.assertEqual(
            round(0.3 * 2 ** 0.5, 4), self.transitionGeometry.getDistance(test_point)
        )

        test_point = Point(1.3, 0.3)
        self.assertEqual(
            round(0.3 * 2 ** 0.5, 6), self.transitionGeometry.getDistance(test_point, 6)
        )

    def testClosestSegment(self):
        self.assertEqual(0, self.transitionGeometry._getClosestSegmentId(Point(-1, 0)))

    def testClosestPointOnSegment(self):
        segment = [Point(0, 0), Point(1, 0)]

        self.assertEqual(
            segment[0],
            getClosestPointOnSegment(Point(-1, 0), segment),
        )
        self.assertEqual(
            segment[1],
            getClosestPointOnSegment(Point(2, 0), segment),
        )
        self.assertEqual(
            Point(0.5, 0),
            getClosestPointOnSegment(Point(0.5, 2), segment),
        )

    def testClosestPoint(self):
        test_point = Point(0.3, 0.5)
        closes_point = Point(0.3, 0)

        self.assertEqual(
            closes_point, self.transitionGeometry.getClosestPoint(test_point)
        )


if __name__ == "__main__":
    unittest.main()
