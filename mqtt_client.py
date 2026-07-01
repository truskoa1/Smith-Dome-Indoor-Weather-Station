import json

import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
TOPIC = "weather_outside"

outside_weather = {
    "temperature_c": "--",
    "temperature_f": "--",
    "pressure_hpa": "--",
    "timestamp_utc": "--",
    "status": "waiting"
}


