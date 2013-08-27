from lan_control import *
import time

VNAHOST = '137.229.27.112'
VNAPORT = 23

def vna_init():
    sock = lan_init(VNAHOST, VNAPORT)
    sock.send("INITiate:CONTinuous OFF")
    sock.send("CALCulate:PARameter:DEFine s21meas,S21")
    sock.send("CALCulate:PARameter:DEFine s11meas,S11")
    sock.send("CALCulate:PARameter:DEFine s12meas,S12")
    sock.send("CALCulate:PARameter:DEFine s22meas,S22")
    sock.send("MMEM:STOR:TRAC:FORM:SNP RI") # real/im
    sock.send(":SENS1:AVER OFF")
    return sock

# TODO: setup triggering

def vna_setspan(sock, span, center, points):
    sock.send("SENSe1:FREQuency:SPAN " + str(span) + "e9")
    sock.send("SENSe1:FREQuency:CENTer " + str(center) + "e9")
    sock.send("SENSe1:SWEep:POINts " + str(points))

def vna_preset(sock):
    return sock.send("SYSTem:PRESet;*wai")

def vna_through_cal(sock):
    raw_input('connect S21 through and press enter to continue')
    sock.send(":SENS1:CORR:COLL:METH:THRU 1,2")
    time.sleep(1) 
    sock.send("SENS1:CORR:COLL:THRU 1,2")
    time.sleep(4)
    sock.send(":SENS1:CORR:COLL:METH:THRU 2,1")
    time.sleep(1)
    sock.send(":SENS1:CORR:COLL:THRU 2,1")
    time.sleep(4)
    sock.send(":SENS1:CORR:COLL:SAVE")
    time.sleep(1)
    raw_input('calibration complete, connect DUT and press enter to continue')

def vna_readspan(sock, measurement):
    sock.send("CALCulate:PARameter:SELect " + measurement_name)
    sock.send("INITiate:IMMediate;*wai")
    sock.send("CALCulate:DATA? SDATA")


