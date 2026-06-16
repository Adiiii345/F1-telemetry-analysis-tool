import streamlit as st
import sys
sys.path.append('etl')
sys.path.append('analysis')

from extract import extract_session
from transform import transform_laps,transform_weather, transform_drivers
from load import load_session, load_drivers, load_laps, load_weather
from lap_analysis import get_all_sessions

st.set_page_config(
    page_title="F1 Telemetry Analysis Tool",
    page_icon="🏎",
    layout="wide"
)
st.sidebar.title("🏎 Analyze a Race")
st.sidebar.markdown("---")
st.sidebar.subheader("Load a New Race")
year=st.sidebar.selectbox("Select year", [2025,2024,2023,2022,2021,2020])
races = [
    'Bahrain', 'Saudi Arabia', 'Australia',
    'Japan', 'China', 'Miami', 'Monaco',
    'Canada', 'Spain', 'Austria', 'Britain',
    'Hungary', 'Belgium', 'Netherlands',
    'Italy', 'Azerbaijan', 'Singapore',
    'United States', 'Mexico', 'Brazil',
    'Las Vegas', 'Abu Dhabi'
]
race=st.sidebar.selectbox("Select Race", races)
session_type=st.sidebar.selectbox(
    "Session Type",
    ['R', 'Q', 'FP1', 'FP2', 'FP3'],
    format_func=lambda x: {
        'R': 'Race',
        'Q': 'Qualifying',
        'FP1': 'Practice 1',
        'FP2': 'Practice 2',
        'FP3': 'Practice 3'
    }[x]
)
if st.sidebar.button("Load Race", use_container_width=True,type='primary'):
    with st.spinner(f"Loading {year} {race}"):
        try:
            session=extract_session(year,race,session_type)
            clean_laps=transform_laps(session)
            weather=transform_weather(session)
            drivers=transform_drivers(session)

            session_info={
                'year': year,
                'race_name': race,
                'circuit_name': session.event['Location'],
                'session_type': session_type,
                'race_date': str(session.event['EventDate'].date())
            }

            session_id= load_session(session_info)
            driver_map=load_drivers(drivers)
            load_laps(clean_laps,session_id,driver_map)
            load_weather(weather,session_id)

            st.sidebar.success(f"{year} {race} loaded successfully!")
            st.session_state['session_id'] = session_id
            st.session_state['session_name'] = f"{year} {race}"

        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")

st.sidebar.markdown("---")

st.sidebar.subheader("Analyse a race")
sessions=get_all_sessions()

if len(sessions)>0:
    session_options=(
        sessions['Year'].astype(str)+'--'+ sessions['Race_name']
    ).tolist()
    selected=st.sidebar.selectbox(
        "Select Loaded Race",session_options
    )
    selected_idx= session_options.index(selected)
    st.session_state['session_id']=int(
        sessions.iloc[selected_idx]['Session_id']
    )
    st.session_state['session_name']=selected
else:
    st.sidebar.info("No race loaded yet, Load a race to analyse it.")

st.sidebar.markdown('---')
st.sidebar.caption("Built by Aditya Dashputra")

st.title("🏎 F1 Telemetry Analysis Tool")
if 'session_name' in st.session_state:
    st.subheader(f"Currently Viewing: {st.session_state['session_name']}") 
else:
    st.subheader(f"Welcome! Load a Race from the sidebar to get analysis.")

st.markdown("""
Use the Sidebar to
- **Load a new race** — select year, race and session type then click Load Race
- **Switch between races** — select any previously loaded race instantly
- **Navigate pages** — use the pages in the sidebar to explore different analysis
""")
st.markdown("""
    <style>
        .feature-card {
            position: relative;
            border-radius: 12px;
            padding: 28px 20px;
            text-align: center;
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
            border: 0.5px solid #333;
            background-color: #111;
            background-image: 
                repeating-linear-gradient(
                    45deg,
                    rgba(225, 6, 0, 0.06) 0px,
                    rgba(225, 6, 0, 0.06) 2px,
                    transparent 2px,
                    transparent 14px
                );
        }
        .feature-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #e10600, #ff6b00);
        }
        .feature-card .icon {
            font-size: 40px;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }
        .feature-card .title {
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        .feature-card .desc {
            color: #999;
            font-size: 14px;
            position: relative;
            z-index: 1;
        }
        .feature-card:hover {
            border-color: #e10600;
            transition: border-color 0.3s ease;
        }
    </style>
""",unsafe_allow_html=True)

col1,col2,col3=st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="title">Race Overview</div>
            <div class="desc">Podium, fastest laps and race pace for all drivers</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
     st.markdown("""
        <div class="feature-card">
        <div class="title">Driver Comparison</div>
        <div class="desc">Head to head lap time and sector analysis</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="icon"></div>
            <div class="title">Tyre Strategy</div>
            <div class="desc">Stint chart and tyre degradation analysis</div>
        </div>
    """, unsafe_allow_html=True)