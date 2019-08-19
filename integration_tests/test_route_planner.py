import sys
import logger
sys.path.append("../problem_3")
from route_planner import route_planner
import time

logger = logger.get_logger()


class TestRoutePlanner:
    def test_route_planner_same_route(self):
        expected_response = 'Answer: Ashmont --> Alewife: Red'
        start = 'ASHMONT'
        end = 'AleWiFe'
        response = route_planner(start, end)
        assert expected_response == response

    def test_route_planner_1_transfer(self):
        expected_response = 'Answer: Ruggles --> Harvard: Orange, Red'
        start = 'ruggles'
        end = 'harvard'
        response = route_planner(start, end)
        assert expected_response == response

    def test_route_planner_2_transfers(self):
        possible_responses = ['Answer: Bowdoin --> Central: Blue, Orange, Red',
                              'Answer: Bowdoin --> Central: Blue, Green-E, Red',
                              'Answer: Bowdoin --> Central: Blue, Green-C, Red',
                              'Answer: Bowdoin --> Central: Blue, Green-D, Red']
        start = 'bowdoin'
        end = 'central'
        response = route_planner(start, end)
        assert response in possible_responses

    def test_route_planner_invalid_stop(self):
        expected_response = 'Invalid subway stops: Apple, Pear'
        start = 'AppLE'
        end = 'pear'
        response = route_planner(start, end)
        assert expected_response == response


if __name__ == '__main__':
    # there is a 40s sleep between each test call so that we don't get rate limited
    sleep_time = 40
    test_obj = TestRoutePlanner()
    try:
        test_obj.test_route_planner_same_route()
        time.sleep(sleep_time)
        test_obj.test_route_planner_1_transfer()
        time.sleep(sleep_time)
        test_obj.test_route_planner_2_transfers()
        time.sleep(sleep_time)
        test_obj.test_route_planner_invalid_stop()

        logger.info('All route planner tests passed!')
    except Exception as e:
        logger.error('Route planner tests failed :(')


