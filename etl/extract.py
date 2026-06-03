import pandas as pd
import fastf1
fastf1.Cache.enable_cache('cache')
def extract_session(year,race_name,session__type='R'):
    """
    Downloads the session details from fastf1 API
    year=race_year
    race_name=name of the race
    session_name= qualifying(Q), Free practice(FP), Race(R)
    """  
    print(f"Extracting {year} {race_name} {session__type} ...")
    session=fastf1.get_session(year,race_name,session__type)
    session.load(telemetry=False, weather=True)
    print("Extraction Complete.")
    return session

