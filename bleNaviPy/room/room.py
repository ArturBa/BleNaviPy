import logging

from bleNaviPy.beacon.beacon import Beacon
from bleNaviPy.beacon.location import Location


class Room:
    def __init__(self):
        self.edges = None
        self.beacons = []
        self.user = None

    def setRoomEdges(self, edges: Location):
        if not self.edges:
            self.edges = edges
        else:
            pass
            # Check all beacons if still in a room or exit, action not permitted

    def addBeacon(self, beacon: Beacon):
        if self.isInsideRoom(beacon.location):
            self.beacons.append(beacon)
        else:
            logging.warning(f"Point {beacon.location} is not inside a room")

    def addUser(self, user: Location):
        self.user = user

    def isInsideRoom(self, location: Location) -> bool:
        # Add validation if point is inside a room
        return True

    def getUserLocationByBeacons(self) -> Location:
        return Location(1, 2)
