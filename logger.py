import logging


def get_logger():
    lg = logging.getLogger('logger')
    for h in lg.handlers:
        lg.removeHandler(h)
    log_handler = logging.StreamHandler()
    lg.addHandler(log_handler)
    lg.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    return lg
