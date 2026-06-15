"""
Python module for the Smith Lab Weather Station.

Needs to:
- Display a warning light on the display if temp goes above a certain threshold or below a certain threshold
- Send an alert to the website
- Possibly shut down if temperatures get extreme
"""
from internal_sensor import temperature_c, humidity
from tkinter import messagebox

# 1. Define your safety thresholds
TEMP_MAX = 80      # Trigger warning if temperature is over 35°C
HUMIDITY_MAX = 100  # Trigger warning if humidity is over 70%

# 2. Simulate current sensor readings
current_temp = 80
current_humidity = 100

# 3. Setup hidden tkinter root instance (required for pop-ups)
root = tk.Tk()
root.withdraw()

# 4. Evaluate thresholds using an 'or' condition
if current_temp > TEMP_MAX or current_humidity > HUMIDITY_MAX:
    # Build a descriptive warning message
    warning_text = f"Threshold Exceeded!\n\nTemp: {current_temp}°C (Max: {TEMP_MAX})\nHumidity: {current_humidity}% (Max: {HUMIDITY_MAX})"
    
    # Display the native error pop-up alert
    messagebox.showwarning("Environmental Warning", warning_text)

# 5. Clean up the system memory
root.destroy()