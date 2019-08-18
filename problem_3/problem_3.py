from route_planner import route_planner
import logger
import time

logger = logger.get_logger()

starting_stop = input("Please enter starting point station: ")
ending_stop = input("Please enter your final destination: ")
start_time = time.time()
logger.info(route_planner(starting_stop, ending_stop))
end_time = time.time()
logger.info(f"Total run time for problem 3: {'%.5f'%(end_time-start_time)} (s)\n")