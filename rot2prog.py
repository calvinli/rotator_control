#
# rot2prog.py
#
# Python functions for sending commands to the ROT2PROG controller.
#
# Note: if the shell call fails, a subprocess.CalledProcessError will be thrown.
#
# I have no idea what happens if you interleave these calls. I presume the
# OS-level I/O systems take care of that.
#
from subprocess import check_call, check_output

rotctl = """rotctl -m 901 -r /dev/ttyUSB0 -C post_write_delay=2,az_resolution=1,el_resolution=1"""
# for details on the arguments here, see the man page for rotctl(1) and
# <http://hamlib.sourceforge.net/wiki/index.php/Rotor_Specific_Notes>, section "SPID_Rot2Prog"

def get_pos():
    az, el = check_output("{} p".format(rotctl), shell=True).split()
    az, el = int(round(float(az))), int(round(float(el)))
    return az, el

def set_pos(az, el):
    """Warning: this does no input checking at all, relying instead
    on the controller and rotator hardware to keep things sane."""
    return check_call("{} P {} {}".format(rotctl, az, el), shell=True)
