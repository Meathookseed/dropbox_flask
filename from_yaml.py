import yact
from flask import Config


class YactConfig(Config):

    def from_yaml(self, config_file: str, directory=None):
        config = yact.from_file(config_file, directory=directory)
        for section in config.sections:
            self[section.upper()] = config[section]
