import math

from bleNaviPy.beacon.location import Location


beaconType = {
    "iBeaconNear": {
        "maxDistance": 5,
    }
}


class Beacon:
    def __init__(self, location: Location):
        self.location = location
        self.RSSI_0 = -80  # beacon RSSI
        self.N = 2  # beacon strength

    def getRSSI(self, location: Location) -> float:
        """Calculate RSSI on given location

        Args:
            location (Location):

        Returns:
            float: RSSI in dB
        """
        # Distance = 10 ^ ((Measured Power — RSSI) / (10 * N))
        distance = location.distance(self.location)
        return -10 * self.N * math.log(distance) + self.RSSI_0
