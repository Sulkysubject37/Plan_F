import fastf1
import pandas as pd
import os
import numpy as np

# Setup
CACHE_DIR = os.path.join(os.getcwd(), 'data', 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
fastf1.Cache.enable_cache(CACHE_DIR)

OUTPUT_FILE = os.path.join(os.getcwd(), 'data', 'ferrari_strategy_data.csv')

# Target drivers: Ferrari vs key rivals
TARGET_DRIVERS = ['LEC', 'SAI', 'VER', 'PER', 'NOR', 'PIA', 'HAM', 'RUS'] 

def ingest_strategy_data(start_year=2024, end_year=2025):
    all_laps = []
    
    for year in range(start_year, end_year + 1):
        print(f"\n--- Ingesting Strategy Data for {year} Season (Robust Mode) ---")
        
        try:
            schedule = fastf1.get_event_schedule(year)
        except Exception as e:
            print(f"CRITICAL: Could not fetch schedule for {year}: {e}")
            continue

        # Filter for completed races
        completed_races = schedule[schedule['EventDate'] < pd.Timestamp.now()]
        print(f"{len(completed_races)} races completed in {year} season.")

        for i, row in completed_races.iterrows():
            round_num = row['RoundNumber']
            event_name = row['EventName']
            
            # Skip testing
            if 'Pre-Season' in event_name or 'Test' in event_name:
                continue
            
            print(f"\nProcessing {year} - Round {round_num}: {event_name}...")
            
            try:
                session = fastf1.get_session(year, round_num, 'R')
                session.load(laps=True, telemetry=False, weather=True, messages=False)
                
            except Exception as e:
                print(f"  Error loading session for {event_name}: {e}")
                continue

            if session.laps.empty:
                print("  No lap data found. Skipping.")
                continue

            winner_abbrev = None
            try:
                if hasattr(session, 'results') and not session.results.empty:
                    winner_abbrev = session.results.loc[session.results['Position'] == 1.0].iloc[0]['Abbreviation']
                else:
                    winner_abbrev = 'VER' 
            except:
                winner_abbrev = 'VER'

            print(f"  Benchmark Driver: {winner_abbrev}")
            
            winner_times = pd.DataFrame()
            try:
                winner_laps = session.laps.pick_driver(winner_abbrev)
                winner_times = winner_laps[['LapNumber', 'LapStartTime']].set_index('LapNumber')
            except:
                print("  Could not process winner laps. Skipping gap calc.")

            avg_track_temp = session.weather['TrackTemp'].mean() if hasattr(session, 'weather') and not session.weather.empty else 30.0

            for driver in TARGET_DRIVERS:
                try:
                    d_laps = session.laps.pick_driver(driver).reset_index(drop=True)
                except:
                    continue 
                
                if not winner_times.empty:
                    d_laps = d_laps.merge(winner_times, on='LapNumber', how='left', suffixes=('', '_winner'))
                    d_laps['GapToWinner'] = (d_laps['LapStartTime'] - d_laps['LapStartTime_winner']).dt.total_seconds()
                else:
                    d_laps['GapToWinner'] = np.nan
                
                for _, lap in d_laps.iterrows():
                    if pd.isna(lap['LapTime']): continue

                    all_laps.append({
                        'Year': year,
                        'Round': round_num,
                        'Event': event_name,
                        'Driver': driver,
                        'LapNumber': lap['LapNumber'],
                        'LapTime': lap['LapTime'].total_seconds(),
                        'Compound': lap['Compound'],
                        'TyreLife': lap['TyreLife'],
                        'Stint': lap['Stint'],
                        'PitInTime': lap['PitInTime'].total_seconds() if pd.notna(lap['PitInTime']) else None,
                        'PitOutTime': lap['PitOutTime'].total_seconds() if pd.notna(lap['PitOutTime']) else None,
                        'GapToWinner': lap['GapToWinner'],
                        'TrackTemp': avg_track_temp
                    })

    if all_laps:
        df = pd.DataFrame(all_laps)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n--- Data Ingestion Complete ---")
        print(f"Saved {len(df)} rows to {OUTPUT_FILE}")
    else:
        print("\n--- No data collected ---")

if __name__ == "__main__":
    ingest_strategy_data(start_year=2024, end_year=2025)
