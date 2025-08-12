from configparser import ConfigParser, DuplicateSectionError

from weather_types import GeoCity

CONFIG_FILE_PATH = "./src/config.ini"


def write_config():
    with open(CONFIG_FILE_PATH, "w") as f:
        config.write(f)


def save_city(city: GeoCity):
    try:
        section = f"CITY - {city['full_name']}"
        config.add_section(section)

        config.set(section, "lat", str(city["lat"]))
        config.set(section, "lon", str(city["lon"]))
        config.set(section, "name", str(city["name"]))
        config.set(section, "region", str(city["region"]))

        write_config()
        return f"Success! '{city['name']}' saved"
    except DuplicateSectionError:
        return f"'{city['full_name']}' already exists on the config file"
    except Exception:
        return f"Failed to save '{city['name']}'"


def load_cities():
    cities = []
    for section in config.sections():
        if section.startswith("CITY - "):
            city = dict(config.items((section)))
            cities.append(city)
    return cities


config = ConfigParser()
config.read(CONFIG_FILE_PATH)
