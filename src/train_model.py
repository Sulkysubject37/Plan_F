import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from neural_ode_model import NeuralODE # Import our previously defined model

# Define the F1 Dataset
class F1StrategyDataset(Dataset):
    def __init__(self, processed_data_path, scaler=None):
        self.df = pd.read_csv(processed_data_path)
        
        # Sort by Year, Round, Driver, LapNumber to ensure temporal consistency
        self.df.sort_values(by=['Year', 'Round', 'Driver', 'LapNumber'], inplace=True)
        
        # Features for the Neural ODE state vector (input_dim)
        self.features = [
            'LapTime',
            'GapToWinner',
            'TyreLife',
            'TireDegradation',
            'Compound_SOFT',
            'Compound_MEDIUM',
            'Compound_HARD',
            'TrackTemp'
        ]
        
        # Ensure all feature columns exist, fill with 0 or NaN where compounds might be missing
        for col in self.features:
            if col not in self.df.columns:
                if 'Compound' in col:
                    self.df[col] = 0
                else:
                    self.df[col] = np.nan

        # Convert boolean Compound columns to int/float
        for col in [f for f in self.features if 'Compound_' in f]:
            self.df[col] = self.df[col].astype(float)

        # Drop any remaining NaNs in features, or fill them (e.g., with mean/median)
        original_rows = len(self.df)
        self.df.dropna(subset=self.features, inplace=True)
        if len(self.df) < original_rows:
            print(f"Dropped {original_rows - len(self.df)} rows due to NaN values in features.")
            
        self.data = self.df[self.features].values

        # Initialize scaler only if not provided (for training set)
        if scaler is None:
            self.scaler = StandardScaler()
            self.scaler.fit(self.data)
        else:
            self.scaler = scaler
        
        # self.data = self.scaler.transform(self.data) # This line was causing issues with 'group' later. Scaled per group.
        
        self.sequences = []
        for (year, round_num, driver), group in self.df.groupby(['Year', 'Round', 'Driver']):
            # Each 'group' is a sequence of laps for one driver in one race
            
            lap_numbers = group['LapNumber'].values
            
            # Scale the features for this specific group (sequence)
            feature_data_group = self.scaler.transform(group[self.features].values)
            
            if len(lap_numbers) > 1: # Need at least 2 laps for a sequence
                self.sequences.append({
                    'x0': torch.tensor(feature_data_group[0, :], dtype=torch.float32),
                    'integration_times': torch.tensor(lap_numbers - lap_numbers[0], dtype=torch.float32).squeeze(), # Squeeze added here
                    'targets': torch.tensor(feature_data_group[1:, :], dtype=torch.float32),
                    'original_laps': torch.tensor(lap_numbers, dtype=torch.float32)
                })
        
        print(f"Created {len(self.sequences)} training sequences.")

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return self.sequences[idx]

# Training Function
def train_neural_ode(
    processed_data_path = os.path.join(os.getcwd(), 'data', 'processed_strategy_data.csv'),
    input_dim = 8, # Corrected: LapTime, GapToWinner, TyreLife, TireDegradation, Compound_SOFT, Compound_MEDIUM, Compound_HARD, TrackTemp
    hidden_dim = 64,
    output_dim = 8,
    epochs = 50,
    batch_size = 1, # Batch size of 1 because each sequence is a full race/stint
    learning_rate = 0.001,
    solver = 'dopri5', # Default solver
    use_sindy = False, # Flag to use SINDy-inspired model
    use_physics = False # Flag for Physics-Guided model
):
    # Device setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data preparation
    dataset = F1StrategyDataset(processed_data_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Model, Loss, Optimizer
    # We enable augmentation for SINDy by default here for the test
    aug_dim = 2 if use_sindy else 0
    
    model = NeuralODE(input_dim, hidden_dim, output_dim, ode_solver=solver, use_sindy=use_sindy, use_physics=use_physics, augmented_dim=aug_dim).to(device)
    criterion = nn.MSELoss() 
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Training Loop
    print(f"\n--- Starting Neural ODE Training (Solver: {solver}, AugDim: {aug_dim}) ---")
    for epoch in range(epochs):
        total_loss = 0
        for i, data in enumerate(dataloader):
            x0 = data['x0'].to(device)
            integration_times = data['integration_times'].squeeze().to(device) # Squeeze added here
            targets = data['targets'].to(device) 
            
            # Predict subsequent states
            predicted_states = model(x0, integration_times)
            
            if predicted_states.shape[0] > 1:
                loss = criterion(predicted_states[1:, 0, :], targets.squeeze(0)) # [0,:] because batch_size=1
            else:
                loss = torch.tensor(0.0).to(device)

            optimizer.zero_grad()
            loss.backward()
            
            # Gradient Clipping to prevent NaN
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()

            total_loss += loss.item()
            
            if use_sindy and hasattr(model.ode_func, 'prune'):
                model.ode_func.prune() # Apply sparsity
            
            if (i + 1) % 50 == 0:
                print(f"Epoch {epoch+1}, Batch {i+1}/{len(dataloader)}, Current Loss: {loss.item():.4f}")
        
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")

    print("\n--- Training Complete ---")
    model_filename = f"neural_ode_strategy_model_{solver}{'_sindy' if use_sindy else ''}{'_physics' if use_physics else ''}.pth"
    torch.save(model.state_dict(), os.path.join(os.getcwd(), 'models', model_filename))
    print(f"Model saved to models/{model_filename}")

    if use_sindy and hasattr(model.ode_func, 'print_equation'):
        print("\n--- Learned SINDy Equations ---")
        
        # AUGMENTATION: Add names for augmented dimensions
        aug_dim = 2 if use_sindy else 0 # Hardcoded to match training
        feature_names = temp_dataset.features + [f"Aug_{i+1}" for i in range(aug_dim)]
        
        model.ode_func.print_equation(feature_names)


if __name__ == "__main__":
    import sys
    import time

    MODELS_DIR = os.path.join(os.getcwd(), 'models')
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    temp_dataset = F1StrategyDataset(os.path.join(os.getcwd(), 'data', 'processed_strategy_data.csv'))
    actual_input_dim = len(temp_dataset.features)
    
    # Default settings
    solver_to_use = 'rk4' # Switched default to faster solver
    epochs_to_run = 5    # Reduced to 5 to prevent divergence (optimal point was Epoch 5)
    use_sindy_model = True # Default to SINDy for this run
    use_physics_model = False

    # Simple CLI argument parsing
    if len(sys.argv) > 1:
        solver_to_use = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == 'sindy':
            use_sindy_model = True
        elif sys.argv[2].lower() == 'physics':
            use_physics_model = True
    
    print(f"--- Benchmarking Solver: {solver_to_use}, SINDy: {use_sindy_model}, Physics: {use_physics_model} ---")
    start_time = time.time()
    
    train_neural_ode(
        input_dim=actual_input_dim, 
        output_dim=actual_input_dim, 
        epochs=epochs_to_run,
        solver=solver_to_use,
        use_sindy=use_sindy_model,
        use_physics=use_physics_model
    )
    
    end_time = time.time()
    print(f"Training with {solver_to_use} took {end_time - start_time:.2f} seconds.")