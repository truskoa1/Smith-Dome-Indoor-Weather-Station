import time

from weather_logger import log_weather_data

log_interval = 60 # seconds

def main():
    print("Starting weather logger.")

    while True:
        log_weather_data()
        time.sleep(log_interval)

if __name__ == "__main__":
    main()

    