# stupid function to control qnx box over ssh commands to set beam numbers
# copy over ssh keys to make this faster

import os
import time

QNX_IP = '192.168.0.4'
BEAM_SETTLE = 2

def qnx_setbeam(ip, beam):
    os.system('ssh root@' + QNX_IP + ' "/root/current_ros/dio_beam_direction -b ' + str(int(beam)) + ' >/dev/null 2>/dev/null"')
    time.sleep(BEAM_SETTLE)

