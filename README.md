---
title: "Plan F: Neural ODE Strategy Engine"
emoji: "🏎️"
colorFrom: "red"
colorTo: "yellow"
sdk: docker
app_port: 7860
---

# Plan F: Neural ODE Strategy Engine

**Plan F** is a race strategy simulation engine designed to model Formula 1 race dynamics using **Neural Ordinary Differential Equations (Neural ODEs)**. 

Unlike traditional static models, Plan F learns the continuous physics of tire degradation, fuel burn, and pace evolution directly from telemetry data, allowing for dynamic "What-If" scenario modeling.

## Project Architecture

1.  **Data Ingestion (`src/ingest`)**: 
    - Fetches telemetry using `fastf1`.
    - Preprocesses sector times, tyre compounds, and gaps.
2.  **The Neural ODE Core (`src/model`)**: 
    - Models the derivative of pace and tire health: $dz/dt = f(z, t)$.
    - Learns non-linear degradation curves ("the cliff").
3.  **Scenario Engine (`src/strategy`)**: 
    - Simulates events (Pit Stops, Safety Cars, Undercuts).
    - Solves the initial value problem for various strategic decisions.

## Getting Started

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```