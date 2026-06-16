from sqlalchemy import create_engine,text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
import pandas as pd

load_dotenv()
DB_URL=(
    f"mysql+mysqlconnector://"
    f"{os.getenv('DB_USER')}:"
    f"{quote_plus(os.getenv('DB_PASSWORD'))}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)
engine=create_engine(DB_URL)
def load_session(session_info):
    with engine.connect() as conn:
        result=conn.execute(text("""
            SELECT Session_id FROM Sessions
            WHERE Year=:year
            AND Race_name=:race_name
            AND Session_type=:session_type
            """),session_info).fetchone()
        if result:
            print(f"Session already exists with id{result[0]}")
            return result[0]
        conn.execute(text("""
            INSERT INTO Sessions
            (Year, Race_name, Circuit_name, Session_type, Race_date)
            VALUES (:year, :race_name, :circuit_name, :session_type, :race_date)                  
        """), session_info)
        conn.commit()

        session_id=conn.execute(
            text("SELECT LAST_INSERT_ID()")
        ).scalar()
        print(f"Inserted session with id {session_id}")
        return session_id

def load_drivers(drivers_df):
    driver_map={}
    with engine.connect() as conn:
        for _, row in drivers_df.iterrows():
            result=conn.execute(text("""
                SELECT Driver_id FROM Drivers
                WHERE Driver_Code=:code                         
            """), {'code': row['code']}).fetchone()

            if result:
                driver_map[row['code']]= result[0]
                continue

            conn.execute(text("""
                INSERT INTO Drivers (Driver_Code,Driver_name, Team)
                VALUES (:code, :driver_name, :team)           
            """), {'code': row['code'], 'driver_name': row['driver_name'], 'team': row['team']})
            conn.commit()

            driver_id= conn.execute(
                text("SELECT LAST_INSERT_ID()")
            ).scalar()

            driver_map[row['code']]=driver_id
    print(f"Loaded {len(driver_map)} drivers")
    return driver_map

def load_laps(laps_df, session_id, driver_map):
    laps_df=laps_df.copy()
    with engine.connect() as conn:
        existing=conn.execute(text("""
            SELECT COUNT(*) 
            FROM Laps 
            WHERE Session_id = :session_id
        """),{'session_id':session_id}).scalar()

        if existing > 0:
            print(f"Laps already exist for session {session_id}, skipping insert")
            return

    laps_df['Session_id']= session_id
    laps_df['Driver_id']=laps_df['Driver'].map(driver_map)
    laps_df = laps_df.rename(columns={
        'LapNumber':  'Lap_number',
        'LapTimeSec': 'Lap_time_sec',
        'Sector1Sec': 'Sector1_time',
        'Sector2Sec': 'Sector2_time',
        'Sector3Sec': 'Sector3_time',
        'Compound':   'Tyre_Compound',
        'TyreLife':   'Tyre_life',
        'IsPitOut':   'is_pit_out'
    })
    final_cols=['Session_id', 'Driver_id', 'Lap_number',
        'Lap_time_sec', 'Sector1_time', 'Sector2_time',
        'Sector3_time', 'Tyre_Compound', 'Tyre_life', 'is_pit_out']
    laps_df=laps_df[final_cols]
    laps_df.to_sql('Laps', con=engine, if_exists='append', index=False)
    print(f"Loaded {len(laps_df)} laps into MySQL")

def load_weather(weather_df, session_id):
    weather_df=weather_df.copy()
    with engine.connect() as conn:
        existing = conn.execute(text("""
            SELECT COUNT(*)
            FROM weather 
            WHERE Session_id = :session_id
        """),{'session_id': session_id}).scalar()

        if existing > 0:
            print(f"Weather already exists for session {session_id}, skipping insert")
            return
    weather_df['Session_id']=session_id
    weather_df = weather_df.rename(columns={
        'AirTemp':     'air_temp',
        'TrackTemp':   'track_temp',
        'Rainfall':    'rainfall',
        'WindSpeed':   'wind_speed',
        'TimeElapsed': 'time_elapsed'
    })
    weather_df.to_sql('weather', con=engine, if_exists='append', index=False)
    print(f"Loaded {len(weather_df)} weather records into MySQL")


