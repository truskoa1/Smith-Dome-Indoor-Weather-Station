"""
Reads weather data from our Pi and displays it to the external display

This file provides get_weather_data(), which returns a weather dictionary to the FOH dashboard, BOH dashboard, weather logger,
and alert system.

Behavior:
    - Intended for use with the Adafruit BME280 weather sensor.
    - If the BME280 is unavailable, placeholder values are utilized for development purposes.
    - Outside weather data is given a string placeholder of "--" until Pi-to-Pi communication is established.

Prior to being installed in the Smith Dome, the float placeholders for interior data will be changed to also be "--". 
"""

from astropy.time import Time


try:
    import board
    from adafruit_bme280 import basic as adafruit_bme280

    i2c = board.I2C() # uses board.SCL and board.SDA
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    sensor_avail = True

except Exception as error:
    print("Sensor unavailable. Using placeholders.")
    print(error)

    bme280 = None
    sensor_avail = False

def celsius_to_fahrenheit(temp_c):
    return (temp_c * 9/5) + 32

def get_weather_data():
    """
    Return the current weather data used by the dashboards.

    Returns:
        dict:
            Nested dictionary containing inside weather, outside weather, and timestamps.

    Notes: 
        - Until communication with the outside Pi is possible, placeholder strings are currently hardcoded into the return statement.
          This will always result in an "unknown" alert state. 
    """
    if sensor_avail:
        inside_temp_c = bme280.temperature
        inside_humidity = bme280.humidity
        inside_pressure = bme280.pressure
    else:
        inside_temp_c = "--"
        inside_humidity = "--"
        inside_pressure = "--"

    inside_temp_f = celsius_to_fahrenheit(inside_temp_c)
    current_time = Time.now()

    # if none of the values are available, return placeholders
    if inside_temp_c or inside_humidity or inside_pressure == None:
        return
    else:
    # else, return below
        return {
            "inside": {
                "temperature_c": round(inside_temp_c, 1),
                "temperature_f": round(inside_temp_f, 1),
                "pressure_hpa": round(inside_pressure, 1),
                "humidity": round(inside_humidity, 1)
            },
            # need to communicate with other group to get measurements from outside weather station for both of these
            "outside": {
                "temperature_c": "--",  
                "temperature_f": "--",
                "pressure_hpa": "--",
                "humidity": "--"
            },
            "time": {
                "timestamp_utc": current_time.isot,
                "julian_date": current_time.jd
            }
        }
