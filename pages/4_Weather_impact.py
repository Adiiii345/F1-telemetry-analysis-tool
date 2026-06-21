import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys 
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

sys.path.append(os.path.join(os.path.dirname(__file__),'..','analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','etl'))

from lap_analysis import get_race_results, get_race_pace

load_dotenv()

DB_URL=(
    f"mysql+mysqlconnector://"
    f"{os.getenv('DB_USER')}:"
    f"{quote_plus(os.getenv('DB_PASSWORD'))}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)
engine=create_engine(DB_URL)

def get_weather_data(session_id):
    query=text("""
        SELECT time_elapsed, air_temp, track_temp, rainfall, wind_speed
        FROM weather
        WHERE Session_id= :session_id
        ORDER BY time_elapsed
    """)
    with engine.connect() as conn:
        result=conn.execute(query,{'session_id': session_id})
        return pd.DataFrame(result.fetchall(), columns=result.keys())
st.set_page_config(layout='wide')

st.markdown("""
    <style>
        .stButton > button{
        background-color: #e10600 !important;
        color: white !important;
        border: none !important;
        }
        h1, h2, h3 { color: #e10600 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Weather Impact Analysis")

if 'session_id' not in st.session_state:
    st.warning("No race selected. Please select a race.")
    st.stop()

session_id=st.session_state['session_id']
session_name=st.session_state.get('session_name', 'Selected Race')

st.subheader(f"{session_name}")

weather=get_weather_data(session_id)
pace=get_race_pace(session_id)

if weather.empty:
    st.error("No weather data found. Please reload the race from the home page.")
    st.stop()

st.markdown("---")

st.markdown("### Weather Summary")
col1,col2,col3,col4 = st.columns(4)

avg_air_temp=round(weather['air_temp'].mean(),1)
avg_track_temp=round(weather['track_temp'].mean(),1)
max_track_temp= round(weather['track_temp'].max(),1)
any_rain=weather['rainfall'].any()

with col1:
    st.metric("Average Air Temperature", f"{avg_air_temp}°C")
with col2:
    st.metric("Average Track Temperature", f"{avg_track_temp}°C")
with col3:
    st.metric("Maximum Track Temperature", f"{max_track_temp}°C")
with col4:
    st.metric("Rainfall Recorderd", "Yes" if any_rain else "No")

st.markdown("---")

st.markdown("### Temperature throughout the session")

fig_temp=go.Figure()

fig_temp.add_trace(go.Scatter(
    x=weather['time_elapsed']/60,
    y=weather['air_temp'],
    mode='lines',
    name='Track temp',
    line=dict(color='#e10600', width=2),
    hovertemplate="Track Temp: %{y:.1f}°C<extra></extra>"
))
fig_temp.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#111111',
    xaxis_title='Race Time (minutes)',
    yaxis_title='Temperature (°C)',
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

if any_rain:
    st.markdown("### Rainfall during Session")
    st.warning("Had Rainfall during the session.")

    fig_rain=go.Figure()
    fig_rain.add_trace(go.Bar(
        x=weather['time_elapsed']/60,
        y=weather['rainfall'].astype(int),
        marker_color='#0067FF',
        hovertemplate="Rain: %{y}<extra></extra>"
    ))
    fig_rain.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1a1a',
        plot_bgcolor='#111111',
        xaxis_title='Race Time (minutes)',
        yaxis_title='Rainfall (1=Yes, 0=No)',
        height=250
    )
    st.plotly_chart(fig_rain,use_container_width=True)
    st.markdown("---")
else:
    st.info("This race had no rainfall — a dry race throughout")
st.markdown("---")
st.markdown("### Track Temperature VS Lap Time")
st.caption("Each point is one lap. Shows how change in track temperature affects the laptime")

if not pace.empty:

    weather_sorted = weather.sort_values('time_elapsed').reset_index(drop=True)
    total_laps = pace['Lap_number'].max()
    weather_sorted['lap_estimate'] = (
        (weather_sorted['time_elapsed'] / weather_sorted['time_elapsed'].max() * total_laps)
        .round().astype(int)
    )
    lap_temp_map=weather_sorted.groupby('lap_estimate')['track_temp'].mean()

    pace_with_temp=pace.copy()
    pace_with_temp['track_temp']=pace_with_temp['Lap_number'].map(lap_temp_map)
    pace_with_temp=pace_with_temp.dropna(subset=['track_temp'])
    fig_corr=go.Figure()
    fig_corr.add_trace(go.Scatter(
        x=pace_with_temp['track_temp'],
        y=pace_with_temp['Lap_time_sec'],
        mode='markers',
        marker=dict(
            color=pace_with_temp['track_temp'],
            colorscale=[[0, '#3b82f6'], [1, '#e10600']],
            size=5,
            opacity=0.6,
            colorbar=dict(title="Track Temp (°C)")
        ),
        hovertemplate="Track Temp: %{x:.1f}°C<br>Lap Time: %{y:.3f}s<extra></extra>"
    ))
    fig_corr.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1a1a',
        plot_bgcolor='#111111',
        xaxis_title='Track Temperature (°C)',
        yaxis_title='Lap Time (seconds)',
        height=450
    )

    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("No lap pace data available for correlation analysis")

