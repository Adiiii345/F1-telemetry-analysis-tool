import fastf1
import pandas as pd
fastf1.Cache.enable_cache('cache')

Session=fastf1.get_session(2024, 'Bahrain','R')
Session.load()
laps=Session.laps
Ver_data=laps.pick_driver('STR')
print(Ver_data[['LapNumber', 'LapTime', 'Compound','TyreLife']].head(15))
print("Verstappen's fastest lap: ",Ver_data.pick_fastest())
fastest=Ver_data.pick_fastest()
telemetry=fastest.get_telemetry()
print(telemetry.columns.tolist())
print(telemetry[['DistanceToDriverAhead', 'Time', 'RPM', 'Speed', 'Brake', 'DRS']].head(10))
print(laps[['Team']].drop_duplicates())
