from .lib_config import ConfigReader
import ssl, socket, base64, os.path
from .lib_logger import LoggerDNS

class TlsDnsServer:
    def __init__(self)-> None:
        self.logger = LoggerDNS()
        dns_config = ConfigReader()
        dns_list = open( dns_config.all_config['DnsTlsServers']['ServerListPath'].strip('"'), "r")
        self.dns_port = int(dns_config.all_config['DnsTlsServers']['DnsOverTlsPort'])
        self.server_list = ()
        for row in dns_list.readlines():
            if not row.startswith("#"):
                new_row = row.strip()
                if new_row:
                    server_tuple = new_row.split(",")
                    self.server_list = (server_tuple,)
                    print("IP: {} - {}".format(server_tuple[0],server_tuple[1]))
                    self.logger.logger.info("Reading DNS-over-TLS server {} hostname {}".format(server_tuple[0],server_tuple[1]))
        dns_list.close()

        for row in self.server_list:
            try:
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(110)
                host = self.server_list[row][0]

                tls_context = ssl.create_default_context()

                tls_sock = tls_context.wrap_socket(sock,server_hostname=host)
                tls_sock.connect((host,self.dns_port))
                tls_sock.close()
                self.logger.logger.info("DNS server {} - {} is able to connected. Keeping it in the server list".format(self.server_list[row][0], self.server_list[row][1]))
            except TimeoutError:
                self.server_list.pop(row)
                self.logger.logger.warning("DNS server {} - {} fail to connect due the timeout configured".format(self.server_list[row][0], self.server_list[row][1]))
            finally:
                continue


    def test_conn(self,ip,port):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(110)
            tls_context = ssl.create_default_context()

            tls_sock = tls_context.wrap_socket(sock,server_hostname=ip)
            tls_sock.connect((ip,port))
            tls_sock.close()
            return True
            
        except TimeoutError:
            self.logger.logger.warning("DNS server {} has failed to connect during the second test".format(ip))
            return False
        finally:
            pass
                

    # Function to download the remote certificate from server and write it locally
    # to be imported further
    def load_server_certificate(self,host_name,port):
        current_dir = os.path.dirname(__file__)

        if current_dir.endswith("/lib"):
            config_dir = "{}{}".format(current_dir[0:current_dir.find("/lib")],"/certs")

        else:
            config_dir = "{}{}".format(current_dir,"/certs")

        if os.path.isdir(config_dir):
            print(type(host_name))
            file_name = host_name.replace(".","_")
            file_path = "{}/{}.pem".format(config_dir,file_name)
            print("File path {}".format(file_path))
            cert_file = open(file_path,"w+")
            cert_pem = ssl.get_server_certificate(addr=(host_name,port))
            print(cert_pem)
            cert_file.write(cert_pem)
            cert_file.close()

            if os.path.isfile(file_path):  
                return file_path
            else:
                return False