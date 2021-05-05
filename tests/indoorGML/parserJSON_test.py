import logging
import unittest
from pathlib import Path

import pytest

from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.parserJSON import ParserJSON
from bleNaviPy.indoorGML.parserJSONKeys import ParserJsonKeys


class LocationTest(unittest.TestCase):
    indoor_gml_filename: str = "tests/indoorGML/indoor_gml.json"
    ble_navi_filename: str = "tests/indoorGML/ble_navi.json"
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
            "beaconGeometry": [
                {
                    "rssi_1": 70,
                    "n": 2,
                    "n_wall": 7,
                    "noise_var": 7,
                    "points": [{"point": {"x": 1, "y": 1}}],
                }
            ],
        },
        "propertyContainer": {
            "cellProperties": [{"id": "001", "name": "name001"}],
            "floorProperties": [{"scale": 1, "noise": False, "wall_detection": False}],
        },
    }

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def testGetGeometryFromGMLFile(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile(
            self.indoor_gml_filename
        )
        self.assertEqual(5, len(floor.cells))

    def testGetGeometryFromGMLFileWrongFile(self):
        with self._caplog.at_level(logging.INFO):
            floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile(
                self.ble_navi_filename
            )
            assert (
                f"File {self.ble_navi_filename} read error. Please check the file content"
                in self._caplog.text
            )
            self.assertEqual(0, len(floor.cells))

    def testGetGeometryFromFileFailure(self):
        fake_path: str = "tests/indoorGML/nonExisting.json"
        with self._caplog.at_level(logging.INFO):
            floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile(fake_path)
            assert (
                f"File {fake_path} open error. Please check the path"
                in self._caplog.text
            )
            self.assertEqual(0, len(floor.cells))

    def testGetGeometryFromBleNaviFileFile(self):
        floor: FloorGeometry = ParserJSON.getGeometryFromBleNaviFile(
            self.ble_navi_filename
        )
        self.assertEqual(1, len(floor.beacons))
        self.assertEqual(1, floor.scale)

    def testGetGeometryFromBleNaviFileWrongFile(self):
        with self._caplog.at_level(logging.INFO):
            floor: FloorGeometry = ParserJSON.getGeometryFromBleNaviFile(
                self.indoor_gml_filename
            )
            assert (
                f"File {self.indoor_gml_filename} read error. Please check the file content"
                in self._caplog.text
            )
            self.assertEqual(0, len(floor.cells))

    def testGetGeometryFromBleNaviFileFailure(self):
        fake_path: str = "tests/indoorGML/nonExisting.json"
        with self._caplog.at_level(logging.INFO):
            floor: FloorGeometry = ParserJSON.getGeometryFromBleNaviFile(fake_path)
            assert (
                f"File {fake_path} open error. Please check the path"
                in self._caplog.text
            )
            self.assertEqual(0, len(floor.cells))

    def testSaveFile(self):
        floor = FloorGeometry([], [])
        save_filepath = "test_file.json"
        ParserJSON.saveFloorGeometry(save_filepath, floor, None)
        path = Path(save_filepath)
        assert path.is_file()

    def testSaveFileFailure(self):
        floor = FloorGeometry([], [])
        save_filepath = "ignore21/save_file.json"
        with self._caplog.at_level(logging.INFO):
            ParserJSON.saveFloorGeometry(save_filepath, floor, None)
            assert (
                f"File {save_filepath} open error. Please check the path"
                in self._caplog.text
            )

    def testGetProjectData(self):
        value = {"test": {"1": 1}}
        self.assertEqual(value["test"], ParserJSON.getProjectData(value))

    def testCellGeometries(self):
        l_cell_geom = ParserJSON.getCellGeometries(self.projectData)
        self.assertEqual(2, len(l_cell_geom))

    def testCellName(self):
        cell_properties = self.projectData[ParserJsonKeys.property_container.value][
            ParserJsonKeys.cell_properties.value
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

    def testBeaconsGeometries(self):
        beacons = ParserJSON.getBeaconGeometries(self.projectData)
        self.assertEqual(beacons[0].location.x, 1)
        self.assertEqual(beacons[0].location.y, 1)
        self.assertEqual(1, len(beacons))


if __name__ == "__main__":
    unittest.main()
