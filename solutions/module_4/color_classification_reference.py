from lineRobot import Robot
from tcs3472 import tcs3472
import machine
import time

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
    if r_ratio > 0.5:
        return "Red"
    elif g_ratio > 0.4:
        return "Green"
    elif b_ratio > 0.4:
        return "Blue"
    return "Floor"

time.sleep(0.5)
for step in range(6):
    r, g, b = sensor.rgb()
    color_name = detect_color_name(r, g, b)
    print(f"Scan - {color_name} (Raw: R:{r} G:{g} B:{b})")
    if step < 5:
        robot.move_forward_speed_distance(40, 13)
        time.sleep(0.5)
