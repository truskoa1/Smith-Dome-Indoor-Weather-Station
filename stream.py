"""
Camera stream server.

This file runs a Flask app on port 5000 and serves a live MJPEG stream from the Raspberry Pi camera at
/video_feed. It is intended to run as a systemd service named camera-stream.service.

Main routes:
    /               Basic JSON status endpoint
    /health         Endpoint used to verify stream server is running
    /video_feed     MJPEG stream endpoint used by BOH dashboard
"""

import io
from picamera2 import Picamera2
from flask import Flask, Response, jsonify
import time

app = Flask(__name__)


camera = None

def initialize_cam():
    """
    Initialize and return the Pi camera.

    Returns:
        Picamera2:
            Initialized camera object
    """
    global camera 

    if camera is not None:
        return camera
    
    camera = Picamera2()
    camera_config = camera.create_video_configuration(
    main={"size": (640, 480)}
    )
    camera.configure(camera_config)
    camera.start()
    # Give camera time to warm up
    time.sleep(2)

    return camera

def generate_frames():
    """
    Continuously capture frames.

    Yields: 
        bytes:
            JPEG frame data formatted for a multipart MJPEG HTTP response.
    
    Loop runs continuously when a client is connected to /video_feed.
    """
    camera = initialize_cam()
    stream = io.BytesIO()

    while True:
        # Capture JPEG directly into memory
        stream.seek(0)
        stream.truncate()

        camera.capture_file(stream, format="jpeg")

        stream.seek(0)
        frame = stream.read()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

@app.route("/")
def index():
    """
    Returns basic JSON status for the camera stream service. 
    """
    return jsonify({
        "service": "camera-stream",
        "status": "running",
        "video_feed": "/video_feed"
    })

@app.route("/health")
def health():
    """
    Returns a health-check response.
    """
    return jsonify({
        "camera_stream": "running"
    })

@app.route("/video_feed")
def video_feed():
    """
    Returns the live MJPEG camera stream.
    """
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)