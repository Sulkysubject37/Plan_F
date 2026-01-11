import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF, Stage, OrbitControls } from '@react-three/drei';
import { motion } from 'framer-motion';

const Model = () => {
    // Construct path handling the base URL for GitHub Pages
    const baseUrl = import.meta.env.BASE_URL;
    const modelPath = `${baseUrl}sf25.glb`.replace(/\/\//g, '/'); 
    
    const { scene } = useGLTF(modelPath);
    return <primitive object={scene} />;
};

const FerrariModel: React.FC = () => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                zIndex: 0,
            }}
        >
            <Canvas shadows dpr={[1, 2]} camera={{ fov: 45 }} gl={{ alpha: true }}>
                <Suspense fallback={null}>
                    <Stage environment="city" intensity={0.5} adjustCamera={1.2}>
                        <Model />
                    </Stage>
                    <OrbitControls 
                        autoRotate 
                        autoRotateSpeed={1.0} 
                        enableZoom={false} 
                        enablePan={false}
                        minPolarAngle={Math.PI / 3}
                        maxPolarAngle={Math.PI / 2}
                    />
                </Suspense>
            </Canvas>
        </motion.div>
    );
};

export default FerrariModel;
