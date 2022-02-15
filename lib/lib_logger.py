from fileinput import filename
import logging


class LoggerDNS:
    def __init__(self) -> None:
        logging.basicConfig(filename="/var/log/dns_proxy.log")
        self.logger = logging.getLogger('DNS proxy')
        self.logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('file.log')
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        f_handler.setFormatter(formatter)
        

        pass


    pass