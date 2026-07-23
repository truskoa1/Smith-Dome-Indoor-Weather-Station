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
  The code starts by importing io, Picamera (the camera attached to the Pi), Flask, Response, jsonify, and time.
  The function initialize_cam initializes and returns the correct camera that will be used.
  The function generate_frames captures frames from the camera by taking JPEGs of what it sees and saves them into memory. When a client is connected to /video_feed, this will loop continuously.
  The function index returns a basic JSON status for the camera stream service (camera-stream status for service, running status for status, and /video_feed status for video_feed).
  The function health returns how healthy the stream is (running status).
  The /video_feed is routed to the Flask app.
  The function video_feed retuns the JEPG frames captured by the camera.

Camera.py:
This code takes a sample picture using the camera. Its only purpose is to test and make sure the camera is functional. If so, a single JPEG image will get taken by the camera and sent to the folder path /home/surp/test_image.jpg upon running.

Camera_control.py:
This code allows the camera to be controlled through the touchscreen display
  The code starts by importing subprocess.
  The function run_systemctl runs a systemctl command for the camera stream survice.
  The function camera_on returns a boolean that represents whether the camera is on or not.
  The function start_camera starts the camera using run_systemctl.
    It will return an error message if the camera is off.
  The function stop_camera does likewise, stopping the camera only if the camera is already on.
  The function toggle_stream toggles the status of the stream.

App.py:
This code contols the FOH (Front of House) Flask application.
  The code starts by importing get_weather_data, toggle_stream, camera_on, evaluate_warnings, and snooze_warning.
  The function dashboard renders the main FOH touchscreen dashboard.
  The function weather_api returns the current weather data as a JSON.
  The function camera_status returns whether or not the camera stream is active.
  The function toggle_camera toggles the camera stream. This is different from the toggle_stream function in camera_control.py, which toggles the streaming of the camera, not the camera itself.
  The function alerts_api retuns the current alert state as a JSON.
  The function snooze_alert snoozes the current caution alert.
  The function 
  
Boh_app.py:
This code controls the BOH (Back of House) Flask applicaton.
  The code starts by importing Flask, render_template, jsonify, send_file, get_weather_data, log_file, initialize_log, read_recent_log, and camera_on.
  The BOH app is set to Flask.
  The function boh_dashboard renders the dashboard and receives the current weather data and recent log rows.
  The function weather_api returns the current weather as a JSON for the BOH (the function with the same name under app.py is for FOH)
  The function weather_log_api returns the log rows as a JSON for the BOH.
  The function donwload_weather_log will return a file attachment containing the log file.
  The function cmaera_status retuns whether or not the camera is running.
  
The javascript files under static and the html files under templates are for visual formatting and parsing code so that the website can actually use it.
