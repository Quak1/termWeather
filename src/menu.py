from weather_api import get_cities


def choose_city():
    city_name = input("Enter a city name: ")
    cities = get_cities(city_name)

    print("Cities found: ")
    for i in range(len(cities)):
        city = cities[i]
        print(f"{i+1}: {city['name']}, {city["region"]}")

    opt = input(
        "Choose a city from the list (1 - 5) or leave empty to try another search: "
    )

    invalid_msg = (
        "Invalid option, choose another entry or leave empty to try another search: "
    )

    while True:
        try:
            if not opt:
                return choose_city()
            opt = int(opt)
            if opt <= 0 or opt > len(cities):
                opt = input(invalid_msg)
                continue
            return cities[opt - 1]
        except ValueError:
            opt = input(invalid_msg)
            continue
