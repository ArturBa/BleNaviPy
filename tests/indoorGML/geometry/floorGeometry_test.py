import unittest

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class LocationTest(unittest.TestCase):
    cellName = "cellName"
    cellPoints = [Point(0, 0), Point(1, 1)]
    cellGeometry = [CellGeometry(cellName, cellPoints)]

    transitionPoints = [Point(0.1, 0.1), Point(0.5, 0.5)]
    transitionGeometry = [TransitionGeometry(transitionPoints)]

    floor: FloorGeometry = FloorGeometry(cellGeometry, transitionGeometry)

    def testInit(self):
        self.assertEqual(len(self.cellGeometry), len(self.floor.cells))
        self.assertEqual(len(self.transitionGeometry), len(self.floor.transitions))

    def testStringify(self):
        self.assertEqual(
            f"Floor. Cells: {len(self.cellGeometry)}", self.floor.__str__()
        )


if __name__ == "__main__":
    unittest.main()
