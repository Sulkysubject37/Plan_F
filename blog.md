# Plan F: F1 Strategy Optimization with Neural ODEs & SINDy

## 1. Project Overview
**Goal:** Develop an AI-powered race strategy simulator for Ferrari (Plan F) that predicts tire degradation, pace evolution, and optimal pit windows using data-driven differential equations.

**Core Hypothesis:** F1 races are continuous-time dynamical systems. Instead of discrete time-step models (like RNNs/LSTMs), **Neural Ordinary Differential Equations (Neural ODEs)** can better model the continuous evolution of tire wear and fuel load, while **SINDy (Sparse Identification of Nonlinear Dynamics)** can extract interpretable governing equations (e.g., "Pace drops by 0.1s per lap after lap 15").

## 2. Data Pipeline
### Ingestion (`src/ingest.py`)
- **Source:** FastF1 API (Live Timing & Telemetry data).
- **Scope:** 2024-2025 Seasons (Completed races).
- **Features:** LapTime, Sector Times, Tyre Compound, Tyre Life, Track Temp, Gap to Leader.
- **Processing:** 
    - Bypasses Ergast API (often down) by using direct session loading.
    - Alignment of laps between drivers to calculate relative gaps.

### Preprocessing (`src/preprocess_data.py`)
- **Cleaning:** Drops outliers (Safety Car laps, In/Out laps).
- **Feature Engineering:**
    - `TireDegradation`: Rate of pace change within a stint.
    - `GapToWinner`: Relative performance metric.
    - Scaling: Standard scaling (Mean 0, Std 1) is critical for Neural ODE stability.

## 3. Modeling Approaches
We explored three distinct architectures to model the race dynamics $ \frac{dz}{dt} = f(z, t) $.

### A. Pure Neural ODE (`src/neural_ode_model.py`)
- **Concept:** $f(z, t)$ is a black-box Neural Network (MLP).
- **Solver:** Tested `dopri5` (adaptive, slow) and `rk4` (fixed-step, fast).
- **Results:**
    - **Loss:** ~1.13 (MSE).
    - **Pros:** Flexible, learns any function.
    - **Cons:** "Black box" (uninterpretable), prone to overfitting noise.

### B. Physics-Guided ODE
- **Concept:** Hard-coded known physics (e.g., $\frac{d(\text{TyreLife})}{dt} = 1$) and learned the rest.
- **Results:** **Failed (Loss ~137)** due to unit mismatch.
    - *Issue:* Hard-coded derivatives were in real units (laps), but the model operates in scaled space (sigma).
    - *Lesson:* Physics constraints must be normalized to the data scale.

### C. SINDy (Sparse Identification of Nonlinear Dynamics) (`src/sindy_model.py`)
- **Concept:** $f(z, t) = \Theta(z) \cdot \Xi$
    - $\Theta(z)$: Library of candidate functions ($1, z, z^2, \sin(z)$).
    - $\Xi$: Sparse coefficient matrix learned via sparse regression/pruning.
- **Innovation:** Replaced the black-box MLP with a `SINDyLayer` that learns the *coefficients* of the differential equation.
- **Results:**
    - **Loss:** ~0.86 (Best so far).
    - **Issues:** Initial pruning threshold was too aggressive ($0.1$), killing all learning. Lowering to $10^{-4}$ fixed it.
    - **Pros:** Interpretable equations, lower loss.

## 4. Optimization Steps
1.  **Solver Switch:** Moved from `dopri5` (300s+) to `rk4` (~80s) for 4x speedup with minimal accuracy loss.
2.  **Stability Fixes:**
    - **Clamping:** Restricted polynomial features to $[-10, 10]$ to prevent `NaN` explosions.
    - **Gradient Clipping:** Added to `train_model.py` to stabilize training.
    - **Initialization:** Reduced weight variance to $0.001$ for SINDy stability.

## 5. Current Frontier: Augmented SINDy
**Objective:** Combine the interpretability of SINDy with the flexibility of Augmented Neural ODEs.
- **Method:** Add "dummy" dimensions ($a_1, a_2$) to the state space.
- **Equation:** $\frac{d[x, a]}{dt} = \Theta([x, a]) \cdot \Xi$
- **Benefit:** Allows the model to learn latent variables (like "Driver Confidence" or "Tire Core Temp") that aren't in the dataset but affect the dynamics.
- **Training Run (5 Epochs):**
    - **Final Loss:** ~0.705.
    - **Equations:** Successfully learned dynamics for real + augmented variables.

## 6. The "What-If" Simulator (`src/what_if_simulator.py`)
We built a CLI tool to predict future race outcomes using the trained Augmented SINDy model.

**Scenario 1: Leclerc (LEC) on fresh HARD tyres, 5s behind leader (Round 1, 2024)**
- **Input:** `--driver LEC --compound HARD --laps 15 --life 0 --gap 5.0 --year 2024 --round 1`
- **Prediction (15 Laps):**
    - **Tyre Life:** Correctly evolved from 0.0 to 13.3 laps (Model learned physics!).
    - **Pace:** Improved from 96.8s to 91.0s (Capturing fuel burn effect).
    - **Gap:** Widened from 5.0s to 25.9s (Predicting pace deficit to leader).

**Scenario 2: Hamilton (HAM) on fresh MEDIUM tyres, 0s behind leader (Round 19, 2024 - Qatar GP)**
- **Input:** `--driver HAM --compound MEDIUM --laps 20 --life 0 --gap 0.0 --year 2024 --round 19`
- **Prediction (20 Laps):**
    - **Tyre Life:** Progressed from 0.0 to 11.5 laps.
    - **Pace:** Lap times decreased from 108.064s to 93.707s.
    - **Gap:** Initially closed to -0.962s (briefly faster), then steadily widened to 11.887s (losing time to median pace).
- **Interpretation:** This simulation shows a plausible race stint where initial pace improvement from cold tires / fuel burn allows HAM to briefly gain, before the underlying pace deficit to the median reference widens the gap.

**Conclusion:** The Augmented SINDy model provides a viable prototype for strategy simulation, capturing key F1 dynamics and offering insights into potential race outcomes.

---
*Last Updated: Wednesday, 26 November 2025*
