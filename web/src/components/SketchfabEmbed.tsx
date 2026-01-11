import React from 'react';
import { motion } from 'framer-motion';

interface SketchfabEmbedProps {
    modelId: string;
    title?: string;
}

const SketchfabEmbed: React.FC<SketchfabEmbedProps> = ({ modelId, title = "3D Model" }) => {
    // Construct the Sketchfab embed URL
    // Added autospin=0.2 for rotation and ui_hint=0 to remove the interaction hint
    const embedUrl = `https://sketchfab.com/models/${modelId}/embed?autostart=1&autospin=0.2&ui_controls=0&ui_infos=0&ui_stop=0&ui_help=0&ui_hint=0&ui_theme=dark&background=%23000000`;

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
                pointerEvents: 'none' // Allows interaction with elements behind the iframe
            }}
        >
            <iframe
                title={title}
                frameBorder="0"
                allowFullScreen
                allow="autoplay; fullscreen"
                src={embedUrl}
                style={{ width: '100%', height: '100%', border: 'none' }}
            ></iframe>
        </motion.div>
    );
};

export default SketchfabEmbed;
