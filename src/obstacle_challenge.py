# `obstacle_challenge.py`

```python
"""
obstacle_challenge.py
--------------------
Main control program for the Obstacle Challenge.
Handles autonomous navigation with obstacle detection and avoidance
using the HuskyLens AI camera in addition to distance sensors.
"""

import time
from motor_control import move_forward, stop_motors
from servo_control import set_servo_angle, center_servo
from sensor_readings import get_average_distance, get_start_distance
from huskylens_control import detect_obstacle
from utils import update_corner_count, calculate_lap, adjust_speed, print_status

# Configuration
FORWARD_SPEED = 0.35
TURN_SPEED = 0.35
FINAL_SPEED = 0.15
MAX_ANGLE = 30
KP = 0.15
ACCEL_THRESHOLD = 120
ACCEL_FACTOR = 2
ANGLE_CENTER = 90
TURN_DURATION = 2.0

# State variables
running = False
turn_direction = None
lap_count = 0
corner_count = 0
passed_corner = False
start_distance_initial = 0

# Main loop
print("🚗 Waiting for button press...")

try:
    while True:
        if running:
            # Sensor readings
            dist_left = get_average_distance(sensor_left)
            dist_right = get_average_distance(sensor_right)
            current_distance = get_start_distance()

            # Obstacle detection
            husky_override, husky_angle = detect_obstacle()
            if husky_override:
                set_servo_angle(husky_angle)
                move_forward(TURN_SPEED)
            else:
                # Corner detection
                if dist_left > 750 or dist_right > 750:
                    corner_count, passed_corner = update_corner_count(corner_count, passed_corner)
                    lap_count = calculate_lap(corner_count)

                    # Determine turn direction
                    if turn_direction is None:
                        turn_direction = "LEFT" if dist_left > dist_right else "RIGHT"

                    # Execute turn
                    angle = ANGLE_CENTER - MAX_ANGLE if turn_direction == "LEFT" else ANGLE_CENTER + MAX_ANGLE
                    set_servo_angle(angle)
                    move_forward(TURN_SPEED)
                    time.sleep(TURN_DURATION)
                    center_servo()
                else:
                    passed_corner = False
                    error = dist_left - dist_right
                    correction = KP * error
                    correction = max(-MAX_ANGLE, min(MAX_ANGLE, correction))
                    set_servo_angle(ANGLE_CENTER - correction)

                    # Speed adjustment
                    if corner_count >= 12:
                        move_forward(FINAL_SPEED)
                        if current_distance <= start_distance_initial:
                            print(f"🎯 Back to start | Distance: {current_distance:.1f}")
                            running = False
                            stop_motors()
                            continue
                        speed = FINAL_SPEED
                    else:
                        speed = adjust_speed(FORWARD_SPEED, current_distance, ACCEL_THRESHOLD, ACCEL_FACTOR)
                        move_forward(speed)

                    print_status(dist_left, dist_right, correction, turn_direction, lap_count, corner_count, current_distance, speed)

            time.sleep(0.05)
        else:
            stop_motors()
except KeyboardInterrupt:
    stop_motors()
