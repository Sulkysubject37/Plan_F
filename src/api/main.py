import sys
import os
import torch
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List

# Add project root to path to import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Add src directory to path so internal imports in neural_ode_model work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.neural_ode_model import NeuralODE
from src.train_model import F1StrategyDataset
from src.api.schemas import SimulateRequest, SimulateResponse, SimulationPoint
from src.api.data import CALENDAR_2025, GrandPrix

# Global variables for model and dataset
model = None
dataset = None
feature_map = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model and data on startup
    global model, dataset, feature_map
    
    print("Loading Plan F Model...")
    
    # Use absolute paths relative to this file (src/api/main.py)
    # Go up two levels to reach root, then into data/ or models/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    data_path = os.path.join(base_dir, 'data', 'processed_strategy_data.csv')
    model_path = os.path.join(base_dir, 'models', 'neural_ode_strategy_model_rk4_sindy.pth')
    
    print(f"Looking for data at: {data_path}")
    print(f"Looking for model at: {model_path}")
    
    if not os.path.exists(data_path):
        print(f"CRITICAL ERROR: Data not found at {data_path}")
        # In production, we might want to raise an error, but for now let's print
    
    dataset = F1StrategyDataset(data_path)
    input_dim = len(dataset.features)
    aug_dim = 2
    
    model = NeuralODE(input_dim, 64, input_dim, use_sindy=True, augmented_dim=aug_dim).to('cpu')
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        model.eval()
        print("Model loaded successfully.")
    else:
        print(f"WARNING: Model not found at {model_path}")
        
    feature_map = {name: i for i, name in enumerate(dataset.features)}
    yield
    # Clean up if needed

app = FastAPI(title="Plan F Strategy API", lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation Error: {exc.errors()}")
    print(f"Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )

# CORS - Allow all for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Plan F Strategy Engine Online"}

@app.get("/calendar", response_model=List[GrandPrix])
def get_calendar():
    return CALENDAR_2025

@app.post("/simulate", response_model=SimulateResponse)
def simulate_strategy(req: SimulateRequest):
    global model, dataset, feature_map
    
    if model is None or dataset is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 1. Prepare Initial State
    # Fetch historical average lap time if possible
    ref_data = dataset.df[(dataset.df['Year'] == req.year) & (dataset.df['Round'] == req.round) & (dataset.df['Driver'] == req.driver)]
    if not ref_data.empty:
        avg_lap_time = ref_data['LapTime'].median()
    else:
        # Fallback logic based on track/round if available, else generic
        avg_lap_time = 90.0 
        print(f"Warning: No data for {req.driver} at Round {req.round}. Using fallback {avg_lap_time}s")

    x0_real = np.zeros(len(dataset.features))
    
    # Fill features
    x0_real[feature_map['LapTime']] = avg_lap_time
    x0_real[feature_map['GapToWinner']] = req.gap
    x0_real[feature_map['TyreLife']] = req.life
    x0_real[feature_map['TireDegradation']] = 0.0
    x0_real[feature_map['TrackTemp']] = 30.0 # Default track temp
    
    # One-Hot Compound
    if req.compound == 'SOFT':
        x0_real[feature_map['Compound_SOFT']] = 1.0
    elif req.compound == 'MEDIUM':
        x0_real[feature_map['Compound_MEDIUM']] = 1.0
    elif req.compound == 'HARD':
        x0_real[feature_map['Compound_HARD']] = 1.0

    # 2. Scale & Simulate
    x0_scaled = dataset.scaler.transform(x0_real.reshape(1, -1))
    x0_tensor = torch.tensor(x0_scaled, dtype=torch.float32)
    
    t_span = torch.linspace(0, req.laps, req.laps + 1)
    
    with torch.no_grad():
        predicted_scaled = model(x0_tensor, t_span)
        
    # 3. Inverse Transform
    predicted_scaled_np = predicted_scaled.squeeze(1).numpy()
    predicted_real = dataset.scaler.inverse_transform(predicted_scaled_np)
    
    # 4. Format Response
    lap_times = predicted_real[:, feature_map['LapTime']]
    tyre_lives = predicted_real[:, feature_map['TyreLife']]
    gaps = predicted_real[:, feature_map['GapToWinner']]
    
    simulation_points = []
    for i in range(len(t_span)):
        point = SimulationPoint(
            lap=int(i),
            lap_time=float(lap_times[i]),
            tyre_life=float(tyre_lives[i]),
            gap_to_leader=float(gaps[i])
        )
        simulation_points.append(point)

    total_time = float(np.sum(lap_times[1:]))
    degradation = float(lap_times[-1] - lap_times[0])

    return SimulateResponse(
        driver=req.driver,
        compound=req.compound,
        total_time=total_time,
        degradation=degradation,
        data=simulation_points
    )