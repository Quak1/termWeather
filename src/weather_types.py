from typing import NotRequired, TypedDict, List


class WeatherItem(TypedDict):
    id: int
    main: str
    description: str
    icon: str


class CurrentWeather(TypedDict):
    dt: int
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    clouds: int
    uvi: float
    visibility: int
    wind_speed: float
    wind_gust: float
    wind_deg: int
    weather: List[WeatherItem]


class MinutelyWeather(TypedDict):
    dt: int
    precipitation: int


class HourlyWeather(TypedDict):
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: int
    clouds: int
    visibility: int
    wind_speed: float
    wind_gust: float
    wind_deg: int
    pop: float
    weather: List[WeatherItem]


class DayTemps(TypedDict):
    morn: float
    day: float
    eve: float
    night: float


class DailyTemp(DayTemps):
    min: float
    max: float


class DailyWeather(TypedDict):
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    summary: str
    temp: DailyTemp
    feels_like: DayTemps
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_gust: float
    wind_deg: int
    clouds: int
    uvi: float
    pop: float
    rain: NotRequired[float]
    snow: NotRequired[float]
    weather: List[WeatherItem]


class WeatherResponse(TypedDict):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: CurrentWeather
    minutely: List[MinutelyWeather]  # optional
    hourly: List[HourlyWeather]  # optional
    daily: List[DailyWeather]  # optional


class City(TypedDict):
    name: str
    lat: float
    lon: float
    country: str
    state: NotRequired[str]
    region: str
    full_name: str
