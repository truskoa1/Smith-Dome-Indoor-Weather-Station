"""
Reads weather data from our Pi and displays it to the external display

This file provides get_weather_data(), which returns a weather dictionary to the FOH dashboard, BOH dashboard, weather logger,
and alert system.

Behavior:
    - Intended for use with the Adafruit BME280 weather sensor.
    - If the BME280 is unavailable, placeholder values are utilized for development purposes.
"""

from astropy.time import Time
from zoneinfo import ZoneInfo
from mqtt_client import outside_weather_data

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

# If our sensor reads a bad value, this will store the most recent valid read
last_good_inside = None
last_good_outside = None

EASTERN_TIMEZONE = ZoneInfo("America/New_York")

def eastern_timestamp(time=None):
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



def celsius_to_fahrenheit(temp_c):
    return (temp_c * 9/5) + 32

def placeholders(last_updated="unknown"):
    """
    Assigns placeholder strings to weather variables.

    Used when sensor is unavailable, for diagnostic and development purposes. 
    """
    return {
        "temperature_c": "--",
        "temperature_f": "--",
        "pressure_hpa": "--",
        "humidity": "--",
        "last_updated": last_updated
    }

def valid_temp_c(temp_c):
    """
    Returns True if temperature reading is plausible.
    """

    return isinstance(temp_c, (int, float)) and -25.0 <= temp_c <= 55.0

def valid_humidity(humidity):
    """
    Returns True if the humidity reading is plausible.
    """

    return isinstance(humidity, (int, float)) and 0.0 <= humidity <= 100.0

def valid_pressure_hpa(pressure):
    """
    Return True if the pressure reading is plausible.
    """

    return isinstance(pressure, (int, float)) and 800.0 <= pressure <= 1100.0

def get_weather_data():
    """
    Return the current weather data used by the dashboards.

    Returns:
        dict:
            Nested dictionary containing inside weather, outside weather, and timestamps.
    """

    global last_good_inside
    global last_good_outside

    current_time = Time.now()

    # Default to placeholders. These will be replaced below if the sensor read is valid.
    inside = placeholders(last_updated="Inside sensor unavailable")
    outside = placeholders(last_updated="Outside Pi unavailable")

    if sensor_avail:
        try:
            inside_temp_c = bme280.temperature
            inside_humidity = bme280.humidity
            inside_pressure = bme280.pressure

            readings_valid = (
                valid_temp_c(inside_temp_c)
                and valid_humidity(inside_humidity)
                and valid_pressure_hpa(inside_pressure)
            )

            if readings_valid:
                inside = {
                    "temperature_c": round(inside_temp_c, 1),
                    "temperature_f": round(celsius_to_fahrenheit(inside_temp_c), 1),
                    "pressure_hpa": round(inside_pressure, 1),
                    "humidity": round(inside_humidity, 1),
                    "last_updated": eastern_timestamp(current_time)
                }

                last_good_inside = inside

            else:
                print("Rejected invalid BME280 reading:")
                print(
                    f"temperature_c={inside_temp_c}, "
                    f"humidity={inside_humidity}, "
                    f"pressure={inside_pressure}"
                )

                if last_good_inside is not None:
                    inside = last_good_inside

        except Exception as error:
            print("BME280 read failed. Using last valid reading or placeholder.")
            print(error)

            if last_good_inside is not None:
                inside = last_good_inside


    outside_data = outside_weather_data()
    
    outside_temp_c = outside_data["temperature_c"]
    outside_humidity = outside_data["humidity"]
    outside_pressure = outside_data["pressure_hpa"]

    if outside_temp_c is not None and outside_humidity is not None and outside_pressure is not None:
        try: 
            outside_temp_c = float(outside_temp_c)
            outside_humidity = float(outside_humidity)
            outside_pressure = float(outside_pressure)

            outside_readings_valid = (
                valid_temp_c(outside_temp_c)
                and valid_humidity(outside_humidity)
                and valid_pressure_hpa(outside_pressure)
            )

            if outside_readings_valid:
                outside = {
                    "temperature_c": round(outside_temp_c, 1),
                    "temperature_f": round(celsius_to_fahrenheit(outside_temp_c), 1),
                    "pressure_hpa": round(outside_pressure, 1),
                    "humidity": round(outside_humidity, 1),
                    "last_updated": eastern_timestamp(current_time)
                }

                last_good_outside = outside
            else:
                if last_good_outside is not None:
                    outside = last_good_outside
        except ValueError:
            print("Could not convert outside data values to floats.")
            if last_good_outside is not None:
                outside = last_good_outside
        
    else:
        if last_good_outside is not None:
            outside = last_good_outside


    return {
        "inside": inside,

        "outside": outside,

        "time": {
            "timestamp_utc": current_time.isot,
            "timestamp_eastern": eastern_timestamp(current_time),
            "julian_date": current_time.jd
        }
    }