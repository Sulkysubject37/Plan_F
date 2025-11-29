import torch
import numpy as np
import pandas as pd
import os
from neural_ode_model import NeuralODE
from train_model import F1StrategyDataset
import argparse

def what_if_simulator(
    model_path,
    data_path,
    driver='LEC',
    compound='HARD',
    current_tyre_life=0,
    laps_to_simulate=20,
    starting_lap=1,
    gap_to_leader=0.0,
    track_temp=30.0,
    year=2024, # New parameter
    round_num=1 # New parameter
):
    print(f"\n--- Plan F Strategy Simulator ---")
    print(f"Driver: {driver}")
    print(f"Scenario: Pitting for {compound} Tyres")
    print(f"Current Tyre Life: {current_tyre_life} laps")
    print(f"Simulating: {laps_to_simulate} laps ahead")
    
    # 1. Load Data & Scaler
    dataset = F1StrategyDataset(data_path)
    
    # 2. Load Model (Augmented SINDy)
    # We know from training that input_dim=8, aug_dim=2
    input_dim = len(dataset.features)
    aug_dim = 2
    model = NeuralODE(input_dim, 64, input_dim, use_sindy=True, augmented_dim=aug_dim).to('cpu')
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        model.eval()
        print("Model loaded successfully.")
    else:
        print(f"Error: Model not found at {model_path}")
        return

    # 3. Construct Initial State Vector (x0)
    # Features: ['LapTime', 'GapToWinner', 'TyreLife', 'TireDegradation', 'Compound_SOFT', 'Compound_MEDIUM', 'Compound_HARD', 'TrackTemp']
    
    # We need a "reference" LapTime to start from. Let's take the driver's average or last known lap from data.
    # For a pure "what-if", we can use a realistic baseline (e.g., 90 seconds)
    # Ideally, we fetch the driver's actual pace from the dataset for that Round.
    
    ref_data = dataset.df[(dataset.df['Year'] == year) & (dataset.df['Round'] == round_num) & (dataset.df['Driver'] == driver)]
    if not ref_data.empty:
        avg_lap_time = ref_data['LapTime'].median()
        print(f"Using historical median lap time for {driver}: {avg_lap_time:.3f}s")
    else:
        avg_lap_time = 90.0 # Fallback
        print(f"Warning: No historical data found for {driver}. Using fallback lap time: {avg_lap_time}s")

    # Construct the feature vector in REAL units
    x0_real = np.zeros(input_dim)
    feature_map = {name: i for i, name in enumerate(dataset.features)}
    
    x0_real[feature_map['LapTime']] = avg_lap_time
    x0_real[feature_map['GapToWinner']] = gap_to_leader
    x0_real[feature_map['TyreLife']] = current_tyre_life
    x0_real[feature_map['TireDegradation']] = 0.0 # Assume fresh start of stint or stable
    x0_real[feature_map['TrackTemp']] = track_temp
    
    # One-Hot Encode Compound
    if compound == 'SOFT':
        x0_real[feature_map['Compound_SOFT']] = 1.0
    elif compound == 'MEDIUM':
        x0_real[feature_map['Compound_MEDIUM']] = 1.0
    elif compound == 'HARD':
        x0_real[feature_map['Compound_HARD']] = 1.0
        
    # 4. Scale Input
    x0_scaled = dataset.scaler.transform(x0_real.reshape(1, -1))
    x0_tensor = torch.tensor(x0_scaled, dtype=torch.float32)
    
    # 5. Simulate
    # Integration times: 0, 1, 2, ... laps_to_simulate
    t_span = torch.linspace(0, laps_to_simulate, laps_to_simulate + 1)
    
    with torch.no_grad():
        # Forward pass (NeuralODE handles augmentation internally now)
        predicted_scaled = model(x0_tensor, t_span)
        
    # 6. Inverse Transform Output
    predicted_scaled_np = predicted_scaled.squeeze(1).numpy()
    predicted_real = dataset.scaler.inverse_transform(predicted_scaled_np)
    
    # 7. Analysis
    lap_times = predicted_real[:, feature_map['LapTime']]
    tyre_lives = predicted_real[:, feature_map['TyreLife']]
    gaps = predicted_real[:, feature_map['GapToWinner']]
    
    print("\n--- Simulation Results ---")
    print(f"{ 'Lap':<5} | { 'Lap Time':<10} | { 'Tyre Life':<10} | { 'Gap to Leader':<15}")
    print("-" * 50)
    
    for i in range(len(t_span)):
        print(f"{int(starting_lap + i):<5} | {lap_times[i]:.3f}s    | {tyre_lives[i]:.1f}       | {gaps[i]:.3f}s")

    total_race_time = np.sum(lap_times[1:]) # Exclude t=0 (initial state)
    print(f"\nTotal Time for {laps_to_simulate} laps: {total_race_time:.3f}s")
    
    # Simple advice
    degradation = lap_times[-1] - lap_times[0]
    print(f"Estimated Degradation: {degradation:.3f}s over {laps_to_simulate} laps")
    
    return predicted_real

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plan F Strategy Simulator")
    parser.add_argument('--driver', type=str, default='LEC', help='Driver Code (e.g., LEC, VER)')
    parser.add_argument('--compound', type=str, default='HARD', choices=['SOFT', 'MEDIUM', 'HARD'], help='Tyre Compound')
    parser.add_argument('--laps', type=int, default=20, help='Number of laps to simulate')
    parser.add_argument('--life', type=int, default=0, help='Initial tyre life')
    parser.add_argument('--gap', type=float, default=10.0, help='Initial gap to leader')
    parser.add_argument('--year', type=int, default=2024, help='Year of the Grand Prix') # New arg
    parser.add_argument('--round', type=int, default=24, help='Round number of the Grand Prix') # New arg, default to Abu Dhabi as it's the last in 2024
    
    args = parser.parse_args()
    
    what_if_simulator(
        model_path=os.path.join(os.getcwd(), 'models', 'neural_ode_strategy_model_rk4_sindy.pth'),
        data_path=os.path.join(os.getcwd(), 'data', 'processed_strategy_data.csv'),
        driver=args.driver,
        compound=args.compound,
        laps_to_simulate=args.laps,
        current_tyre_life=args.life,
        gap_to_leader=args.gap,
        year=args.year, # Pass new arg
        round_num=args.round # Pass new arg
    )
