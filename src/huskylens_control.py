# `huskylens_control.py`

```python
"""
huskylens_control.py
-------------------
Provides functions to interact with the HuskyLens AI camera.
Detects colored blocks for obstacle avoidance and returns corresponding actions.
"""

from HUSKYLENS.huskylib import HuskyLensLibrary

# Initialize HuskyLens camera
hl = HuskyLensLibrary("I2C", "", address=0x32)

# Predefined angles for obstacle avoidance
ANGLE_HUSKY_LEFT = 55
ANGLE_HUSKY_RIGHT = 125

def detect_obstacle():
    """
    Returns a tuple (override, angle) if an obstacle is detected:
    - Red block → return (True, ANGLE_HUSKY_RIGHT)
    - Green block → return (True, ANGLE_HUSKY_LEFT)
    - None → (False, None)
    """
    blocks = hl.requestAll()
    if blocks:
        for block in blocks:
            if block.ID == 1:  # Red detected
                return True, ANGLE_HUSKY_RIGHT
            elif block.ID == 2:  # Green detected
                return True, ANGLE_HUSKY_LEFT
    return False, None
