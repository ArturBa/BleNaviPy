import json
from typing import List

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.floorGeometry import FloorGeometry
from bleNaviPy.indoorGML.geometry.pointGeometry import Point
from bleNaviPy.indoorGML.geometry.transitionGeometry import TransitionGeometry


class ParserJSON:
    @staticmethod
    def getGeometryFromFile(filename: string) -> FloorGeometry:
        jsonData = json.load(open(filename))
        projectData = ParserJSON.getProjectData(jsonData)
        return FloorGeometry(
            ParserJSON.getCellGeometries(projectData),
            ParserJSON.getTransitionGeometries(projectData),
        )

    @staticmethod
    def getProjectData(jsonData: Any) -> Any:
        projectId = list(jsonData.keys())[0]
        return jsonData[projectId]

    @staticmethod
    def getCellGeometries(projectData: Any) -> list[CellGeometry]:
        cellGeometries: List[CellGeometry] = []
        cellGeometry = list(projectData["geometryContainer"]["cellGeometry"])
        cellProperties = list(projectData["propertyContainer"]["cellProperties"])
        for cell in cellGeometry:
            cellPoints: List[Point] = []
            cellName: string = ParserJSON.__getCellName(cell["id"], cellProperties)
            for points in cell["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                cellPoints.append(Point(x, y))
            cellGeometries.append(CellGeometry(cellName, cellPoints))
        return cellGeometries

    @staticmethod
    def getCellName(cellId: str, cellProperties: List[any]) -> str:
        for cellProperty in cellProperties:
            if cellProperty["id"] == cellId:
                return cellProperty["name"]
        return cellId

    @staticmethod
    def getTransitionGeometries(projectData: any) -> list[TransitionGeometry]:
        transitionGeometries: List[TransitionGeometry] = []
        transitionGeometry = list(
            projectData["geometryContainer"]["transitionGeometry"]
        )
        for transition in transitionGeometry:
            transitionPoints: List[Point] = []
            for points in transition["points"]:
                x = points["point"]["x"]
                y = points["point"]["y"]
                transitionPoints.append(Point(x, y))
            transitionGeometries.append(TransitionGeometry(transitionPoints))
        return transitionGeometries
