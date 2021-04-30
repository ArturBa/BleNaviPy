from enum import Enum
from enum import unique


@unique
class ParserJsonKeys(Enum):
    geometry_container = "geometryContainer"
    cell_geometry = "cellGeometry"
    transition_geometry = "transitionGeometry"
    hole_geometry = "holeGeometry"
    beacon_geometry = "beaconGeometry"
    property_container = "propertyContainer"
    cell_properties = "cellProperties"
