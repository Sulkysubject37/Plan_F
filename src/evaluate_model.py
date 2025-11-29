import torch
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from neural_ode_model import NeuralODE
from train_model import F1StrategyDataset # Reuse the dataset class for consistent scaling

def evaluate_model(model_path, data_path, driver_code='LEC', year=2024, round_num=1, use_sindy=False, augmented_dim=0):
    print(f"--- Evaluating Model for {driver_code}, Year {year}, Round {round_num} (SINDy: {use_sindy}, AugDim: {augmented_dim}) ---")
    
    # 1. Load Dataset (to get the scaler and processed data)
    # We create the dataset instance to fit the scaler exactly as training did
    dataset = F1StrategyDataset(data_path)
    
    # 2. Load Model
    input_dim = len(dataset.features)
    model = NeuralODE(input_dim, 64, input_dim, use_sindy=use_sindy, augmented_dim=augmented_dim).to('cpu') # Run eval on CPU
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        print("Model loaded successfully.")
    else:
        print(f"Error: Model not found at {model_path}")
        return

    model.eval()

    # 3. Extract specific sequence
    # Find the specific group in the dataframe
    df_group = dataset.df[(dataset.df['Year'] == year) & 
                          (dataset.df['Round'] == round_num) & 
                          (dataset.df['Driver'] == driver_code)]
    
    if df_group.empty:
        print("No data found for this specific query.")
        return

    # Prepare input
    lap_numbers = df_group['LapNumber'].values
    feature_data = dataset.df.loc[df_group.index, dataset.features].values
    
    # Transform using the dataset's scaler
    feature_data_scaled = dataset.scaler.transform(feature_data)
    
    x0 = torch.tensor(feature_data_scaled[0, :], dtype=torch.float32).unsqueeze(0) # Add batch dim
    integration_times = torch.tensor(lap_numbers - lap_numbers[0], dtype=torch.float32)
    
    # 4. Predict
    with torch.no_grad():
        # Output shape: [n_steps, batch_size, input_dim]
        predicted_scaled = model(x0, integration_times)
        
    # Remove batch dim and convert to numpy
    predicted_scaled_np = predicted_scaled.squeeze(1).numpy()
    
    # Inverse transform to get real units
    predicted_real = dataset.scaler.inverse_transform(predicted_scaled_np)
    actual_real = feature_data # Already in real units
    
    # 5. Visualization
    # Features: LapTime, GapToWinner, TyreLife, TireDegradation...
    feature_map = {name: i for i, name in enumerate(dataset.features)}
    
    plt.figure(figsize=(15, 10))
    
    # Plot Lap Time
    plt.subplot(2, 2, 1)
    plt.plot(lap_numbers, actual_real[:, feature_map['LapTime']], 'b-', label='Actual', alpha=0.7)
    plt.plot(lap_numbers, predicted_real[:, feature_map['LapTime']], 'r--', label='Predicted')
    plt.title('Lap Time Comparison')
    plt.xlabel('Lap Number')
    plt.ylabel('Lap Time (s)')
    plt.legend()
    plt.grid(True)

    # Plot Gap To Winner
    plt.subplot(2, 2, 2)
    plt.plot(lap_numbers, actual_real[:, feature_map['GapToWinner']], 'b-', label='Actual', alpha=0.7)
    plt.plot(lap_numbers, predicted_real[:, feature_map['GapToWinner']], 'r--', label='Predicted')
    plt.title('Gap to Winner')
    plt.xlabel('Lap Number')
    plt.ylabel('Gap (s)')
    plt.legend()
    plt.grid(True)

    # Plot Tyre Life
    plt.subplot(2, 2, 3)
    plt.plot(lap_numbers, actual_real[:, feature_map['TyreLife']], 'b-', label='Actual', alpha=0.7)
    plt.plot(lap_numbers, predicted_real[:, feature_map['TyreLife']], 'r--', label='Predicted')
    plt.title('Tyre Life')
    plt.xlabel('Lap Number')
    plt.ylabel('Laps Used')
    plt.legend()
    plt.grid(True)

    # Plot Tire Degradation (Pace drop off)
    plt.subplot(2, 2, 4)
    plt.plot(lap_numbers, actual_real[:, feature_map['TireDegradation']], 'b-', label='Actual', alpha=0.7)
    plt.plot(lap_numbers, predicted_real[:, feature_map['TireDegradation']], 'r--', label='Predicted')
    plt.title('Tire Degradation (Delta per Lap)')
    plt.xlabel('Lap Number')
    plt.ylabel('Delta (s)')
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.getcwd(), 'data', 'evaluation_plot.png')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    import sys
    
    # Default path
    model_file = 'neural_ode_strategy_model.pth'
    is_sindy = False
    
    if len(sys.argv) > 1:
        model_file = sys.argv[1]
        
    if 'sindy' in model_file:
        is_sindy = True
        
    # Assuming augmented_dim=2 for SINDy based on training default
    aug_dim = 2 if is_sindy else 0
        
    evaluate_model(
        model_path=os.path.join(os.getcwd(), 'models', model_file),
        data_path=os.path.join(os.getcwd(), 'data', 'processed_strategy_data.csv'),
        use_sindy=is_sindy,
        augmented_dim=aug_dim
    )
