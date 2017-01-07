#!/usr/bin/env python

import time
import sys
from pypowermate import Powermate

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write('usage: %s <input device>\n' % sys.argv[0])
		sys.exit(1)

	p = Powermate(sys.argv[1])

	speed = 255
	brightness = 255
	speed_mode = True

	print("- Rotate the knob to test different pulse speeds.")
	print("- Rotate the knob while it's pushed test different brightness levels.")

	while True:
		(ts, evt, val) = p.read_event()
		if evt == Powermate.EVENT_BUTTON:
			if val == Powermate.BUTTON_UP:
				speed_mode = True
				print("Speed mode activated.")
			else:
				speed_mode = False
				print("Brightness mode activated.")
		elif evt == p.EVENT_ROTATE:
			if speed_mode:
				speed += val
				speed = min(max(speed, 0), 510)
				print("Setting pulse speed %d" % speed)
				p.set_pulse(speed)
			else:
				brightness += val
				brightness = min(max(brightness, 0), 255)
				print("Setting brightness level %d" % brightness)
				p.set_steady_led(brightness)
