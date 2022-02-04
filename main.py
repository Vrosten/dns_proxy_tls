from audioop import add
import socket, socketserver, threading
import sys, getopt
import netifaces
from netifaces import interfaces, ifaddresses, AF_INET
from lib.proxy_service import ThreadedDnsUdpHandler,ThreadedDnsTcpHandler,ThreadedTcpDnsProxy,ThreadedUdpDnsProxy

#Asign the ip address of the container to bind the DNS port

def main():
    
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        interface_details = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in interface_details:
            interface_dict = interface_details[netifaces.AF_INET]
            for i in interface_dict:
                if i['addr'] != "127.0.0.1":
                    print(i['addr'])
                    HOST = i['addr']
    
    PORT = 53
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True

    print(">>>> Initiating DNS proxy TCP based in {}:{} <<<<".format(HOST,PORT))
    tcp_server = ThreadedTcpDnsProxy((HOST,PORT),ThreadedDnsTcpHandler)
    tcp_server_threaded = threading.Thread(target=tcp_server.serve_forever)
    tcp_server_threaded.daemon = True
    tcp_server_threaded.start()
    print(">>>> Listen on TCP {}:{} <<<<".format(HOST,PORT))

    print(">>>> Initiating DNS proxy UDP based in {}:{} <<<<".format(HOST,PORT))
    udp_server = ThreadedUdpDnsProxy((HOST,PORT),ThreadedDnsUdpHandler)
    udp_server_threaded = threading.Thread(target=udp_server.serve_forever)
    udp_server_threaded.daemon = True
    udp_server_threaded.start()
    print(">>>> Listen on UDP {}:{} <<<<".format(HOST,PORT))

    tcp_server_threaded.join()
    udp_server_threaded.join()


if __name__ == "__main__":
    main()