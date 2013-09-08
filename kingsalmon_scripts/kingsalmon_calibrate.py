#!/usr/bin/python
# script to measure save a bunch of VNA phase measurements while stepping beam numbers
# useful for characterizing the RF path (transmitter antenna port to receiver input) and looking for time delay differences
# requires ssh key for QNX box and VNA
# jon klein, jtklein@alaska.edu, mit license

from pylab import *
from vna_control import *
from qnx_beamcontrol import *
import argparse, csv, os
import sys

SWEEP_CENTER = 15e6
SWEEP_SPAN = 20e6
SWEEP_POINTS = 1201 

BEAMS = 16

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--cal", action="count", help="run through calibration on VNA before taking measurements", default=0)
    parser.add_argument("--vnaip", help="specify VNA ip address", default=VNAHOST)
    parser.add_argument("--qnxip", help="specify QNX ip address", default=QNX_IP)
    parser.add_argument("--ddir", help="specify a directory to save the data in", default='sandbox')
    parser.add_argument("--b", type=int, help="specify number of beams", default=BEAMS)
    parser.add_argument("--c", type=int, help="specify count to average", default=1)
    parser.add_argument("--cards", type=int, help="specify number of cards to calibrate", default=1)

    args = parser.parse_args()
    if args.c < 1 : args.c = 1 

    # open connection with VNA
    vna = lan_init(args.vnaip)

    if args.cal:
        vna_preset(vna)

    vna_init(vna)
    # set VNA span
    vna_setspan(vna, SWEEP_SPAN, SWEEP_CENTER, SWEEP_POINTS)
    timeout=max(0.1,0.04/201.0 * SWEEP_POINTS)
    # calibrate VNA if run with --cal
    # TODO: calibration is undertested... verify this
    if args.cal:
        print 'calibrating VNA'
        vna_through_cal(vna)

    qnx_setbeam(args.qnxip, 7)
    vna_smoothapeture(vna,2,5.0)  
    vna_enablesmoothing(vna,2,True)  
    vna_setave(vna,args.c)  
    vna_enableave(vna,True)  
    for i in xrange(args.c):
        print "Trigger : %d" % (i)
        vna_trigger(vna,timeout)
    time.sleep(1.0)
    tdelay=vna_readtimedelay(vna)
    time.sleep(0.2)
    ephase=vna_readextendedphase(vna)
    time.sleep(0.2)
    mlog=vna_readmlog(vna)
    time.sleep(0.2)
    phase=vna_readphase(vna)
    time.sleep(0.2)
    sys.exit(0)
    # step through each card and measure phase at each beam setting
    # TODO: save this data in a useful format
    # TODO: log magnitude data and complain if it is unreasonable

    for c in range(args.cards):
        for b in range(args.b):
            #qnx_setbeam(args.qnxip, b)
            #vna_readphase(vna)
            pass
    lan_close(vna)
    


