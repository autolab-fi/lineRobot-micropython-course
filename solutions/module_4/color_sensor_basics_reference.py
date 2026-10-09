from lineRobot import Robot
import machine
from tcs3472 import tcs3472
import time

robot = Robot()

bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
color_sensor = tcs3472(bus)

# Let the first I2C color measurement settle before reading.
time.sleep(0.5)
for step in range(6):
    r, g, b = color_sensor.rgb()
    print(f"Scan - R:{r} G:{g} B:{b}")
    if step < 5:
        robot.move_forward_distance(12)
        time.sleep(0.5)

print("Linear scan complete.")
