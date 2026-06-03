import sys
sys.path.append('..')
from extract import extract_session
from transform import transform_laps, _transform_weather, transform_drivers
session=extract_session(2023, 'Bahrain')
clean_laps=transform_laps(session)
weather=_transform_weather(session)
drivers=transform_drivers(session)
print("\n=== CLEAN LAPS ===")
print(clean_laps.head())

print("\n=== WEATHER ===")
print(weather.head())

print("\n=== DRIVERS ===")
print(drivers)