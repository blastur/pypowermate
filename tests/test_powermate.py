import unittest
import glob
import time
from pypowermate import Powermate, PowermateTimeoutException

POWERMATE_GLOB_STRING = '/dev/input/by-id/usb-Griffin_Technology_Inc._Griffin_PowerMate*'

class TestPowermate(unittest.TestCase):
    def setUp(self):
        paths = glob.glob(POWERMATE_GLOB_STRING)
        if paths:
            self.pm = Powermate(paths[0])
        else:
            self.fail('No Powermate found (%s)' % POWERMATE_GLOB_STRING)
        while self.pm.read_event(0) is not None:
            pass

    def tearDown(self):
        del self.pm

    def testReadWithTimeout(self):
        raw_input("Rotate the knob one step to the left. Hit Enter when you're done.")

        # Read the button down event
        event = self.pm.read_event(0.5)
        self.assertIsNotNone(event)
        (ts, evt, val) = event
        self.assertEquals(evt, Powermate.EVENT_ROTATE)
        self.assertTrue(val < 0)

    def testPolledEvents(self):
        raw_input("Rotate the knob one step to the right. Hit Enter when you're done.")
        event = self.pm.read_event(0)
        self.assertIsNotNone(event)
        (ts, evt, val) = event
        self.assertEquals(evt, Powermate.EVENT_ROTATE)
        self.assertTrue(val > 0)

    def testTimeout(self):
        with self.assertRaises(PowermateTimeoutException):
            self.pm.read_event(0.5)

    def testSteadyLed(self):
        self.pm.set_steady_led(255)
        answer = raw_input("Is the Powermate LED lit (not pulsing?) (y/n)")
        if answer.upper() != "Y":
            self.fail("LED did not light up as expected")

    def testPulse(self):
        self.pm.set_pulse(255)
        answer = raw_input("Is the Powermate LED pulsing (y/n)")
        if answer.upper() != "Y":
            self.fail("LED did not pulse as expected")

if __name__ == '__main__':
    unittest.main()
