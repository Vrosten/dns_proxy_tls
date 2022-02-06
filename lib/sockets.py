import socket,select, sys, queue, os


class tcpServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 53
        self.bind_address = ("0.0.0.0",53)


    def receive_tcp_data_socket(self):
        ADDRESS = (self.host, self.port)
        tcp_addr=(os.environ.get("DNS_IP", "0.0.0.0"), int(os.environ.get("DNS_PORT", 53)))

        print(tcp_addr)
        tcp_socket = socket.socket()
        #tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.connect(tcp_addr)

        while True:
            data,src = tcp_socket.recv(4096)
        #tcp_socket.start()
        #tcp_socket.connect((self.host,self.port))
        #text = tcp_socket.recv(4096)

        print(tcp_socket.recv(4096))

    pass

tcp_server = tcpServer()
tcp_server.receive_tcp_data_socket()