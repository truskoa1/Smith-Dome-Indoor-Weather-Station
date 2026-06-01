"""
Python module for Smith Lab weather station.

Needs to:
- Update the website/display with the current internal temp
"""

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
# "time" is a default Python library
import time
# "board" is the Raspberry Pi GPIO library
import board
# "adafruit_dht" is the library used to read data from the DHT11 sensor
import adafruit_dht
 
# Initialize the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D2)
 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
 
while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(f"Temp: {temperature_f:.1f} F / {temperature_c:.1f} C    Humidity: {humidity}% ")
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(2.0)
