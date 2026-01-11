export interface GrandPrix {
    round: number;
    name: string;
    location: string;
    date: string;
    circuit_image: string;
    is_completed: boolean;
}

export interface SimulateRequest {
    driver: string;
    compound: 'SOFT' | 'MEDIUM' | 'HARD';
    laps: number;
    life: number;
    gap: number;
    year?: number;
    round?: number;
}

export interface SimulationPoint {
    lap: number;
    lap_time: number;
    tyre_life: number;
    gap_to_leader: number;
}

export interface SimulateResponse {
    driver: string;
    compound: string;
    total_time: number;
    degradation: number;
    data: SimulationPoint[];
}
