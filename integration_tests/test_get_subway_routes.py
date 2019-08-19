import sys
import unittest
sys.path.append("../problem_1")
from get_subway_routes import get_subway_routes
import time


class TestGetSubwayRoutes(unittest.TestCase):

    def test_get_routes(self):
        [route_str, route_list] = get_subway_routes()
        time.sleep(5)  # so that next tests aren't rate limited
        expected_long_names = ['Red Line', 'Mattapan Trolley', 'Orange Line', 'Green Line B',
                               'Green Line C', 'Green Line D', 'Green Line E', 'Blue Line']
        expected_short_names = ['Red', 'Mattapan', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E', 'Blue']

        for route in expected_long_names:
            self.assertIn(route, route_str)
        for route in expected_short_names:
            self.assertIn(route, route_list)


if __name__ == '__main__':
    unittest.main()
