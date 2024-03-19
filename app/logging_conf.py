import logging
import sys

def setup():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
