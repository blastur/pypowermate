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

  >>> while True:
  ...     (ts, evt, val) = p.read_event()
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
import select
import time

class PowermateTimeoutException(Exception):
  pass

class Powermate(object):
  EVENT_BUTTON = 'button'
  EVENT_ROTATE = 'rotate'
  BUTTON_DOWN = 1
  BUTTON_UP = 0

  def __init__(self, path):
    self.dev = InputDevice(path)

  def read_event(self, timeout = None):
    ''' Read a Powermate event.

    Arguments:
        timeout: Timeout (in seconds). If zero is specified, read_event will
        only poll (not block). If timeout is None, it'll block until an event
        is received.

    Returns:
        A tuple (tstamp, event, value) if an event was read, otherwise None.

        Event & value defines action:
        Powermate.EVENT_BUTTON -- Knob is pressed (value==Powermate.BUTTON_DOWN)
                                  or depressed (value==Powermate.BUTTON_UP).
        Powermate.EVENT_ROTATE -- Knob is rotated 'value' steps. Value is
                                  usually 1 or -1, but can be up to +- 7.

        tstamp is the Linux Input Device event timestamp (seconds).

    Raises:
        PowermateTimeoutException when the timeout expires (only applicable when
        timeout > 0).
    '''
    if timeout == 0:
      return self.__poll_event()

    t0 = time.time()
    while True:
      if timeout is None:
        event = self.__read_event(None)
      else:
        elapsed = time.time() - t0
        if elapsed >= timeout:
          raise PowermateTimeoutException()

        event = self.__read_event(max(timeout - elapsed, 0))

      if event is None:
        continue
      if event.type == ecodes.EV_REL:
        return (event.timestamp(), self.EVENT_ROTATE, event.value)
      elif event.type == ecodes.EV_KEY:
        return (event.timestamp(), self.EVENT_BUTTON, event.value)

  def __poll_event(self):
    ''' Finds the first button or rotate event in the pending queue '''
    while True:
      event = self.dev.read_one()
      if event is None:
        return None
      if event.type == ecodes.EV_REL:
        return (event.timestamp(), self.EVENT_ROTATE, event.value)
      elif event.type == ecodes.EV_KEY:
        return (event.timestamp(), self.EVENT_BUTTON, event.value)

  def __read_event(self, timeout):
    if timeout is None:
      (r, _, _) = select.select([self.dev.fileno()], [], [])
    else:
      (r, _, _) = select.select([self.dev.fileno()], [], [], timeout)
    return self.dev.read_one()

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
