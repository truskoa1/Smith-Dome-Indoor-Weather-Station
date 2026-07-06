"""
Reads weather data from our Pi and displays it to the external display

6.15.2026 -
    For development purposes, I have added code so default values display when
    the I2C connection isn't possible. That way, on the RasPi the real values will display
    and on a personal machine it will display defaults. 
    -SS
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
