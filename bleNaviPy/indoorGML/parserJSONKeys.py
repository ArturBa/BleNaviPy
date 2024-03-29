"""This is a module for keeping shared json keys"""
from enum import Enum
from enum import unique


@unique
class ParserJsonKeys(Enum):
    """Json keys enum"""

    geometry_container = "geometryContainer"
    cell_geometry = "cellGeometry"
    transition_geometry = "transitionGeometry"
    hole_geometry = "holeGeometry"
    beacon_geometry = "beaconGeometry"

    property_container = "propertyContainer"
    cell_properties = "cellProperties"
    floor_properties = "floorProperties"
