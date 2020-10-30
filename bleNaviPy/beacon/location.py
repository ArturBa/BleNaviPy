class Location:
    """
    Location class
    Contains 2D point location in meters
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, loc):
        return self.x == loc.x and self.y == loc.y

    def __str__(self):
        return f"Location x: {self.x}\ty: {self.y}"

    def __add__(self, loc):
        self.x += loc.x
        self.y += loc.y
        return self

    def __sub__(self, loc):
        print(self, loc)
        self.x -= loc.x
        self.y -= loc.y
        return self