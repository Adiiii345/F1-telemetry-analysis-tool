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

def get_best_sectors(session_id):
    """
    Returns each driver's best sector times
    and their theoritical best lap
    """
    query=text("""
        SELECT 
            d.Driver_code,
            d.Team,
            MIN(l.Sector1_time) AS best_sector1,
            MIN(l.Sector2_time) AS best_sector2,
            MIN(l.Sector3_time) AS best_sector3,
            MIN(l.Sector1_time) + MIN(l.Sector2_time) + MIN(l.Sector3_time) as theoretical_best
            FROM Laps l
            JOIN Drivers d ON l.Driver_id=d.Driver_id
            WHERE l.Session_id= :session_id
            AND l.Sector1_time IS NOT NULL
            AND l.Sector2_time IS NOT NULL
            AND l.Sector3_time IS NOT NULL
            GROUP BY d.Driver_Code, d.Team
            ORDER BY theoretical_best ASC
            """)
    with engine.connect() as conn:
        result=conn.execute(query, {'session_id': session_id})
        return pd.DataFrame(result.fetchall(),columns= result.keys())

def get_sector_comparison(session_id, driver1,driver2):
    """
    Returns sector by sector comparison between two drivers
    """
    query=text("""
        SELECT 
            d.Driver_Code,
            l.Lap_number,
            l.Sector1_time,
            l.Sector2_time,
            l.Sector3_time,
            l.Lap_time_sec
        FROM Laps l
        JOIN Drivers d ON l.Driver_id=d.Driver_id
        WHERE l.Session_id= :session_id
        AND d.Driver_Code IN (:driver1,:driver2)
        AND l.Sector1_time IS NOT NULL
        ORDER BY d.Driver_Code,l.Lap_number
    """)
    with engine.connect() as conn:
        result=conn.execute(query,{
            'session_id': session_id,
            'driver1': driver1,
            'driver2': driver2
        })
        return pd.DataFrame(result.fetchall(),columns=result.keys())
