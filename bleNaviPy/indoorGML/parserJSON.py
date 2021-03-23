from __future__ import annotations

import json
import logging
from typing import List

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class ParserJSON:
    """
    Class to parse a JSON file with indoorGML info
    """

    geometryContainer = "geometryContainer"
    cellGeometry = "cellGeometry"
    transitionGeometry = "transitionGeometry"
    propertyContainer = "propertyContainer"
    cellProperties = "cellProperties"

    @staticmethod
    def getGeometryFromFile(filename: str) -> FloorGeometry:
        """Get floor geometry from json file

        Args:
            filename (str): [file path]

        Returns:
            FloorGeometry: [Floor geometry from file]

        Examples:
            >>> from bleNaviPy.indoorGML.parserJSON import ParserJSON
            >>> from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
            >>> floor: FloorGeometry = ParserJSON.getGeometryFromFile("test.json")
            Floor: Cells: 3

        """
        try:
            open(filename, "r")
            json_data = json.load(open(filename, "r"))
            project_data = ParserJSON.getProjectData(json_data)
            return FloorGeometry(
                ParserJSON.getCellGeometries(project_data),
                ParserJSON.getTransitionGeometries(project_data),
            )
        except IOError:
            logging.error(f"File {filename} open error. Please check the path")
            return FloorGeometry([], [])

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
            list[CellGeometry]: List of cells from project file
        """
        cell_geometries: List[CellGeometry] = []
        cell_geometry = list(
            project_data[ParserJSON.geometryContainer][ParserJSON.cellGeometry]
        )
        cell_properties = list(
            project_data[ParserJSON.propertyContainer][ParserJSON.cellProperties]
        )
        for cell in cell_geometry:
            cell_points: List[Point] = []
            cell_name: str = ParserJSON.getCellName(cell["id"], cell_properties)
            for points in cell["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                cell_points.append(Point(x, y))
            cell_geometries.append(CellGeometry(cell_name, cell_points))
        return cell_geometries

    @staticmethod
    def getCellName(cell_id: str, cell_properties: List[any]) -> str:
        """Get cell name by cellId

        Args:
            cell_id (str): Cell id
            cell_properties (list[any]): List of all cell properties

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
            list[TransitionGeometry]: List of transitions geometries from the project file
        """
        transition_geometries: List[TransitionGeometry] = []
        transition_geometry = list(
            project_data[ParserJSON.geometryContainer][ParserJSON.transitionGeometry]
        )
        for transition in transition_geometry:
            transition_points: List[Point] = []
            for points in transition["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                transition_points.append(Point(x, y))
            transition_geometries.append(TransitionGeometry(transition_points))
        return transition_geometries
