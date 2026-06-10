import sys
sys.path.append('..')
from lap_analysis import get_all_sessions,get_race_results,get_lap_comparison, get_race_pace
print("ALL SESSIONS")
sessions=get_all_sessions()
print(sessions)

print("Race Results")
result=get_race_results(1)
print(result)

print("VER VS HAM")
comparison=get_lap_comparison(1,'VER','HAM')
print(comparison.head(10))
