import csv
from pathlib import Path

from sensor_reader import get_weather_data

base_dir = Path(__file__).resolve().parent
log_file = base_dir / "weather_log.csv"

def initialize_log():
    if not log_file.exists():
        with open(log_file, mode="w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "timestamp_utc",
                "julian_date",
                "inside_temperature_f",
                "inside_temperature_c",
                "inside_humidity",
                "inside_pressure_hpa",
                "outside_temperature_f",
                "outside_temperature_c",
                "outside_humidity",
                "outside_pressure_hpa"
                ])

def log_weather_data():
    initialize_log()

    data = get_weather_data()

    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            data["time"]["timestamp_utc"],
            data["time"]["julian_date"],
            data["inside"]["temperature_f"],
            data["inside"]["temperature_c"],
            data["inside"]["humidity"],
            data["inside"]["pressure_hpa"],
            data["outside"]["temperature_f"],
            data["outside"]["temperature_c"],
            data["outside"]["humidity"],
            data["outside"]["pressure_hpa"]
            ])

def read_recent_log(limit=25):
    initialize_log()

    with open(log_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    return rows[-limit:]