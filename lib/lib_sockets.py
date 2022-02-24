from pickle import TRUE
from pkgutil import ImpImporter
import socket, socketserver, ssl
import struct, threading, os, select, errno, sys
from .lib_config import ConfigReader


HOST,PORT = "1.0.0.1", 853
CONFIG = ConfigReader()
print(CONFIG.all_config.sections())
HOST = CONFIG.all_config['DnsTlsServers']['DnsServer']
PORT = int(CONFIG.all_config['DnsTlsServers']['DnsOverTlsPort'])



class SocketTLS:
    def config_ssl_socket():

        tls_context = ssl.create_default_context()
        #tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        #tls_context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt",)
        
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(110)

        tls_sock = tls_context.wrap_socket(sock,server_hostname=HOST)
        tls_sock.connect((HOST,PORT))
        return tls_sock


class ThreadedDnsTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(1024).strip()

        print(type(received_data))
        print("Received data {}".format(received_data))
        
        cur_thread = threading.current_thread()
        print("DNS TCP proxy processing thread {}. Sending request".format(cur_thread))
        tls_sock = SocketTLS.config_ssl_socket()
        tls_sock.send(received_data)
        server_response = tls_sock.recv(4096)
        self.request.sendall(server_response)
        tls_sock.close()

            

class ThreadedDnsUdpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        client_data = self.request[0].strip()
        sock = self.request[1]
        client_addr = self.client_address

        cur_thread = threading.current_thread()
        print("DNS UDP<>TCP proxy processing thread {}. Sending request".format(cur_thread))

        print(" self.request from client {} = \n {} \n".format(client_addr, self.request)) 
        print("Query received from DNS Client\n\n {} \n\n".format(client_data))

        self.send_recv_udp_to_tcp(sock,client_data,client_addr)

    

    def send_recv_udp_to_tcp(self,udp_sock,recv_data,client_addr):
        tx_map = {}
        net_short = struct.Struct(">H")
        to_recv = 0
        tcp_data_buffer = []
        incoming = [udp_sock]
        tcp_sock = None

        print ("incoming > {}\n ".format(incoming))

        s_in, s_out, s_ext = select.select(incoming, [], [], 10)

        #print ("s_in > {}\n, s_out > {}\n, s_ext > {}\n".format(s_in, s_out, s_ext))
        #if udp_sock in s_in:
            #data, src = udp_sock.recvfrom(8192)
        data = recv_data
        src = client_addr
        (tx_id,) = net_short.unpack_from(data)
        tx_map[tx_id] = src
            
        print("UDP received {} bytes from: {}, tx_id={}".format(len(data),src,tx_id))

        if tcp_sock is None:
            print ("Calling set_tcp_tls_conn >\n ")
            tcp_sock = SocketTLS.config_ssl_socket()
            incoming.append(tcp_sock)
        
        tcp_sock.sendall(net_short.pack(len(data)) + data)
        
        #if tcp_sock in s_in:
        if not to_recv:
            data = tcp_sock.recv(2)
            if not data:
                print("DNS Server closed connect, removing from loop")
                incoming.remove(tcp_sock)
                tcp_sock.close()
                tcp_sock = None
                if tx_map: print("Unresolved queries: {}".format(map(hex, tx_map.keys())))
                tx_map.clear()
                #continue
            (to_recv,) = net_short.unpack_from(data)
            
        data = tcp_sock.recv(to_recv)
        if not data:
            raise EOFError("DNS server closed connection in transit for %d bytes"%(to_recv,))
            
        tcp_data_buffer.append(data)
        to_recv -= len(data)
        if to_recv:
            print("TCP need additional {} bytes".format(to_recv))
            #continue
        data = b"".join(tcp_data_buffer)
        tcp_data_buffer[:] = []
        to_recv = 0
        (tx_id,) = net_short.unpack_from(data)
        send_addr = tx_map.pop(tx_id, None)
        print("tcp reply %d bytes to %r, tx_id=0x%04x", len(data), send_addr, tx_id)
        if send_addr is None: 
            print("No matching tx_id, already processed?")
        else:
            udp_sock.sendto(data,send_addr)



    def send_udp_msg(self,received_data):
            server_address = "8.8.8.8",53
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                

                sock.sendto(received_data,server_address)
                data_from_dns = sock.recvfrom(4096)
            finally:
                sock.close()
            
            print("Query from DNS Server\n\n {} \n\n".format(data_from_dns))
            return (data_from_dns[0])



class ThreadedTcpDnsProxy(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedUdpDnsProxy(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass