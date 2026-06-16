from flask import Flask, render_template, jsonify

from sensor_reader import get_weather_data


app = Flask(__name__)

@app.route("/")
def dashboard():
    data = get_weather_data()
    return render_template("dashboard.html", data=data)

@app.route("/api/weather")
def weather_api():
    data = get_weather_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)