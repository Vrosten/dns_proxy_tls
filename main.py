import socket, socketserver, threading
import sys, getopt
import docker
from lib.proxy_service import ThreadedDnsUdpHandler,ThreadedDnsTcpHandler,ThreadedTcpDnsProxy,ThreadedUdpDnsProxy

#Asign the ip address of the container to bind the DNS port

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:p:",["interface=,port="])
    except getopt.GetoptError:
        print (">>>> Usage: main.py -i <ip_address> -p <port>")
        sys.exit(2)

    for opt,arg in opts:
        if opt in ("-i","--interface"):
            HOST = arg
        elif opt in ("-p","--port"):
            PORT = arg

    if HOST:
        if PORT:
            print("{} {}".format(HOST,PORT))
            #HOST, PORT = "192.168.0.13", 9999

            socketserver.TCPServer.allow_reuse_address = True
            socketserver.UDPServer.allow_reuse_address = True

            print(">>>> Initiating DNS proxy TCP based in {}:{} <<<<".format(HOST,PORT))
            tcp_server = ThreadedTcpDnsProxy((HOST,PORT),ThreadedDnsTcpHandler)
            tcp_server_threaded = threading.Thread(target=tcp_server.serve_forever,daemon=True)
            tcp_server_threaded.start()
            print(">>>> Listen on TCP {}:{} <<<<".format(HOST,PORT))

            print(">>>> Initiating DNS proxy UDP based in {}:{} <<<<".format(HOST,PORT))
            udp_server = ThreadedUdpDnsProxy((HOST,PORT),ThreadedDnsUdpHandler)
            udp_server_threaded = threading.Thread(target=udp_server.serve_forever,daemon=True)
            udp_server_threaded.start()
            print(">>>> Listen on UDP {}:{} <<<<".format(HOST,PORT))

            tcp_server_threaded.join()
            udp_server_threaded.join()

if __name__ == "__main__":
    print("Initiating the proxy with {}".format(sys.argv[1:]))
  
    client = docker.DockerClient()
    container = client.containers.get("magical_meitner")
    ip_add = container.attrs['NetworkSettings']['IPAddress']
    print(ip_add)
    #main(sys.argv[1:])