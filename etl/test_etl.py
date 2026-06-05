import sys
sys.path.append('..')
from extract import extract_session
from transform import transform_laps, _transform_weather, transform_drivers
from load import load_session, load_drivers, load_laps, load_weather

session=extract_session(2024, 'Monaco', 'R')
clean_laps=transform_laps(session)
weather=_transform_weather(session)
drivers=transform_drivers(session)
session_info= {
    'year' : 2024,
    'race_name': 'Monaco',
    'circuit_name': session.event['Location'],
    'session_type': 'R',
    'race_date': str(session.event['EventDate'].date())
}
print("\n=== CLEAN LAPS ===")
print(clean_laps.head())

print("\n=== WEATHER ===")
print(weather.head())

print("\n=== DRIVERS ===")
print(drivers)
print("\nLoading data into MySQL...")
session_id = load_session(session_info)
driver_map = load_drivers(drivers)
load_laps(clean_laps, session_id, driver_map)
load_weather(weather, session_id)

print("\nETL Pipeline Complete!")
print(f"Session ID: {session_id}")
print(f"Driver Map: {driver_map}")

winner=session.laps.pick_driver(session.results.iloc[0]['Abbreviation'])

print(f"Winner: {session.results.iloc[0]['Abbreviation']}")
