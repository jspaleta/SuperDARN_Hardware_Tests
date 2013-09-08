# script to measure save a bunch of VNA phase measurements while stepping beam numbers
# useful for characterizing the RF path (transmitter antenna port to receiver input) and looking for time delay differences
# requires ssh key for QNX box and VNA
# jon klein, jtklein@alaska.edu, mit license

from pylab import *
from vna_control import *
from qnx_beamcontrol import *
import argparse, csv, os

SWEEP_CENTER = 13e6
SWEEP_SPAN = 10e6
SWEEP_POINTS = 201

BEAMS = 16

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--cal", action="count", help="run through calibration on VNA before taking measurements", default=0)
    parser.add_argument("--vnaip", help="specify VNA ip address", default=VNAHOST)
    parser.add_argument("--qnxip", help="specify QNX ip address", default=QNX_IP)
    parser.add_argument("--ddir", help="specify a directory to save the data in", default='sandbox')
    parser.add_argument("--b", type=int, help="specify number of beams", default=BEAMS)
    parser.add_argument("--cards", type=int, help="specify number of cards to calibrate", default=1)

    args = parser.parse_args()

    # open connection with VNA
    vna = lan_init(args.vnaip)

    # calibrate VNA if run with --cal
    # TODO: calibration is undertested... verify this
    if args.cal:
        print 'calibrating VNA'
        vna_preset(vna)
        vna_through_cal(vna)

    # set VNA span
    vna_setspan(vna, SWEEP_SPAN, SWEEP_CENTER, SWEEP_POINTS):
   
    # step through each card and measure phase at each beam setting
    # TODO: save this data in a useful format
    # TODO: log magnitude data and complain if it is unreasonable

    for c in range(args.cards):
        for b in range(args.b):
            qnx_setbeam(args.qnxip, b)
            vna_readphase(vna)
    
    lan_close(vna)
    


