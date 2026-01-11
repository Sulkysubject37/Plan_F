import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Story: React.FC = () => {
    return (
        <Container className="page-container">
            <Row className="justify-content-center">
                <Col md={8}>
                    <div className="section-title">
                        <h1 className="font-impact display-4">THE PLAN</h1>
                    </div>
                    
                    <p className="lead text-secondary mb-5">
                        "Plan F" is not just a backup strategy. It is a deterministic approach to chaos.
                    </p>

                    <h3 className="text-white mb-3 font-impact">ORIGIN</h3>
                    <p className="text-secondary mb-5" style={{ lineHeight: '1.8' }}>
                        Formula 1 strategy is often reactive. Teams rely on static tire models that fail to account for
                        complex non-linear dynamics during a race. Plan F utilizes <strong>Neural Ordinary Differential Equations (Neural ODEs)</strong> 
                        to model the continuous evolution of tire degradation and car pace.
                        <br /><br />
                        By learning the underlying physics from historical telemetry data, Plan F can simulate "What If" scenarios
                        with higher fidelity than traditional statistical models.
                    </p>

                    <h3 className="text-white mb-3 font-impact">ARCHITECTURE</h3>
                    <p className="text-secondary mb-5" style={{ lineHeight: '1.8' }}>
                        The system is powered by a Hybrid Neural ODE. It combines a known physical model of tire wear
                        with a neural network that learns the residual dynamics—the "unknown unknowns" of track evolution,
                        driver aggression, and thermal degradation.
                    </p>

                    <div className="p-4 border border-secondary rounded" style={{ background: '#0a0a0a' }}>
                        <h5 className="text-accent font-impact">TECHNOLOGY STACK</h5>
                        <ul className="list-unstyled text-secondary mt-3">
                            <li className="mb-2"><strong>Core:</strong> PyTorch, torchdiffeq</li>
                            <li className="mb-2"><strong>Data:</strong> FastF1 API (Telemetry)</li>
                            <li className="mb-2"><strong>API:</strong> FastAPI</li>
                            <li className="mb-2"><strong>Interface:</strong> React, Recharts</li>
                        </ul>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default Story;
