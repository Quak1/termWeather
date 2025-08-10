from configparser import ConfigParser

CONFIG_FILE_PATH = "./src/config.ini"


def write_config():
    with open(CONFIG_FILE_PATH, "w") as f:
        config.write(f)


def save_city(city):
    section = f"CITY - {city['name']}"
    config.add_section(section)

    for k in city:
        config.set(section, k, str(city[k]))

    write_config()


config = ConfigParser()
config.read(CONFIG_FILE_PATH)
