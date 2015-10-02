
import socket,errno   #for sockets
import sys  #for exit
 
class scanner:
    def __init__(self,ipv4='localhost',ipv6='localhost6'):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
    def tcp_ipv4(self,port_start,port_end):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print ('Failed to create socket')
            sys.exit()
      
        for port in range(port_start,port_end):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((self.ipv4, port))
            if (result == 0):
                print('ipv4 Port ' + str(port) + ':Open')
            else:
                print('ipv4 Port ' + str(port) + ':Close')
            s.close()
            

    def udp_ipv4(self,port_start,port_end):
        
        
    #    for port in range(port_start,port_end):
        port = 5555
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = b'Hello'
        ret =s.sendto(msg,(self.ipv4,port))
        ret = s.recv(100)
        print(ret)
    

    def tcp_ipv6(self,port_start,port_end):
        
        for port in range(port_start,port_end):
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            result = s.connect_ex((self.ipv6, port))
            if (result == 0):
                print('ipv6 Port ' + str(port) + ':Open')
            else:
                print('ipv6 Port ' + str(port) + ':Close')
            s.close()


if __name__ == '__main__':

    s = scanner(ipv4='10.10.15.181',ipv6='fe80::226:b9ff:fe8a:77eb')
    # s.tcp_ipv4(5554,5559)
    # s.tcp_ipv6(21,30)
    s.udp_ipv4(5554,5556)



