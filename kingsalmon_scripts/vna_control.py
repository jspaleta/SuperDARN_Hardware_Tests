from lan_control import *
from pylab import *
import time, pdb

VNAHOST = '192.168.17.100'

UNWRAPPED_PHASE = 'UPH'
LOG_MAGNITUDE = 'MLOG'
REAL = 'REAL'
IMAG = 'IMAG'

def vna_init(vna):
    lan_send(vna, ":INITiate:CONTinuous OFF")
    lan_send(vna, ":CALC1:PARameter:DEFine S21")
    lan_send(vna, ":SENS1:AVER OFF");

# span and center in hertz
def vna_setspan(vna, span, center, points):
    lan_send(vna, ":SENSe1:FREQuency:SPAN " + str(span))
    lan_send(vna, ":SENSe1:FREQuency:CENTer " + str(center))
    lan_send(vna, ":SENSe1:SWEep:POINts " + str(points))

def vna_preset(vna):
    return lan_send(vna, ":SYSTem:PRESet")

def vna_readdat(vna, form):
    lan_send(vna, ":CALC1:FORM " + form)
    lan_send(vna, ":INIT1:IMM")
    time.sleep(.5)
    sweep = lan_send(vna, ":CALC1:DATA:FDAT?").split(',') # run this twice?.. first time is just SCPI> .. wtf
    sweep = lan_send(vna, ":CALC1:DATA:FDAT?").split(',')
    sweep[-1] = sweep[-1][:-7] # trim off trailing '\r\nSCPI>'
    sweep = [float(s) for s in sweep]
    return sweep 

def vna_readphase(vna):
    phase = vna_readdat(vna, UNWRAPPED_PHASE)
    return phase[0::2]

def vna_through_cal(vna):
    raw_input('connect S21 through and press enter to continue')
    lan_send(vna, ":SENS1:CORR:COLL:METH:THRU 1,2")
    time.sleep(1) 
    lan_send(vna, "SENS1:CORR:COLL:THRU 1,2")
    time.sleep(4)
    lan_send(vna, ":SENS1:CORR:COLL:METH:THRU 2,1")
    time.sleep(1)
    lan_send(vna, ":SENS1:CORR:COLL:THRU 2,1")
    time.sleep(4)
    lan_send(vna, ":SENS1:CORR:COLL:SAVE")
    time.sleep(1)
    raw_input('calibration complete, connect DUT and press enter to continue')

def vna_readspan(sock, measurement):
    lan_send(vna, ":CALCulate:PARameter:SELect " + measurement_name)
    lan_send(vna, ":INITiate:IMMediate;*wai")
    return lan_send(vna, ":CALCulate:DATA? SDATA")

if __name__ == '__main__':
    vna = lan_init(VNAHOST)
    vna_preset(vna)
    vna_init(vna)
    vna_setspan(vna, 10e6, 10e6, 401)
#    vna_through_cal(vna)
    plot(vna_readphase(vna))
    lan_close(vna)
    show()
