import time
from lineRobot import Robot
from octoliner import Octoliner
from tcs3472 import tcs3472
import machine

SENSITIVITY = 245
LINE_THRESHOLD = 700
BASE_SPEED = 20
KP = 25
robot = Robot()
bus = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(bus)
octoliner.set_sensitivity(SENSITIVITY)
color_sensor = tcs3472(bus)

def get_mineral_color():
    red, green, blue = color_sensor.rgb()
    total = red + green + blue
    try:
        ratios = (red / total, green / total, blue / total)
    except ZeroDivisionError:
        return "Unknown"
    if ratios[0] > 0.5:
        return "Red"
    if ratios[1] > 0.4:
        return "Green"
    if ratios[2] > 0.4:
        return "Blue"
    return "Floor"

def calculate_steering(position):
    return KP * position

def apply_movement(correction):
    robot.run_motors_speed(int(BASE_SPEED + correction), int(BASE_SPEED - correction))

last_color = "Floor"
lost_readings = 0
while True:
    sensor_array = octoliner.analog_read_all()
    if max(sensor_array) < LINE_THRESHOLD:
        lost_readings += 1
        if lost_readings < 5:
            time.sleep(0.01)
            continue
        robot.stop()
        break
    lost_readings = 0
    position = octoliner.track_line()
    mineral = get_mineral_color()
    if mineral != last_color and mineral not in ("Floor", "Unknown"):
        print("Mineral Detected:", mineral)
        last_color = mineral
    apply_movement(calculate_steering(position))
    time.sleep(0.05)
