# stupid function to control qnx box over ssh commands to set beam numbers
# copy over ssh keys to make this faster

import time
import subprocess
QNX_IP = '192.168.0.4'
BEAM_SETTLE = 2

def write(ip, card,beamcode,phasecode,attencode,rnum=1):
    commpath="/root/current_ros/write_card_memory"
    commstring='ssh root@%s "%s -c %i -m %i -p %i -a %i -r %i >/dev/null 2>/dev/null"' % \
      (ip,commpath,card,beamcode,phasecode,attencode,rnum)
    print commstring
    retval=subprocess.call(commstring,shell=True)
    if retval==0: return True
    else: return False 

def verify(ip, card,beamcode,phasecode,attencode,rnum=1):
    commpath="/root/current_ros/verify_card_memory"
    commstring='ssh root@%s "%s -c %i -m %i -p %i -a %i -r %i >/dev/null 2>/dev/null"' % \
      (ip,commpath,card,beamcode,phasecode,attencode,rnum)
    print commstring
    retval=subprocess.call(commstring,shell=True)
    if retval==0: return True
    else: return False 

def read_memory(ip, card,beamcode,rnum=1):
    commpath="/root/current_ros/verify_card_memory"
    commstring='ssh root@%s "%s -c %i -m %i -r %i 2>/dev/null"' % \
      (ip,commpath,card,beamcode,rnum)
    print commstring
    output=subprocess.check_output(commstring,shell=True).split("\n")
    atten=int(output[0][23:31])  
    phase=int(output[1][23:31])  
    return atten,phase

