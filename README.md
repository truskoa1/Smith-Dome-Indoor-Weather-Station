This entire project takes temperature, humidity, and pressure from Raspberry Pi sensors and outputs them into to both a Flask website and a Raspberry Pi display. There is a camera attached to the Pi that can view the inside of the dome (viewable on the website), and the display has touch-friendly buttons where you can turn the camera on and off.

Sensor_reader.py:
This code returns values recorded by the sensors.
  The code first starts by searching for a compatible raspberry pi with temperature, humidity, and pressure sensors.
  If no such sensors exist, then it will return an error.
  The function celsius_to_fahrenheit does exactly that—convert a celcius value to fahrenheit.
  The function get_weather_data also does exactly that—returns data gathered.
    If valid sensors were detected, then it sets four variables (temp, hum, pres, and temp in F)
    to the values that those sensors output.
    If no valid sensors were detected, then it sets those variables to "--".
  Sensor_reader will return a few things:
    1. An "inside" variable containing the variables returned by get_weather_data
    2. An "outside" variable containing the variables returned by a similar function from a second group that similarly recorded these four variables on the outside of the dome
    3. A "time" variable that records the time (in UTC) and date (in Julian date)

Weather_logger.py:
This code logs weather data recorded by the Pi.
  The code first starts by importing the get_weather_data from sensor_reader.py.
  It then set sets up a csv file to be created/edited.
  The function initialize_log appends one Pi reading to the weather log.
  The function get_weather datacreates a csv file if none exist.
    It then creates headers for the time, temperature, humidity, and pressure.
  The function read_recent_log returns the most recent rows from the weather log.
    It is set by default to return 25 lines from the csv file.

Weather_warnings.py:
The code defines the safety state of the telescope based off of outside data (there is a second Raspberry Pi that has similar code to collect weather data from outside, which communicates with this Raspberry Pi).
  The code first starts by importing the functions Time and TimeDelta from astropy.time.
  It then defines the default (temporary) limits:
    High humidity is 85%, and danger is 90%
    Cautious temperature is 104 F, and dangerous is 122
    Snooze_min is 15 minutes
  The function is_number returns true if the parameter given is an integer or a float.
  The function data_missing returns true if the parameter given is None or a placeholder variable type.
  The function warning_snoozed returns true if a caution alert is snoozed; that is, if the current elapsed time since the warning is less than the time defined by the above variable snooze_min.
  The function clear_snooze clears any active snooze.
  The function warn calculates if any of the temperature or humidity recordings from outside are higher than the threshold variables (defined on lines 29-30 of this readme), then returns the appropriate warning state.
  The function evaluate_warnings returns the appropriate response due to the weather data.

Run_logger.py:
The code imports the function log_weather_data from weather_logger.py and calls it every 60 seconds. In other words, this code makes the csv file with weather data update every minute.

Stream.py:
This code runs runs a Flask app on port 5000 and serves a live MJPEG stream from the Raspberry Pi camera at /video_feed. It is intended to run as a systemd service named camera-stream.service.

Camera.py:
This code allows the camera to update its feed to the Flask website.

Camera_control.py:
This code allows the camera to be controlled through the touchscreen display.

App.py:
This code contols the FOH (Front of House) Flask application.

Boh_app.py:
This code controls the BOH (Back of House) Flask applicaton.
  
