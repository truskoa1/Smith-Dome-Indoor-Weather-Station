"""
7.1.2026 -
    * Updated to return alert states given weather data.
    * Temporarily defining danger/caution states.
    * Renamed to weather_warnings.py to prevent conflict with the built-in
      Python warnings module.
    -SS
"""

from astropy.time import Time, TimeDelta


# Placeholder values until we get something more concrete.
HIGH_HUMIDITY = 80.0
DANGER_HUMIDITY = 95.0

# Disabled for now until we know what temperature threshold matters.
TEMP_THRESHOLD_F = None

SNOOZE_MIN = 15

snooze_until = None


def is_number(value):
    return isinstance(value, int) or isinstance(value, float)


def data_missing(value):
    return value is None or value == "--"


def warning_snoozed():
    global snooze_until

    if snooze_until is None:
        return False

    return Time.now() < snooze_until


def snooze_warning(minutes=SNOOZE_MIN):
    global snooze_until

    snooze_until = Time.now() + TimeDelta(minutes * 60, format="sec")

    return {
        "snoozed": True,
        "snooze_until": snooze_until.isot
    }


def clear_snooze():
    global snooze_until
    snooze_until = None


def warn(temp, humidity, rainfall=False):
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