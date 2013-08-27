import socket
def lan_init(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def lan_send(sock, command):
    sock.send(command + '\r\n')
    response = sock.recv(1)
    while(response[-1] != '>'):
        response = response + sock.recv(1)
    return response

if __name__ == '__main__':
    VNAHOST = '137.229.27.122'
    VNAPORT = 23 
    sock = lan_init(VNAHOST, VNAPORT)
    lan_send(sock, ":SYST:PRES")

