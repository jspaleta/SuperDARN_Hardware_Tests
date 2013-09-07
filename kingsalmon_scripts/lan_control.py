import telnetlib 
VNATIMEOUT = 5 # seconds
VNAHOST = '192.168.17.100'

def lan_init(host):
    tn = telnetlib.Telnet(host)
    return tn 

def lan_send(tn, command):
    tn.write(command + '\r\n')
    response = tn.read_until('>', VNATIMEOUT)
    return response

def lan_close(tn):
    tn.close()

if __name__ == '__main__':
    tn = lan_init(VNAHOST)
    print lan_send(tn, ":SYST:PRES")
    lan_close(tn)
