from enum import Flag
import ssl, socket, base64
import OpenSSL, OpenSSL.crypto, cryptography, idna
import pprint
import os.path

from .lib_logger import LoggerDNS

class TlsDnsServer:
    def __init__(self,config)-> None:
        logger = LoggerDNS()
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
                    logger.logger.info("Reading DNS-over-TLS server {} hostname {}".format(ipv4,hostname))
        dns_list.close()

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
        


    def check_server_certificate(self):
        
        logger = LoggerDNS()
        prefered_server = {}
        x509_buffer = ""
        for key in self.server_list.keys():
            #try:
            # Establishing the context parameters
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH) 
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            #context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt",)
        
            print("\n\n================================")
            print("Checking {}".format(self.server_list[key]))
            logger.logger.info("Checking {}".format(self.server_list[key]))
            server_name = str(self.server_list[key])
            print ("Server name {}".format(server_name))
            cert_pem = self.load_server_certificate(server_name, self.dns_port)

            if cert_pem is not None:
            
                cert = open(cert_pem,"r")
                cert_buffer = cert.read()

                x509_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_buffer)
                print(x509_cert.get_pubkey())
                print(type(cert))
                #cert64_bytes = cert.encode('ascii')
                #message_bytes = base64.b64decode(cert64_bytes)
                #clear_cert = message_bytes.decode('ascii')


                print("Teste")
                #print("CERT {}".format(clear_cert))
                    
                    
                    
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(20)
                print("Socket Socket {}".format(s))
                ssl_sock = context.wrap_socket(s, server_hostname=self.server_list[key])
                print("SSL Sock {}".format(type(ssl_sock)))
                    
                
                #ssl_sock.connect((self.server_list[key], self.dns_port))
                #server_cert = ssl_sock.getpeercert()
                #print(ssl_sock.cipher())
                #print(ssl_sock.getpeercert(binary_form=True))
                #pprint(server_cert)
                    #print(ssl_sock.getpeercert())
                    #ssl_sock.do_handshake()
                    #print(ssl_sock)
                    #pprint("SSL Socket {} ".format(ssl_sock.))
                    #print("Peername for {} is {}".format(self.server_list[key],ssl_sock.getpeername()))
                    #peer_cert = ssl_sock.getpeercert()
                    #pprint(peer_cert)
                ssl_sock.close()
                '''
                    remove_from_dict = True

                    for cert_detail in peer_cert.keys():
                        

                        i = 0
                        

                        if cert_detail.startswith("subjectAltName") is True:
                            print("len(peer_cert[cert_detail]): {} {}".format(len(peer_cert[cert_detail]),peer_cert[cert_detail]))
                            count_ip_addresses = 0
                            while i <= len(peer_cert[cert_detail]):
                                peer_cert_altername = peer_cert[cert_detail]
                                
                                j = 0
                                
                                
                                #while j <= len(peer_cert_altername[i]):
                                print ("i: {} - j: {} len(peer_cert_altername[i] {} ".format(i,j,peer_cert_altername[i]))
                                altername = peer_cert_altername[i]
                                
                                #print(">>>>Altername {} || {}".format(altername,peer_cert_altername[i] ))
                        
                                if altername[0].startswith('DNS') is True:
                                    print("******* Comparing DNS {} {}".format(self.server_list[key],key,altername[0],altername[1]))
                                    print("{} {} {}".format(altername[1].startswith(self.server_list[key]),altername[1],self.server_list[key]))
                                    if altername[1].startswith(self.server_list[key]):
                                        print(">>>>> {} {} {} {}".format(self.server_list[key],key,altername[0],altername[1]))
                                        #prefered_server[key] = count_ip_addresses
                        
                                elif altername[0].startswith('IP Address') is True:
                                    if altername[1].startswith(key): #Checking the IP address 
                                        print(">>>>> {} {} {} {}".format(self.server_list[key],key,altername[0],altername[1]))                   
                                        count_ip_addresses += 1
                                        prefered_server[key] = count_ip_addresses
                                        print(prefered_server)
                                    
                                i += 1

                        

                '''
                
                            
                    #print("Could not connect to {} {}. Removing from the list".format(self.server_list[key], key))
                    #logger.logger.critical("Could not connect to {} {}. Removing from the list".format(self.server_list[key], key))
                #except TimeoutError:
                #logger.logger.warning("Timeout test connection with {}.".format(self.server_list[key]))
                #ssl_sock.shutdown(socket.SHUT_RDWR)
                #ssl_sock.close()
                #finally:
                #     continue
            
            #ip_count = 0
            #best_server = ""
            #for ip_address in prefered_server.keys():
            #    print(prefered_server[ip_address])
            #    if prefered_server[ip_address] > ip_count:
            #        ip_count = prefered_server[ip_address]
            #        best_server = prefered_server[ip_address]
                #context.load_default_certs()
                #try:
                
            #print(" Best option {} ".format(best_server))
                #print(ssl.match_hostname(peer_cert,self.server_list[key]))
                
                
                
                #except OSError:

                #finally:
                    #continue

                    