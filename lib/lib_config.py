import configparser, os.path

class ConfigReader:
    def __init__(self) -> None:
        self.all_config = configparser.ConfigParser()
        current_dir = os.path.dirname(__file__)

        if current_dir.endswith("/lib"):
            config_dir = "{}{}".format(current_dir[0:current_dir.find("/lib")],"/etc/automation.conf")

        else:
            config_dir = "{}{}".format(current_dir,"/etc/automation.conf")

        self.all_config.read(config_dir)