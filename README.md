# pypowermate

This module encapsulates access to the Griffin USB PowerMate "knob" device [1].
The PowerMate is an "assignable controller" in the shape of a knob. The knob
can be rotated, pressed and also features a LED at its base that can be used
to indicate events to the operator.

This module provides functions to read knob events (rotate/press) and to write/set
the LED brightness and pulse speed (when in "pulse"-mode).

The module interfaces with the device through the powermate Linux kernel driver
and will therefore only work on Linux systems.

[1]: https://griffintechnology.com/us/powermate

## Getting started

For python3, just use python3/pip3 instead of python/pip2 in all command.

1. Install using pip:
	```
	$ cd pypowermate-master
	$ sudo pip2 install .
	```
2. Ensure "powermate" kernel module is loaded in your system. It ships with
most modern Linux distros and should insmod automatically when you plug in
the PowerMate.
	```
	$ lsmod | grep powermate
	```
3. Ensure your user can read/write the powermate input device. On Ubuntu,
this means adding yourself to the "input" usergroup.
	```
	$ sudo groupadd input
	$ sudo usermod -a -G input "$USER"
	$ echo 'KERNEL=="event*", NAME="input/%k", MODE="660", GROUP="input"' | sudo tee -a /etc/udev/rules.d/99-input.rules
	```
then reboot

4. Testrun the example script.
	```
	$ python examples/pulse_and_brightness.py
	```

Depending on the exact model, you will have to change MinSpeed and MaxSpeed values.


## API

See the documentation in pypowermate/powermate.py for details on how to use the
module from your own code.

## License

This module is licensed under GNU Lesser General Public License (LGPL v3). See
LICENSE.txt for details.
