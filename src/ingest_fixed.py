import fastf1
import os
import pandas as pd

# Setup
CACHE_DIR = os.path.join(os.getcwd(), 'Plan_F', 'data', 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
    
fastf1.Cache.enable_cache(CACHE_DIR)

print("--- Direct Session Load (Bypassing Scheduler) ---")

# Instead of searching for the event (which uses Ergast), we create a session directly
# We need to know the year and the approximate event name.
# FastF1 v3.x typically needs the event object to load correctly, but we can try
# providing the specific identifier that maps to the LiveTiming path.

try:
    # We define the session by its specific LiveTiming identifier if possible, 
    # but fastf1 abstracts this. 
    # Let's try to instantiate a session explicitly.
    
    print("Attempting to load Bahrain 2024 Race...")
    
    # Force use of 'fastf1' backend for schedule if possible? 
    # Actually, let's just try get_session with strict identification.
    session = fastf1.get_session(2024, 'Bahrain', 'R')
    
    # MONKEY PATCH: If the internal event lookup failed to populate via Ergast,
    # we might need to manually set the 'date' if it's missing, as that triggers errors.
    # But let's see if just loading the 'laps' works now that we know HTTPS to LiveTiming works.
    
    print("Session created. Loading Laps (ignoring Ergast failures)...")
    
    # We assume Ergast failed, so driver info might be missing.
    # But the timing data (laps) comes from LiveTiming (which works).
    session.load(laps=True, telemetry=False, weather=False, messages=False)
    
    print(f"\nSUCCESS! Loaded {len(session.laps)} laps.")
    print(session.laps[['Driver', 'LapTime', 'Compound']].head())
    
    # Save to verify
    session.laps.to_csv(os.path.join(os.getcwd(), 'Plan_F', 'data', 'bahrain_2024_test.csv'))
    print("Saved test CSV.")

except Exception as e:
    print(f"\nFAILURE: {e}")
    import traceback
    traceback.print_exc()
