import unittest
import logging

from tdlog import logger

class TestHandler(unittest.TestCase):
    def testLogging(self):
        logging.basicConfig(level=logging.INFO)
        l = logging.getLogger('td_logger.test')
        l.addHandler(logger.TreasureDataHandler(verbose=True))

        js = { "semicolon" : ";", "at" : "@" }
        for i in range(0, 5):
            l.info(js)
