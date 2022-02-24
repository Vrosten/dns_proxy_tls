from fileinput import filename
import logging


class LoggerDNS:
    def __init__(self) -> None:
        # create formatter
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        #f_handler = logging.FileHandler('file.log')
        #f_handler.setFormatter(formatter)
    
        logging.basicConfig(filename="/var/log/dns_proxy.log", format=FORMAT)
        self.logger = logging.getLogger('DNS proxy')
        self.logger.setLevel(logging.DEBUG)