This entire epic project takes temperature, humidity, and pressure from Raspberry Pi sensors and 

Sensor_reader.py:
  The code first starts by searching for a compatible raspberry pi with temperature, humidity, and pressure sensors.
  If no such sensors exist, then it will return an error.
  The function celsius_to_fahrenheit does exactly that—convert a celcius value to fahrenheit.
  The function get_weather_data also does exactly that (wowwwww!!!!! uwu)
    If valid sensors were detected, then it sets four "goofy-ahh weather variables" (temp, hum, pres, and temp in F)
    to the values that those sensors output.
    If no valid sensors were detected, then it sets those variables to "--".
  Sensor_reader will return a few things:
    1. An "inside" variable containing the variables returned by get_weather_data
    2. An "outside" variable containing the variables returned by a similar function from a second group that similarly recorded
    these four variables on the outside of the dome
    3. A "time" variable that records the time (in UTC) and date (in Julian date)
