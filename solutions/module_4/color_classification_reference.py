from lineRobot import Robot
from tcs3472 import tcs3472
import machine

robot = Robot()
bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
sensor = tcs3472(bus)

def detect_color_name(r, g, b):
    total = r + g + b
    if total == 0:
        return "Unknown"
    r_ratio = r / total
    g_ratio = g / total
    b_ratio = b / total
    if r_ratio > 0.45:
        return "Red"
    elif g_ratio > 0.45:
        return "Green"
    elif b_ratio > 0.45:
        return "Blue"
    return "Floor"

for i in range(6):
    r, g, b = sensor.rgb()
    color_name = detect_color_name(r, g, b)
    print(f"Scan - {color_name} (Raw: R:{r} G:{g} B:{b})")
    robot.move_forward_distance(10)
