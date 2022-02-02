import socket
import socketserver
import threading


from lib.proxy_service import ThreadedDnsUdpHandler,ThreadedDnsTcpHandler,ThreadedTcpDnsProxy,ThreadedUdpDnsProxy

HOST, PORT = "192.168.0.13", 53

socketserver.TCPServer.allow_reuse_address = True
socketserver.UDPServer.allow_reuse_address = True

tcp_server = ThreadedTcpDnsProxy((HOST,PORT),ThreadedDnsTcpHandler)
tcp_server_threaded = threading.Thread(target=tcp_server.serve_forever,daemon=True)
tcp_server_threaded.start()

udp_server = ThreadedUdpDnsProxy((HOST,PORT),ThreadedDnsUdpHandler)
udp_server_threaded = threading.Thread(target=udp_server.serve_forever,daemon=True)
udp_server_threaded.start()

tcp_server_threaded.join()
udp_server_threaded.join()