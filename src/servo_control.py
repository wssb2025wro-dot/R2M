# `servo_control.py`

```python
"""
servo_control.py
----------------
This module controls the steering servo of the R2M robot.
It allows angle adjustments for cornering, obstacle avoidance, and lateral centering.
"""

from adafruit_servokit import ServoKit

# --------------------------
# Servo Setup
# --------------------------
kit = ServoKit(channels=16, address=0x40)
servo = kit.servo[0]
servo.set_pulse_width_range(500, 2500)
ANGLE_CENTER = 90  # Neutral angle

# --------------------------
# Servo Functions
# --------------------------
def set_servo_angle(angle: float):
    """
    Set the servo to a specific angle.
    Angle is in degrees (0-180), 90 is centered.
    """
    servo.angle = max(0, min(180, angle))

def center_servo():
    """Return the servo to the center position."""
    servo.angle = ANGLE_CENTER
