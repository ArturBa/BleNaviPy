import logging
import unittest

import pytest

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
            "holeGeometry": [
                {
                    "holeOf": "001",
                    "points": [
                        {"point": {"x": 1.1, "y": 1.1}},
                        {"point": {"x": 1.1, "y": 1.2}},
                        {"point": {"x": 1.2, "y": 1.1}},
                    ],
                }
            ],
        },
        "propertyContainer": {"cellProperties": [{"id": "001", "name": "name001"}]},
    }

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def testGetGeometryFromFile(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile(self.filename)
        self.assertEqual(5, len(floor.cells))

    def testGetGeometryFromFileFailure(self):
        fake_path: str = "tests/indoorGML/nonExisting.json"
        with self._caplog.at_level(logging.INFO):
            floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile(fake_path)
            assert (
                f"File {fake_path} open error. Please check the path"
                in self._caplog.text
            )
            self.assertEqual(0, len(floor.cells))

    def testGetProjectData(self):
        value = {"test": {"1": 1}}
        self.assertEqual(value["test"], ParserJSON.getProjectData(value))

    def testCellGeometries(self):
        l_cell_geom = ParserJSON.getCellGeometries(self.projectData)
        self.assertEqual(2, len(l_cell_geom))

    def testCellName(self):
        cell_properties = self.projectData[ParserJSON.property_container][
            ParserJSON.cell_properties
        ]
        self.assertEqual("name001", ParserJSON.getCellName("001", cell_properties))

        self.assertEqual("002", ParserJSON.getCellName("002", cell_properties))

    def testTransitionGeometries(self):
        l_transition_geom = ParserJSON.getTransitionGeometries(self.projectData)
        self.assertEqual(2, len(l_transition_geom))

    def testHolesGeometries(self):
        holes_geom = ParserJSON.getHolesGeometries(self.projectData)
        self.assertEqual(1, len(holes_geom))

    def testAddingHolesToCell(self):
        cell_geom = ParserJSON.getCellGeometries(self.projectData)
        holes_geom = ParserJSON.getHolesGeometries(self.projectData)
        ParserJSON.addHolesToCells(cell_geom, holes_geom)
        self.assertEqual(1, len(cell_geom[0].holes))


if __name__ == "__main__":
    unittest.main()
