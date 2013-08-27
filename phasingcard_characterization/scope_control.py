# jon klein, jtklein@alaska.edu
# mit license
# library for reading from an Agilent 54620 series scope over rs232 (tested on 54624A)
# set scope for 9600 baud with xon/xoff software flow control in the util menu

import serial, time, numpy 
import pdb
from scipy.signal import kaiser

SCOPE_BAUDRATE = 9600 
SCOPE_PORT = '/dev/ttyUSB0'
SCOPE_TIMEOUT = 2
SCOPE_POINTS = 2000
SCOPE_INFINITY = 9.9E+37

def scope_init():
    ser = serial.Serial(SCOPE_PORT, SCOPE_BAUDRATE, timeout=SCOPE_TIMEOUT, xonxoff=True) 
    ser.flush()
    ser.flushInput()
    return ser 

# channels - list of channels
def scope_digitize(scope, channels, points = SCOPE_POINTS):
    scope.write(":TIM:MODE NORM\n")
    scope.write(":ACQ:TYPE NORM\n")
    scope.write(":ACQ:MODE RTIMe\n")
    scope.write(":WAV:POIN " + str(points) + '\n')
    scope.write(":WAV:FORMAT BYTE\n")

    channelstr = ', '.join('CHANnel' + str(c) for c in channels) 
    scope.write(":DIGITIZE " + channelstr + "\n")
   
def scope_getraw(scope, channels, points = SCOPE_POINTS):
    data = [] 
    
    for c in channels:
        scale = scope_getscale(scope, c)
        data = data + [[(8 * scale) * ((b-128.0)/255) for b in scope_readwave(scope, c)]]
    return data 
    
def scope_readwave(scope, channel):
    scope.write(":WAVEFORM:SOURCE CHANnel" + str(int(channel)) + '\n')
    scope.flushInput()
    scope.write(":WAVEFORM:DATA?\n")
    headerlen = scope.read(2)[-1]
    header = scope.read(int(headerlen))
    body = scope.read(SCOPE_POINTS)
    scope.flush()
    scope.flushInput()
    time.sleep(.1)
    return [ord(c) for c in body]

def scope_edgetrigger(scope, channel, level = 2, polarity = "POSitive", sweeptype = 'NORMal'):
    scope.write(":TRIGger:MODE EDGE\n")
    scope.write(":TRIGger:SLOPe " + polarity + '\n') 
    scope.write(":TRIGger:SOURce CHANNEL" + str(channel) + '\n')
    scope.write(":TRIGger:LEVel " + str(float(level)) + '\n')
    scope.write(":TRIGger:SWEep " + sweeptype + '\n')

def scope_settimebase(scope, base, delay = 0, reference = 'CENTER'):
    scope.write(":TIMEBASE:RANGE " + str(base) + "E-6\n") # set time base (in microseconds)
    scope.write(":TIMEBASE:DELAY " + str(delay) + "E-6\n")
    scope.write(":TIMEBASE:REFERENCE " + reference + "\n")

def scope_gettimebase(scope):
    scope.write(":TIMEBASE:RANGE?\n")
    return float(scope.readline())

def scope_setchannel(scope, channel, scale, offset = 0, coupling = 'DC'):
    scope.write(":CHANNEL" + str(channel) + ':SCALE ' + str(scale) + '\n') # set full range scale (in volts)
    scope.write(":CHANNEL" + str(channel) + ':OFFSET ' + str(offset) + '\n') # set offset (in volts)
    scope.write(":CHANNEL" + str(channel) + ':COUPLING ' + str(coupling) + '\n')

def scope_getscale(scope, channel):
    scope.write(":CHANNEL" + str(channel) + ':SCALE?\n')
    return float(scope.readline())

def scope_getphase(scope, ch1, ch2):
    scope.write(':MEASure:PHASe? CHAN' + str(ch1) + ',CHAN' + str(ch2) + '\n')
    return float(scope.readline())

def scope_getvpp(scope, ch):
    scope.write(':MEASure:VPP? CHAN' + str(ch) + '\n')
    return float(scope.readline())

def scope_getvrms(scope, ch):
    scope.write(':MEASure:VRMS? CHAN' + str(ch) + '\n')
    return float(scope.readline())

def scope_clear(scope):
    scope.write(":DISPlay:CLEar\n")
    scope.flush()
    scope.flushInput()

def scope_autoscale(scope):
    scope.write("AUTOSCALE\n")
    
def scope_preset(scope):
    scope.write("*RST\n")

def scope_analyzevpp(data, channel):
    # calculate vpp from rms (to help with quantization..?)
    return numpy.sqrt(numpy.mean(numpy.array(data[channel-1]) ** 2)) * 2 * numpy.sqrt(2)

def scope_analyzephase(data, channel1, channel2):
    fft1 = numpy.fft.rfft(data[channel1-1])
    fft2 = numpy.fft.rfft(data[channel2-1])

    maxarg = numpy.argmax(abs(fft1))
    phase = numpy.rad2deg(numpy.angle(fft2[maxarg]) - numpy.angle(fft1[maxarg])) 

    if phase < 0:
        phase = phase + 360

    return phase

def scope_analyzethd(data, channel):
    signal = (data[channel-1]-numpy.mean(data[channel-1])) * kaiser(len(data[channel-1]),100)
    signal_f = numpy.fft.rfft(signal)
    fidx = numpy.argmax(abs(signal_f))
    return sum([abs(signal_f[i * fidx]) for i in range(2,10)]) / abs(signal_f[fidx])
    

def scope_analyzedistortion(data, channel):
    # analyzes distortion by comparing the ratio of the peak to peak voltage to the predicted peak to peak voltage from vrms
    # not really that great of of a metric, calculating THD from the fft might be smarter?
    # nominally this would be one
    vpp_vrms = scope_analyzevpp(data, channel)
    vpp_measured = max(data[channel-1]) - min(data[channel-1])
    return vpp_measured / vpp_vrms
    
if __name__ == "__main__":
    ser = scope_init()
   
