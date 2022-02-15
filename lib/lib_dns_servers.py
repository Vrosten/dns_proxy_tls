import ssl, socket
import lib_config

class TlsDnsServer:
    def __init__(self,config)-> None:
        dns_config = config
        dns_list = open( dns_config.all_config['DnsTlsServers']['ServerListPath'].strip('"'), "r")
        self.dns_port = int(dns_config.all_config['DnsTlsServers']['DnsOverTlsPort'])
        self.server_list={}
        for row in dns_list.readlines():
            if not row.startswith("#"):
                new_row = row.strip()
                if new_row:
                    ipv4,hostname = new_row.split(",")
                    self.server_list[ipv4] = hostname
                    print("IP: {} - {}".format(ipv4,hostname))
        dns_list.close()
        
    def check_server_certificate(self):
        for key in self.server_list.keys():
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            #context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt",)
            context.load_default_certs()
            try:
                print("Checking {}.".format(self.server_list[key]))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssl_sock = context.wrap_socket(s, server_hostname=self.server_list[key])
                peer_cert = ssl_sock.getpeercert()
                print(ssl.match_hostname(peer_cert,self.server_list[key]))
            
                ssl_sock.connect((self.server_list[key], self.dns_port))
                ssl_sock.close()
            except OSError:
                print("Could not connect to {} {}. Removing from the list".format(self.server_list[key], key))
            finally:
                continue