import logging
import socket, socketserver, threading
import sys, getopt
from lib.lib_sockets import ThreadedDnsUdpHandler,ThreadedDnsTcpHandler,ThreadedTcpDnsProxy,ThreadedUdpDnsProxy
from lib.lib_config import ConfigReader
from lib.lib_dns_servers import TlsDnsServer
from lib.lib_logger import LoggerDNS


def main():

    config = ConfigReader()
    logger = LoggerDNS()
   

    logger.logger.info("Reading the configuration to run the DNS proxy")
    HOST = config.all_config['InternalComm']['AddressToBind']
    PORT = int(config.all_config['InternalComm']['PortToBind'])

    # Allow to reuse the address to bind to TCP and UDP connections
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True

    # Creating a new object to a TCP DNS socket server to receive
    # DNS queries over TCP
    
    print(">>>> Initiating DNS proxy TCP based in {}:{} <<<<".format(HOST,PORT))
    
    tcp_server = ThreadedTcpDnsProxy((HOST,PORT),ThreadedDnsTcpHandler)
    tcp_server_threaded = threading.Thread(target=tcp_server.serve_forever)
    tcp_server_threaded.daemon = True
    tcp_server_threaded.start()
    logger.logger.info("Initiating the DNS proxy to accept TCP requests on host {} and port {}, in the current thread id {}".format(HOST, PORT, tcp_server_threaded.native_id))

    print(">>>> Listen on TCP {}:{} <<<<".format(HOST,PORT))

    # Creating a new object to a UDP DNS socket server to receive
    # DNS queries over UDP
    
    print(">>>> Initiating DNS proxy UDP based in {}:{} <<<<".format(HOST,PORT))
    
    udp_server = ThreadedUdpDnsProxy((HOST,PORT),ThreadedDnsUdpHandler)
    udp_server_threaded = threading.Thread(target=udp_server.serve_forever)
    udp_server_threaded.daemon = True
    udp_server_threaded.start()

    logger.logger.info("Initiating the DNS proxy to accept UDP requests on host {} and port {}, in the current thread id {}".format(HOST, PORT, udp_server_threaded.native_id))
    print(">>>> Listen on UDP {}:{} <<<<".format(HOST,PORT))

    # Using the method join to keep the process running until
    # all the threads has been closed
    tcp_server_threaded.join()
    udp_server_threaded.join()

if __name__ == "__main__":
    main()