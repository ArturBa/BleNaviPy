import json
from typing import List

from bleNaviPy.indoorGML.geometry.cellGeometry import CellGeometry
from bleNaviPy.indoorGML.geometry.point import Point


class ParserJSON:
    @staticmethod
    def getGeometryFromFile(filename: string):
        jsonData = json.load(open(filename))

    @staticmethod
    def getCellGeometries(jsonData: Any) -> list[CellGeometry]:
        cellGeometries: List[CellGeometry] = []
        projectId = list(jsonData.keys())[0]
        cellGeometry = list(jsonData[projectId]["geometryContainer"]["cellGeometry"])
        cellProperties = list(
            jsonData[projectId]["propertyContainer"]["cellProperties"]
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
    def getCellName(cellId: str, cellProperties: List[any]) -> str:
        for cellProperty in cellProperties:
            if cellProperty["id"] == cellId:
                return cellProperty["name"]
        return cellId
