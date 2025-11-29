from pydantic import BaseModel
from typing import List, Optional

class SimulateRequest(BaseModel):
    driver: str = "LEC"
    compound: str = "HARD"
    laps: int = 20
    life: int = 0
    gap: float = 0.0
    year: int = 2024
    round: Optional[int] = 24

class SimulationPoint(BaseModel):
    lap: int
    lap_time: float
    tyre_life: float
    gap_to_leader: float

class SimulateResponse(BaseModel):
    driver: str
    compound: str
    total_time: float
    degradation: float
    data: List[SimulationPoint]
