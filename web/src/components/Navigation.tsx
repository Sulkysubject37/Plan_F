import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const Navigation: React.FC = () => {
    const location = useLocation();

    return (
        <Navbar expand="lg" fixed="top" className="navbar-custom" variant="dark">
            <Container>
                <Navbar.Brand as={Link} to="/" className="font-impact text-accent" style={{ fontSize: '1.5rem' }}>
                    PLAN F
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="ms-auto">
                        <Nav.Link as={Link} to="/" active={location.pathname === '/'}>Home</Nav.Link>
                        <Nav.Link as={Link} to="/story" active={location.pathname === '/story'}>Story</Nav.Link>
                        <Nav.Link as={Link} to="/calendar" active={location.pathname === '/calendar'}>Calendar</Nav.Link>
                        <Nav.Link as={Link} to="/simulator" active={location.pathname === '/simulator'} className="text-accent fw-bold">Simulator</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default Navigation;
