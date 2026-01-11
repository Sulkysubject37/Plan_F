import React, { useEffect, useRef } from 'react';

const NeuralBackground: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width = window.innerWidth;
        let height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;

        // Particles representing telemetry data
        const particles: { x: number; y: number; speed: number; length: number; opacity: number }[] = [];
        const particleCount = 60;

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                speed: 2 + Math.random() * 15, // Fast speed
                length: 50 + Math.random() * 150, // Long trails
                opacity: 0.1 + Math.random() * 0.3
            });
        }

        const animate = () => {
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, width, height); // Clear with black

            // Draw Grid (Subtle)
            ctx.strokeStyle = 'rgba(255, 40, 0, 0.05)';
            ctx.lineWidth = 1;
            
            // Draw particles (Racing Lines)
            particles.forEach(p => {
                p.y += p.speed;
                
                // Reset if off screen
                if (p.y > height + p.length) {
                    p.y = -p.length;
                    p.x = Math.random() * width;
                }

                const gradient = ctx.createLinearGradient(p.x, p.y, p.x, p.y - p.length);
                gradient.addColorStop(0, `rgba(255, 40, 0, 0)`);
                gradient.addColorStop(0.5, `rgba(255, 40, 0, ${p.opacity})`);
                gradient.addColorStop(1, `rgba(255, 40, 0, 0)`);

                ctx.beginPath();
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 2;
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p.x, p.y - p.length);
                ctx.stroke();
            });

            requestAnimationFrame(animate);
        };

        animate();

        const handleResize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <canvas 
            ref={canvasRef} 
            style={{ 
                position: 'fixed', 
                top: 0, 
                left: 0, 
                zIndex: -1, 
                width: '100vw', 
                height: '100vh',
                background: '#000'
            }} 
        />
    );
};

export default NeuralBackground;
