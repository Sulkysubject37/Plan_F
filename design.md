# Plan F: Project Architecture & Design Document

## 1. Executive Summary
**Plan F** is an AI-driven race strategy optimization platform designed to simulate Formula 1 race dynamics. By modeling tire degradation, fuel burn, and pace evolution as a continuous-time dynamical system, it provides strategists with "What-If" simulation capabilities (e.g., "What happens if we pit Leclerc for Hards on Lap 20?").

The project leverages **Neural Ordinary Differential Equations (Neural ODEs)** and **Sparse Identification of Nonlinear Dynamics (SINDy)** to learn the governing physics of F1 races directly from telemetry data, offering a superior alternative to traditional discrete-time models.

---

## 2. Core Scientific Approach

### 2.1 The Hypothesis
F1 races are not discrete sequences of steps; they are continuous physical processes.
*   **Traditional AI:** Recurrent Neural Networks (RNNs/LSTMs) predict $t+1$ from $t$. They struggle with irregular time intervals and lacks interpretability.
*   **Plan F Approach:** We model the *rate of change* of the system state $z$ over time:
    $$ \frac{dz}{dt} = f(z, t, \theta) $$
    This allows us to query the system state at *any* continuous time point.

### 2.2 Model Architecture: Augmented SINDy
We utilize a hybrid architecture that combines the flexibility of Neural Networks with the interpretability of Physics:

1.  **State Space ($z$):**
    *   **Observable:** `LapTime`, `GapToWinner`, `TyreLife`, `TireDegradation`, `TyreCompound` (One-Hot), `TrackTemp`.
    *   **Latent (Augmented):** $a_1, a_2$ (Hidden variables representing unmeasured factors like driver confidence or core tire temperature).
2.  **Dynamics Function ($f$):**
    *   Instead of a "Black Box" Neural Network, we use a **SINDy Layer**.
    *   It constructs a library of candidate functions ($\Theta(z) = [1, z, z^2, z \cdot a, ...]$).
    *   It learns a sparse coefficient matrix $\Xi$ to select the active terms.
    *   *Result:* We discovered that Tyre Life evolution is linear (Coefficient ~1.0), while Pace is a complex interaction of Fuel (Time) and Degradation.
3.  **Solver:**
    *   **Runge-Kutta 4 (RK4):** A fixed-step solver chosen for its balance of speed (~80s training time) and stability compared to adaptive solvers like `dopri5`.

---

## 3. System Architecture (Current Research Prototype)

The current repository serves as the "Research Lab" for training and validating models.

### 3.1 Data Pipeline
*   **Ingestion:** `src/ingest.py` fetches telemetry via FastF1 API.
*   **Processing:** `src/preprocess_data.py` cleanses safety car outliers, aligns driver laps, and performs standard scaling (crucial for ODE stability).

### 3.2 Training Pipeline
*   **Trainer:** `src/train_model.py` handles the optimization loop.
*   **Validation:** `src/evaluate_model.py` visualizes predicted trajectories vs. actual race data.

### 3.3 The Simulator
*   **Engine:** `src/what_if_simulator.py`
*   **Function:** Loads the trained `.pth` model, accepts a scenario (Driver, Tyre, Gap), and integrates the ODE forward in time to generate a race forecast.

---

## 4. Deployment Architecture & Design

To transition from a CLI tool to a premium web experience, we will implement a **Hybrid Client-Server Architecture** with a strong focus on high-end aesthetics.

### 4.1 Design & UX Philosophy
*   **Theme:** "Scuderia Noir" - A deep, immersive Black & Red palette inspired by Ferrari's racing heritage but with a modern, digital twist.
*   **Vibe:** Premium, aggressive, and data-rich. Think "Mission Control" meets "Luxury Fashion".
*   **Inspiration:** [landonorris.com](https://landonorris.com) (for the smooth, cinematic feel), but tailored to the technical depth of F1 strategy.
*   **Key Visuals:**
    *   Dark mode by default (OLED Black).
    *   Neon Red accents (`#FF2800`) for critical data points.
    *   Glassmorphism for panels to create depth.
    *   Smooth, physics-based animations for graphs and transitions.

### 4.2 Technical Stack

#### A. The Frontend (React + Vite)
*   **Framework:** React 18 with Vite for lightning-fast builds.
*   **Styling:** Tailwind CSS (v3.4) for utility-first styling, plus custom CSS for complex animations.
*   **Visualization:** Recharts or Visx for high-performance, interactive degradation curves.
*   **State Management:** React Query (TanStack Query) for handling API states.

#### B. The Backend (FastAPI)
*   **Framework:** FastAPI (Python) for high-performance async endpoints.
*   **Inference:** PyTorch (CPU-optimized) to run the Neural ODE models.
*   **API Structure:**
    *   `POST /simulate`: Accepts scenario params, returns time-series data.
    *   `GET /drivers`: Returns available drivers and historical stats.

### 4.3 Architecture Diagram
```mermaid
graph LR
    User[User / Browser] -->|Interacts| UI[React Frontend (Black/Red Theme)]
    UI -->|JSON Request| API[FastAPI Backend]
    API -->|Load Model| Model[Neural ODE (PyTorch)]
    Model -->|Inference| API
    API -->|Simulation Data| UI
```

## 5. Implementation Roadmap

1.  **Backend Core:** Setup FastAPI, create `SimulateRequest` model, and wrap `what_if_simulator.py` logic into an API endpoint.
2.  **Frontend Foundation:** Initialize Vite project, configure Tailwind with "Ferrari" color palette, and build the layout shell.
3.  **Simulation UI:** Create the input form (Driver, Tyre, Laps) and the interactive results chart.
4.  **Polish:** Add micro-interactions, loading states, and responsive design.
