import fastf1
import os

# 1. Setup simple cache
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

print("--- Minimal FastF1 Test ---")

try:
    # 2. Fetch a known stable historic session (Bahrain 2023, Race)
    # Using the exact string identifier 'Bahrain Grand Prix'
    session = fastf1.get_session(2023, 'Bahrain Grand Prix', 'R')
    
    print("Session object created. Loading data...")
    
    # 3. Minimal load
    session.load(laps=True, telemetry=False, weather=False, messages=False)
    
    print("\nSUCCESS!")
    print(f"Driver 1 (Verstappen) Lap Count: {len(session.laps.pick_driver('VER'))}")
    print(session.laps.pick_driver('VER')[['LapNumber', 'LapTime', 'Compound']].head())

except Exception as e:
    print(f"\nFAILURE: {e}")
