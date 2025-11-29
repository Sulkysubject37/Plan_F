import pandas as pd
import numpy as np
import os

# Load the ingested data
DATA_FILE = os.path.join(os.getcwd(), 'data', 'ferrari_strategy_data.csv')
PROCESSED_DATA_FILE = os.path.join(os.getcwd(), 'data', 'processed_strategy_data.csv')

def preprocess_data(data_file=DATA_FILE):
    df = pd.read_csv(data_file)

    # Convert LapTime from seconds to timedelta for easier calculations if needed, then back to float
    # It's already in seconds, so ensure it's numeric
    df['LapTime'] = pd.to_numeric(df['LapTime'], errors='coerce')

    # Drop rows with NaN LapTime or TyreLife
    df.dropna(subset=['LapTime', 'TyreLife'], inplace=True)

    # Calculate Pace relative to the benchmark driver (GapToWinner)
    # A positive GapToWinner means the driver is slower than the benchmark
    # We want to model the *rate of change* of this gap and other states.
    # For now, let's just make sure it's a numeric column.
    df['GapToWinner'] = pd.to_numeric(df['GapToWinner'], errors='coerce')

    # Handle 'Compound'
    # 'Compound' is categorical (SOFT, MEDIUM, HARD). One-hot encode them.
    df = pd.get_dummies(df, columns=['Compound'], prefix='Compound', dummy_na=False)

    # Feature Engineering: Normalized TireLife (e.g., as a percentage of expected life)
    # This requires external knowledge or a VAE for tire wear, but for now, use raw TyreLife.
    # More advanced:
    # df['NormalizedTyreLife'] = df['TyreLife'] / df['ExpectedTyreLifeForCompound'] # (Requires a model or lookup)

    # Add Stint number (already present, but ensure it's numeric)
    df['Stint'] = pd.to_numeric(df['Stint'], errors='coerce')

    # Sort data for time-series consistency
    df.sort_values(by=['Year', 'Round', 'Driver', 'LapNumber'], inplace=True)

    # Additional features for the Neural ODE:
    # The ODE will model the change in state (z) over time (t).
    # z = [LapTime, GapToWinner, TyreLife, Compound_SOFT, Compound_MEDIUM, Compound_HARD]
    # We need to ensure that these features are scaled appropriately for the NN.

    # Example: Calculate a rudimentary "Tire Degradation" per lap within a stint
    # This is a simplification; a real model would infer this.
    df['StintLap'] = df.groupby(['Year', 'Round', 'Driver', 'Stint'])['LapNumber'].rank(method='first')
    df['PaceInStint'] = df.groupby(['Year', 'Round', 'Driver', 'Stint'])['LapTime'].transform(lambda x: x - x.iloc[0])

    # Simple degradation metric: change in lap time from the start of the stint
    df['TireDegradation'] = df.groupby(['Year', 'Round', 'Driver', 'Stint'])['LapTime'].diff().fillna(0)

    print(f"Original data shape: {df.shape}")
    print(f"Number of unique drivers: {df['Driver'].nunique()}")
    print(f"Number of unique races: {df['Event'].nunique()}")

    # Select features that will be part of the state vector for the Neural ODE
    # We'll include raw values for now, scaling will be done before model training
    features = [
        'LapTime',
        'GapToWinner',
        'TyreLife',
        'Stint',
        'StintLap',
        'TireDegradation',
        'Compound_SOFT',
        'Compound_MEDIUM',
        'Compound_HARD',
        'TrackTemp'
    ]
    
    # Ensure all feature columns exist, fill with 0 or NaN where compounds might be missing
    for col in features:
        if col not in df.columns:
            if 'Compound' in col:
                df[col] = 0
            else:
                df[col] = np.nan

    df_processed = df[['Year', 'Round', 'Event', 'Driver', 'LapNumber'] + features]
    df_processed.to_csv(PROCESSED_DATA_FILE, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_FILE}")
    print(df_processed.head())
    return df_processed

if __name__ == "__main__":
    preprocess_data()
