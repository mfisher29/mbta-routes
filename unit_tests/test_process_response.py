import sys
import json
import unittest
sys.path.append("../problem_1")
from get_subway_routes import process_response


class TestProcessResponse(unittest.TestCase):
    @staticmethod
    def get_test_file(f):
        with open(f) as json_resp:
            resp_dict = json.loads(json_resp.read())
        return resp_dict

    def test_valid_response(self):
        response_dict = self.get_test_file('test_files/response_valid.json')
        [output_str, output_list] = process_response(response_dict)
        expected_long_names = ['Red Line', 'Orange Line']
        expected_routes = ['Red', 'Orange']
        for route in expected_long_names:
            self.assertIn(route, output_str)
        for route in expected_routes:
            self.assertIn(route, output_list)

    def test_no_long_name(self):
        response_dict = self.get_test_file('test_files/response_invalid.json')
        final_output = process_response(response_dict)
        self.assertIn("KeyError when processing json response:", final_output)

    def test_no_data(self):
        response_dict = {
            "meta": {
                "test": True
            }
        }
        final_output = process_response(response_dict)
        self.assertEqual("KeyError when processing json response: {'meta': {'test': True}}", final_output)

    def test_no_attributes(self):
        response_dict = {
            "data": [{
                    "test": True
            }]
        }
        final_output = process_response(response_dict)
        self.assertEqual("KeyError when processing json response: {'data': [{'test': True}]}", final_output)

    def test_no_response(self):
        response_dict = {}
        final_output = process_response(response_dict)
        self.assertEqual(final_output, 'No response body to process')


if __name__ == '__main__':
    unittest.main()
