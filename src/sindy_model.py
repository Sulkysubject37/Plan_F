import torch
import torch.nn as nn
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.preprocessing import PolynomialFeatures

class SINDyLayer(nn.Module):
    """
    Sparse Identification of Nonlinear Dynamics (SINDy) Layer.
    
    Instead of a black-box Neural Network, this layer tries to find a sparse
    combination of library functions (polynomials, trig functions) that best
    describe the derivatives dx/dt.
    
    Equation: dx/dt = Theta(x) * Xi
    Where:
    - x is the state
    - Theta(x) is the library of candidate functions (e.g., [1, x, x^2, sin(x)...])
    - Xi is the sparse coefficient matrix we want to learn
    """
    def __init__(self, input_dim, augmented_dim=0, poly_degree=2, threshold=1e-4):
        super(SINDyLayer, self).__init__()
        self.input_dim = input_dim
        self.augmented_dim = augmented_dim
        self.total_dim = input_dim + augmented_dim
        
        self.poly_degree = poly_degree
        self.threshold = threshold
        
        # We'll use sklearn's PolynomialFeatures to generate the library names/indices
        # helping us map the library size.
        self.poly = PolynomialFeatures(degree=poly_degree, include_bias=True)
        
        # Dummy fit to get feature names/count based on TOTAL dimension
        dummy_input = np.zeros((1, self.total_dim))
        self.library_dim = self.poly.fit_transform(dummy_input).shape[1]
        
        # The learnable coefficients (Xi). 
        # Shape: [library_dim, total_dim] (predicts derivative for each state var + aug var)
        self.coefficients = nn.Parameter(torch.randn(self.library_dim, self.total_dim) * 0.001)
        
        # Mask to enforce sparsity (1 means active, 0 means pruned)
        self.register_buffer('mask', torch.ones(self.library_dim, self.total_dim))

    def forward_library(self, x):
        """
        Constructs the library matrix Theta(x) manually using PyTorch operations.
        """
        batch_size = x.shape[0]
        dim = x.shape[1] # Should be self.total_dim
        
        # 1. Constant term
        library = [torch.ones(batch_size, 1).to(x.device)]
        
        # 2. Degree 1 terms (Linear)
        library.append(x)
        
        # 3. Degree 2 terms (Quadratic)
        if self.poly_degree >= 2:
            for i in range(dim):
                for j in range(i, dim):
                    term = (x[:, i] * x[:, j]).unsqueeze(1)
                    library.append(term)
                    
        # Concatenate all terms
        theta = torch.cat(library, dim=1)
        
        # CLAMPING: Prevent exploding values which cause NaN in ODE solvers
        theta = torch.clamp(theta, min=-10.0, max=10.0)
        
        return theta

    def forward(self, t, x):
        # x has shape [batch, total_dim]
        
        # Compute Library Theta(x)
        theta = self.forward_library(x)
        
        # Apply Mask to Coefficients
        active_coeffs = self.coefficients * self.mask
        
        # Compute Derivative: dx/dt = Theta(x) * Xi
        dxdt = torch.matmul(theta, active_coeffs)
        
        return dxdt
    
    def prune(self):
        """
        Updates the mask to zero out coefficients smaller than the threshold.
        Call this periodically during training.
        """
        with torch.no_grad():
            self.mask = (torch.abs(self.coefficients) > self.threshold).float()
            
    def print_equation(self, feature_names):
        """
        Prints the learned differential equations in human-readable format.
        """
        # Get feature names from polynomial features
        lib_names = self.poly.get_feature_names_out(feature_names)
        
        coeffs = (self.coefficients * self.mask).detach().cpu().numpy()
        
        print("\n--- Discovered SINDy Equations ---")
        for i, target_feat in enumerate(feature_names):
            equation = f"d({target_feat})/dt = "
            terms = []
            for j, coef in enumerate(coeffs[:, i]):
                if abs(coef) > 1e-5: # Display non-zero terms
                    terms.append(f"{coef:.4f}*{lib_names[j]}")
            
            if not terms:
                print(f"{equation} 0")
            else:
                print(f"{equation} " + " + ".join(terms))