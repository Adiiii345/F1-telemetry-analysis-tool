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

def get_tyre_strategy(session_id):
    """
    Returns tyre compound used per lap per driver
    Used for drawing the stint chart
    """
    query=text("""
        SELECT
            d.Driver_Code,
            l.Lap_number,
            l.Tyre_Compound,
            l.Tyre_life
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id=:session_id
        AND l.Lap_time_sec IS NOT NULL
        ORDER BY d.Driver_Code, l.Lap_number       
    """)

    with engine.connect() as conn:
        result=conn.execute(query,{'session_id': session_id})
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def get_tyre_degradation(session_id, compound):
    """
    Returns how laptime changes as tyre age increases for a specific compound
    """
    query=text("""
        SELECT
            d.Driver_Code,
            l.Tyre_life,
            l.Lap_time_sec,
            l.Tyre_Compound        
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND l.Tyre_Compound= :compound
        AND is_pit_out=0
        AND l.Lap_time_sec IS NOT NULL
        AND l.Lap_time_sec <200
        ORDER BY l.Tyre_life                
    """)
    with engine.connect() as conn:
        result=conn.execute(query,{
            'session_id': session_id,
            'compound': compound
        })
        return pd.DataFrame(result.fetchall(),columns=result.keys())

def get_stint_summary(session_id):
    """
    Returns a summary on each driver's stint
    how many laps on each compound
    """
    query=text("""
        SELECT
            d.Driver_Code,
            l.Tyre_Compound,
            COUNT(l.Lap_id) AS laps_on_compound,
            MIN(l.Lap_time_sec) AS best_lap_on_compound,
            AVG(l.Lap_time_sec) AS average_lap_on_compound
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND l.is_pit_out=0
        AND l.Lap_time_sec<200
        GROUP BY d.Driver_Code, l.Tyre_Compound
        ORDER BY d.Driver_Code                     
    """)
    with engine.connect() as conn:
        result=conn.execute(query,{'session_id': session_id})
        return pd.DataFrame(result.fetchall(),columns=result.keys())