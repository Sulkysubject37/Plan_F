import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Card, Spinner, Alert } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiClient } from '../api/client';
import type { GrandPrix, SimulateRequest, SimulateResponse } from '../api/types';

const Simulator: React.FC = () => {
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
    const [selectedRound, setSelectedRound] = useState<number>(24); 

    useEffect(() => {
        fetchCalendar();
    }, []);

    const fetchCalendar = async () => {
        try {
            const response = await apiClient.get<GrandPrix[]>('/calendar');
            setCalendar(response.data);
        } catch (err) {
            console.error("Failed to load calendar", err);
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
            year: 2025, 
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
        <Container fluid className="p-4 text-light">
            <Row className="mb-4">
                <Col>
                    <h2 className="font-impact text-uppercase" style={{ color: '#FF2800' }}>
                        Strategy Simulator
                    </h2>
                    <p className="text-secondary">Configure stint parameters and analyze tyre degradation models.</p>
                </Col>
            </Row>

            <Row>
                {/* CONTROLS */}
                <Col md={3}>
                    <Card className="mb-4 card-custom shadow">
                        <Card.Header className="font-impact text-uppercase" style={{ borderBottom: '1px solid #FF2800', color: '#FF2800' }}>
                            Configuration
                        </Card.Header>
                        <Card.Body>
                            <Form onSubmit={handleSimulate}>
                                <Form.Group className="mb-3">
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Grand Prix</Form.Label>
                                    <Form.Select 
                                        value={selectedRound} 
                                        onChange={(e) => setSelectedRound(Number(e.target.value))}
                                        className="bg-dark text-white border-secondary"
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
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Driver</Form.Label>
                                    <Form.Select 
                                        value={driver} 
                                        onChange={(e) => setDriver(e.target.value)}
                                        className="bg-dark text-white border-secondary"
                                    >
                                        <option value="LEC">Charles Leclerc (16)</option>
                                        <option value="SAI">Carlos Sainz (55)</option>
                                        <option value="HAM">Lewis Hamilton (44)</option>
                                    </Form.Select>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Compound</Form.Label>
                                    <div className="d-flex gap-2">
                                        {['SOFT', 'MEDIUM', 'HARD'].map((c) => (
                                            <button 
                                                key={c}
                                                type="button"
                                                className={`flex-fill fw-bold btn btn-sm ${compound === c ? (c === 'SOFT' ? 'btn-danger' : c === 'MEDIUM' ? 'btn-warning' : 'btn-light') : 'btn-outline-secondary'}`}
                                                onClick={() => setCompound(c as any)}
                                            >
                                                {c[0]}
                                            </button>
                                        ))}
                                    </div>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Stint Laps: {laps}</Form.Label>
                                    <Form.Range 
                                        min={1} max={60} step={1} 
                                        value={laps} 
                                        onChange={(e) => setLaps(Number(e.target.value))} 
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Used Life: {life} laps</Form.Label>
                                    <Form.Range 
                                        min={0} max={20} step={1} 
                                        value={life} 
                                        onChange={(e) => setLife(Number(e.target.value))} 
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label className="text-secondary small text-uppercase fw-bold">Gap to Leader: {gap}s</Form.Label>
                                    <Form.Control 
                                        type="number" 
                                        step="0.1" 
                                        value={gap} 
                                        onChange={(e) => setGap(Number(e.target.value))}
                                        className="bg-dark text-white border-secondary"
                                    />
                                </Form.Group>

                                <div className="d-grid mt-4">
                                    <button 
                                        type="submit" 
                                        disabled={loading} 
                                        className={`btn btn-danger font-impact text-uppercase tracking-wider ${loading ? 'disabled' : ''}`}
                                    >
                                        {loading ? <Spinner as="span" animation="border" size="sm" /> : 'Run Simulation'}
                                    </button>
                                </div>
                            </Form>
                        </Card.Body>
                    </Card>
                    
                    {simulation && (
                        <Card className="mb-4 card-custom shadow border-danger">
                             <Card.Body className="text-center">
                                <div className="mb-3">
                                    <small className="text-secondary text-uppercase fw-bold">Total Time</small>
                                    <h2 className="text-white font-impact">{simulation.total_time.toFixed(2)}s</h2>
                                </div>
                                <div>
                                    <small className="text-secondary text-uppercase fw-bold">Degradation</small>
                                    <h2 className="text-danger font-impact">+{simulation.degradation.toFixed(2)}s</h2>
                                </div>
                             </Card.Body>
                        </Card>
                    )}
                </Col>

                {/* VISUALIZATION */}
                <Col md={9}>
                    {error && <Alert variant="danger" className="bg-danger text-white border-0">{error}</Alert>}
                    
                    {!simulation && !loading && !error && (
                        <div className="d-flex justify-content-center align-items-center h-100" style={{ minHeight: '400px', border: '1px dashed #333', borderRadius: '10px' }}>
                            <div className="text-center">
                                <h4 className="text-secondary font-impact opacity-50">Awaiting Input</h4>
                                <p className="text-secondary small">Select parameters to generate strategy models</p>
                            </div>
                        </div>
                    )}

                    {simulation && (
                        <>
                            <Card className="mb-4 card-custom shadow border-0">
                                <Card.Body>
                                    <Card.Title className="text-uppercase fw-bold small text-secondary mb-4">Pace Evolution (Neural ODE)</Card.Title>
                                    <div style={{ width: '100%', height: 400 }}>
                                        <ResponsiveContainer>
                                            <LineChart data={simulation.data}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                                <XAxis dataKey="lap" stroke="#666" tick={{fill: '#666'}} />
                                                <YAxis domain={['auto', 'auto']} stroke="#666" tick={{fill: '#666'}} />
                                                <Tooltip 
                                                    contentStyle={{ backgroundColor: '#000', borderColor: '#333', color: '#FFF' }}
                                                    itemStyle={{ color: '#FFF' }}
                                                    cursor={{ stroke: '#FF2800', strokeWidth: 1 }}
                                                />
                                                <Legend />
                                                <Line 
                                                    type="monotone" 
                                                    dataKey="lap_time" 
                                                    stroke="#FF2800" 
                                                    strokeWidth={3} 
                                                    dot={false} 
                                                    name="Lap Time"
                                                    animationDuration={1000}
                                                />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    </div>
                                </Card.Body>
                            </Card>

                            <Row>
                                <Col md={6}>
                                    <Card className="mb-4 card-custom shadow border-0">
                                        <Card.Body>
                                            <Card.Title className="text-uppercase fw-bold small text-secondary">Tyre Life</Card.Title>
                                            <div style={{ width: '100%', height: 200 }}>
                                                <ResponsiveContainer>
                                                    <LineChart data={simulation.data}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                                        <XAxis dataKey="lap" hide />
                                                        <YAxis hide domain={[0, 100]}/>
                                                        <Tooltip contentStyle={{ backgroundColor: '#000', border: 'none' }} />
                                                        <Line 
                                                            type="monotone" 
                                                            dataKey="tyre_life" 
                                                            stroke="#FFC107" 
                                                            strokeWidth={2} 
                                                            dot={false} 
                                                        />
                                                    </LineChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col md={6}>
                                    <Card className="mb-4 card-custom shadow border-0">
                                        <Card.Body>
                                            <Card.Title className="text-uppercase fw-bold small text-secondary">Gap to Leader</Card.Title>
                                            <div style={{ width: '100%', height: 200 }}>
                                                <ResponsiveContainer>
                                                    <LineChart data={simulation.data}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                                        <XAxis dataKey="lap" hide />
                                                        <YAxis hide />
                                                        <Tooltip contentStyle={{ backgroundColor: '#000', border: 'none' }} />
                                                        <Line 
                                                            type="monotone" 
                                                            dataKey="gap_to_leader" 
                                                            stroke="#0d6efd" 
                                                            strokeWidth={2} 
                                                            dot={false} 
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

export default Simulator;
