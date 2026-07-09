"""
Back of house Flask application.

This serves the BOH dashboard on port 5002. The BOH dashboard is intended for monitoring from a laptop or desktop. 

Responsibilities:
    - Displays current weather data inside and outside the dome.
    - Displays recent weather data in rows.
    - Provides a CSV download of weather data.
    - Displays camera stream/status
"""

from flask import Flask, render_template, jsonify, send_file

from sensor_reader import get_weather_data
from weather_logger import log_file, initialize_log, read_recent_log
from camera_control import camera_on

boh_app = Flask(__name__)

@boh_app.route("/")
def boh_dashboard():
    """
    Renders dashboard.

    Receives current weather data and recent log rows.
    """
    data = get_weather_data()
    initialize_log()
    log_rows = read_recent_log(limit=25)
    return render_template("boh_dashboard.html", data=data, log_rows=log_rows)

@boh_app.route("/api/weather")
def weather_api():
    """
    Returns current weather data as JSON for BOH dashboard.
    """
    data = get_weather_data()
    return jsonify(data)

@boh_app.route("/api/weather-log")
def weather_log_api():
    """
    
    """
    log_rows = read_recent_log(limit=25)
    return jsonify(log_rows)

@boh_app.route("/download/weather-log.csv")
def download_weather_log():
    initialize_log()
    return send_file(log_file, as_attachment=True)

@boh_app.route("/api/camera/status")
def camera_status():
    return jsonify({
        "camera_running": camera_on()
    })

if __name__ == "__main__":
    boh_app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)
    
