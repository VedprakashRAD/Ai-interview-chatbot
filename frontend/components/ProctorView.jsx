import React, { useEffect, useRef, useState } from 'react';

const ProctorView = ({ candidateId }) => {
    const videoRef1 = useRef(null);
    const videoRef2 = useRef(null);
    const [warningCount, setWarningCount] = useState(0);
    const [wsConnection, setWsConnection] = useState(null);

    useEffect(() => {
        // Initialize cameras
        const initializeCameras = async () => {
            try {
                const streams = await Promise.all([
                    navigator.mediaDevices.getUserMedia({ video: true }),
                    navigator.mediaDevices.getUserMedia({ video: true })
                ]);

                videoRef1.current.srcObject = streams[0];
                videoRef2.current.srcObject = streams[1];

                // Start proctoring session
                await fetch(`/api/proctor/start/${candidateId}`, {
                    method: 'POST'
                });

                // Initialize WebSocket connection
                const ws = new WebSocket(`ws://localhost:8001/api/proctor/ws/${candidateId}`);
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    setWarningCount(data.warning_count);
                    
                    if (data.warning_count >= data.max_warnings) {
                        alert("Test auto-submitted due to multiple violations. Please contact test admin.");
                        window.location.href = "/test-completed";
                    }
                };
                setWsConnection(ws);
            } catch (error) {
                console.error("Error initializing cameras:", error);
                alert("Failed to initialize cameras. Please check camera permissions.");
            }
        };

        initializeCameras();

        return () => {
            // Cleanup
            if (wsConnection) {
                wsConnection.close();
            }
            fetch('/api/proctor/stop', { method: 'POST' });
        };
    }, [candidateId]);

    return (
        <div className="proctor-view">
            <div className="camera-feeds">
                <video
                    ref={videoRef1}
                    autoPlay
                    playsInline
                    muted
                    className="camera-feed"
                />
                <video
                    ref={videoRef2}
                    autoPlay
                    playsInline
                    muted
                    className="camera-feed"
                />
            </div>
            {warningCount > 0 && (
                <div className="warning-message">
                    Warning {warningCount}/3: Violation detected
                </div>
            )}
        </div>
    );
};

export default ProctorView; 