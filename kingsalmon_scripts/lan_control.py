import telnetlib, time
VNATIMEOUT = 5 # seconds
VNAHOST = '192.168.17.100'

def lan_init(host):
    tn = telnetlib.Telnet(host)
    time.sleep(.5)
    print "hello: " + tn.read_until("MAGIC", timeout=5)
    return tn 

def lan_send(tn, command):
    tn.write(command + ';*WAI\r\n')
    time.sleep(.05)
    response = tn.read_until('>', VNATIMEOUT)
    response = response[:-7] # strip trailing SCPI>\r\n
    print str(command) + ', reponse: ' + str(response)
    return response

def lan_close(tn):
    print tn.read_very_lazy()
    tn.close()

if __name__ == '__main__':
    tn = lan_init(VNAHOST)
    lan_close(tn)
