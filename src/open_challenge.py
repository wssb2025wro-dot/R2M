# `open_challenge.py`

```python
"""
open_challenge.py
-----------------
Main control program for the Open Challenge.
Handles autonomous navigation around the track without obstacles,
using VL53L0X distance sensors for lateral centering and corner detection.
"""

import time
from motor_control import move_forward, stop_motors
from servo_control import set_servo_angle, center_servo
from sensor_readings import get_average_distance

# --------------------------
# Configuration
# --------------------------
FORWARD_SPEED = 0.35
TURN_SPEED = 0.35
MAX_ANGLE = 30
KP = 0.15
SENSOR_DELAY = 0.05
ANGLE_CENTER = 90

# Initialize state variables
running = False
turn_direction = None
lap_count = 0
corner_count = 0
passed_corner = False

# --------------------------
# Main Loop
# --------------------------
print("🚗 Waiting for button press to start Open Challenge...")

try:
    while True:
        if running:
            # Read sensors
            dist_left = get_average_distance(sensor_left)
            dist_right = get_average_distance(sensor_right)

            # Corner detection and turning logic
            if dist_left > 750 or dist_right > 750:
                if not passed_corner:
                    corner_count += 1
                    passed_corner = True
                    lap_count = (corner_count // 4) + 1
                    print(f"🔄 Corner {corner_count} | Lap {lap_count}")

                # Determine turn direction
                if turn_direction is None:
                    turn_direction = "LEFT" if dist_left > dist_right else "RIGHT"

                # Execute turn
                angle = ANGLE_CENTER - MAX_ANGLE if turn_direction == "LEFT" else ANGLE_CENTER + MAX_ANGLE
                set_servo_angle(angle)
                move_forward(TURN_SPEED)
                time.sleep(2.0)
                center_servo()
            else:
                passed_corner = False
                error = dist_left - dist_right
                correction = KP * error
                correction = max(-MAX_ANGLE, min(MAX_ANGLE, correction))
                set_servo_angle(ANGLE_CENTER - correction)
                move_forward(FORWARD_SPEED)
                print(f"L:{dist_left} R:{dist_right} | Corr:{correction} | Dir:{turn_direction}")

            time.sleep(SENSOR_DELAY)
        else:
            stop_motors()
except KeyboardInterrupt:
    stop_motors()
