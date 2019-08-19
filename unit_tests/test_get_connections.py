import sys
import unittest
sys.path.append("../problem_2")
from get_subway_stop_data import get_connecting_stops


class TestGetConnectingStops(unittest.TestCase):

    def test_get_connnecting_stops(self):
        stop_dict = {'Barney Street': ['Purple', 'Green'], 'Pikachu': ['Yellow'], 'Gryffindor': ['Red', 'Yellow']}
        actual_output = get_connecting_stops(stop_dict)

        self.assertIn('Barney Street', actual_output)
        self.assertIn('Gryffindor', actual_output)
        self.assertNotIn('Pikachu', actual_output)

        self.assertEqual(actual_output['Barney Street'], ['Purple', 'Green'])
        self.assertEqual(actual_output['Gryffindor'], ['Red', 'Yellow'])


if __name__ == '__main__':
    unittest.main()
