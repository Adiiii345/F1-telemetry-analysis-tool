import pandas as pd
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

DB_URL=(
    f"mysql+mysqlconnector://"
    f"{os.getenv('DB_USER')}:"
    f"{quote_plus(os.getenv('DB_PASSWORD'))}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)
engine=create_engine(DB_URL)

def get_all_sessions():
    """
    Returns all available sessions from the SQL Database.
    """
    query="""
        SELECT Session_id, Year, Race_name, Session_type
        FROM Sessions    
        ORDER BY Year, Race_name
    """
    return pd.read_sql(query, engine)

def get_race_results(session_id):
    """
    Returns finishing order and fastest lap for each driver
    """
    query=text("""
        SELECT d.Driver_Code,
        d.Driver_name,
        d.Team,
        MIN(l.Lap_time_sec) as fastest_lap,
        COUNT(l.Lap_id) as total_laps,
        AVG(l.Lap_time_sec) as avg_lap_time
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND l.is_pit_out=0
        GROUP BY d.Driver_Code, d.Driver_name, d.Team
        ORDER BY fastest_lap ASC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {'session_id': session_id})
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def get_lap_comparison(session_id,driver1,driver2):
    """
    Returns lap by lap times for two drivers for comparison
    """
    query=text("""
        SELECT 
            d.Driver_Code,
            l.Lap_number,
            l.Lap_time_sec,
            l.Tyre_Compound
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND d.Driver_Code IN (:driver1,:driver2)
        AND l.is_pit_out=0
        AND l.Lap_time_sec IS NOT NULL
        AND l.Lap_time_sec < 200
        ORDER BY l.Lap_number
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {
            'session_id': session_id,
            'driver1': driver1,
            'driver2': driver2
        })
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def get_race_pace(session_id):
    query=text("""
        SELECT 
            d.Driver_Code,
            d.Team,
            l.Lap_number,
            l.Lap_time_sec
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND l.is_pit_out=0
        AND l.Lap_time_sec IS NOT NULL
        AND l.Lap_time_sec < (
            SELECT AVG(Lap_time_sec)+ 2 * STDDEV(Lap_time_sec)
            FROM Laps
            WHERE Session_id= :session_id
        )
        ORDER BY d.Driver_Code, l.Lap_number
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {'session_id': session_id})
        return pd.DataFrame(result.fetchall(), columns=result.keys())