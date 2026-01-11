import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { apiClient } from '../api/client';
import type { GrandPrix } from '../api/types';

const Calendar: React.FC = () => {
    const [calendar, setCalendar] = useState<GrandPrix[]>([]);

    useEffect(() => {
        apiClient.get<GrandPrix[]>('/calendar')
            .then(res => setCalendar(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <Container className="page-container">
             <div className="section-title">
                <h1 className="font-impact display-4">2026 SEASON</h1>
            </div>
            
            <Row>
                {calendar.map((gp) => (
                    <Col md={6} lg={4} key={gp.round} className="mb-4">
                        <Card className="card-custom h-100 border-0 shadow-sm hover-effect" style={{ transition: 'transform 0.2s' }}>
                            <div style={{ height: '150px', overflow: 'hidden', position: 'relative' }}>
                                <img 
                                    src={gp.circuit_image} 
                                    alt={gp.name}
                                    style={{ width: '100%', height: '100%', objectFit: 'contain', padding: '20px', filter: 'invert(1)' }} 
                                />
                                <div style={{ position: 'absolute', top: 10, left: 10, background: '#FF2800', color: 'white', padding: '2px 8px', fontWeight: 'bold', fontSize: '0.8rem' }}>
                                    R{gp.round}
                                </div>
                            </div>
                            <Card.Body>
                                <h5 className="font-impact text-uppercase mb-1">{gp.location}</h5>
                                <p className="text-secondary small mb-2 text-uppercase">{gp.name}</p>
                                <hr style={{ borderColor: '#333' }} />
                                <div className="d-flex justify-content-between align-items-center">
                                    <span className="text-white fw-bold">{gp.date}</span>
                                    <span className={`badge ${gp.is_completed ? 'bg-secondary' : 'bg-danger'}`}>
                                        {gp.is_completed ? 'COMPLETED' : 'UPCOMING'}
                                    </span>
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default Calendar;
