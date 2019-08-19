import sys
import unittest
sys.path.append("../problem_2")
from get_subway_stop_data import get_subway_stop_data
import time


class TestGetSubwayStopData(unittest.TestCase):

    def test_get_subway_stop_data_valid(self):
        input_list = ['Red', 'Mattapan', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E', 'Blue']
        [stops_dict, connecting_stops_dict] = get_subway_stop_data(input_list)
        time.sleep(5)  # so that next tests aren't rate limited
        expected_stops_sample = ['Alewife', 'Ruggles', 'Shawmut', 'Symphony', 'Wonderland', 'Mattapan']
        expected_connections = ['Park Street', 'Downtown Crossing', 'Ashmont', 'State', 'Haymarket', 'North Station',
                                'Saint Paul Street', 'Kenmore', 'Hynes Convention Center', 'Copley', 'Arlington',
                                'Boylston', 'Government Center']

        self.assertEqual(type(stops_dict), dict)
        self.assertEqual(type(connecting_stops_dict), dict)

        for stop in expected_stops_sample:
            self.assertIn(stop, stops_dict)
        for stop in expected_connections:
            self.assertIn(stop, connecting_stops_dict)

    def test_get_subway_stop_data_no_input(self):
        input_list = []
        self.assertIsNone(get_subway_stop_data(input_list))

    def test_get_subway_stop_data_invalid(self):
        input_list = ['Purple', 'Yellow']
        self.assertIsNone(get_subway_stop_data(input_list))


if __name__ == '__main__':
    unittest.main()
