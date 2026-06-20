import streamlit as st
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))

from lap_analysis import get_race_results
from tyre_analysis import get_tyre_strategy, get_tyre_degradation, get_stint_summary

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

st.title("Tyre Strategy")
if 'session_id' not in st.session_state:
    st.warning("No race selected. Please select a race first.")
    st.stop()

session_id=st.session_state['session_id']
session_name=st.session_state.get('session_name', 'Selected Race')

st.subheader(f"{session_name}")
st.markdown("""
    <style>
        .tyre-legend-wrap {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .tyre-card {
            background: #111;
            border: 0.5px solid #333;
            border-radius: 10px;
            padding: 14px 10px;
            text-align: center;
        }
        .tyre-icon {
            width: 48px;
            height: 48px;
            margin: 0 auto 8px;
        }
        .tyre-name {
            font-size: 13px;
            font-weight: 600;
            margin: 0 0 2px;
        }
        .tyre-desc {
            font-size: 11px;
            color: #888;
            margin: 0;
            line-height: 1.4;
        }
        .tyre-life {
            font-size: 10px;
            color: #666;
            border-top: 0.5px solid #2a2a2a;
            padding-top: 6px;
            margin: 0;
        }
        .tyre-life b {
            color: #aaa;
        }    
    </style>

    <div class="tyre-legend-wrap">
        <div class="tyre-card">
            <svg class="tyre-icon" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="#1a1a1a" stroke="#333" stroke-width="1"/>
                <circle cx="24" cy="24" r="20" fill="none" stroke="#e10600" stroke-width="5"/>
                <circle cx="24" cy="24" r="9" fill="#0d0d0d"/>
                <circle cx="24" cy="24" r="3" fill="#333"/>
            </svg>
            <p class="tyre-name" style="color:#e10600;">Soft</p>
            <p class="tyre-desc">Fastest grip, wears out quickest</p>
            <p class="tyre-life">Ideal life: <b>10-15 laps</b></p>
        </div>
        <div class="tyre-card">
            <svg class="tyre-icon" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="#1a1a1a" stroke="#333" stroke-width="1"/>
                <circle cx="24" cy="24" r="20" fill="none" stroke="#FFD700" stroke-width="5"/>
                <circle cx="24" cy="24" r="9" fill="#0d0d0d"/>
                <circle cx="24" cy="24" r="3" fill="#333"/>
            </svg>
            <p class="tyre-name" style="color:#FFD700;">Medium</p>
            <p class="tyre-desc">Balanced pace and durability</p>
            <p class="tyre-life">Ideal life: <b>20-30 laps</b></p>
        </div>
        <div class="tyre-card">
            <svg class="tyre-icon" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="#1a1a1a" stroke="#333" stroke-width="1"/>
                <circle cx="24" cy="24" r="20" fill="none" stroke="#e6e6e6" stroke-width="5"/>
                <circle cx="24" cy="24" r="9" fill="#0d0d0d"/>
                <circle cx="24" cy="24" r="3" fill="#333"/>
            </svg>
            <p class="tyre-name" style="color:#e6e6e6;">Hard</p>
            <p class="tyre-desc">Slowest grip, lasts the longest</p>
            <p class="tyre-life">Ideal life: <b>35-45 laps</b></p>
        </div>
        <div class="tyre-card">
            <svg class="tyre-icon" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="#1a1a1a" stroke="#333" stroke-width="1"/>
                <circle cx="24" cy="24" r="20" fill="none" stroke="#39B54A" stroke-width="5"/>
                <circle cx="24" cy="24" r="9" fill="#0d0d0d"/>
                <circle cx="24" cy="24" r="3" fill="#333"/>
            </svg>
            <p class="tyre-name" style="color:#39B54A;">Intermediate</p>
            <p class="tyre-desc">Light rain, grooved tread</p>
            <p class="tyre-life">Ideal life: <b>Depends on rain</b></p>
        </div>
        <div class="tyre-card">
            <svg class="tyre-icon" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="#1a1a1a" stroke="#333" stroke-width="1"/>
                <circle cx="24" cy="24" r="20" fill="none" stroke="#0067FF" stroke-width="5"/>
                <circle cx="24" cy="24" r="9" fill="#0d0d0d"/>
                <circle cx="24" cy="24" r="3" fill="#333"/>
            </svg>
            <p class="tyre-name" style="color:#0067FF;">Wet</p>
            <p class="tyre-desc">Heavy rain, deepest grooves</p>
            <p class="tyre-life">Ideal life: <b>Depends on rain</b></p>
        </div>
    </div>
""", unsafe_allow_html=True)

results=get_race_results(session_id)
strategy=get_tyre_strategy(session_id)
stint_summary=get_stint_summary(session_id)

if results.empty or strategy.empty:
    st.error("No data found. Please select a race.")
    st.stop()

COMPOUND_COLORS={
    'SOFT': '#e10600',
    'MEDIUM': '#FFD700',
    'HARD': '#e6e6e6',
    'INTERMEDIATE': '#39B54A',
    'WET': '#0067FF'
}

st.markdown("---")
st.markdown("### Tyre Strategy for all drivers")
st.markdown("""
    <div style="display:flex; gap:16px; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#e10600; border-radius:2px;"></div>
            <span style="color:#888; font-size:13px;">Soft</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#FFD700; border-radius:2px;"></div>
            <span style="color:#888; font-size:13px;">Medium</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#e6e6e6; border-radius:2px;"></div>
            <span style="color:#888; font-size:13px;">Hard</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#39B54A; border-radius:2px;"></div>
            <span style="color:#888; font-size:13px;">Intermediate</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:12px; height:12px; background:#0067FF; border-radius:2px;"></div>
            <span style="color:#888; font-size:13px;">Wet</span>
        </div>
    </div>
""", unsafe_allow_html=True)

driver_order=results['Driver_Code'].tolist()
fig=go.Figure()

for driver in driver_order:
    driver_laps=strategy[strategy['Driver_Code']==driver].sort_values('Lap_number')
    if driver_laps.empty:
        continue

    for _, lap in driver_laps.iterrows():
        fig.add_trace(go.Bar(
            x=[1],
            y=[driver],
            base=lap['Lap_number']-1,
            orientation='h',
            marker=dict(
                color=COMPOUND_COLORS.get(lap['Tyre_Compound'], '#888888'),
                line=dict(width=0)
            ),
            showlegend=False,
            hovertemplate=f"<b>{driver}</b><br>Lap {lap['Lap_number']}<br>{lap['Tyre_Compound']}<br>Tyre Life: {lap['Tyre_life']}<extra></extra>"
        ))

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#111111',
    barmode='stack',
    xaxis_title='Lap Number',
    height=600,
    yaxis=dict(
        categoryorder='array',
        categoryarray=driver_order[::-1]
    ),
    bargap=0.3
)
st.plotly_chart(fig,use_container_width=True)

st.markdown("### Stint Summary")
display_stint=stint_summary.copy()
display_stint.columns=['Driver', 'Compound', 'Laps','Best Lap(s)', 'Average Lap(s)']
display_stint['Best Lap(s)']=display_stint['Best Lap(s)'].round(3)
display_stint['Average Lap(s)']=display_stint['Average Lap(s)'].round(3)

st.dataframe(
    display_stint,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.markdown("### Tyre Degradation by Compound")

available_compounds=strategy['Tyre_Compound'].dropna().unique().tolist()

if available_compounds:
    selected_compound=st.selectbox("Select a compound", available_compounds)

    degradation=get_tyre_degradation(session_id, selected_compound)

    if not degradation.empty:
        fig_deg=go.Figure()

        for driver in degradation['Driver_Code'].unique():
            driver_deg=degradation[degradation['Driver_Code']==driver]
            fig_deg.add_trace(go.Scatter(
                x=driver_deg['Tyre_life'],
                y=driver_deg['Lap_time_sec'],
                mode='lines+markers',
                name=driver,
                line=dict(width=1.5),
                marker=dict(size=4),
                hovertemplate=f"<b>{driver}</b><br>Tyre Age: %{{x}}<br>%{{y:.3f}}s<extra></extra>"
            ))
        fig_deg.update_layout(
             template='plotly_dark',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#111111',
            xaxis_title='Tyre Life (laps)',
            yaxis_title='Lap Time (seconds)',
            hovermode='closest',
            height=450
        )
        st.plotly_chart(fig_deg, use_container_width=True)
        st.caption(f"Shows how the lap time changes as the {selected_compound} tyre ages.")
    else:
        st.info(f"No degradation data available for {selected_compound}")
else:
    st.info("No tyre compound data available")