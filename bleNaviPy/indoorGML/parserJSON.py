"""This is a module for parcing indoorGML json files"""
from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from typing import List

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.beacon import BeaconType
from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.holeGeometry import HoleGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry
from bleNaviPy.indoorGML.parserJSONKeys import ParserJsonKeys


class ParserJSON:
    """
    Class to parse a JSON file with indoorGML info
    """

    @staticmethod
    def getGeometryFromIndoorGMLFile(filename: str) -> FloorGeometry:
        """Get floor geometry from json file

        Args:
            filename (str): [file path]

        Returns:
            FloorGeometry: [Floor geometry from file]

        Examples:
            >>> from bleNaviPy.indoorGML.parserJSON import ParserJSON
            >>> from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
            >>> floor: FloorGeometry = ParserJSON.getGeometryFromIndoorGMLFile("test.json")
            Floor: Cells: 3

        """
        with ParserJSON.opened(filename) as (f, err):
            if err:
                logging.error(f"File {filename} open error. Please check the path")
                logging.debug(f"File open error {err}")
                return FloorGeometry([], [])
            json_data = json.load(f)
            project_data = ParserJSON.getProjectData(json_data)

            cells_geometry = ParserJSON.getCellGeometries(project_data)
            holes_geometry = ParserJSON.getHolesGeometries(project_data)
            ParserJSON.addHolesToCells(cells_geometry, holes_geometry)

            floor_geometry: FloorGeometry = FloorGeometry(
                cells_geometry,
                ParserJSON.getTransitionGeometries(project_data),
            )
            return floor_geometry

    @staticmethod
    def getGeometryFromBleNaviFile(filename: string) -> FloorGeometry:
        with ParserJSON.opened(filename) as (f, err):
            if err:
                logging.error(f"File {filename} open error. Please check the path")
                logging.debug(f"File open error {err}")
                return FloorGeometry([], [])
            project_data = json.load(f)

            cells_geometry = ParserJSON.getCellGeometries(project_data)
            holes_geometry = ParserJSON.getHolesGeometries(project_data)
            ParserJSON.addHolesToCells(cells_geometry, holes_geometry)

            floor_geometry: FloorGeometry = FloorGeometry(
                cells_geometry,
                ParserJSON.getTransitionGeometries(project_data),
                ParserJSON.getBeaconGeometries(project_data),
            )
            ParserJSON.setFloorProperties(project_data, floor_geometry)
            return floor_geometry

    @staticmethod
    def saveFloorGeometry(
        filename: string, floor_geometry: FloorGeometry, indent: number = 4
    ) -> None:
        with ParserJSON.opened(filename, "w") as (f, err):
            if err:
                logging.error(f"File {filename} open error. Please check the path")
                logging.debug(f"File open error {err}")
                return
            json.dump(floor_geometry.getDict(), f, indent=indent)
            logging.info(f"{floor_geometry} saved into {filename}")

    @staticmethod
    @contextmanager
    def opened(filename: string, mode: string = "r") -> (TextIOWrapper, IOError):
        try:
            f = open(filename, mode)
        except IOError as err:
            yield None, err
        else:
            try:
                yield f, None
            finally:
                f.close()

    @staticmethod
    def getProjectData(json_data: any) -> any:
        """get first project data

        Args:
            json_data (any): Json data read from the file

        Returns:
            any: project json data
        """
        project_id = list(json_data.keys())[0]
        return json_data[project_id]

    @staticmethod
    def getCellGeometries(project_data: any) -> List[CellGeometry]:
        """Get Cell geometries from a project data

        Args:
            project_data (any): Project json data

        Returns:
            List[CellGeometry]: List of cells from project file
        """
        cell_geometries: List[CellGeometry] = []
        cell_geometry = list(
            project_data[ParserJsonKeys.geometry_container.value][
                ParserJsonKeys.cell_geometry.value
            ]
        )
        cell_properties = list(
            project_data[ParserJsonKeys.property_container.value][
                ParserJsonKeys.cell_properties.value
            ]
        )
        for cell in cell_geometry:
            cell_points: List[Point] = []
            cell_name: str = ParserJSON.getCellName(cell["id"], cell_properties)
            for points in cell["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                cell_points.append(Point(x, y))
            cell_geometries.append(CellGeometry(cell["id"], cell_name, cell_points))
        return cell_geometries

    @staticmethod
    def getCellName(cell_id: str, cell_properties: List[any]) -> str:
        """Get cell name by cellId

        Args:
            cell_id (str): Cell id
            cell_properties (List[any]): List of all cell properties

        Returns:
            str: Cell name
        """
        for cellProperty in cell_properties:
            if cellProperty["id"] == cell_id:
                return cellProperty["name"]
        return cell_id

    @staticmethod
    def getTransitionGeometries(project_data: any) -> List[TransitionGeometry]:
        """Get transitions from a project file

        Args:
            project_data (any): Project json data

        Returns:
            List[TransitionGeometry]:
             List of transitions geometries from the project file
        """
        transition_geometries: List[TransitionGeometry] = []
        transition_geometry = list(
            project_data[ParserJsonKeys.geometry_container.value][
                ParserJsonKeys.transition_geometry.value
            ]
        )
        for transition in transition_geometry:
            transition_points: List[Point] = []
            for points in transition["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                transition_points.append(Point(x, y))
            transition_geometries.append(TransitionGeometry(transition_points))
        return transition_geometries

    @staticmethod
    def getHolesGeometries(project_data: any) -> List[HoleGeometry]:
        """Get holes from a project file

        Args:
            project_data (any): Project json data

        Returns:
            List[HoleGeometry]: List of holes geometries from the project file
        """
        hole_geometries: List[HoleGeometry] = []
        hole_geometry = list(
            project_data[ParserJsonKeys.geometry_container.value][
                ParserJsonKeys.hole_geometry.value
            ]
        )
        for hole in hole_geometry:
            hole_point: List[Point] = []
            for points in hole["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                hole_point.append(Point(x, y))
            hole_geometries.append(HoleGeometry(hole_point, hole["holeOf"]))

        return hole_geometries

    @staticmethod
    def addHolesToCells(cells: List[CellGeometry], holes: List[HoleGeometry]) -> None:
        """Add holes geometries to matching cells

        Args:
            cells (List[CellGeometry]):
            holes (List[HoleGeometry]):
        """
        for hole in holes:
            for cell in cells:
                if cell.id == hole.memberOf:
                    cell.addHole(hole)

    @staticmethod
    def getBeaconGeometries(project_data: any) -> List[Beacon]:
        """Get beacons from project file

        Args:
            project_data (any): Project json data

        Returns:
            List[Beacon]: List of beacons from the project file
        """
        beacon_geometries: List[Beacon] = []
        beacon_geometry = list(
            project_data[ParserJsonKeys.geometry_container.value][
                ParserJsonKeys.beacon_geometry.value
            ]
        )
        for beacon in beacon_geometry:
            for points in beacon["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                beacon_location = Point(x, y)
            beacon_type = BeaconType(
                beacon["rssi_1"], beacon["n"], beacon["n_wall"], beacon["noise_var"]
            )
            beacon_geometries.append(Beacon(beacon_location, beacon_type))

        return beacon_geometries

    @staticmethod
    def setFloorProperties(project_data: any, floor: FloorGeometry) -> None:
        floor_properties = project_data[ParserJsonKeys.property_container.value][
            ParserJsonKeys.floor_properties.value
        ][0]
        print(floor_properties)
        floor.setScale(floor_properties["scale"])
        floor.setWallDetection(floor_properties["wall_detection"])
        floor.setNoise(floor_properties["noise"])
