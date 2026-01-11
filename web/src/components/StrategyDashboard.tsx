import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Card, Spinner, Alert } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { apiClient } from '../api/client';
import type { GrandPrix, SimulateRequest, SimulateResponse } from '../api/types';

const StrategyDashboard: React.FC = () => {
    const [calendar, setCalendar] = useState<GrandPrix[]>([]);
    const [simulation, setSimulation] = useState<SimulateResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Form State
    const [driver, setDriver] = useState('LEC');
    const [compound, setCompound] = useState<'SOFT' | 'MEDIUM' | 'HARD'>('HARD');
    const [laps, setLaps] = useState(20);
    const [life, setLife] = useState(0);
    const [gap, setGap] = useState(0.0);
    const [selectedRound, setSelectedRound] = useState<number>(24); // Default to Abu Dhabi?

    useEffect(() => {
        fetchCalendar();
    }, []);

    const fetchCalendar = async () => {
        try {
            const response = await apiClient.get<GrandPrix[]>('/calendar');
            setCalendar(response.data);
        } catch (err) {
            console.error("Failed to load calendar", err);
            // Fallback or silent fail
        }
    };

    const handleSimulate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const payload: SimulateRequest = {
            driver,
            compound,
            laps,
            life,
            gap,
            year: 2025, // Assuming we are simulating next season or current
            round: selectedRound
        };

        try {
            const response = await apiClient.post<SimulateResponse>('/simulate', payload);
            setSimulation(response.data);
        } catch (err) {
            setError("Simulation failed. Ensure the backend is running.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container fluid className="p-4 text-light" style={{ backgroundColor: '#121212', minHeight: '100vh' }}>
            <Row className="mb-4">
                <Col>
                    <h1 className="display-4" style={{ fontFamily: 'Impact, sans-serif', color: '#FF2800' }}>
                        PLAN F <span style={{ fontSize: '0.5em', color: '#FFF' }}>STRATEGY SIMULATOR</span>
                    </h1>
                    <p className="lead">Scuderia Ferrari Strategy & Tyre Degradation Analysis</p>
                </Col>
            </Row>

            <Row>
                {/* CONTROLS */}
                <Col md={3}>
                    <Card bg="dark" text="white" className="mb-4 border-danger shadow">
                        <Card.Header style={{ borderBottomColor: '#FF2800' }}>Strategy Configuration</Card.Header>
                        <Card.Body>
                            <Form onSubmit={handleSimulate}>
                                <Form.Group className="mb-3">
                                    <Form.Label>Grand Prix</Form.Label>
                                    <Form.Select 
                                        value={selectedRound} 
                                        onChange={(e) => setSelectedRound(Number(e.target.value))}
                                        className="bg-secondary text-white border-0"
                                    >
                                        {calendar.map((gp) => (
                                            <option key={gp.round} value={gp.round}>
                                                {gp.round}. {gp.location} ({gp.name})
                                            </option>
                                        ))}
                                        {calendar.length === 0 && <option value={24}>24. Abu Dhabi (Default)</option>}
                                    </Form.Select>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Driver</Form.Label>
                                    <Form.Select 
                                        value={driver} 
                                        onChange={(e) => setDriver(e.target.value)}
                                        className="bg-secondary text-white border-0"
                                    >
                                        <option value="LEC">Charles Leclerc (16)</option>
                                        <option value="SAI">Carlos Sainz (55)</option>
                                        <option value="HAM">Lewis Hamilton (44)</option>
                                    </Form.Select>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Tyre Compound</Form.Label>
                                    <div className="d-flex gap-2">
                                        {['SOFT', 'MEDIUM', 'HARD'].map((c) => (
                                            <button 
                                                key={c}
                                                type="button"
                                                className={`flex-fill btn ${compound === c ? (c === 'SOFT' ? 'btn-danger' : c === 'MEDIUM' ? 'btn-warning' : 'btn-light') : 'btn-outline-secondary'}`}
                                                onClick={() => setCompound(c as any)}
                                            >
                                                {c}
                                            </button>
                                        ))}
                                    </div>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Stint Length (Laps): {laps}</Form.Label>
                                    <Form.Range 
                                        min={1} max={60} step={1} 
                                        value={laps} 
                                        onChange={(e) => setLaps(Number(e.target.value))} 
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Used Tyre Life (Laps): {life}</Form.Label>
                                    <Form.Range 
                                        min={0} max={20} step={1} 
                                        value={life} 
                                        onChange={(e) => setLife(Number(e.target.value))} 
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Gap to Leader (s): {gap}</Form.Label>
                                    <Form.Control 
                                        type="number" 
                                        step="0.1" 
                                        value={gap} 
                                        onChange={(e) => setGap(Number(e.target.value))}
                                        className="bg-secondary text-white border-0"
                                    />
                                </Form.Group>

                                <div className="d-grid">
                                    <button 
                                        type="submit" 
                                        disabled={loading} 
                                        className={`btn btn-danger fw-bold ${loading ? 'disabled' : ''}`}
                                    >
                                        {loading ? <Spinner as="span" animation="border" size="sm" /> : 'RUN SIMULATION'}
                                    </button>
                                </div>
                            </Form>
                        </Card.Body>
                    </Card>
                    
                    {simulation && (
                        <Card bg="dark" text="white" className="mb-4 border-danger shadow">
                             <Card.Header style={{ borderBottomColor: '#FF2800' }}>KPIs</Card.Header>
                             <Card.Body>
                                <h6>Total Race Time</h6>
                                <h3 className="text-warning">{simulation.total_time.toFixed(3)} s</h3>
                                <hr className="border-secondary"/>
                                <h6>Total Degradation</h6>
                                <h3 className="text-danger">+{simulation.degradation.toFixed(3)} s</h3>
                             </Card.Body>
                        </Card>
                    )}
                </Col>

                {/* VISUALIZATION */}
                <Col md={9}>
                    {error && <Alert variant="danger">{error}</Alert>}
                    
                    {!simulation && !loading && !error && (
                        <div className="d-flex justify-content-center align-items-center h-100 text-secondary">
                            <h4>Configure simulation parameters and press RUN to see analysis.</h4>
                        </div>
                    )}

                    {simulation && (
                        <>
                            <Card bg="dark" text="white" className="mb-4 shadow border-0">
                                <Card.Body>
                                    <Card.Title>Predicted Pace Evolution</Card.Title>
                                    <div style={{ width: '100%', height: 300 }}>
                                        <ResponsiveContainer>
                                            <LineChart data={simulation.data}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                                                <XAxis dataKey="lap" label={{ value: 'Lap', position: 'insideBottomRight', offset: -5 }} stroke="#ccc" />
                                                <YAxis domain={['auto', 'auto']} label={{ value: 'Lap Time (s)', angle: -90, position: 'insideLeft' }} stroke="#ccc" />
                                                <Tooltip 
                                                    contentStyle={{ backgroundColor: '#333', borderColor: '#FF2800', color: '#FFF' }}
                                                    itemStyle={{ color: '#FFF' }}
                                                />
                                                <Legend />
                                                <ReferenceLine y={simulation.data[0].lap_time} label="Ref" stroke="red" strokeDasharray="3 3" />
                                                <Line 
                                                    type="monotone" 
                                                    dataKey="lap_time" 
                                                    stroke="#FF2800" 
                                                    strokeWidth={3} 
                                                    dot={false} 
                                                    name="Lap Time"
                                                    animationDuration={1500}
                                                />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    </div>
                                </Card.Body>
                            </Card>

                            <Row>
                                <Col md={6}>
                                    <Card bg="dark" text="white" className="mb-4 shadow border-0">
                                        <Card.Body>
                                            <Card.Title>Tyre Life Projection</Card.Title>
                                            <div style={{ width: '100%', height: 250 }}>
                                                <ResponsiveContainer>
                                                    <LineChart data={simulation.data}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                                                        <XAxis dataKey="lap" stroke="#ccc" />
                                                        <YAxis stroke="#ccc" />
                                                        <Tooltip contentStyle={{ backgroundColor: '#333' }} />
                                                        <Line 
                                                            type="monotone" 
                                                            dataKey="tyre_life" 
                                                            stroke="#FFC107" 
                                                            strokeWidth={2} 
                                                            dot={false} 
                                                            name="Tyre Life" 
                                                        />
                                                    </LineChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col md={6}>
                                    <Card bg="dark" text="white" className="mb-4 shadow border-0">
                                        <Card.Body>
                                            <Card.Title>Gap to Leader</Card.Title>
                                            <div style={{ width: '100%', height: 250 }}>
                                                <ResponsiveContainer>
                                                    <LineChart data={simulation.data}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                                                        <XAxis dataKey="lap" stroke="#ccc" />
                                                        <YAxis stroke="#ccc" />
                                                        <Tooltip contentStyle={{ backgroundColor: '#333' }} />
                                                        <Line 
                                                            type="monotone" 
                                                            dataKey="gap_to_leader" 
                                                            stroke="#007bff" 
                                                            strokeWidth={2} 
                                                            dot={false} 
                                                            name="Gap (s)" 
                                                        />
                                                    </LineChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            </Row>
                        </>
                    )}
                </Col>
            </Row>
        </Container>
    );
};

export default StrategyDashboard;
