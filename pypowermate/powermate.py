'''
This file implements the main Powermate class that provides functionality to
interface with a Griffin PowerMate USB knob.

Usage:

  >>> from pypowermate import Powermate
  >>> p = Powermate('/dev/input/by-id/usb-Griffin_Technology_Inc._Griffin_PowerMate-event-if00')

Configure the PowerMate (LED brightness and LED pulse speed):

  >>> p.set_cfg(255, 0)

See set_cfg docstring for more flags. You can also use the two convenience
functions,

  >>> p.set_steady_led(255)

and

  >>> p.set_pulse(255)

... to achieve the same thing.

To listen for events (knob press & rotate):

  >>> for (ts, evt, val) in p.read_event():
  ...     print("%f: event %s val %d" % (ts, evt, val))
  ...
  1483389541.878913: event rotate val 1
  1483389542.806825: event rotate val -1


The timestamp (ts) can be used to detect double-clicks.
'''

# Constants from the Powermate kernel driver (drivers/input/misc/powermate.c)
MAGIC_SPEED_SHIFT = 8
MAGIC_PULSE_SHIFT = 17
MAGIC_ASLEEP_SHIFT = 19
MAGIC_AWAKE_SHIFT = 20

from evdev import ecodes, InputDevice

class Powermate(object):
  EVENT_BUTTON = 'button'
  EVENT_ROTATE = 'rotate'

  def __init__(self, path):
    self.dev = InputDevice(path)

  def read_event(self):
    ''' Read a Powermate input event.

    Block until an event (knob press or rotate) occurs and return it.

    Returns:
        A tuple (tstamp, event, value). tstamp is a monotonic counter can be
        used to determine elapsed time (seconds) between a previous event

        Events:
        Powermate.EVENT_BUTTON -- Knob is pressed (value==1) or depressed
                                  (value==0).
        Powermate.EVENT_ROTATE -- Knob is rotated 'value' steps. Value is
                                  usually 1 or -1, but can be up to +- 7.

    '''
    for event in self.dev.read_loop():
        if event.type == ecodes.EV_REL:
          yield (event.timestamp(), self.EVENT_ROTATE, event.value)
        elif event.type == ecodes.EV_KEY:
          yield (event.timestamp(), self.EVENT_BUTTON, event.value)

  def set_cfg(self, brightness, pulse_speed, asleep=False, awake=True, pulse_table=0):
    ''' Writes powermate config.

    Arguments:
        brightness: LED brightness (0-255)
        pulse_speed: LED pulse speed (0-510).
        asleep: Pulse when computer is hibernating/sleeping
        awake: Pulse when comptuer is awake/normal state
        pulse_table: Type of pulse (0, 1 or 2).
    '''

    value = (
        brightness |
        pulse_speed << MAGIC_SPEED_SHIFT |
        pulse_table << MAGIC_PULSE_SHIFT |
        int(asleep) << MAGIC_ASLEEP_SHIFT |
        int(awake) << MAGIC_AWAKE_SHIFT
    )
    self.dev.write(ecodes.EV_MSC, ecodes.MSC_PULSELED, value)


  def set_steady_led(self, brightness):
    ''' Set LED to a steady (non-pulsing) mode at given brightness.

    Arguments:
        brightness: Level of brightness (0-255).
    '''
    self.set_cfg(brightness, 0, False, False)

  def set_pulse(self, speed):
    ''' Set LED to pulsing mode at given speed.

    Arguments:
        speed: Pulse speed (0-510)

    '''
    self.set_cfg(0, speed, True, True)
