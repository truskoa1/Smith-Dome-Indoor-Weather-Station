"""
Needs to read data off the raspberry pi and then disply it to the external temp/humidity display.
"""

from astropy.time import Time

import board
from adafruit_bme280 import basic as adafruit_bme280
i2c = board.I2C() # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def get_weather_data():
    return {
        "inside dome": {
            "temperature": bme280.temperature,
            "humidity": bme280.humidity
        },
        "outside dome": {
            "temperature": None,    # need to communicate with other group to get measurements from outside weather station for both of these
            "humidity": None
        },
        "time": {
            "Time Stamp": Time.now()
        }
    }