from lan_control import *
from pylab import *
import time, pdb

VNAHOST = '192.168.0.145'

UNWRAPPED_PHASE = 'UPH'
PHASE = 'PHAS'
LOG_MAGNITUDE = 'MLOG'
GROUP_DELAY = 'GDEL'
REAL = 'REAL'
IMAG = 'IMAG'

def vna_init(vna):
    lan_send(vna, ":INITiate:CONTinuous OFF")
    lan_send(vna, ":CALC1:PAR:COUN 4")
    lan_send(vna, ":CALC1:PAR1:SEL")
    lan_send(vna, ":CALC1:PAR1:DEFine S12")
    lan_send(vna, ":CALC1:FORM UPH")
    lan_send(vna, ":CALC1:PAR2:SEL")
    lan_send(vna, ":CALC1:PAR2:DEFine S12")
    lan_send(vna, ":CALC1:FORM GDEL")
    lan_send(vna, ":CALC1:PAR3:SEL")
    lan_send(vna, ":CALC1:PAR3:DEFine S12")
    lan_send(vna, ":CALC1:FORM MLOG")
    lan_send(vna, ":CALC1:PAR4:SEL")
    lan_send(vna, ":CALC1:PAR4:DEFine S12")
    lan_send(vna, ":CALC1:FORM PHAS")
    lan_send(vna, ":SENS1:AVER OFF");

# span and center in hertz
def vna_setspan(vna, span, center, points):
    lan_send(vna, ":SENSe1:FREQuency:SPAN " + str(span))
    lan_send(vna, ":SENSe1:FREQuency:CENTer " + str(center))
    lan_send(vna, ":SENSe1:SWEep:POINts " + str(points))

def vna_setave(vna, count):
    lan_send(vna, ":SENS1:AVER:COUN %i" % (count));

def vna_clearave(vna):
    lan_send(vna, ":SENS1:AVER:CLE");

def vna_enableave(vna, enable):
    if enable:
        lan_send(vna, ":SENS1:AVER ON");
    else:
        lan_send(vna, ":SENS1:AVER OFF");

def vna_smoothapeture(vna, param,percent):
    param_str="PAR%i" % (param) 
    lan_send(vna, ":CALC1:%s:SEL" % (param_str))
    lan_send(vna, ":CALC1:SMO:APER %f" % (percent))
    pass

def vna_enablesmoothing(vna, param,enable):
    param_str="PAR%i" % (param) 
    if enable:
        lan_send(vna, ":CALC1:%s:SEL" % (param_str))
        lan_send(vna, ":CALC1:SMO:STAT ON")
    else:
        lan_send(vna, ":CALC1:%s:SEL" % (param_str))
        lan_send(vna, ":CALC1:SMO:STAT OFF")

def vna_preset(vna):
    return lan_send(vna, ":SYSTem:PRESet")
    
def vna_trigger(vna,timeout=0.1, triggers=1):
    for i in xrange(triggers):
        lan_send(vna, ":INIT1:IMM")
        time.sleep(timeout)
     

def vna_readdat(vna,param,form):
    time.sleep(.2)
    param_str="PAR%i" % (param) 
    lan_send(vna, ":CALC1:%s:SEL" % (param_str))
    lan_send(vna, ":CALC1:FORM %s" % (form))
    sweep = lan_send(vna, ":CALC1:DATA:FDAT?").split(',')
    try:	
        sweep = [float(s) for s in sweep]
    except:
        print 'This is bad, the data sweep of ' + str(form) + ' read back from the VNA was probably empty.'  
        print "This usually doesn't happen, rerunning the program might avoid it"
        print 'We are dumping back to a debugging shell, maybe you can figure out what happened.'
    return sweep 

def vna_readextendedphase(vna):
    ephase = vna_readdat(vna, 1,UNWRAPPED_PHASE)
    return ephase[0::2]

def vna_readmlog(vna):
    mlog = vna_readdat(vna, 3,LOG_MAGNITUDE)
    return mlog[0::2]

def vna_readphase(vna):
    phase = vna_readdat(vna, 4,PHASE)
    return phase[0::2]

def vna_readtimedelay(vna):
    delay = vna_readdat(vna, 2,GROUP_DELAY)
    return delay[0::2]

def vna_through_cal(vna):
    raw_input('connect S12 through and press enter to continue')
    lan_send(vna, ":SENS1:CORR:COLL:METH:THRU 1,2")
    time.sleep(1) 
    lan_send(vna, "SENS1:CORR:COLL:THRU 1,2")
    time.sleep(4)
    lan_send(vna, ":SENS1:CORR:COLL:SAVE")
    time.sleep(1)
#    lan_send(vna, ":SENS1:CORR:COLL:METH:THRU 2,1")
#    time.sleep(1)
#    lan_send(vna, ":SENS1:CORR:COLL:THRU 2,1")
#    time.sleep(4)
#    lan_send(vna, ":SENS1:CORR:COLL:SAVE")
#    time.sleep(1)
    raw_input('calibration complete, connect DUT and press enter to continue')

def vna_readspan(vna):
    freqs = []
    start = float(lan_send(vna, ":SENSe1:FREQuency:STAR?"))
    stop = float(lan_send(vna, ":SENSe1:FREQuency:STOP?"))
    points = float(lan_send(vna, ":SENSe1:SWEep:POINts?"))
    return linspace(start, stop, points) 

if __name__ == '__main__':
    vna = lan_init(VNAHOST)
#   vna_preset(vna)
    vna_init(vna)
    vna_setspan(vna, 12e6, 18e6, 401)
#    vna_through_cal(vna)
    vna_readspan(vna) 
    lan_close(vna)
    show()
