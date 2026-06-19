import os
import streamlit as st
import sys
import plotly.graph_objects as go

sys.path.append(os.path.join(os.path.dirname(__file__), '..','analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..','etl'))

from lap_analysis import get_race_results, get_lap_comparison
from sector_analysis import get_sector_comparison

st.set_page_config(layout='wide')

st.markdown("""
     <style>
        .stButton > button {
            background-color: #e10600 !important;
            color: white !important;
            border: none !important;
        }
        h1, h2, h3 { color: #e10600 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Driver Comparison")

if 'session_id' not in st.session_state:
    st.warning("No race selected. Please select a race to view analysis.")
    st.stop()
session_id= st.session_state['session_id']
session_name=st.session_state.get('session_name',' Selected Race')

st.subheader(f"{session_name}")
results=get_race_results(session_id)

if results.empty:
    st.error("No data found. Please reload the race from the home page.")
    st.stop()

driver_list=results['Driver_Code'].tolist()

col1,col2=st.columns(2)

with col1:
    driver1=st.selectbox("Select Driver 1",driver_list, index=0)
with col2:
    driver2=st.selectbox("Select Driver 2",driver_list,index=1 if len(driver_list)>1 else 0)

if driver1==driver2:
    st.warning("Please select two different drivers for comparison.")
    st.stop()

comparison=get_lap_comparison(session_id,driver1,driver2)
sector_comp=get_sector_comparison(session_id, driver1,driver2)

if comparison.empty:
    st.error("No lap data found for these drivers.")
    st.stop()
DRIVER_COLORS={
    driver1: '#3b82f6',
    driver2: '#e10600'
}

st.markdown("---")
st.markdown("Summary of drivers.")

d1_laps=comparison[comparison['Driver_Code']==driver1]
d2_laps=comparison[comparison['Driver_Code']==driver2]

d1_fastest=d1_laps['Lap_time_sec'].min()
d2_fastest=d2_laps['Lap_time_sec'].min()
d1_avg = d1_laps['Lap_time_sec'].mean()
d2_avg = d2_laps['Lap_time_sec'].mean()

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric(f"{driver1} Fastest Lap", f"{round(d1_fastest, 3)}s")
with col2:
    st.metric(f"{driver2} Fastest Lap", f"{round(d2_fastest, 3)}s")
with col3:
    st.metric(f"{driver1} Avg Pace", f"{round(d1_avg, 3)}s")
with col4:
    st.metric(f"{driver2} Avg Pace", f"{round(d2_avg, 3)}s")

st.markdown("---")    

st.markdown(f"Laptime Comparison - {driver1} vs {driver2}")

fig=go.Figure()
for driver in [driver1,driver2]:
    driver_data=comparison[comparison['Driver_Code']==driver]
    fig.add_trace(go.Scatter(
        x=driver_data['Lap_number'],
        y=driver_data['Lap_time_sec'],
        mode='lines+markers',
        name=driver,
        line=dict(color=DRIVER_COLORS[driver],width=2),
        marker=dict(size=4),
        hovertemplate=f"<b>{driver}</b><br>Lap %{{x}}<br>%{{y:.3f}}s<extra></extra>"
    ))
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#111111',
    xaxis_title='Lap Number',
    yaxis_title='Lap Time (seconds)',
    hovermode='x unified',
    height=450
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")  

st.markdown(f"Lap time Delta ({driver1} - {driver2})")
st.caption("Negative values indicate that driver 1 was faster on that particular lap.")

d1_indexed=d1_laps.set_index('Lap_number')['Lap_time_sec']
d2_indexed=d2_laps.set_index('Lap_number')['Lap_time_sec']
common_laps=d1_indexed.index.intersection(d2_indexed.index)
delta = d1_indexed[common_laps] - d2_indexed[common_laps]

fig_delta=go.Figure()

fig_delta.add_trace(go.Bar(
    x=delta.index,
    y=delta.values,
    marker_color=['#3b82f6' if v < 0 else '#e10600' for v in delta.values],
    hovertemplate="Lap %{x}<br>Delta: %{y:.3f}s<extra></extra>"
))
fig_delta.add_hline(y=0, line_color='#666', line_width=1)
fig_delta.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#111111',
    xaxis_title='Lap Number',
    yaxis_title='Time Delta (seconds)',
    height=350
)
st.plotly_chart(fig_delta,use_container_width=True)

st.markdown("---")

if not sector_comp.empty:
    st.markdown(f"Sector Time Comparison - {driver1} vs {driver2}")
    sector_summary= sector_comp.groupby('Driver_Code')[['Sector1_time','Sector2_time', 'Sector3_time']].mean().round(3)
    col1,col2,col3 = st.columns(3)

    sectors=['Sector1_time', 'Sector2_time', 'Sector3_time']
    sector_labels=['Sector 1', 'Sector 2', 'Sector 3']
    
    for col, sector, label in zip([col1, col2, col3], sectors, sector_labels):
        with col:
            d1_sector = sector_summary.loc[driver1, sector] if driver1 in sector_summary.index else None
            d2_sector = sector_summary.loc[driver2, sector] if driver2 in sector_summary.index else None

            if d1_sector is not None and d2_sector is not None:
                fastest=driver1 if d1_sector<d2_sector else driver2
                st.markdown(f"""
                    <div style="background:#111; border:0.5px solid #333; border-radius:8px; padding:16px; text-align:center;">
                        <p style="color:#888; font-size:12px; margin:0;">{label} Average</p>
                        <p style="color:#3b82f6; font-size:16px; margin:8px 0 2px;">{driver1}: {d1_sector}s</p>
                        <p style="color:#e10600; font-size:16px; margin:0;">{driver2}: {d2_sector}s</p>
                        <p style="color:#22c55e; font-size:12px; margin-top:8px;">{fastest} faster</p>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("Sector data not available for these drivers.")