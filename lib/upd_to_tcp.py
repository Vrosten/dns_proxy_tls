import socket, os, select, struct
import errno

import logging
from logging import info, warn, error

logging.root.setLevel(logging.INFO)

udp_addr=(os.environ.get("LISTEN_IP", "0.0.0.0"), int(os.environ.get("LISTEN_PORT", 53)))
tcp_addr=(os.environ.get("DNS_IP", "0.0.0.0"), int(os.environ.get("DNS_PORT", 53)))

udp_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try: udp_sock.bind(udp_addr)
except socket.error as e:
    error("Cannot bind socket: %s", e)
    info("Please configure via {LISTEN,DNS}_{PORT,IP} environment variables")
    if e.errno==errno.EACCES:
        warn("No permission error. Perhaps set LISTEN_PORT environment variable or run as root?")
    elif e.errno==errno.EADDRINUSE:
        warn("Address in use error. Perhaps set LISTEN_IP or LISTEN_PORT to different value?")
    raise SystemExit(1)

# Initiating a tx_map dictionary
tx_map={}

# Creating a struct to interpret the bytes received in UDP 
net_short=struct.Struct(">H")


to_recv=0

# Initiating the tcp list that will receive the UDP
tcp_data_buf=[]

# Initiatign the incoming list to receive the UDP flow sent by the client
incoming=[udp_sock]

# TBD to understand
tcp_sock=None

while True:
    # Declaring the selectors to manage the I/O of between UDP and TCP
    s_in, s_out, s_exc=select.select(incoming, [], [], 10)


    if udp_sock in s_in:
        data, src=udp_sock.recvfrom(8192)
        print("UDP Sock \n\n {} \n\n".format(udp_sock.recvfrom(8192)))
        
        (tx_id,)=net_short.unpack_from(data)
        tx_map[tx_id]=src
        info("udp recv %d bytes from: %r, tx_id=0x%04x", len(data), src, tx_id)
        if tcp_sock is None:
            info("Connecting tcp to %r", tcp_addr)
            tcp_sock=socket.socket()
            tcp_sock.connect(tcp_addr)
            incoming.append(tcp_sock)
        tcp_sock.sendall(net_short.pack(len(data)) + data)
    if tcp_sock in s_in:
        if not to_recv:
            data=tcp_sock.recv(2)
            if not data:
                info("DNS server closed connection, removing from loop")
                incoming.remove(tcp_sock)
                tcp_sock.close()
                tcp_sock=None
                if tx_map: warn("unresolved queries: %r", map(hex, tx_map.keys()))
                tx_map.clear()
                continue
            (to_recv,)=net_short.unpack_from(data)
        data=tcp_sock.recv(to_recv)
        if not data:
            raise EOFError("DNS server closed connection in transit for %d bytes"%(to_recv,))
        tcp_data_buf.append(data)
        to_recv-=len(data)#
        if to_recv:
            info("tcp need additional %d bytes", to_recv)
            continue
        data=b"".join(tcp_data_buf)
        tcp_data_buf[:]=[]
        to_recv=0
        (tx_id,)=net_short.unpack_from(data)
        send_addr=tx_map.pop(tx_id, None)
        info("tcp reply %d bytes to %r, tx_id=0x%04x", len(data), send_addr, tx_id)
        if send_addr is None:
            warn("No matching tx_id, already processed?")
        else: udp_sock.sendto(data, send_addr)