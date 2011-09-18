import unittest
import logging

from tdlog import handler, logger

class TestHandler(unittest.TestCase):
    def testLogging(self):
        logging.basicConfig(level=logging.INFO)
        l = logger.TreasureDataLogger('td_logger.test')
        l.addHandler(handler.TreasureDataHandler())

        js = { "semicolon" : ";", "at" : "@" }
        for i in range(0, 100):
            l.info(js)
