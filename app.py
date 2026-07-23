"""
This is the FOH Flask application for the Smith Dome indoor weather station. This serves the touchscreen
display, exposing the API routes utilized by dashboard.js. The browser loads dashboard.html once, then 
JavaScript periodically requests updated weather, camera, and alert data from the API routes defined here.

Routes:
    /                       Main dashboard page
    /api/weather            Current weather data
    /api/camera/status      Camera stream status
    /api/camera/toggle      Start/stop camera stream
    /api/alerts             Current alert state
    /api/alerts/snooze      Snooze caution condition warnings


app.py is a coordinator script, not necessarily a logic file.       
"""


from flask import Flask, render_template, jsonify, Response

from sensor_reader import get_weather_data
from camera_control import toggle_stream, camera_on
from weather_warnings import evaluate_warnings, snooze_warning
from mqtt_client import get_allsky_status, get_latest_image

app = Flask(__name__)

@app.route("/")
def dashboard():
    """
    Renders the main FOH touchscreen dashboard.

    Initial weather data gets passed into dashboard.html so there is immediately data when the page loads. 
    After loading, dashboard.js updates the values via repeated API calls. 
    """
    data = get_weather_data()
    return render_template("dashboard.html", data=data)

@app.route("/api/weather")
def weather_api():
    """
    Returns current weather data as JSON.

    Polled by dashboard.js so the FOH updates without refreshing the entire page.
    """
    data = get_weather_data()
    return jsonify(data)

@app.route("/api/camera/status")
def camera_status():
    """
    Return whether the camera stream is currently active. 

    The frontend uses this to display "Start/stop camera".
    """
    return jsonify({
        "camera_running": camera_on()
    })

@app.route("/api/camera/toggle", methods=["POST"])
def toggle_camera():
    """
    Start or stop camera stream.

    This route changes a state, so it utilizes "POST". The frontend calls this when a user presses the "Start/stop camera" button.
    """
    result = toggle_stream()
    return jsonify(result)

@app.route("/api/alerts")
def alerts_api():
    """
    Returns current alert state as JSON.

    Weather data is recorded in sensor_reader.py, alert state is evaluated in weather_warnings.py. dashboard.js uses
    this to update the alert banner and background color.
    """
    data = get_weather_data()
    alert = evaluate_warnings(data)
    return jsonify(alert)

@app.route("/api/alerts/snooze", methods=["POST"])
def snooze_alert():
    """
        Snoozes current caution alert.

        Utilizes "POST" because it changes a backend state (updates snooze expiration time). Danger and unknown alerts
        are not snoozable in the frontend.
    """
    result = snooze_warning(minutes=15)
    return jsonify(result)

@app.route("/api/allsky/latest.jpg")
def latest_view():
    view = get_latest_image()
    if view is None:
        return jsonify({"error": "Image not available"}), 404
    
    return Response(view, mimetype="image/jpeg")

@app.route("/api/allsky/status")
def allsky_status():
    status = get_allsky_status()

    return jsonify(status)


if __name__ == "__main__":
    """
    host="0.0.0.0" allows the dashboard to be accessed by devices on the same network. Assuming there isn't something like
    OSU WiFi blocking device-to-device traffic :/
    """
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

