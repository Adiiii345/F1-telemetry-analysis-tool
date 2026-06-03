import pandas as pd
def transform_laps(session):
    """Transforms the raw data from fastf1 into a clean and reshaped data"""
    laps=session.laps.copy()
    laps=laps.dropna(subset=['LapTime'])
    laps['LapTimeSec']=laps['LapTime'].dt.total_seconds()
    laps['Sector1Sec']=laps['Sector1Time'].dt.total_seconds()
    laps['Sector2Sec']=laps['Sector2Time'].dt.total_seconds()
    laps['Sector3Sec']=laps['Sector3Time'].dt.total_seconds()
    laps=laps[laps['LapTimeSec']>60]
    laps['IsPitOut']=laps['PitOutTime'].notna()

    cols=[
        'Driver', 'LapNumber', 'LapTimeSec',
        'Sector1Sec', 'Sector2Sec', 'Sector3Sec',
        'Compound', 'TyreLife', 'IsPitOut'
    ]
    laps=laps[cols].reset_index(drop=True)
    print(f"Transformed {len(laps)} clean laps")
    return laps

def _transform_weather(session):
    """Cleans Weather Data of the session"""
    weather=session.weather_data.copy()
    weather = weather[['Time', 'AirTemp', 'TrackTemp','Rainfall', 'WindSpeed']]
    weather['TimeElapsed']=weather['Time'].dt.total_seconds()
    weather=weather.drop(columns=['Time'])
    print(f"Tranformed {len(weather)} weather records.")
    return weather

def transform_drivers(session):
    """Extracts unique driver and team info from the session"""
    laps=session.laps.copy()
    drivers=laps[['Driver','Team']].drop_duplicates()
    drivers.colums=['code','team']
    print(f"Found {len(drivers)} drivers")
    return drivers



