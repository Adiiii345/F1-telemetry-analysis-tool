F1 TELEMETRY ANALYSIS TOOL

This is a end to end Data Engineering and Analysis Project which extracts real Formula 1 Race Data from the FastF1 python library, stores it in a structured MySQL database, and presents insights using an interactive streamlit dashboard.


Project Overview
This project is developed to showcase real life Data-Engineering skills, from raw data extraction to a deployed interactive dashboard. It covers all the steps in an ideal data cycle.

Fetching live F1 race data from the FastF1

Cleaning and Transforming the fetched data using Python and Pandas

Storing structured data in a MySQL database by implementing a star schema design

Analyzing lap times, tyre strategies, sector performance, and weather impact

Visualizing insights through an interactive Streamlit dashboard


HOW FASTF1 functions:

When you request race data through FastF1, it queries multiple external APIs:

F1 Live Timing API: Pulls official, real-time, and historical telemetry directly from the Formula 1 app.

Jolpica-F1 (Ergast) API: Provides historical race context, schedules, and standings dating back to 1950.

MultiViewer API: Supplies extra telemetry and session metadata.


TECH STACK

Language: Python 3.12

Data Source: FastF1 API

Data Preprocessing: Pandas, Numpy

Database: MySQL

Object Relational Mapping (ORM): SQLAlchamy

Visualization: Plotly, Streamlit

Version Control: Git, Github

Deployment: Streamlit Cloud


PROJECT/FOLDER STRUCTURE
'''
F1-Telemetry-Analysis-Tool/
│
├── etl/
│   ├── extract.py    #Fetches race data from fastf1 API
│   ├── transform.py  #Cleans and reshapes raw data into a structured format
│   ├── load.py       #Loads transformed data into the MySQL Database
│   └── test_etl.py   # For testing the ETL Pipeline
│
├── analysis/
│   ├── lap_analysis.py
│   ├── tyre_analysis.py
│   └── sector_analysis.py
│
├── pages/
│   ├── 1_Race_Overview.py
│   ├── 2_Driver_Comparison.py
│   ├── 3_Tyre_Strategy.py
│   └── 4_Weather_Impact.py
│
├── utils/
│   └── db_connector.py
│
├── sql/
│   └── schema.sql   # MySQL Database Schema     
│
├── .streamlit/
│   └── config.toml
│
├── cache/           # For storing cached data 
│
├── .env
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
'''

DATABASE SCHEMA

This project implements a star design which is a crucial concept in data warehousing where a central table is connected to multiple data tables.

Tables:
Sessions: Race Information inlcuding Session type, circuit, Session id and race date.

Driver: Table for driver details such as name, code and team.

Laps: Containing lap times, sector times and tyre data.

Pitstops: Contains Pitstop lap numbers and duration

Weather: Weather data throughout the race


DASHBOARD FEATURES

Race Overview: Finishing positions, fastest laps and race pace for all drivers.

Driver Comparison: head to head laptime delta chart for any two drivers.

Tyre Strategy: Visual stint showing tyre usage across the race.

Weather Impact: Relation between track temperatures and lap times.


KEY INSIGHTS:

Verstappen's average race pace in Bahrain 2023 was consistently 0.3 to 0.5 seconds faster per lap than his nearest competitor.

Tyre degradation on the Medium compound was significantly higher in the final stint due to rising track temperatures.

Sector 2 showed the biggest variation between drivers and was a key differentiator in qualifying pace.


REQUIREMENTS:

fastf1

pandas

numpy

matplotlib

plotly

streamlit

mysql-connector-python

sqlalchemy

python-dotenv

Install all at once:

pip install fastf1 pandas numpy matplotlib plotly streamlit mysql-connector-python sqlalchemy python-dotenv


AUTHOR
Aditya Dashputra

LinkedIn: https://www.linkedin.com/in/adityadashputra/

GitHub: https://github.com/Adiiii345

Email: adiidashputra@gmail.com


ACKNOWLEDGEMENTS:

FastF1 - https://github.com/theOehrly/Fast-F1

For providing free access to Formula 1 timing and telemetry data.

Streamlit - https://streamlit.io

For making it easy to build and deploy data apps.
