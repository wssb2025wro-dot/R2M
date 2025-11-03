# `utils.py`

```python
"""
utils.py
--------
Helper functions for the R2M robot.
Includes lap/corner counting, speed adjustment, and logging utilities.
"""

# --------------------------
# Lap and Corner Counting
# --------------------------
def update_corner_count(corner_count, passed_corner) -> tuple:
    """
    Increment corner count if a new corner is detected.
    Returns updated corner_count and passed_corner flag.
    """
    if not passed_corner:
        corner_count += 1
        passed_corner = True
    return corner_count, passed_corner

def calculate_lap(corner_count) -> int:
    """
    Calculate the current lap number based on corner count.
    4 corners per lap.
    """
    return (corner_count // 4) + 1

# --------------------------
# Speed Utilities
# --------------------------
def adjust_speed(forward_speed, current_distance, accel_threshold, accel_factor):
    """
    Adjust forward speed dynamically.
    If distance > accel_threshold → multiply speed by accel_factor
    """
    if current_distance > accel_threshold:
        return min(forward_speed * accel_factor, 1.0)
    return forward_speed

# --------------------------
# Logging Utility
# --------------------------
def print_status(dist_left, dist_right, correction, turn_direction, lap_count, corner_count, front_distance, speed):
    """
    Print current robot status in a formatted way.
    """
    print(f"L:{dist_left:6.1f} R:{dist_right:6.1f} | Corr={correction:+.1f} | "
          f"Dir:{turn_direction} | Lap:{lap_count} | Corners:{corner_count} | "
          f"Front:{front_distance:.1f} cm | Speed:{speed:.2f}")
