"""
Defines the caution and danger states for the weather station. 

Since our telescope cannot exactly be moved out of the dome, the alert state is determined by the outside weather data.
Our alert states are defined as follows:
    none:
        No active alert. This will be the default state, with no alert banner and a black background. 
    unknown:
        This means the inside pi is not actively communicating with the outside pi. Since observatory safety cannot be
        ascertained, a persistent alert will be displayed and the background will be a blue-grey.
    warning:
        Caution state. This implies poor observing conditions, but no immediate danger to the telescope. The user is able to temporarily
        snooze these alerts.
    danger: 
        Unsafe state. Implies conditions that pose an immediate danger to the telescope, requiring the dome to be closed. This
        will turn the screen red until it is resolved. 

Current limitations: 
    - Outside Pi communication not currently implemented.
    - Alert thresholds are placeholder values.
"""

from astropy.time import Time, TimeDelta


# Placeholder values until we get something more concrete.
HIGH_HUMIDITY = 85.0
DANGER_HUMIDITY = 90.0

# Disabled for now until we know what temperature threshold matters.
TEMP_THRESHOLD_F_CAUTION = 104
TEMP_THRESHOLD_F_DANGER = 122

SNOOZE_MIN = 15

snooze_until = None


def is_number(value):
    """
    Returns true if value is of type integer or float.

    This prevents comparisons between placeholder strings like "--" and numbers. 
    """
    return isinstance(value, int) or isinstance(value, float)


def data_missing(value):
    """
    Returns true if the value is None or still a placeholder. 

    Since observing when the conditions are unknown could be dangerous, this is later used for the 
    unknown state determination.
    """
    return value is None or value == "--"


def warning_snoozed():
    """
    Returns true if a caution alert is currently snoozed. It does this by checking if the current time
    is less than the time defined by "snooze_until". 
    """
    global snooze_until

    if snooze_until is None:
        return False

    return Time.now() < snooze_until


def snooze_warning(minutes=SNOOZE_MIN):
    """
    Snoozes the current danger alert for a pre-defined time. 

    Args:
        minutes (int or float): # of minutes alert should be snoozed
    
    Returns: 
        dict:
            Dictionary returned to frontend after a snooze request. Includes timestamp (ISO) when snooze expires. 
    
    Only warnings are snoozable. 
    """
    global snooze_until

    snooze_until = Time.now() + TimeDelta(minutes * 60, format="sec")

    return {
        "snoozed": True,
        "snooze_until": snooze_until.isot
    }


def clear_snooze():
    """
    Clears any active snooze. 

    This is utilized when caution warnings resolve. 
    """
    global snooze_until
    snooze_until = None


def warn(temp, humidity, rainfall=False):
    """
    Converts weather data into an alert state.

    Args:
        temp (float): 
            Outside temperature in Fahrenheit.
        humidity (float):
            Outside humidity percentage.
        rainfall (bool):
            True if rainfall is detected. Currently defaults to false because we do not have a rainfall sensor to read from.
    
    Returns: 
        dict: 
            Alert dictionary utilized by Flask and dashboard.js

            Important keys: 
                level: 
                    "none", "warning", or "danger"
                active:
                    True if an alert should be displayed.
                snoozed: 
                    True if alert is currently snoozed
                can_snooze:
                    True only for warning alerts
                messages: 
                    List of alert messages
    
                    
    Alert behavior:
        - Danger conditions: rainfall detected, extremely high humidity
        - Warning conditions: High humidity, high temperature
        - Unknown: no reading
    """
    tempwarning = False
    humiditywarning = False
    rainfalldanger = False
    humidityDanger = False

    messages = []

    if (
        TEMP_THRESHOLD_F is not None
        and is_number(temp)
        and temp > TEMP_THRESHOLD_F
    ):
        tempwarning = True
        messages.append(f"Outside temperature is high: {temp}°F.")

    if is_number(humidity) and humidity >= HIGH_HUMIDITY:
        humiditywarning = True
        messages.append(f"Outside humidity is high: {humidity}%.")

    if rainfall is True:
        rainfalldanger = True
        messages.append("Rainfall detected.")

    if is_number(humidity) and humidity >= DANGER_HUMIDITY:
        humidityDanger = True
        messages.append(f"Outside humidity is dangerously high: {humidity}%.")

    danger = rainfalldanger or humidityDanger
    warning = humiditywarning or tempwarning

    if danger:
        level = "danger"
    elif warning:
        level = "warning"
    else:
        level = "none"

    if level == "none":
        clear_snooze()

    snoozed = level == "warning" and warning_snoozed()

    return {
        "level": level,
        "active": level != "none",
        "snoozed": snoozed,
        "can_snooze": level == "warning",
        "messages": messages,

        "tempwarning": tempwarning,
        "humiditywarning": humiditywarning,
        "rainfalldanger": rainfalldanger,
        "humidityDanger": humidityDanger
    }


def evaluate_warnings(weather_data):
    """
    Evaluates safety based on weather data.

    Args:
        weather_data (dict):
            Weather dictionary returned by sensor_reader.get_weather_data().
    Returns:
        dict:
            Alert state dictionary used by the /api/alerts Flask route.
    """
    outside = weather_data["outside"]

    outside_temp = outside.get("temperature_f")
    outside_humidity = outside.get("humidity")
    outside_rainfall = outside.get("rainfall", False)

    if data_missing(outside_temp) or data_missing(outside_humidity):
        return {
            "level": "unknown",
            "active": True,
            "snoozed": False,
            "can_snooze": False,
            "messages": [
                "Outside weather data unavailable. Safety unknown."
            ],

            "tempwarning": False,
            "humiditywarning": False,
            "rainfalldanger": False,
            "humidityDanger": False
        }

    return warn(
        temp=outside_temp,
        humidity=outside_humidity,
        rainfall=outside_rainfall
    )