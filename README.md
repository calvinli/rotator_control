Cory EMEDish rotator control
==============================

Code for a web page controlling the UC Berkeley Cory Hall EME dish rotator.

Dependencies
-----------------------

This project is designed for running on a Linux system; regardless, it should
still work on any system on which the following dependencies can be satisfied:

* **hamlib**: On Debian and its variants, this is available as the `libhamlib2`
    package. (https://github.com/N0NB/hamlib)
* **rotctl**: This is part of `hamlib`; on Debian-based OSes it is available
    in the `libhamlib-utils` package.
* **Python 2**: most Linux distros should ship with this pre-installed.
    In addition the following Python packages are required:
    - PyEphem: astronomical computation library; used for the Moon tracking
        (https://pypi.python.org/pypi/pyephem/)
    - Flask: web framework, used for the web page backend (http://flask.pocoo.org/)

It is recommended that development and testing use a Python `virtualenv`.


Notes
----------------------

The code expects the rotator to be connected via a RS-232-to-USB adapter at
`/dev/ttyUSB0`. The script must be able to write to this device
(to do serial communication), so file permissions should be set accordingly.
(On Debian-based systems, this can be accomplished by adding the user
the script is running as to the `dialout` group.)
