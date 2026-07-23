import paho.mqtt.client as mqtt
import json
import sys
import threading
from astropy.time import Time
from zoneinfo import ZoneInfo   
# DEBUG ONLY:
from io import BytesIO
from PIL import Image

# new packages: paho-mqqt, pillow
# NOTE: Should not need pillow if we are just bouncing raw jpeg data
# to web clients! Only use it for debugging. Don't include in final
# python venv.

# LOAD CONFIG
try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    print("config.json not found. Exiting.")
    sys.exit(1)

MQTT_HOST = config["mqtt"]["host"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_USERNAME = config["mqtt"]["username"]
MQTT_PASSWORD = config["mqtt"]["password"]

latest_image_bytes = None
latest_image_received = None
latest_data = {}
# thread lock for data dictionary. prevents weird race conditions
# with multiple threads trying to access data
image_lock = threading.Lock()
data_lock = threading.Lock()

TEMP_C_TOPIC = "indi-allsky/sensor_user_20"
HUMIDITY_TOPIC = "indi-allsky/sensor_user_21"
PRESSURE_TOPIC = "indi-allsky/sensor_user_22"

EASTERN_TIMEZONE = ZoneInfo("America/New_York")

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe("indi-allsky/sensor_temp_0") # camera temp (c)
    client.subscribe("indi-allsky/sensor_user_1") # dew heater level
    client.subscribe("indi-allsky/sensor_user_4") # fan level pwm
    client.subscribe("indi-allsky/sensor_user_10") # dht11 temp (c)
    client.subscribe("indi-allsky/sensor_user_11") # dht11 rh (%)
    client.subscribe("indi-allsky/sensor_user_12") # dht11 calculated dew point
    client.subscribe("indi-allsky/sensor_user_20") # bme280 temp (c)
    client.subscribe("indi-allsky/sensor_user_21") # bme280 rh (%)
    client.subscribe("indi-allsky/sensor_user_22") # bme280 pressure (hP)
    client.subscribe("indi-allsky/sensor_user_23") # bme280 calculated dew point
    # all sky image
    client.subscribe("indi-allsky/exposure") # all sky image exposure time (s)
    # NOTE: I currently have the Exposure Period (Day) set to 10 seconds in the Camera tab
    # of INDI allsky. Expect new images every 10 seconds during the day, and 15 seconds
    # during the night. DON'T SAVE THESE IMAGES. indi-allsky saves the images automatically
    # and backs them up to a remote server. Only use this if you want to show the image 
    # in the 
    client.subscribe("indi-allsky/latest")

def on_message(client, userdata, msg):
    """ DEBUG FUNCTION - REPLACE WITH FUNCTION TO SAVE DATA IN DB """
    # check if the incoming data is an image or text data
    # NOTE: image data is in raw jpeg format
    global latest_image_bytes
    global latest_data
    global latest_image_received

    if msg.topic == "indi-allsky/latest":
        # TODO: Remove these 3 lines as this opens the image in a window. Don't decode the
        # raw image data, just save it and send it straight to web clients
        # Keeping these comments here so you can debug!
        #img = Image.open(BytesIO(msg.payload))
        #print(f"Got image: {img.size}, format={img.format}")
        #img.show("latest.jpg")

        # Use this if you use the flask route below to send latest all sky image data
        with image_lock: 
            latest_image_bytes = msg.payload
            latest_image_received = view_timestamp()
    else:
        with data_lock:
            # TODO: can remove this debug print statement
            print(f"{msg.topic}: {msg.payload.decode()}")
            # save data to latest data global
            latest_data[msg.topic] = msg.payload.decode()

def get_latest_image():
    with image_lock:
        view = latest_image_bytes
    
    return view

def get_allsky_status():
    with image_lock:
        if latest_image_bytes is None or latest_image_received is None:
            image_available = False
            timestamp = "No image received."
        else:
            image_available = True
            timestamp = latest_image_received
    return {
        "image_available": image_available,
        "last_image_received": timestamp
    }

def outside_weather_data():
    with data_lock:
        temp_c = latest_data.get(TEMP_C_TOPIC)
        humidity = latest_data.get(HUMIDITY_TOPIC)
        pressure = latest_data.get(PRESSURE_TOPIC)
    
    return {
        "temperature_c": temp_c,
        "humidity": humidity,
        "pressure_hpa": pressure
    }


def view_timestamp(time=None):
    """
    Returns a timestamp. ISO format, EST/EDT depending on date.

    Args:
        time (astropy.time.Time or None):
            Astropy Time object. If None, current time is used.

    Returns:
        str : 
            Timestamp formatted for EST/EDT (24-hour time)
                ex: "2026-07-09 12:20:18 EDT"
    """

    if time is None:
        time = Time.now()

    eastern_datetime = time.to_datetime(timezone=EASTERN_TIMEZONE)

    return eastern_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

# TODO: CHANGE THIS IN PROD
# NOTE: use loop_forever() if not running in flask server!
# loop_start() will NOT block flash thread
# this may need testing though
mqtt_client.loop_start()

"""
Example Flask route to send latest all sky image data as jpeg image
NOTE: We should replace the poll loop in the web client with websocket
transport when new data is received in the flask server. Use this for
testing only.

from flask import Response, jsonify

@app.route("/latest.jpg")
def latest_image():
    with image_lock:
        if latest_image_bytes is None:
            # Return 404 not found if no image is available
            return jsonify({"error": "Image not available"}), 404
        return Response(latest_image_bytes, mimetype="image/jpeg")

@app.route("/latest")
def latest():
    with data_lock:
        # automatically returns latest_data dictionary as json object
        return latest_data
"""

