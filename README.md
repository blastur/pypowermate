# pypowermate

This module encapsulates access to the Griffin USB PowerMate "knob" device [1].
The PowerMate is an "assignable controller" in the shape of a knob. The knob
can be rotated, pressed and also features a LED at its base that can be used
to indicate events to the operator.

This module provides functions to read knob events (rotate/press) and to set
the LED brightness and pulse speed (when in "pulse"-mode).

The module interfaces with the device through the powermate Linux kernel driver
and will therefore only work on Linux systems.

[1]: https://griffintechnology.com/us/powermate

## Getting started

1. Install using pip:
	```
	$ pip install .
	```
2. Ensure "powermate" kernel module is loaded in your system. It ships with
most modern Linux distros and should insmod automatically when you plug in
the PowerMate.
	```
	$ lsmod | grep powermate
	```
3. Ensure your user can read/write the powermate input device. On Ubuntu,
this means adding yourself to the "input" usergroup.
4. Testrun the example script.
	```
	$ python examples/pulse_and_brightness.py /dev/input/by-id/usb-Griffin_Technology_Inc._Griffin_PowerMate-event-if00
	```
(Device path may differ in your case)


## API

See the documentation in pypowermate/powermate.py for details on how to use the
module from your own code.

## License

This module is licensed under GNU Lesser General Public License (LGPL v3). See
lgpl-3.0.txt for details.
