#!/usr/bin/python
# script to measure save a bunch of VNA phase measurements while stepping beam numbers
# useful for characterizing the RF path (transmitter antenna port to receiver input) and looking for time delay differences
# requires ssh key for QNX box and VNA
# jon klein, jtklein@alaska.edu, mit license
# jef spaleta

from pylab import *
from vna_control import *
from qnx_beamcontrol import *
from csv_utils import *

import argparse, os, time

SWEEP_CENTER = 15e6
SWEEP_SPAN = 20e6
SWEEP_POINTS = 1201 
TIMEOUT = max(0.1,0.04/201.0 * SWEEP_POINTS)
BEAMS = 16

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--cal", action="count", help="run through calibration on VNA before taking measurements", default=0)
    parser.add_argument("--vnaip", help="specify VNA ip address", default=VNAHOST)
    parser.add_argument("--qnxip", help="specify QNX ip address", default=QNX_IP)
    parser.add_argument("--ddir", help="specify a directory to save the data in", default='sandbox')
    parser.add_argument("--beams", type=int, help="specify number of beams", default=BEAMS)
    parser.add_argument("--avg", type=int, help="specify count to average", default=1)
    parser.add_argument("--paths", type=int, help="specify number of paths to calibrate", default=1)
    

    args = parser.parse_args()

    # sanity check average count
    if args.avg < 1 : args.avg = 1 

    # open connection with VNA
    vna = lan_init(args.vnaip)
    
    # preset VNA if calibrating
    if args.cal:
        vna_preset(vna)
    
    # init VNA measurements
    vna_init(vna)
    
    # set VNA span
    vna_setspan(vna, SWEEP_SPAN, SWEEP_CENTER, SWEEP_POINTS)
  
    # calibrate VNA if run with --cal
    # TODO: calibration is undertested... verify this
    if args.cal:
        print 'calibrating VNA'
        vna_through_cal(vna)
        vna_trigger(vna, TIMEOUT, args.avg)

    # configure VNA measurements (add smoothing to time delay channel, enable averaging) 
    vna_smoothapeture(vna,2,5.0)  
    vna_enablesmoothing(vna,2,True)  
    vna_setave(vna,args.avg)  
    vna_enableave(vna,True)  
  
    # setup csv data structure
    csvdat = csv_data()
    csvdat.sweep_count = SWEEP_POINTS
    csvdat.ave_count = args.avg
    csvdat.ave_enable = (args.avg > 1)
    csvdat.smoothing_percent = 5
    csvdat.smoothing_enable = True
    csvdat.freqs = vna_readspan(vna)
    csvdat.freq_start = min(csvdat.freqs)
    csvdat.freq_end = max(csvdat.freqs)

    # step through each path and measure phase, time delay, and magnitude at each beam setting
    for p in range(args.paths):
        p = int(raw_input('connect and enter a path number and then press enter to continue... '))
        csvdat.card = p

        for b in range(args.beams):
            csvdat.beam = b
            qnx_setbeam(args.qnxip, b)

            vna_trigger(vna, TIMEOUT, args.avg)

            csvdat.tdelay = vna_readtimedelay(vna)
            csvdat.ephase = vna_readextendedphase(vna)
            csvdat.phase = vna_readphase(vna)
            csvdat.mlog = vna_readmlog(vna)
            
            write_csv(args.ddir, csvdat)
    lan_close(vna)
