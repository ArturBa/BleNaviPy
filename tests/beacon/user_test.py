import unittest

from bleNaviPy.beacon.user import User
from bleNaviPy.indoorGML.geometry.pointGeometry import Point


class UserTest(unittest.TestCase):

    location = Point(1, 1)
    user = User(location)

    def testInit(self):
        self.assertEqual(self.location, self.user.location)


if __name__ == "__main__":
    unittest.main()
