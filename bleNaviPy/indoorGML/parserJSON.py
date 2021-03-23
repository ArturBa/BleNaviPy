from __future__ import annotations

import json
import logging

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
            jsonData = json.load(open(filename, "r"))
            projectData = ParserJSON.getProjectData(jsonData)
            return FloorGeometry(
                ParserJSON.getCellGeometries(projectData),
                ParserJSON.getTransitionGeometries(projectData),
            )
        except IOError:
            logging.error(f"File {filename} open error. Please check the path")
            return FloorGeometry([], [])

    @staticmethod
    def getProjectData(jsonData: any) -> any:
        """get first project data

        Args:
            jsonData (any): Json data read from the file

        Returns:
            any: project json data
        """
        projectId = list(jsonData.keys())[0]
        return jsonData[projectId]

    @staticmethod
    def getCellGeometries(projectData: any) -> list[CellGeometry]:
        """Get Cell geometries from a project data

        Args:
            projectData (any): Project json data

        Returns:
            list[CellGeometry]: List of cells from project file
        """
        cellGeometries: List[CellGeometry] = []
        cellGeometry = list(
            projectData[ParserJSON.geometryContainer][ParserJSON.cellGeometry]
        )
        cellProperties = list(
            projectData[ParserJSON.propertyContainer][ParserJSON.cellProperties]
        )
        for cell in cellGeometry:
            cellPoints: List[Point] = []
            cellName: string = ParserJSON.getCellName(cell["id"], cellProperties)
            for points in cell["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                cellPoints.append(Point(x, y))
            cellGeometries.append(CellGeometry(cellName, cellPoints))
        return cellGeometries

    @staticmethod
    def getCellName(cellId: str, cellProperties: list[any]) -> str:
        """Get cell name by cellId

        Args:
            cellId (str): Cell id
            cellProperties (list[any]): List of all cell properties

        Returns:
            str: Cell name
        """
        for cellProperty in cellProperties:
            if cellProperty["id"] == cellId:
                return cellProperty["name"]
        return cellId

    @staticmethod
    def getTransitionGeometries(projectData: any) -> list[TransitionGeometry]:
        """Get transitions from a project file

        Args:
            projectData (any): Project json data

        Returns:
            list[TransitionGeometry]: List of transitions geometries from the project file
        """
        transitionGeometries: list[TransitionGeometry] = []
        transitionGeometry = list(
            projectData[ParserJSON.geometryContainer][ParserJSON.transitionGeometry]
        )
        for transition in transitionGeometry:
            transitionPoints: list[Point] = []
            for points in transition["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                transitionPoints.append(Point(x, y))
            transitionGeometries.append(TransitionGeometry(transitionPoints))
        return transitionGeometries
