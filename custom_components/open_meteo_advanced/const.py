"""Constants for Open-Meteo Advanced integration."""
from dataclasses import dataclass
from typing import Optional

DOMAIN = "open_meteo_advanced"

CONF_NAME = "name"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_MODEL = "model"
CONF_FORECAST_DAYS = "forecast_days"
CONF_PAST_DAYS = "past_days"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_HOURLY_VARS = "hourly_variables"
CONF_DAILY_VARS = "daily_variables"
CONF_CURRENT_VARS = "current_variables"

DEFAULT_NAME = "Open-Meteo"
DEFAULT_UPDATE_INTERVAL = 60  # minutes
DEFAULT_FORECAST_DAYS = 7
DEFAULT_PAST_DAYS = 0

CONF_WEATHER_ENTITY = "weather_entity"

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Variables always fetched when the weather entity is enabled
WEATHER_CURRENT_VARS = [
    "temperature_2m", "relative_humidity_2m", "apparent_temperature",
    "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
    "pressure_msl", "weather_code", "cloud_cover", "visibility",
    "precipitation", "is_day",
]
WEATHER_HOURLY_VARS = [
    "temperature_2m", "weather_code", "wind_speed_10m", "wind_direction_10m",
    "precipitation_probability", "precipitation", "pressure_msl",
    "cloud_cover", "relative_humidity_2m",
]
WEATHER_DAILY_VARS = [
    "temperature_2m_max", "temperature_2m_min", "weather_code",
    "wind_speed_10m_max", "wind_direction_10m_dominant",
    "precipitation_sum", "precipitation_probability_max",
]

# WMO code → HA weather condition
_WMO_TO_CONDITION: dict[int, str] = {
    0: "sunny", 1: "sunny", 2: "partlycloudy", 3: "cloudy",
    45: "fog", 48: "fog",
    51: "rainy", 53: "rainy", 55: "rainy",
    56: "snowy-rainy", 57: "snowy-rainy",
    61: "rainy", 63: "rainy", 65: "pouring",
    66: "snowy-rainy", 67: "snowy-rainy",
    71: "snowy", 73: "snowy", 75: "snowy", 77: "snowy",
    80: "rainy", 81: "rainy", 82: "pouring",
    85: "snowy", 86: "snowy",
    95: "lightning", 96: "hail", 99: "hail",
}


def wmo_to_ha_condition(code: int | None, is_day: int | None = 1) -> str:
    """Convert a WMO weather code to a Home Assistant condition string."""
    if code is None:
        return "exceptional"
    condition = _WMO_TO_CONDITION.get(int(code), "exceptional")
    if condition == "sunny" and is_day == 0:
        return "clear-night"
    return condition


@dataclass
class VariableMeta:
    name: str
    unit: Optional[str]
    device_class: Optional[str]
    icon: Optional[str] = None


HOURLY_VARIABLES: dict[str, VariableMeta] = {
    # Temperature
    "temperature_2m": VariableMeta("Temperature 2m", "°C", "temperature"),
    "dew_point_2m": VariableMeta("Dew Point 2m", "°C", "temperature"),
    "apparent_temperature": VariableMeta("Apparent Temperature", "°C", "temperature"),
    "soil_temperature_0cm": VariableMeta("Soil Temperature 0cm", "°C", "temperature"),
    "soil_temperature_6cm": VariableMeta("Soil Temperature 6cm", "°C", "temperature"),
    "soil_temperature_18cm": VariableMeta("Soil Temperature 18cm", "°C", "temperature"),
    "soil_temperature_54cm": VariableMeta("Soil Temperature 54cm", "°C", "temperature"),
    # Humidity
    "relative_humidity_2m": VariableMeta("Relative Humidity 2m", "%", "humidity"),
    # Pressure
    "pressure_msl": VariableMeta("Pressure MSL", "hPa", "atmospheric_pressure"),
    "surface_pressure": VariableMeta("Surface Pressure", "hPa", "atmospheric_pressure"),
    "vapour_pressure_deficit": VariableMeta("Vapour Pressure Deficit", "kPa", "atmospheric_pressure"),
    # Precipitation
    "precipitation": VariableMeta("Precipitation", "mm", "precipitation"),
    "rain": VariableMeta("Rain", "mm", "precipitation"),
    "showers": VariableMeta("Showers", "mm", "precipitation"),
    "snowfall": VariableMeta("Snowfall", "cm", None, "mdi:snowflake"),
    "snow_depth": VariableMeta("Snow Depth", "m", None, "mdi:snowflake-variant"),
    "precipitation_probability": VariableMeta("Precipitation Probability", "%", None, "mdi:weather-rainy"),
    "evapotranspiration": VariableMeta("Evapotranspiration", "mm", "precipitation"),
    "et0_fao_evapotranspiration": VariableMeta("ET₀ FAO Evapotranspiration", "mm", "precipitation"),
    # Wind
    "wind_speed_10m": VariableMeta("Wind Speed 10m", "km/h", "wind_speed"),
    "wind_speed_80m": VariableMeta("Wind Speed 80m", "km/h", "wind_speed"),
    "wind_speed_120m": VariableMeta("Wind Speed 120m", "km/h", "wind_speed"),
    "wind_speed_180m": VariableMeta("Wind Speed 180m", "km/h", "wind_speed"),
    "wind_direction_10m": VariableMeta("Wind Direction 10m", "°", None, "mdi:compass"),
    "wind_direction_80m": VariableMeta("Wind Direction 80m", "°", None, "mdi:compass"),
    "wind_direction_120m": VariableMeta("Wind Direction 120m", "°", None, "mdi:compass"),
    "wind_direction_180m": VariableMeta("Wind Direction 180m", "°", None, "mdi:compass"),
    "wind_gusts_10m": VariableMeta("Wind Gusts 10m", "km/h", "wind_speed"),
    # Radiation
    "shortwave_radiation": VariableMeta("Shortwave Radiation", "W/m²", "irradiance"),
    "direct_radiation": VariableMeta("Direct Radiation", "W/m²", "irradiance"),
    "direct_normal_irradiance": VariableMeta("Direct Normal Irradiance", "W/m²", "irradiance"),
    "diffuse_radiation": VariableMeta("Diffuse Radiation", "W/m²", "irradiance"),
    "global_tilted_irradiance": VariableMeta("Global Tilted Irradiance", "W/m²", "irradiance"),
    # Cloud
    "cloud_cover": VariableMeta("Cloud Cover", "%", None, "mdi:cloud"),
    "cloud_cover_low": VariableMeta("Cloud Cover Low", "%", None, "mdi:cloud"),
    "cloud_cover_mid": VariableMeta("Cloud Cover Mid", "%", None, "mdi:cloud"),
    "cloud_cover_high": VariableMeta("Cloud Cover High", "%", None, "mdi:cloud-outline"),
    # Other
    "visibility": VariableMeta("Visibility", "m", "distance"),
    "cape": VariableMeta("CAPE", "J/kg", None, "mdi:weather-lightning"),
    "freezing_level_height": VariableMeta("Freezing Level Height", "m", None, "mdi:thermometer-minus"),
    "weather_code": VariableMeta("Weather Code (WMO)", None, None, "mdi:weather-partly-cloudy"),
    "is_day": VariableMeta("Is Day", None, None, "mdi:weather-sunny"),
    # Soil moisture
    "soil_moisture_0_to_1cm": VariableMeta("Soil Moisture 0-1cm", "m³/m³", "moisture"),
    "soil_moisture_1_to_3cm": VariableMeta("Soil Moisture 1-3cm", "m³/m³", "moisture"),
    "soil_moisture_3_to_9cm": VariableMeta("Soil Moisture 3-9cm", "m³/m³", "moisture"),
    "soil_moisture_9_to_27cm": VariableMeta("Soil Moisture 9-27cm", "m³/m³", "moisture"),
    "soil_moisture_27_to_81cm": VariableMeta("Soil Moisture 27-81cm", "m³/m³", "moisture"),
}

DAILY_VARIABLES: dict[str, VariableMeta] = {
    "temperature_2m_max": VariableMeta("Temperature Max", "°C", "temperature"),
    "temperature_2m_mean": VariableMeta("Temperature Mean", "°C", "temperature"),
    "temperature_2m_min": VariableMeta("Temperature Min", "°C", "temperature"),
    "apparent_temperature_max": VariableMeta("Apparent Temp Max", "°C", "temperature"),
    "apparent_temperature_mean": VariableMeta("Apparent Temp Mean", "°C", "temperature"),
    "apparent_temperature_min": VariableMeta("Apparent Temp Min", "°C", "temperature"),
    "precipitation_sum": VariableMeta("Precipitation Sum", "mm", "precipitation"),
    "rain_sum": VariableMeta("Rain Sum", "mm", "precipitation"),
    "showers_sum": VariableMeta("Showers Sum", "mm", "precipitation"),
    "snowfall_sum": VariableMeta("Snowfall Sum", "cm", None, "mdi:snowflake"),
    "precipitation_hours": VariableMeta("Precipitation Hours", "h", "duration"),
    "precipitation_probability_max": VariableMeta("Precip. Probability Max", "%", None, "mdi:weather-rainy"),
    "precipitation_probability_mean": VariableMeta("Precip. Probability Mean", "%", None, "mdi:weather-rainy"),
    "precipitation_probability_min": VariableMeta("Precip. Probability Min", "%", None, "mdi:weather-rainy"),
    "et0_fao_evapotranspiration": VariableMeta("ET₀ FAO Evapotranspiration", "mm", "precipitation"),
    "weather_code": VariableMeta("Weather Code (WMO)", None, None, "mdi:weather-partly-cloudy"),
    "sunrise": VariableMeta("Sunrise", None, "timestamp", "mdi:weather-sunset-up"),
    "sunset": VariableMeta("Sunset", None, "timestamp", "mdi:weather-sunset-down"),
    "sunshine_duration": VariableMeta("Sunshine Duration", "s", "duration"),
    "daylight_duration": VariableMeta("Daylight Duration", "s", "duration"),
    "wind_speed_10m_max": VariableMeta("Wind Speed Max", "km/h", "wind_speed"),
    "wind_gusts_10m_max": VariableMeta("Wind Gusts Max", "km/h", "wind_speed"),
    "wind_direction_10m_dominant": VariableMeta("Wind Direction Dominant", "°", None, "mdi:compass"),
    "shortwave_radiation_sum": VariableMeta("Shortwave Radiation Sum", "MJ/m²", None, "mdi:solar-power"),
    "uv_index_max": VariableMeta("UV Index Max", None, None, "mdi:sun-wireless"),
    "uv_index_clear_sky_max": VariableMeta("UV Index Clear Sky Max", None, None, "mdi:sun-wireless-outline"),
}

CURRENT_VARIABLES: dict[str, VariableMeta] = {
    "temperature_2m": VariableMeta("Temperature", "°C", "temperature"),
    "relative_humidity_2m": VariableMeta("Relative Humidity", "%", "humidity"),
    "apparent_temperature": VariableMeta("Apparent Temperature", "°C", "temperature"),
    "precipitation": VariableMeta("Precipitation", "mm", "precipitation"),
    "rain": VariableMeta("Rain", "mm", "precipitation"),
    "showers": VariableMeta("Showers", "mm", "precipitation"),
    "snowfall": VariableMeta("Snowfall", "cm", None, "mdi:snowflake"),
    "weather_code": VariableMeta("Weather Code (WMO)", None, None, "mdi:weather-partly-cloudy"),
    "cloud_cover": VariableMeta("Cloud Cover", "%", None, "mdi:cloud"),
    "pressure_msl": VariableMeta("Pressure MSL", "hPa", "atmospheric_pressure"),
    "surface_pressure": VariableMeta("Surface Pressure", "hPa", "atmospheric_pressure"),
    "wind_speed_10m": VariableMeta("Wind Speed", "km/h", "wind_speed"),
    "wind_direction_10m": VariableMeta("Wind Direction", "°", None, "mdi:compass"),
    "wind_gusts_10m": VariableMeta("Wind Gusts", "km/h", "wind_speed"),
    "is_day": VariableMeta("Is Day", None, None, "mdi:weather-sunny"),
}

@dataclass
class ForecastModel:
    provider:str
    model_name:str
    type:str
    id:str
    areas:list[str]

# Models are extracted from https://open-meteo.com/en/docs/model-updates
# Only 'forecast' and 'ensemble' models are listed.
WEATHER_MODELS: dict[str, ForecastModel] = {
    "cma_grapes_global": ForecastModel(
            provider = "CMA",
            model_name = "GFS Grapes 0.125°",
            type = "forecast",
            id = "cma_grapes_global",
            areas = [],
        ),
    "cmc_gem_gdps_15km": ForecastModel(
            provider = "Canadian Weather Service",
            model_name = "GDPS 0.125°",
            type = "forecast",
            id = "cmc_gem_gdps_15km",
            areas = [],
        ),
    "cmc_gem_rdps_10km": ForecastModel(
            provider = "Canadian Weather Service",
            model_name = "RDPS",
            type = "forecast",
            id = "cmc_gem_rdps_10km",
            areas = ['ca', 'us'],
        ),
    "cmc_gem_hrdps": ForecastModel(
            provider = "Canadian Weather Service",
            model_name = "HRDPS",
            type = "forecast",
            id = "cmc_gem_hrdps",
            areas = ['ca'],
        ),
    "cmc_gem_hrdps_west": ForecastModel(
            provider = "Canadian Weather Service",
            model_name = "HRDPS West",
            type = "forecast",
            id = "cmc_gem_hrdps_west",
            areas = ['ca'],
        ),
    "chmi_aladin_central_europe_2km": ForecastModel(
            provider = "CHMI",
            model_name = "CHMI Aladin Central Europe 2km",
            type = "forecast",
            id = "chmi_aladin_central_europe_2km",
            areas = ['european_union'],
        ),
    "chmi_aladin_cz_1km": ForecastModel(
            provider = "CHMI",
            model_name = "CHMI Aladin CZ 1km",
            type = "forecast",
            id = "chmi_aladin_cz_1km",
            areas = ['cz'],
        ),
    "dmi_harmonie_arome_europe": ForecastModel(
            provider = "DMI",
            model_name = "Harmonie AROME Europe",
            type = "forecast",
            id = "dmi_harmonie_arome_europe",
            areas = ['european_union'],
        ),
    "dwd_icon": ForecastModel(
            provider = "DWD",
            model_name = "ICON",
            type = "forecast",
            id = "dwd_icon",
            areas = [],
        ),
    "dwd_icon_eu": ForecastModel(
            provider = "DWD",
            model_name = "ICON-EU",
            type = "forecast",
            id = "dwd_icon_eu",
            areas = ['european_union'],
        ),
    "dwd_icon_d2": ForecastModel(
            provider = "DWD",
            model_name = "ICON-D2",
            type = "forecast",
            id = "dwd_icon_d2",
            areas = ['de', 'ch', 'at'],
        ),
    "dwd_icon_d2_15min": ForecastModel(
            provider = "DWD",
            model_name = "ICON-D2 15min",
            type = "forecast",
            id = "dwd_icon_d2_15min",
            areas = ['de', 'ch', 'at'],
        ),
    "ecmwf_ifs": ForecastModel(
            provider = "ECMWF",
            model_name = "IFS HRES 9km",
            type = "forecast",
            id = "ecmwf_ifs",
            areas = [],
        ),
    "ecmwf_aifs025_single": ForecastModel(
            provider = "ECMWF",
            model_name = "AIFS 0.25° Single",
            type = "forecast",
            id = "ecmwf_aifs025_single",
            areas = [],
        ),
    "ecmwf_ifs025": ForecastModel(
            provider = "ECMWF",
            model_name = "IFS 0.25°",
            type = "forecast",
            id = "ecmwf_ifs025",
            areas = [],
        ),
    "geosphere_arome_austria": ForecastModel(
            provider = "GeoSphere Austria",
            model_name = "GeoSphere AROME Austria",
            type = "forecast",
            id = "geosphere_arome_austria",
            areas = ['at'],
        ),
    "italia_meteo_arpae_icon_2i": ForecastModel(
            provider = "ItaliaMeteo ARPAE",
            model_name = "ICON 2I",
            type = "forecast",
            id = "italia_meteo_arpae_icon_2i",
            areas = ['it'],
        ),
    "jma_gsm": ForecastModel(
            provider = "JMA",
            model_name = "GSM 0.5°",
            type = "forecast",
            id = "jma_gsm",
            areas = [],
        ),
    "jma_msm": ForecastModel(
            provider = "JMA",
            model_name = "MSM 0.05°",
            type = "forecast",
            id = "jma_msm",
            areas = ['jp'],
        ),
    "knmi_harmonie_arome_europe": ForecastModel(
            provider = "KNMI",
            model_name = "Harmonie AROME Europe",
            type = "forecast",
            id = "knmi_harmonie_arome_europe",
            areas = ['european_union'],
        ),
    "knmi_harmonie_arome_netherlands": ForecastModel(
            provider = "KNMI",
            model_name = "Harmonie AROME Netherlands",
            type = "forecast",
            id = "knmi_harmonie_arome_netherlands",
            areas = ['nl', 'be'],
        ),
    "meteofrance_arpege_world025": ForecastModel(
            provider = "Météo-France",
            model_name = "ARPEGE World 0.25°",
            type = "forecast",
            id = "meteofrance_arpege_world025",
            areas = [],
        ),
    "meteofrance_arpege_europe": ForecastModel(
            provider = "Météo-France",
            model_name = "ARPEGE Europe 0.1°",
            type = "forecast",
            id = "meteofrance_arpege_europe",
            areas = ['european_union'],
        ),
    "meteofrance_arome_france_hd": ForecastModel(
            provider = "Météo-France",
            model_name = "AROME France 0.01 HD°",
            type = "forecast",
            id = "meteofrance_arome_france_hd",
            areas = ['fr'],
        ),
    "meteofrance_arome_france_hd_15min": ForecastModel(
            provider = "Météo-France",
            model_name = "AROME France 0.01 HD 15min",
            type = "forecast",
            id = "meteofrance_arome_france_hd_15min",
            areas = ['fr'],
        ),
    "meteofrance_arome_france0025": ForecastModel(
            provider = "Météo-France",
            model_name = "AROME France 0.025°",
            type = "forecast",
            id = "meteofrance_arome_france0025",
            areas = ['fr'],
        ),
    "meteofrance_arome_france0025_15min": ForecastModel(
            provider = "Météo-France",
            model_name = "AROME France 0.025° 15min",
            type = "forecast",
            id = "meteofrance_arome_france0025_15min",
            areas = ['fr'],
        ),
    "meteoswiss_icon_ch1": ForecastModel(
            provider = "MeteoSwiss",
            model_name = "ICON CH1",
            type = "forecast",
            id = "meteoswiss_icon_ch1",
            areas = ['ch'],
        ),
    "meteoswiss_icon_ch2": ForecastModel(
            provider = "MeteoSwiss",
            model_name = "ICON CH2",
            type = "forecast",
            id = "meteoswiss_icon_ch2",
            areas = ['ch'],
        ),
    "metno_nordic_pp": ForecastModel(
            provider = "MET Norway",
            model_name = "MET Nordic PP",
            type = "forecast",
            id = "metno_nordic_pp",
            areas = ['no', 'se', 'dk'],
        ),
    "ncep_gfs013": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "GFS 0.11°",
            type = "forecast",
            id = "ncep_gfs013",
            areas = [],
        ),
    "ncep_gfs025": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "GFS 0.25°",
            type = "forecast",
            id = "ncep_gfs025",
            areas = [],
        ),
    "ncep_aigfs025": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "AIGFS 0.25°",
            type = "forecast",
            id = "ncep_aigfs025",
            areas = [],
        ),
    "ncep_hgefs025_ensemble_mean": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "HGEFS 0.25°",
            type = "forecast",
            id = "ncep_hgefs025_ensemble_mean",
            areas = [],
        ),
    "ncep_nbm_conus": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "NBM Conus",
            type = "forecast",
            id = "ncep_nbm_conus",
            areas = ['us', 'ca'],
        ),
    "ncep_hrrr_conus": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "HRRR Conus",
            type = "forecast",
            id = "ncep_hrrr_conus",
            areas = ['us', 'ca'],
        ),
    "ncep_hrrr_conus_15min": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "HRRR Conus 15min",
            type = "forecast",
            id = "ncep_hrrr_conus_15min",
            areas = ['us', 'ca'],
        ),
    "ncep_nam_conus": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "NAM Conus",
            type = "forecast",
            id = "ncep_nam_conus",
            areas = ['us', 'ca'],
        ),
    "ukmo_global_deterministic_10km": ForecastModel(
            provider = "UK Met Office",
            model_name = "UKMO Global Deterministic 0.09°",
            type = "forecast",
            id = "ukmo_global_deterministic_10km",
            areas = [],
        ),
    "ukmo_uk_deterministic_2km": ForecastModel(
            provider = "UK Met Office",
            model_name = "UKMO UKV",
            type = "forecast",
            id = "ukmo_uk_deterministic_2km",
            areas = ['gb'],
        ),
    "cmc_gem_geps": ForecastModel(
            provider = "Canadian Weather Service",
            model_name = "GDPS 0.25° Ensemble",
            type = "ensemble",
            id = "cmc_gem_geps",
            areas = [],
        ),
    "dwd_icon_eps": ForecastModel(
            provider = "DWD",
            model_name = "ICON-EPS",
            type = "ensemble",
            id = "dwd_icon_eps",
            areas = [],
        ),
    "dwd_icon_eu_eps": ForecastModel(
            provider = "DWD",
            model_name = "ICON-EU-EPS",
            type = "ensemble",
            id = "dwd_icon_eu_eps",
            areas = ['european_union'],
        ),
    "dwd_icon_d2_eps": ForecastModel(
            provider = "DWD",
            model_name = "ICON-D2-EPS",
            type = "ensemble",
            id = "dwd_icon_d2_eps",
            areas = ['de', 'ch', 'at'],
        ),
    "ecmwf_ifs025_ensemble": ForecastModel(
            provider = "ECMWF",
            model_name = "IFS 0.25° Ensemble",
            type = "ensemble",
            id = "ecmwf_ifs025_ensemble",
            areas = [],
        ),
    "ecmwf_aifs025_ensemble": ForecastModel(
            provider = "ECMWF",
            model_name = "AIFS 0.25° Ensemble",
            type = "ensemble",
            id = "ecmwf_aifs025_ensemble",
            areas = [],
        ),
    "ncep_gefs025": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "GFS 0.25 Ensemble",
            type = "ensemble",
            id = "ncep_gefs025",
            areas = [],
        ),
    "ncep_gefs05": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "GFS 0.5° Ensemble",
            type = "ensemble",
            id = "ncep_gefs05",
            areas = [],
        ),
    "ncep_aigefs025": ForecastModel(
            provider = "NOAA NCEP",
            model_name = "AIGEFS 0.25°",
            type = "ensemble",
            id = "ncep_aigefs025",
            areas = [],
        ),
    "meteoswiss_icon_ch1_ensemble": ForecastModel(
            provider = "MeteoSwiss",
            model_name = "ICON CH1",
            type = "ensemble",
            id = "meteoswiss_icon_ch1_ensemble",
            areas = ['ch'],
        ),
    "meteoswiss_icon_ch2_ensemble": ForecastModel(
            provider = "MeteoSwiss",
            model_name = "ICON CH2",
            type = "ensemble",
            id = "meteoswiss_icon_ch2_ensemble",
            areas = ['ch'],
        ),
    "ukmo_uk_ensemble_2km": ForecastModel(
            provider = "UK Met Office",
            model_name = "UKMO UK Ensemble 2 km",
            type = "ensemble",
            id = "ukmo_uk_ensemble_2km",
            areas = ['gb'],
        ),
    "ukmo_global_ensemble_20km": ForecastModel(
            provider = "UK Met Office",
            model_name = "UKMO Global Ensemble 20 km",
            type = "ensemble",
            id = "ukmo_global_ensemble_20km",
            areas = [],
        ),
    "google_weathernext2_ensemble": ForecastModel(
            provider = "Google",
            model_name = "WeatherNext 2",
            type = "ensemble",
            id = "google_weathernext2_ensemble",
            areas = [],
        ),
}
