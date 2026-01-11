import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaFlagCheckered, FaCalendarAlt, FaBookOpen } from 'react-icons/fa';
import NeuralBackground from '../components/NeuralBackground';
import FerrariModel from '../components/FerrariModel';

const Home: React.FC = () => {
    const [terminalInput, setTerminalInput] = useState('echo "Ferrari strategy sucks. We built our own."');
    const [showModel, setShowModel] = useState(false);

    // Delay loading the heavy 3D model slightly to allow initial UI paint
    useEffect(() => {
        const timer = setTimeout(() => setShowModel(true), 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="d-flex align-items-center position-relative" style={{ minHeight: '100vh', overflow: 'hidden' }}>
            <NeuralBackground />
            
            {/* Local 3D Model */}
            {showModel && <FerrariModel />}
            
            <Container style={{ zIndex: 10, paddingTop: '80px', position: 'relative' }}>
                <Row className="align-items-center">
                    <Col lg={8} className="mb-5 mb-lg-0">
                        <motion.div
                            initial={{ opacity: 0, x: -100 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8, ease: "easeOut" }}
                        >
                            {/* Massive Background Text Effect */}
                            <h1 className="font-impact text-uppercase" 
                                style={{ 
                                    fontSize: '12rem', 
                                    lineHeight: 0.8, 
                                    color: 'transparent', 
                                    WebkitTextStroke: '2px rgba(255, 255, 255, 0.1)',
                                    position: 'absolute',
                                    top: '-150px',
                                    left: '-50px',
                                    zIndex: -1,
                                    userSelect: 'none',
                                    pointerEvents: 'none'
                                }}>
                                PLAN F
                            </h1>

                            {/* Foreground Main Title */}
                            <h1 className="font-impact text-uppercase display-1 mb-0" style={{ color: '#FFF', letterSpacing: '-2px' }}>
                                PLAN <span className="text-accent glitch-text">F</span>
                            </h1>
                            
                            <div className="mt-4 mb-5 ps-4" style={{ borderLeft: '4px solid #FF2800' }}>
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.5, duration: 0.8 }}
                                >
                                    <h3 className="text-uppercase fw-bold text-white mb-0" style={{ letterSpacing: '2px' }}>
                                        BECAUSE WE'RE TIRED OF WAITING
                                    </h3>
                                    <h3 className="text-uppercase fw-bold mb-4" style={{ letterSpacing: '2px', color: '#FF2800' }}>
                                        FOR THE PIT WALL.
                                    </h3>
                                    
                                    {/* Interactive Terminal */}
                                    <div className="p-3" style={{ background: 'rgba(10, 10, 10, 0.8)', border: '1px solid rgba(255, 40, 0, 0.3)', boxShadow: '0 0 10px rgba(255, 40, 0, 0.1)' }}>
                                        <div className="d-flex align-items-center font-monospace" style={{ fontSize: '1rem' }}>
                                            <span className="text-danger me-2 fw-bold select-none">root@scuderia:~$</span>
                                            <Form.Control 
                                                type="text" 
                                                value={terminalInput}
                                                onChange={(e) => setTerminalInput(e.target.value)}
                                                className="bg-transparent border-0 text-light p-0 shadow-none"
                                                style={{ fontFamily: 'monospace', caretColor: '#FF2800', width: '100%' }}
                                                spellCheck={false}
                                            />
                                        </div>
                                    </div>
                                </motion.div>
                            </div>
                        </motion.div>
                    </Col>

                    <Col lg={4}>
                        <div className="d-grid gap-4">
                            <NavButton 
                                to="/simulator" 
                                title="LAUNCH SIM" 
                                subtitle="Neural ODE Engine" 
                                icon={<FaFlagCheckered />} 
                                delay={0.8} 
                                accent
                            />
                            <NavButton 
                                to="/calendar" 
                                title="2025 CALENDAR" 
                                subtitle="Current Season" 
                                icon={<FaCalendarAlt />} 
                                delay={1.0} 
                            />
                            <NavButton 
                                to="/story" 
                                title="THE STORY" 
                                subtitle="Technical Deep Dive" 
                                icon={<FaBookOpen />} 
                                delay={1.2} 
                            />
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

interface NavButtonProps {
    to: string;
    title: string;
    subtitle: string;
    icon: React.ReactNode;
    delay: number;
    accent?: boolean;
}

const NavButton: React.FC<NavButtonProps> = ({ to, title, subtitle, icon, delay, accent }) => {
    return (
        <Link to={to} style={{ textDecoration: 'none' }}>
            <motion.div 
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: delay, duration: 0.5 }}
                whileHover={{ x: -10, backgroundColor: accent ? '#FF2800' : 'rgba(255,255,255,0.1)' }}
                className={`p-4 d-flex align-items-center justify-content-between ${accent ? 'bg-danger' : ''}`}
                style={{ 
                    border: '1px solid rgba(255,255,255,0.2)', 
                    background: accent ? '#FF2800' : 'rgba(0,0,0,0.6)',
                    backdropFilter: 'blur(5px)',
                    cursor: 'pointer'
                }}
            >
                <div>
                    <h4 className="font-impact mb-0 text-white" style={{ letterSpacing: '1px' }}>{title}</h4>
                    <small className={accent ? 'text-black fw-bold' : 'text-secondary'}>{subtitle}</small>
                </div>
                <div style={{ fontSize: '2rem', color: accent ? '#000' : '#FFF', opacity: 0.8 }}>
                    {icon}
                </div>
            </motion.div>
        </Link>
    );
};

export default Home;
