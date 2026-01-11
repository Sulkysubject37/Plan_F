import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer: React.FC = () => {
    return (
        <footer style={{ 
            backgroundColor: '#000', 
            color: '#444', 
            padding: '40px 0', 
            marginTop: '50px',
            borderTop: '1px solid #1a1a1a' 
        }}>
            <Container>
                <Row className="align-items-center">
                    <Col md={6} className="text-center text-md-start mb-3 mb-md-0">
                        <h5 className="font-impact text-uppercase text-light mb-0">PLAN F</h5>
                        <small style={{ fontSize: '0.7rem', letterSpacing: '1px' }}>STRATEGY ENGINE</small>
                    </Col>
                    <Col md={6} className="text-center text-md-end">
                        <p className="mb-0 small fw-bold" style={{ color: '#FF2800' }}>
                            &copy; 2025 SulkySubject. All Rights Reserved.
                        </p>
                        <small className="text-muted" style={{ fontSize: '0.7rem' }}>
                            Unofficial Project. Not affiliated with Ferrari S.p.A. or Formula 1.
                        </small>
                    </Col>
                </Row>
            </Container>
        </footer>
    );
};

export default Footer;
