from __future__ import annotations

import json

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class ParserJSON:
    @staticmethod
    def getGeometryFromFile(filename: str) -> FloorGeometry:
        jsonData = json.load(open(filename))
        projectData = ParserJSON.getProjectData(jsonData)
        return FloorGeometry(
            ParserJSON.getCellGeometries(projectData),
            ParserJSON.getTransitionGeometries(projectData),
        )

    @staticmethod
    def getProjectData(jsonData: any) -> any:
        projectId = list(jsonData.keys())[0]
        return jsonData[projectId]

    @staticmethod
    def getCellGeometries(projectData: any) -> list[CellGeometry]:
        cellGeometries: List[CellGeometry] = []
        cellGeometry = list(projectData["geometryContainer"]["cellGeometry"])
        cellProperties = list(projectData["propertyContainer"]["cellProperties"])
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
        for cellProperty in cellProperties:
            if cellProperty["id"] == cellId:
                return cellProperty["name"]
        return cellId

    @staticmethod
    def getTransitionGeometries(projectData: any) -> list[TransitionGeometry]:
        transitionGeometries: list[TransitionGeometry] = []
        transitionGeometry = list(
            projectData["geometryContainer"]["transitionGeometry"]
        )
        for transition in transitionGeometry:
            transitionPoints: list[Point] = []
            for points in transition["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                transitionPoints.append(Point(x, y))
            transitionGeometries.append(TransitionGeometry(transitionPoints))
        return transitionGeometries
