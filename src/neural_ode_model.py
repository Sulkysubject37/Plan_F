import torch
import torch.nn as nn
from torchdiffeq import odeint_adjoint as odeint # or odeint for non-adjoint
import numpy as np
from sindy_model import SINDyLayer # Import the new SINDy module

# 1. Define the ODE Function (the Neural Network predicting the derivative)
class ODEFunc(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ODEFunc, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, output_dim)
        )
        # Initialize weights
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.1)
                nn.init.constant_(m.bias, val=0)

    def forward(self, t, x):
        return self.net(x)

class PhysicsGuidedODEFunc(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(PhysicsGuidedODEFunc, self).__init__()
        self.input_dim = input_dim
        # The NN predicts all derivatives initially, but we will overwrite known ones
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, output_dim)
        )
        # Initialize weights
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.01) # Smaller init for stability
                nn.init.constant_(m.bias, val=0)

    def forward(self, t, x):
        # Get NN predictions for all states
        dxdt = self.net(x)
        
        # --- PHYSICS OVERRIDES ---
        # We know TyreLife (index 2) increases by 1 lap per lap time unit (if time is laps)
        # The integration_times are lap differences, so d(TyreLife)/dt should be exactly 1.
        
        # Create a mask to separate learned vs fixed derivatives
        # Clone to avoid in-place modification errors in autograd
        dxdt_constrained = dxdt.clone()
        
        # Index 2 is TyreLife
        dxdt_constrained[:, 2] = 1.0
        
        # Index 4,5,6 are One-Hot Compounds (SOFT, MEDIUM, HARD)
        # These should NOT change during a stint (derivative = 0)
        dxdt_constrained[:, 4] = 0.0
        dxdt_constrained[:, 5] = 0.0
        dxdt_constrained[:, 6] = 0.0
        
        # Index 7 is TrackTemp (External factor, hard to predict, but let's assume constant for short term)
        # Or let the NN learn the drift. Let's keep it learned for now.
        
        return dxdt_constrained

# 2. Define the Neural ODE Model
class NeuralODE(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, ode_solver='dopri5', use_sindy=False, use_physics=False, augmented_dim=0):
        super(NeuralODE, self).__init__()
        self.augmented_dim = augmented_dim
        
        if use_sindy:
            self.ode_func = SINDyLayer(input_dim, augmented_dim=augmented_dim)
        elif use_physics:
            self.ode_func = PhysicsGuidedODEFunc(input_dim, hidden_dim, output_dim)
        else:
            self.ode_func = ODEFunc(input_dim + augmented_dim, hidden_dim, output_dim + augmented_dim)
            
        self.ode_solver = ode_solver
        self.integration_times = None # Will be set during forward pass

    def forward(self, x0, integration_times):
        # x0: initial state [batch_size, input_dim]
        
        # AUGMENTATION: Add zeros to the state if requested
        if self.augmented_dim > 0:
            batch_size = x0.shape[0]
            aug = torch.zeros(batch_size, self.augmented_dim).to(x0.device)
            x0_aug = torch.cat([x0, aug], dim=1)
        else:
            x0_aug = x0
        
        # odeint_adjoint is for backpropagation through the ODE solver
        pred_z_aug = odeint(self.ode_func, x0_aug, integration_times, method=self.ode_solver)
        
        # Slice off the augmented dimensions from the output
        if self.augmented_dim > 0:
            pred_z = pred_z_aug[:, :, :-self.augmented_dim]
        else:
            pred_z = pred_z_aug
            
        return pred_z

# Example Usage (for testing the module)
if __name__ == "__main__":
    # Define state vector components (adjust based on your preprocessed data features)
    # Example state: [LapTime, GapToWinner, TyreLife, Compound_SOFT, Compound_MEDIUM, Compound_HARD, TrackTemp]
    # Let's say input_dim is the size of this state vector
    input_dim = 10 # Corresponds to the 10 features extracted in preprocess_data.py
                   # LapTime, GapToWinner, TyreLife, Stint, StintLap, TireDegradation,
                   # Compound_SOFT, Compound_MEDIUM, Compound_HARD, TrackTemp

    hidden_dim = 64 # Size of the hidden layers in the ODEFunc network
    output_dim = input_dim # The ODEFunc predicts the derivative of each state component

    # Instantiate the Neural ODE model
    model = NeuralODE(input_dim, hidden_dim, output_dim)

    # Create a dummy initial state (x0) and integration times
    # Batch size of 1 for demonstration
    x0 = torch.randn(1, input_dim) # Random initial state for one sample
    
    # Simulate integration over 5 time steps (e.g., 5 laps)
    # Times should be increasing and correspond to actual lap numbers or time deltas
    integration_times = torch.linspace(0., 4., 5) # From lap 0 to lap 4

    print(f"Initial state (x0) shape: {x0.shape}")
    print(f"Integration times shape: {integration_times.shape}")

    # Forward pass
    predicted_states = model(x0, integration_times)

    print(f"Predicted states shape: {predicted_states.shape}")
    print("Predicted states (first sample, first few timesteps):")
    print(predicted_states[:, 0, :].detach().numpy()) # Print for the first batch item
