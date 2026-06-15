import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'etl'))

from lap_analysis import get_race_results, get_race_pace

st.set_page_config(layout='wide')

st.markdown("""
    <style>
        .stButton > button{
            background-color: #e10600 !important;
            color: white !important;
            border: none !important;   
        }
        h1,h2,h3 {color: #e10600 !important;}
    </style>
""",unsafe_allow_html=True)

st.title("Race Overview")
if 'session_id' not in st.session_state:
    st.warning("No race selected. Please go and select a race.")
    st.stop()

session_id=st.session_state['session_id']
session_name=st.session_state.get('session_name', 'Selected Race')

st.subheader(f"{session_name}")

results=get_race_results(session_id)
pace=get_race_pace(session_id)

print(results)
if results.empty:
    st.warning("No race selected. Please go and select a race.")
    st.stop()

st.markdown("Key Stats of the Race")
col1,col2,col3,col4 =st.columns(4)
fastest_driver=results.iloc[0]['Driver_Code']
fastest_time= round(results.iloc[0]['fastest_lap'],3)

best_pace_driver= results.loc[results['avg_lap_time'].idxmin(), 'Driver_Code']
best_pace_time=round(results['avg_lap_time'].min(),3)
total_drivers=len(results)
total_laps=int(results['total_laps'].max())

with col1:
    st.metric("Fastest Lap", f"{fastest_time}s", fastest_driver)
with col2:
    st.metric("Best Average Pace",f"{best_pace_time}s", best_pace_driver)
with col3:
    st.metric("Total Drivers", total_drivers)
with col4:
    st.metric("Total laps", total_laps)

st.markdown("---")

display_results= results[['Driver_Code', 'Driver_name', 'Team','fastest_lap', 'total_laps', 'avg_lap_time']].copy()
display_results.columns= ['Code', 'Driver', 'Team', 'Fastest Lap(s)','Total Laps', 'Average Pace(s)']

display_results['Fastest Lap(s)']=display_results['Fastest Lap(s)'].round(3)
display_results['Average Pace(s)']=display_results['Average Pace(s)'].round(3)

st.dataframe(
    display_results,
    use_container_width=True,
    hide_index=True    
)
TEAM_COLORS= {
    'Red Bull Racing': '#3671C6',
    'Ferrari': '#E8002D',
    'Mercedes': '#27F4D2',
    'McLaren': '#FF8000',
    'Aston Martin': '#229971',
    'Alpine': '#FF87BC',
    'Williams': '#64C4FF',
    'RB': '#6692FF',
    'Kick Sauber': '#52E252',
    'Haas F1 Team': '#B6BABD',
    'Audi': '#F50537',
    'Cadillac': '#1A1AFC'
}
fig=go.Figure()

for driver in pace['Driver_Code'].unique():
    driver_pace=pace[pace['Driver_Code']==driver]
    team=results[results['Driver_Code']==driver]['Team'].values
    color=TEAM_COLORS.get(team[0], '#888888') if len(team)>0 else '#888888'

    fig.add_trace(go.Scatter(
        x=driver_pace['Lap_number'],
        y=driver_pace['Lap_time_sec'],
        mode='lines',
        name=driver,
        line=dict(color=color, width=1.5),
        hovertemplate=f"<b>{driver}</b><br>Lap %{{x}}<br>%{{y:.3f}}s<extra></extra>"
    ))

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor="#1a1a1a",
    plot_bgcolor="#111111",
    xaxis_title='Lap Number',
    yaxis_title='Lap Time (seconds)',
    hovermode='x unified',
    height=500,
    legend=dict(
        orientation='v',
        x=1.02,
        y=1
    )
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.markdown("Fastest Lap Per Driver")

results_sorted= results.sort_values('fastest_lap')

fig2=go.Figure()

fig2.add_trace(go.Bar(
    x=results_sorted['Driver_Code'],
    y=results_sorted['fastest_lap'],
    marker_color=[
        TEAM_COLORS.get(results_sorted[results_sorted['Driver_Code']==d]['Team'].values[0],'#888888'
        )
        for d in results_sorted['Driver_Code']
    ],
    hovertemplate="<b>%{x}</b><br>%{y:.3f}s<extra></extra>"
))
fig2.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#111111',
    xaxis_title='Driver',
    yaxis_title='Fastest Lap (seconds)',
    height=400,
    yaxis=dict(
        range=[
            results_sorted['fastest_lap'].min() - 1,
            results_sorted['fastest_lap'].max() + 1
        ]
    )
)
st.plotly_chart(fig2, use_container_width=True)
