# stupid function to control qnx box over ssh commands to set beam numbers
# copy over ssh keys to make this faster

import os

QNX_IP = '192.168.04'
BEAM_SETTLE = .1

def qnx_setbeam(ip, beam):
    os.system('ssh root@' + QNX_IP + '"dio_set_beam -b ' + str(int(beam)) + '"')
    time.sleep(BEAM_SETTLE)

