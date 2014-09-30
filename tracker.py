# -*- coding: utf-8 -*-

# Moon tracker for the Cory EME dish.
#
# This program outputs the current lunar azimuth and elevation
# for plugging into the rotator controller.
#
# The accuracy of this program has been verified against the 
# "Sun or Moon Altitude/Azimuth Table" tool of the
# US Naval Observatory Astronomical Applications Department,
# <http://aa.usno.navy.mil/data/docs/AltAz.php>
#
# This program is compatible with both Python 2 and 3.
#

import ephem # https://pypi.python.org/pypi/pyephem/
from datetime import datetime
from math import pi
import sys

emedish = ephem.Observer()
emedish.lat, emedish.lon = "37.875", "-122.258";
emedish.date = ephem.now(); # pyEphem's date handling is... weird...

moon = ephem.Moon(emedish)

def get_moon_az_el(digits = 0):
    """Return the azimuth and elevation of the Moon, as seen
    from Cory Hall, at the current time, in degrees.
    
    Arguments:
        - digits (optional): Number of digits past the decimal point
                             to round to. Default: 0.
    Returns:
        - (az, el): In degrees. If `digits` is 0, these will be `int`s,
                    otherwise they will be floats.
    """
    emedish.date = ephem.now()
    moon.compute(emedish)

    az = moon.az * 180 / pi
    el = moon.alt * 180 / pi

    if digits == 0:
        az, el = int(round(az)), int(round(el))
    else:
        az, el = round(az, digits), round(el, digits)
    # reminder: python round() rounds half-to-even

    return (az, el)

def sanitize_az_el(az, el):
    """Ensure azimuth and elevation are both positive.

    The controller box has built in controls and safeguards,
    but it's better to just not send it bad input.
    """
    return max(az, 0), max(el, 0)

def get_moon_params():
    """Return the current time, the Moon's azimuth, elevation,
    phase, and distance."""
    az, el = get_moon_az_el(1)

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dist = int(moon.earth_distance * 149597870.7)
    phase = round(moon.moon_phase, 3)

    return {"time": time, "az": az, "el": el, "phase": phase, "dist": dist}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = get_moon_params()
        print("{} -- Az: {}°, El: {}°, Phase: {}, Distance: {:,} km".format(
                p['time'], p['az'], p['el'], p['phase'], p['dist']))
    else:
        print("{} {}".format(*sanitize_az_el(*get_moon_az_el())))
