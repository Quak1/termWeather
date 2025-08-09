from configparser import ConfigParser

CONFIG_FILE_PATH = "./src/config.ini"


def write_config():
    with open(CONFIG_FILE_PATH, "w") as f:
        config.write(f)


config = ConfigParser()
config.read(CONFIG_FILE_PATH)
