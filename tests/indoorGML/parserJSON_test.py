import unittest

from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.parserJSON import ParserJSON


class LocationTest(unittest.TestCase):
    filename: str = "tests/indoorGML/parserTest.json"
    projectData = {
        "geometryContainer": {
            "cellGeometry": [
                {
                    "id": "001",
                    "points": [
                        {"point": {"x": 1, "y": 1}},
                        {"point": {"x": 2, "y": 1}},
                        {"point": {"x": 2, "y": 2}},
                        {"point": {"x": 1, "y": 2}},
                    ],
                },
                {
                    "id": "002",
                    "points": [
                        {"point": {"x": 1, "y": 1}},
                        {"point": {"x": 2, "y": 1}},
                        {"point": {"x": 2, "y": 2}},
                        {"point": {"x": 1, "y": 2}},
                    ],
                },
            ],
            "transitionGeometry": [
                {
                    "points": [
                        {"point": {"x": 1, "y": 1}},
                        {"point": {"x": 2, "y": 1}},
                        {"point": {"x": 2, "y": 2}},
                        {"point": {"x": 1, "y": 2}},
                    ],
                },
                {
                    "points": [
                        {"point": {"x": 1, "y": 1}},
                        {"point": {"x": 2, "y": 1}},
                        {"point": {"x": 2, "y": 2}},
                        {"point": {"x": 1, "y": 2}},
                    ],
                },
            ],
        },
        "propertyContainer": {"cellProperties": [{"id": "001", "name": "name001"}]},
    }

    def testGetGeometryFromFile(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromFile(self.filename)
        self.assertEqual(5, len(floor.cells))

    def testGetGeometryFromFileFailure(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromFile(
            "tests/indoorGML/nonExisting.json"
        )
        self.assertEqual(0, len(floor.cells))

    def testGetProjectData(self):
        value = {"test": {"1": 1}}
        self.assertEqual(value["test"], ParserJSON.getProjectData(value))

    def testCellGeometries(self):
        l_cell_geom = ParserJSON.getCellGeometries(self.projectData)
        self.assertEqual(2, len(l_cell_geom))

    def testCellName(self):
        cell_properties = self.projectData[ParserJSON.propertyContainer][
            ParserJSON.cellProperties
        ]
        self.assertEqual("name001", ParserJSON.getCellName("001", cell_properties))

        self.assertEqual("002", ParserJSON.getCellName("002", cell_properties))

    def testTransitionGeometries(self):
        l_transition_geom = ParserJSON.getTransitionGeometries(self.projectData)
        self.assertEqual(2, len(l_transition_geom))


if __name__ == "__main__":
    unittest.main()
