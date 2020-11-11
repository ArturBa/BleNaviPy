from bleNaviPy.beacon.location import Location


beaconType = {
    "iBeaconNear": {
        "maxDistance": 5,
    }
}


class Beacon:
    def __init__(self, location: Location, signal_strength: int):
        self.location = location
        self.signal_strength = signal_strength
        self.RSSI_0 = 0

    def getRSSI(self, location: Location) -> float:
        return 1.9
