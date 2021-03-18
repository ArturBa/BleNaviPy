import unittest

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.point import Point


class LocationTest(unittest.TestCase):
    cellName = "cellName"
    cellPoints = [Point(0, 0), Point(1, 1)]
    cellGeometry = CellGeometry(cellName, cellPoints)

    def testInit(self):
        self.assertEqual(self.cellName, self.cellGeometry.name)
        self.assertEqual(self.cellPoints, self.cellGeometry.points)

    def testStringify(self):
        self.assertEqual(
            f"Cell: {self.cellName} Points: [{self.cellPoints[0].x}, {self.cellPoints[0].y}][{self.cellPoints[1].x}, {self.cellPoints[1].y}]",
            self.cellGeometry.__str__(),
        )


if __name__ == "__main__":
    unittest.main()
