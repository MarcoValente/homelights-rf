import unittest
from homelightsrf.LightsManager import LightsManager as lm
import logging as log

log.basicConfig(level=log.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

# Test case class
class TestLightsManager(unittest.TestCase):

    # Test method
    def test_turnOn(self):
        ll=lm(dry_run=True)
        ll.turnOn()
        ll.turnOff()

if __name__ == '__main__':
    unittest.main()
