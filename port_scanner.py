

import socket,errno   #for sockets
import sys,os  #for exit
#import fcntl


class scanner:
    def __init__(self,hostname='localhost'):
        #self.ipv4 = socket.getaddrinfo(hostname,None,socket.AF_INET)[0][4][0]
        #self.ipv6 = socket.getaddrinfo(hostname,None,socket.AF_INET6)[0][4][0]
        self.ipv4 = '127.0.0.1'
        self.ipv6 = 'fe80::ad9c:64fc:754c:e058'
    def scan_tcp_ipv4(self,port_start,port_end):

        for port in range(port_start,port_end):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex((self.ipv4, port))
            if(result == 0):
                print('Port ' + str(port) + ' Open')
            else:
                print('Port ' + str(port) + ' closed')
            s.close()
            

    def scan_udp_ipv4(self,port_start,port_end):
        
        
    #    for port in range(port_start,port_end):
        port = 5555
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = b'Hello'
        setsockopt( socket.IPPROTO_IP, IN.IP_RECVERR, 1 )
        ret =s.sendto(msg,(self.ipv4,port))
        ret = s.recv(100)
        print(ret)
    

    def scan_tcp_ipv6(self,port_start,port_end):
        
        for port in range(port_start,port_end):
            print(self.ipv6 + ':' + str(port))
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            result = s.connect((self.ipv6, port,0,0))
            if (result == 0):
                print('ipv6 Port ' + str(port) + ':Open')
            else:
                print('ipv6 Port ' + str(port) + ':Close')
            s.close()


if __name__ == '__main__':

    s = scanner(hostname='obsengine-qa01.testdev.pelmorex.com')
    start_port = 79
    end_port = 82
    s.scan_tcp_ipv4(start_port,end_port)
    s.scan_tcp_ipv6(start_port,end_port)



