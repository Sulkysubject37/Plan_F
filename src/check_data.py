import fastf1
import pandas as pd
import os

# Setup Cache
CACHE_DIR = os.path.join(os.getcwd(), 'Plan_F', 'data', 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

fastf1.Cache.enable_cache(CACHE_DIR)

def check_available_data():
    print("Fetching Season Schedules...")
    
    # Fetch 2024 Schedule
    schedule_24 = fastf1.get_event_schedule(2024)
    
    # Filter for completed races (where we have data)
    # We check if 'Session5Date' (usually the Race) is in the past? 
    # Or simply check if we can load it. 
    # fastf1 schedule returns an Event object.
    
    completed_races = schedule_24[schedule_24['EventDate'] < pd.Timestamp.now()]
    
    print(f"\n--- 2024 Season: {len(completed_races)} races completed ---")
    print(completed_races[['RoundNumber', 'Country', 'Location', 'EventName']].tail())

    # Fetch 2023 Schedule to ensure we have historical context
    schedule_23 = fastf1.get_event_schedule(2023)
    print(f"\n--- 2023 Season: {len(schedule_23)} races total ---")
    print(schedule_23[['RoundNumber', 'Country', 'Location', 'EventName']].head())

if __name__ == "__main__":
    check_available_data()
