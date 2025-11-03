# `motor_control.py`

```python
"""
motor_control.py
----------------
This module provides functions to control the DC motors of the R2M robot.
It handles forward movement, backward movement, stopping, and speed adjustment
using PWM signals via the gpiozero library.
"""

from gpiozero import PWMOutputDevice, DigitalOutputDevice

# --------------------------
# DC Motor Pins
# --------------------------
ENA = PWMOutputDevice(13)  # PWM speed control
IN1 = DigitalOutputDevice(17)
IN2 = DigitalOutputDevice(27)

# --------------------------
# Motor Control Functions
# --------------------------
def move_forward(speed: float):
    """
    Move the robot forward at the specified speed.
    Speed must be a float between 0.0 (stop) and 1.0 (full speed).
    """
    IN1.on()
    IN2.off()
    ENA.value = speed

def move_backward(speed: float):
    """
    Move the robot backward at the specified speed.
    """
    IN1.off()
    IN2.on()
    ENA.value = speed

def stop_motors():
    """
    Stop the robot completely.
    """
    IN1.off()
    IN2.off()
    ENA.value = 0

