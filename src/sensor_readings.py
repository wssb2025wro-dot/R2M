# `sensor_readings.py`

```python
"""
sensor_readings.py
-----------------
Handles distance measurements using VL53L0X sensors and the HC-SR04 ultrasonic sensor.
Includes averaging for smoother and more reliable readings.
"""

import time
from gpiozero import DistanceSensor
import adafruit_vl53l0x

# --------------------------
# Sensor Setup (HC-SR04)
# --------------------------
start_sensor = DistanceSensor(echo=26, trigger=16, max_distance=4.0)

# --------------------------
# Sensor Functions
# --------------------------
def get_start_distance(sensor=start_sensor, count=3) -> float:
    """
    Returns the averaged distance from HC-SR04 in cm.
    """
    total = 0
    for _ in range(count):
        total += sensor.distance * 100
        time.sleep(0.005)
    return total / count

def get_average_distance(sensor, count=3) -> float:
    """
    Return averaged distance from VL53L0X sensor.
    """
    total = 0
    for _ in range(count):
        try:
            total += sensor.range
        except Exception:
            total += 1000  # Default fallback
        time.sleep(0.005)
    return total / count
