import sys
sys.path.append('..')
from lap_analysis import get_all_sessions,get_race_results,get_lap_comparison, get_race_pace
from sector_analysis import get_best_sectors, get_sector_comparison
from tyre_analysis import get_tyre_degradation,get_stint_summary,get_tyre_strategy

print("ALL SESSIONS")
sessions=get_all_sessions()
print(sessions)

print("Race Results")
result=get_race_results(1)
print(result)

print("VER VS HAM")
comparison=get_lap_comparison(1,'VER','HAM')
print(comparison.head(10))
print("best sector")
best_sector=get_best_sectors(1)
print(best_sector)

print("comparing two drivers on each sector")
sector_comp=get_sector_comparison(1,'VER','HAM')
print(sector_comp[sector_comp['Lap_number']==4])

print("Tyre Strategy")
strategy=get_tyre_strategy(1)
print(strategy.head(20))

print("Medium tyre degradation")
degradation=get_tyre_degradation(1,'HARD')
print(degradation.head(15))

print("stint summary")
summary=get_stint_summary(1)
print(summary)
