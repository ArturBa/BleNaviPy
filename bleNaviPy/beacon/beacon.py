from bleNaviPy.beacon.location import Location


class Beacon:
    def __init__(self, location: Location, signal_strength: int):
        self.location = location
        self.signal_strength = signal_strength
