import sys
import unittest
sys.path.append("../problem_2")
from get_subway_stop_data import get_max_min_stops


class TestGetMaxMinStops(unittest.TestCase):

    def test_max_min_stops(self):
        stop_counts_dict = {'Purple': 12, 'Pink': 10, 'Yellow': 14}
        expected_max = 'Yellow'
        expected_min = 'Pink'
        max_min_stops = get_max_min_stops(stop_counts_dict)
        self.assertEqual(max_min_stops['max'], expected_max)
        self.assertEqual(max_min_stops['min'], expected_min)


if __name__ == '__main__':
    unittest.main()
