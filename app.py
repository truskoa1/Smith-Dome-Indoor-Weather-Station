from flask import Flask, render_template, jsonify

from sensor_reader import get_weather_data
from camera_control import toggle_stream, camera_on

app = Flask(__name__)

@app.route("/")
def dashboard():
    data = get_weather_data()
    return render_template("dashboard.html", data=data)

@app.route("/api/weather")
def weather_api():
    data = get_weather_data()
    return jsonify(data)

@app.route("/api/camera/toggle", methods=["POST"])
def toggle_camera():
    result = toggle_stream()
    return jsonify(result)

@app.route("/api/camera/status")
def camera_status():
    return jsonify({
        "camera_running": camera_on()
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

