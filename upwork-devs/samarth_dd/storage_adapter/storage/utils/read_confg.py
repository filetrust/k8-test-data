import configparser
from storage import settings
# utility class to read properties from config.ini file


class ConfigReader:

    def __init__(self, property_name):
        self.property_name = property_name

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(settings.CONFIG_FILE)
            config_ref = config[self.property_name]
            return config_ref
        except Exception as e:
            raise FileNotFoundError(e)