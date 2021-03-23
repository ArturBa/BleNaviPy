import unittest

from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.parserJSON import ParserJSON


class LocationTest(unittest.TestCase):
    def testGetGeometryFromFile(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromFile(
            "tests/indoorGML/parserTest.json"
        )
        self.assertEqual(5, len(floor.cells))


if __name__ == "__main__":
    unittest.main()
