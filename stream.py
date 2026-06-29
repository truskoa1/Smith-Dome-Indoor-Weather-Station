'''
This code sets up a live video feed. This is the simple case
where both the pi and the local machine are on the same network.
This is just to test that the live feed works, and we will update
the code to work with multiple networks. 
'''

import io
from picamera2 import Picamera2
from flask import Flask, Response
from libcamera import Transform
import time

app = Flask(__name__)

# Initialize camera once
camera = Picamera2()

camera_config = camera.create_video_configuration(
    main={"size": (640, 480)}
)
camera.configure(camera_config)
camera.start()

# Give camera time to warm up
time.sleep(2)


def generate_frames():
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


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)