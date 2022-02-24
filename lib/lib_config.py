import configparser, os.path
from .lib_logger import LoggerDNS

class ConfigReader:
    def __init__(self) -> None:
        logger = LoggerDNS()
        self.all_config = configparser.ConfigParser()
        current_dir = os.path.dirname(__file__)

        if current_dir.endswith("/lib"):
            config_dir = "{}{}".format(current_dir[0:current_dir.find("/lib")],"/etc/proxy.conf")

        else:
            config_dir = "{}{}".format(current_dir,"/etc/proxy.conf")

        if os.path.isfile(config_dir):
            self.all_config.read(config_dir)
            
            logger.logger.critical("The DNS proxy configuration was loaded from {}. Proceeding with the execution.".format(config_dir))
        else:    
            logger.logger.critical("Config file in {} was not found or unaccessible! Please check it and try again.".format(config_dir))
            exit()
        